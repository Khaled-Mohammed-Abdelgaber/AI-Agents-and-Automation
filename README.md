# Article Automation Desktop Application

A desktop GUI application for automating the process of converting Word documents to Excel format and publishing articles to a WordPress website.

## Features

- **User-friendly GUI**: Easy-to-use interface with tabbed layout
- **Configuration Management**: All settings are configurable through the GUI and automatically saved
- **Persistent Settings**: The application remembers your last configuration
- **Real-time Processing**: Live progress tracking and logging
- **Multi-threaded**: Processing runs in the background without freezing the UI
- **Error Handling**: Failed files are moved to a separate folder for review

## Installation

### Prerequisites

- Python 3.8 or higher
- Google Chrome browser (for Selenium automation)

### Setup

1. **Clone or download the application files**
   ```bash
   git clone <repository-url>
   cd article-automation
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

## Configuration

### First Time Setup

1. **Launch the application** by running `python main.py`

2. **Configure the settings** in the "Configuration" tab:

   **Website Credentials:**
   - Username: Your website login username
   - Password: Your website login password
   - Login URL: The website login page URL (default: https://pharmastan.net/pharma-login)

   **File Paths:**
   - Excel Output Path: Where Excel files will be saved
   - Word Input Path: Folder containing Word documents to process
   - Failed Files Path: Where failed files will be moved
   - Done Files Path: Where successfully processed files will be moved
   - Logo Image Path: Path to your watermark logo image
   - Original Images Path: Folder containing original images for featured images
   - Featured Images Path: Where watermarked featured images will be saved

   **API Keys:**
   - Gemini API Key: Your Google Gemini API key for content generation
   - Fireworks API Key: Backup API key for Fireworks AI service

   **Timeouts (optional):**
   - Adjust timeout values for different operations (in milliseconds)

3. **Save Configuration** by clicking the "Save Configuration" button

## Usage

### Processing Articles

1. **Place Word documents** in your configured Word Input Path
2. **Switch to the "Processing" tab**
3. **Click "Start Processing"** to begin automation
4. **Monitor progress** through the progress bar and log window
5. **Stop processing** anytime using the "Stop Processing" button

### What the Application Does

1. **Converts Word to Excel**: Extracts structured content from Word documents and creates Excel files
2. **Website Automation**: Logs into the website using Selenium
3. **Article Creation**: Creates new articles with:
   - Article title and content
   - Subsections with titles and content
   - Category selection
   - Meta descriptions (generated using AI)
   - Featured images (with watermark)
4. **File Management**: Moves processed files to "done" folder, failed files to "failed" folder

### Word Document Format

Your Word documents should follow this structure:

```
### Article Title ###
Article introduction content...

$$$ Subsection 1 Title $$$
Subsection 1 content...

$$$ Subsection 2 Title $$$
Subsection 2 content...
```

## Configuration Storage

All your settings are automatically saved to:
- **Windows**: `C:\Users\<username>\.article_automation_config.ini`
- **Linux/Mac**: `~/.article_automation_config.ini`

The application will remember your settings between sessions.

## Troubleshooting

### Common Issues

1. **Chrome driver issues**: Make sure you have Google Chrome installed. The application will automatically download the compatible Chrome driver.

2. **File permissions**: Ensure the application has read/write access to all configured folders.

3. **API errors**: Verify your API keys are correct and have sufficient quota.

4. **Selenium timeouts**: Increase timeout values in the configuration if the website is slow.

### Log Messages

- 🚀 Starting article processing
- 📄 Processing Word documents
- 📝 Processing individual articles
- ✅ Successfully completed operations
- ❌ Error messages with details
- 🛑 User-initiated stops

## Security Notes

- API keys are stored locally and masked in the interface
- Passwords are hidden with asterisks in the GUI
- Configuration file is stored in your user directory

## Support

If you encounter issues:

1. Check the processing log for error details
2. Verify all file paths exist and are accessible
3. Ensure API keys are valid
4. Check internet connectivity for website automation

## Requirements

See `requirements.txt` for the complete list of Python dependencies.
