import os
import csv
import time
import pandas as pd
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def login_to_website(config):
    """Login to the WordPress website"""
    # Setup Chrome options to disable save password popup
    options = uc.ChromeOptions()
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False
    }
    options.add_experimental_option("prefs", prefs)
    
    # Set headless mode if configured
    headless_mode = config.get("browser", {}).get("headless", False)
    if headless_mode:
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
    
    # Launch browser
    driver = uc.Chrome(options=options)
    wait = WebDriverWait(driver, 15)  # 15-second timeout
    # Navigate to login page
    driver.get(config["credentials"]["url"])
    # Wait for username field and enter username
    wait.until(EC.presence_of_element_located((By.ID, "user_login"))).send_keys(config["credentials"]["username"])
    # Wait for password field and enter password
    wait.until(EC.presence_of_element_located((By.ID, "user_pass"))).send_keys(config["credentials"]["password"])
    # Wait for and click the submit button
    wait.until(EC.element_to_be_clickable((By.ID, "wp-submit"))).click()
    # Wait until dashboard or some post-login element is loaded
    wait.until(EC.url_contains("wp-admin"))

    return driver

def convert_to_paragraphs(text: str) -> str:
    """Convert Arabic text with line breaks into HTML paragraphs"""
    import re
    lines = text.splitlines()
    paragraphs = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if re.match(r"^[\-\•\*]\s+", stripped):
            # Remove bullet symbol, add custom bullet and hanging indent
            bullet_content = re.sub(r"^[\-\•\*]\s*", "", stripped)
            paragraphs.append(
                '<p dir="rtl" style="text-indent:-1.5em; padding-right:2em;">'
                '&bull;&emsp;' + bullet_content +
                '</p>'
            )
        else:
            paragraphs.append(f'<p dir="rtl">{stripped}</p>')

    return ''.join(paragraphs)

def fill_article_intro(driver, text):
    """Fill the article introduction content"""
    text = convert_to_paragraphs(text)
    wait = WebDriverWait(driver, 15)
    textarea = wait.until(EC.visibility_of_element_located((By.ID, "content")))
    textarea.clear()
    textarea.send_keys(text)
    # Return to main page
    driver.switch_to.default_content()
    return driver

def click_add_another_and_wait(driver):
    """Add another content section and wait for it to appear"""
    wait = WebDriverWait(driver, 15)
    # Count current textareas before clicking
    initial_count = len(driver.find_elements(By.NAME, "post_contents_desc[]"))
    # Click the "Add another" button
    add_button = wait.until(EC.element_to_be_clickable((By.ID, "add-contents-row")))
    add_button.click()
    # Wait for number of textareas to increase by 1
    wait.until(lambda d: len(d.find_elements(By.NAME, "post_contents_desc[]")) > initial_count)

def click_all_html_toggle_buttons(driver):
    """Switch all editors to HTML mode"""
    wait = WebDriverWait(driver, 15)

    html_buttons = driver.find_elements(By.TAG_NAME, "button")
    for i, btn in enumerate(html_buttons):
        btn_id = btn.get_attribute("id")
        if btn_id and btn_id.endswith("-html") and "post_contents_desc" in btn_id:
            try:
                # Re-find the button by ID
                button = wait.until(EC.presence_of_element_located((By.ID, btn_id)))
                # Scroll the button into view
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)

                # Only click if not already pressed
                if button.get_attribute("aria-pressed") != "true":
                    wait.until(EC.element_to_be_clickable((By.ID, btn_id))).click()
                    time.sleep(0.2)
            except Exception as e:
                print(f"[{i}] Failed to click button {btn_id}: {e}")

