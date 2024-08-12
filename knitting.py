from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# Configure ChromeDriver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode for no GUI
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
service = Service('/mnt/c/Users/Kat/Desktop/chromedriver-linux64/chromedriver')  # Update path to your chromedriver
driver = webdriver.Chrome(service=service, options=chrome_options)

# Base URL and number of pages
base_url = "https://knitting.org.tw/members"
num_pages = 33  # Number of pages to scrape
data = []

try:
    for page in range(1, num_pages + 1):
        print(f"Scraping page {page}")
        url = f"{base_url}?posts_per_page=9&page={page}&city_name=&company_name=&lang=zh"
        driver.get(url)

        # Wait for the list of members to load
        wait = WebDriverWait(driver, 10)
        member_list = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul.page-members__content__right__info")))

        # Extract member details
        items = member_list.find_elements(By.CSS_SELECTOR, "li.page-members__content__right__info-item")
        for item in items:
            link_element = item.find_element(By.TAG_NAME, 'a')
            name = link_element.find_element(By.XPATH, ".//div[2]/p").text
            phone = link_element.find_element(By.XPATH, ".//div[3]/p").text
            contact_person = link_element.find_element(By.XPATH, ".//div[4]/p").text
            href = link_element.get_attribute('href')
            
            data.append({
                "Company Name": name,
                "Phone": phone,
                "Contact Person": contact_person,
                "Link": href
            })

finally:
    driver.quit()

# Save data to an Excel file
df = pd.DataFrame(data)
df.to_excel("extracted_member_info.xlsx", index=False)

print("Member information has been saved to 'extracted_member_info.xlsx'")
