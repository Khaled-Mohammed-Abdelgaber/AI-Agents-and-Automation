# Pharma Content Automation Desktop App

A desktop application that automates the process of converting Word documents to Excel format and publishing pharmaceutical articles to WordPress websites with AI-generated meta descriptions and featured images.

## Features

- **Document Conversion**: Convert Word (.docx) documents to structured Excel files
- **WordPress Automation**: Automatically publish articles to WordPress websites
- **AI Integration**: Generate Arabic meta descriptions using Gemini AI or Fireworks AI
- **Image Processing**: Add watermarks to images and set featured images
- **Configuration Management**: Save and load application settings
- **Progress Tracking**: Real-time processing logs and progress indicators
- **Error Handling**: Automatic file organization for successful and failed processing

## Prerequisites

- Python 3.8 or higher
- Google Chrome browser (for Selenium automation)
- Valid API keys for AI services (Gemini AI and/or Fireworks AI)
- WordPress website access credentials

## Installation

1. **Clone or download the project files**
2. **Install required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create a `.env` file (optional) with your API keys:**
   ```
   Gemini_api_key=your_gemini_api_key_here
   fireworks_api_key=your_fireworks_api_key_here
   ```

## Usage

### 1. Starting the Application

Run the main application:
```bash
python pharma_automation_app.py
```

### 2. Configuration Setup

#### First Time Setup:
1. Open the **Configuration** tab
2. Fill in the required fields:

**Website Credentials:**
- Username: Your WordPress username
- Password: Your WordPress password
- Login URL: Your WordPress login page URL

**File Paths:**
- Word Documents Folder: Folder containing .docx files to process
- Excel Output Folder: Where converted Excel files will be saved
- Failed Files Folder: Where failed files will be moved
- Completed Files Folder: Where successfully processed files will be moved
- Logo Image Path: Path to your logo/watermark image
- Original Images Folder: Folder containing original images for featured images
- Featured Images Folder: Where processed featured images will be saved

**API Keys:**
- Gemini API Key: Your Google Gemini API key
- Fireworks API Key: Your Fireworks AI API key

**Browser Settings:**
- Headless Mode: Choose whether to run browser automation in hidden mode
  - ✅ **Checked (Headless)**: Browser runs in background (faster, no visual distraction)
  - ❌ **Unchecked (Visible)**: Browser window is visible (useful for debugging)

3. Click **Save Configuration** to store your settings

### 3. Processing Articles

The application now provides two separate processes for better control:

#### Step 1: Convert Word to Excel
1. Switch to the **Process Articles** tab
2. Ensure your Word documents are in the specified input folder
3. Click **Convert Word to Excel**
4. Monitor the conversion progress in the log area
5. Converted Word files will be moved to the "Completed Files" folder
6. Excel files will be ready for publication

#### Step 2: Publish to WordPress
1. After successful conversion, the **Publish to WordPress** button will be enabled
2. Ensure all WordPress credentials and API keys are configured
3. Click **Publish to WordPress**
4. Monitor the publication progress in the log area
5. Successfully published articles will be moved to the "Completed Files" folder
6. Failed publications will be moved to the "Failed Files" folder

#### File Status Monitoring
- The status area shows real-time counts of Word documents and Excel files ready for publication
- **Browser Mode** indicator shows whether automation will run in "Headless" or "Visible" mode
- Click **Refresh** to update file counts manually
- Button states automatically update based on available files

### 4. Document Format Requirements

Your Word documents should follow this structure:

```
### Article Title 1 ###
Introduction content for article 1

$$$ Subsection Title 1 $$$
Content for subsection 1

$$$ Subsection Title 2 $$$
Content for subsection 2

### Article Title 2 ###
Introduction content for article 2

$$$ Subsection Title 1 $$$
Content for subsection 1
```

## File Structure

```
pharma-automation/
├── pharma_automation_app.py    # Main GUI application
├── automation_functions.py     # Selenium automation functions
├── requirements.txt           # Python dependencies
├── disease_categories.csv     # Category mappings
├── config.json               # Saved configuration (auto-generated)
├── README.md                 # This file
└── .env                      # API keys (optional)
```

## Configuration File

The application automatically saves your configuration in `config.json`. This file includes:
- Website credentials
- File paths
- API keys
- Timeout settings

## Category Mapping

The `disease_categories.csv` file maps category names to WordPress category IDs. Update this file to match your WordPress categories:

```csv
id,category_name
1,أمراض القلب والأوعية الدموية
2,أمراض الجهاز التنفسي
...
```

## Troubleshooting

### Common Issues:

1. **Chrome Driver Issues:**
   - Ensure Google Chrome is installed
   - The application uses undetected-chromedriver which auto-downloads compatible drivers

2. **API Errors:**
   - Verify your API keys are correct
   - Check internet connectivity
   - Ensure you have sufficient API credits

3. **WordPress Login Issues:**
   - Verify credentials are correct
   - Check if WordPress site is accessible
   - Ensure login URL is correct

4. **File Processing Errors:**
   - Check Word document format matches expected structure
   - Verify file permissions
   - Ensure input/output folders exist and are accessible

5. **Browser Automation Issues:**
   - If headless mode fails, try disabling it to see what's happening
   - Use visible mode for debugging and testing
   - Headless mode may require additional system resources

### Logs and Debugging:

- Check the processing log in the application for detailed error messages
- Failed files are automatically moved to the "Failed Files" folder
- Review console output for additional technical details

## Security Notes

- API keys and passwords are stored locally in the configuration file
- Ensure your configuration file is kept secure
- Consider using environment variables for sensitive data

## Support

For issues and questions:
1. Check the processing logs for error details
2. Verify all configuration settings
3. Ensure all required dependencies are installed
4. Review the document format requirements

## Version History

- v1.0: Initial release with GUI, automation, and AI integration