def fill_all_subsections_bodies(driver, content_list):
    """Fill all subsection content areas"""
    wait = WebDriverWait(driver, 15)
    # Count the number of matching fields
    count = len(driver.find_elements(By.NAME, "post_contents_desc[]"))
    print(f"{count} textareas found. Filling them...")
    for i in range(count):
        # Re-fetch the textarea by ID if possible (if ID is like post_contents_desc0, 1, 2, etc.)
        textarea = driver.find_element(By.ID, f"post_contents_desc{i}")
        wait.until(EC.visibility_of(textarea))
        content = content_list[i] if i < len(content_list) else f"محتوى افتراضي للجزء {i+1}"
        textarea.clear()
        textarea.send_keys(convert_to_paragraphs(content))

def click_save_draft(driver):
    """Save the article as draft"""
    wait = WebDriverWait(driver, 15)
    # Wait until the Save Draft button is clickable
    save_button = wait.until(EC.element_to_be_clickable((By.ID, "save-post")))
    # Scroll into view to avoid overlap issues (optional)
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save_button)
    # Click the button
    save_button.click()

def click_publish(driver):
    """Publish the article"""
    wait = WebDriverWait(driver, 20)

    try:
        # Ensure page is fully loaded
        wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

        # Wait for Publish button
        publish_button = wait.until(EC.element_to_be_clickable((By.ID, "publish")))

        # Scroll into view and wait a bit
        driver.execute_script("arguments[0].scrollIntoView(true);", publish_button)
        time.sleep(0.5)

        # JS click to avoid overlays
        driver.execute_script("arguments[0].click();", publish_button)

        # Wait for "Post published" message
        wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//p[contains(text(), 'Post published.')]")
        ))

        print("✅ Article published successfully.")

    except Exception as e:
        print("❌ Failed to publish:", e)

def get_category_id_by_name(category_name, csv_path="disease_categories.csv"):
    """Get category ID from CSV file by category name"""
    with open(csv_path, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["category_name"].strip() == category_name.strip():
                return row["id"]
    raise ValueError(f"Category '{category_name}' not found in CSV.")

def select_category_by_name(driver, category_name, csv_path="disease_categories.csv"):
    """Select a category checkbox by name"""
    category_id = get_category_id_by_name(category_name, csv_path)
    wait = WebDriverWait(driver, 10)
    
    selector = f"input[name='tax_input[diseases_category][]'][value='{category_id}']"
    checkbox = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))

    if not checkbox.is_selected():
        driver.execute_script("arguments[0].click();", checkbox)

def upload_featured_image(driver, image_path, timeout=30):
    """Upload a featured image for the article"""
    wait = WebDriverWait(driver, timeout)
    # Step 1: Click "Set featured image"
    set_thumb_button = wait.until(EC.element_to_be_clickable((By.ID, "set-post-thumbnail")))
    driver.execute_script("arguments[0].click();", set_thumb_button)

    wait = WebDriverWait(driver, timeout)
    upload_tab = wait.until(EC.element_to_be_clickable((By.ID, "menu-item-upload")))
    upload_tab.click()

    # Step 2: Wait for iframe and switch to it
    # Wait for the iframe with partial match of src or class (works on all WordPress versions)
    # Locate the actual file input element (may need to inspect the page to find the correct selector)
    file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")

    # Send the file path to the input element
    file_input.send_keys(image_path)
    time.sleep(2)  # Wait for the file to upload

    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "button.media-button-select")
        )
    )
    button.click()
    print("Button clicked successfully!")

def press_all_code_editors(driver):
    """Switch all Classic Editor blocks to Code (HTML) mode"""
    wait = WebDriverWait(driver, 15)
    # Refresh elements each time to avoid staleness
    buttons = wait.until(lambda d: d.find_elements(By.CSS_SELECTOR, "button.wp-switch-editor.switch-html"))
    for i, button in enumerate(buttons):
        try:
            # Re-find the button to avoid staleness
            current_button = wait.until(lambda d: d.find_elements(By.CSS_SELECTOR, "button.wp-switch-editor.switch-html"))[i]
             # Wait for the button to be in a stable state
            wait.until(lambda d: current_button.is_displayed() and current_button.is_enabled())
            
            if current_button.get_attribute("aria-pressed") != "true":
                driver.execute_script("""
                    arguments[0].scrollIntoView({
                        behavior: 'auto',
                        block: 'center',
                        inline: 'center'
                    });
                    arguments[0].click();
                """, current_button)
                print(f"✅ Switched editor #{i} to Code mode.")
            else:
                print(f"⏩ Editor #{i} already in Code mode.")
        except Exception as e:
            print(f"❌ Failed to switch editor #{i}: {e}")

