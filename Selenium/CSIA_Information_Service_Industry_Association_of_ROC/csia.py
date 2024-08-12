from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run headless Chrome
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Path to the ChromeDriver executable
service = Service(executable_path='/mnt/c/Users/Kat/Desktop/chromedriver-linux64/chromedriver')

# Initialize the WebDriver
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get("https://www.cisanet.org.tw/eBook/Index")

def scrape_page():
    data = []
    try:
        # Wait until the cards are present on the page
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".photo-cards .card"))
        )
        # Locate all cards on the page
        cards = driver.find_elements(By.CSS_SELECTOR, ".photo-cards .card")
        for card in cards:
            try:
                # Extract details from each card
                title_element = card.find_element(By.CSS_SELECTOR, ".card-title")
                title = title_element.text
                
                if not title:  # Skip cards without a title
                    continue

                img_element = card.find_element(By.CSS_SELECTOR, ".card-img-top")
                img_src = img_element.get_attribute("src")
                
                # Extract link and ensure it starts with "/eBook/eBook_more/"
                link_element = card.find_element(By.CSS_SELECTOR, "a")
                link = link_element.get_attribute("href")
                if link and link.startswith("/eBook/eBook_more/"):
                    link = "https://www.cisanet.org.tw" + link

                date_text = card.find_element(By.CSS_SELECTOR, ".page-subtitle .text-muted").text
                views_text = card.find_elements(By.CSS_SELECTOR, ".page-subtitle .text-muted")[1].text
                
                # Clean the extracted data
                date = date_text.split("日期 :")[1].strip() if "日期 :" in date_text else ""
                views = views_text.split("點閱數：")[1].strip() if "點閱數：" in views_text else ""
                
                data.append({
                    "Title": title,
                    "Image URL": img_src,
                    "Date": date,
                    "Views": views,
                    "Link": link
                })
            except Exception as e:
                print(f"Error extracting data from card: {e}")
    except Exception as e:
        print(f"Error scraping data: {e}")
    return data

def navigate_to_next_page():
    try:
        # Wait until the 'Next' button is clickable and then click it
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@title, 'next page')]"))
        )
        next_button.click()
        # Wait for the page to load and stabilize
        time.sleep(3)  # Adjust this sleep time based on page load speed
        return True
    except Exception as e:
        print(f"Error navigating to next page: {e}")
        return False

all_data = []
page_number = 1

while True:
    print(f"Scraping page {page_number}")
    page_data = scrape_page()
    if page_data:
        all_data.extend(page_data)
    else:
        print("No more data found on this page.")
        break

    if not navigate_to_next_page():
        break

    page_number += 1

# Save the data to an Excel file
df = pd.DataFrame(all_data)
df.to_excel("links_cisanet.xlsx", index=False)

# Clean up
driver.quit()

print("Scraping complete. Data saved to links_cisanet.xlsx.")
