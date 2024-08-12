import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException

def is_chromedriver_path_valid(chrome_driver_path):
    # Check if the file exists at the given path
    if not os.path.exists(chrome_driver_path):
        print(f"Path does not exist: {chrome_driver_path}")
        return False

    # Check if it's a file
    if not os.path.isfile(chrome_driver_path):
        print(f"Path is not a file: {chrome_driver_path}")
        return False

    try:
        # Create a Service object with the specified ChromeDriver path
        service = Service(executable_path=chrome_driver_path)
        
        # Initialize WebDriver with the Service object
        driver = webdriver.Chrome(service=service)
        
        # Close the browser
        driver.quit()
        
        print("ChromeDriver path is valid.")
        return True
    except WebDriverException as e:
        print(f"WebDriverException: {e}")
        return False

def get_chromedriver_path():
    chrome_driver_path = input("Enter the path to ChromeDriver (e.g., C:\\path\\to\\chromedriver.exe): ").strip()
    return chrome_driver_path

# Check if the ChromeDriver path is provided, otherwise ask the user
chrome_driver_path = input("Enter the path to ChromeDriver (e.g., C:\\path\\to\\chromedriver.exe): ").strip()
if not chrome_driver_path:
    chrome_driver_path = get_chromedriver_path()

# Test the function with the given ChromeDriver path
is_valid = is_chromedriver_path_valid(chrome_driver_path)
print(f"Is the ChromeDriver path valid? {is_valid}")