def article_writer(excel_path, config, automation_engine, progress_callback=None):
    """Main function to write an article to WordPress"""
    try:
        if progress_callback:
            progress_callback(f"Loading article data from {os.path.basename(excel_path)}")
        
        article = pd.read_excel(excel_path)
        category = os.path.basename(os.path.dirname(excel_path))
        title = article.iloc[0,0]
        intro = article.iloc[0,2]
        subtitles = article.iloc[1:,1].tolist()
        subtitles_bodies = article.iloc[1:,2].tolist()
        num_subsections = article.shape[0]-1

        if progress_callback:
            headless_mode = config.get("browser", {}).get("headless", False)
            browser_mode = "headless" if headless_mode else "visible"
            progress_callback(f"Logging into website ({browser_mode} mode)...")

        driver = login_to_website(config)
        driver.get("https://pharmastan.net/wp-admin/post-new.php?post_type=disease")
        wait = WebDriverWait(driver, 15)
        
        if progress_callback:
            progress_callback("Filling article title and content...")
        
        wait.until(EC.visibility_of_element_located((By.ID, "title"))).send_keys(title)

        # Wait for the Visual tab and click it (optional if already active)
        wait = WebDriverWait(driver, 10)
        # Wait for the "Code" tab button
        code_btn = wait.until(EC.element_to_be_clickable((By.ID, "content-html")))
        code_btn.click()
        time.sleep(2)
        driver = fill_article_intro(driver, intro)
        time.sleep(2)

        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.switch-tmce"))
        )
        if button.get_attribute("aria-pressed") != "true":
            button.click()
        # Click only if not already pressed
        press_all_code_editors(driver)
        
        if progress_callback:
            progress_callback("Adding subsections...")
        
        # first add subsections
        for i in range(num_subsections-1):
            click_add_another_and_wait(driver)
        subsections_titles = driver.find_elements(By.NAME, "post_content_titles[]")
        # Fill in the subsections titles
        for i, field in enumerate(subsections_titles):
                field.clear()
                field.send_keys(subtitles[i])
        press_all_code_editors(driver)
        # Fill in the subsections content
        fill_all_subsections_bodies(driver, subtitles_bodies)
        
        if progress_callback:
            progress_callback("Setting category...")
        
        #choose the category
        select_category_by_name(driver, category)
        
        if progress_callback:
            progress_callback("Generating meta description...")
        
        textarea = driver.find_element(By.ID, "excerpt")  # By ID
        textarea.clear()
        try:
            excerpt_text = automation_engine.generate_arabic_meta_expert_summary(excel_path)['meta_expert_summary']
        except:
            excerpt_text = automation_engine.generate_arabic_meta_expert_summary_fireworks(excel_path)['meta_expert_summary']
        textarea.send_keys(excerpt_text)
        time.sleep(2)
        
        if progress_callback:
            progress_callback("Adding featured image...")
        
        featured_img_path = automation_engine.add_watermark_from_folder(
            folder_path=config['paths']['original_images_path'],
            output_path=config['paths']['featured_images_path'],
            watermark_image_path=config['paths']['logo_image_path'],
            base_size=(616, 367),
            transparency=0.2
        )
        upload_featured_image(driver, featured_img_path)
        time.sleep(2)
        
        if progress_callback:
            progress_callback("Publishing article...")
        
        click_publish(driver)
        
        if progress_callback:
            progress_callback(f"✅ Successfully published: {title}")
        
        driver.quit()
        return True
        
    except Exception as e:
        if 'driver' in locals():
            driver.quit()
        raise e