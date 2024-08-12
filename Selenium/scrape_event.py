from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Chrome options setup
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
service = Service('/mnt/c/Users/Kat/Desktop/chromedriver-linux64/chromedriver')  # Update path to your chromedriver
driver = webdriver.Chrome(service=service, options=chrome_options)

# URL of the website
url = 'https://event.cw.com.tw/2024dnb/award.html'
driver.get(url)

# Initialize a list to store the company names
company_names = []

# Define the button texts and their corresponding datatag attributes
award_buttons = {
    "Cooperation Treasury Sustainable Rock Award": "bkArr",
    "Annual Corporate MVP Award": "mvpArr",
    "Sustainable Excellence Award": "esgArr",
    "Trade Pilot Award": "trendArr",
    "Elite Award": "normalArr"
}

# Function to click a button using JavaScript
def click_element_by_js(element):
    driver.execute_script("arguments[0].click();", element)

# Function to wait for and click a button
def wait_and_click(datatag):
    try:
        button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, f"//div[@class='tage' and @datatag='{datatag}']"))
        )
        click_element_by_js(button)
        time.sleep(3)  # Wait for the content to load
    except Exception as e:
        print(f"Failed to click button with datatag '{datatag}': {e}")

# Function to scrape company names
def scrape_companies():
    try:
        companies = driver.find_elements(By.CSS_SELECTOR, ".award_wall .company")
        if companies:
            print(f"Found {len(companies)} companies")
        for company in companies:
            company_names.append(company.text.strip())
    except Exception as e:
        print(f"Failed to scrape companies: {e}")

# Click each button and scrape the company names
for button_text, datatag in award_buttons.items():
    print(f"Processing: {button_text}")  # Debug message
    wait_and_click(datatag)
    scrape_companies()

# Quit the driver
driver.quit()

# Save to a spreadsheet
df = pd.DataFrame(company_names, columns=["Company Name"])
df.to_excel("company_names.xlsx", index=False)

print("Scraping completed and data saved to 'company_names.xlsx'.")
