from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.binary_location = "/usr/bin/google-chrome"  # Path to Chrome binary

service = Service(executable_path='/mnt/c/Users/Kat/Desktop/chromedriver-linux64/chromedriver')
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get("https://www.selenium.dev/documentation/webdriver/getting_started/first_script/")
print(driver.title)

try:
    from selenium import webdriver
    print("Selenium is installed and working.")
except ImportError:
    print("Selenium is not installed.")

driver.quit()
