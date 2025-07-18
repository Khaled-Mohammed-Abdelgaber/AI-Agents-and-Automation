#!/usr/bin/env python3
"""
Article Automation Desktop Application Launcher
This script sets up the environment and launches the GUI application.
"""

import sys
import os
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required.")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    else:
        print(f"✅ Python version OK: {sys.version}")

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'pandas', 'python-docx', 'google-generativeai', 
        'undetected-chromedriver', 'selenium', 'requests', 
        'Pillow', 'xlsxwriter', 'openpyxl'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'python-docx':
                import docx
            elif package == 'google-generativeai':
                import google.generativeai
            elif package == 'undetected-chromedriver':
                import undetected_chromedriver
            elif package == 'Pillow':
                import PIL
            else:
                __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        
        response = input("\n🔧 Would you like to install missing packages automatically? (y/n): ")
        if response.lower() in ['y', 'yes']:
            install_dependencies()
        else:
            print("\n📋 To install manually, run:")
            print("   pip install -r requirements.txt")
            sys.exit(1)
    else:
        print("✅ All required packages are installed")

def install_dependencies():
    """Install missing dependencies"""
    requirements_file = Path(__file__).parent / "requirements.txt"
    
    if not requirements_file.exists():
        print("❌ requirements.txt not found!")
        sys.exit(1)
    
    try:
        print("📦 Installing dependencies...")
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
        ])
        print("✅ Dependencies installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        print("Please install manually using: pip install -r requirements.txt")
        sys.exit(1)

def launch_application():
    """Launch the main application"""
    try:
        from main import main
        print("🚀 Launching Article Automation Tool...")
        main()
    except Exception as e:
        print(f"❌ Failed to launch application: {e}")
        print("\nPlease ensure all dependencies are installed correctly.")
        sys.exit(1)

def main():
    """Main launcher function"""
    print("=" * 60)
    print("   Article Automation Desktop Application Launcher")
    print("=" * 60)
    
    # Check Python version
    check_python_version()
    
    # Check and install dependencies if needed
    check_dependencies()
    
    # Launch the application
    launch_application()

if __name__ == "__main__":
    main()