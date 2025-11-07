"""Script to setup Chrome driver manually."""
import os
import sys
import zipfile
import requests
from pathlib import Path

def get_chrome_version():
    """Get installed Chrome version."""
    # Locations to check for Chrome
    locations = [
        r'C:\Program Files\Google\Chrome\Application\chrome.exe',
        r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
    ]
    
    for loc in locations:
        if os.path.exists(loc):
            from win32com.client import Dispatch
            parser = Dispatch("Scripting.FileSystemObject")
            version = parser.GetFileVersion(loc)
            return version.split('.')[0]  # Major version
    
    return None

def download_chromedriver():
    """Download and setup ChromeDriver."""
    chrome_version = get_chrome_version()
    if not chrome_version:
        print("Chrome not found. Please install Chrome first.")
        sys.exit(1)
    
    # Download URL pattern
    url = f"https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{chrome_version}"
    
    try:
        # Get the exact version
        response = requests.get(url, timeout=10)
        driver_version = response.text.strip()
        
        # Download ChromeDriver
        download_url = f"https://chromedriver.storage.googleapis.com/{driver_version}/chromedriver_win32.zip"
        response = requests.get(download_url, timeout=30)
        
        # Save and extract
        zip_path = Path('chromedriver.zip')
        zip_path.write_bytes(response.content)
        
        with zipfile.ZipFile(zip_path) as zip_file:
            zip_file.extract('chromedriver.exe')
        
        # Cleanup
        zip_path.unlink()
        print("ChromeDriver setup complete!")
        
    except Exception as e:
        print(f"Error downloading ChromeDriver: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    download_chromedriver()