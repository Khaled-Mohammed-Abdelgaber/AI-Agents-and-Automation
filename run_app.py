#!/usr/bin/env python3
"""
Pharma Content Automation Desktop App Launcher
"""

import sys
import os

def check_dependencies():
    """Check if all required dependencies are installed"""
    required_packages = [
        'pandas', 'docx', 'google.generativeai', 'dotenv', 
        'undetected_chromedriver', 'selenium', 'requests', 'PIL'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'docx':
                import docx
            elif package == 'PIL':
                import PIL
            elif package == 'google.generativeai':
                import google.generativeai
            elif package == 'dotenv':
                import dotenv
            elif package == 'undetected_chromedriver':
                import undetected_chromedriver
            else:
                __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n📋 Please install missing packages using:")
        print("   pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies are installed!")
    return True

def main():
    """Main launcher function"""
    print("🚀 Starting Pharma Content Automation App...")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    try:
        # Import and run the main application
        from pharma_automation_app import main as app_main
        app_main()
    except ImportError as e:
        print(f"❌ Error importing application: {e}")
        print("📋 Make sure pharma_automation_app.py is in the same directory")
        input("\nPress Enter to exit...")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        input("\nPress Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    main()