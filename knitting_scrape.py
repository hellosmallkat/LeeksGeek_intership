import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
import random
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up chromedriver options
option = webdriver.ChromeOptions()
option.add_argument('--headless')  # Uncomment this line to run in headless mode
option.add_experimental_option('excludeSwitches', ['enable-automation'])
option.add_argument('--no-sandbox')  # Add this line to avoid sandbox-related issues
option.add_argument('--disable-dev-shm-usage')  # Add this line to avoid /dev/shm usage

# Specify the path to ChromeDriver executable
chromedriver_path = '/path/to/chromedriver'
driver = webdriver.Chrome(executable_path=chromedriver_path, options=option)

# Go to the textile website
url = "https://knitting.org.tw/members?posts_per_page=9&page=1&city_name=&company_name=&lang=zh"
driver.get(url)
driver.implicitly_wait(8)
sleep(3)

# Initialize data list
data = []

# Find company data on 33 pages
for i in range(0, 34):
    print("Page", i-9)
    try:
        next_pages = driver.find_elements(By.CSS_SELECTOR, '#wrapper > main > div > div.page-members__content > article > div > div > ul > li')[i]
        # Click on the page button
        next_pages.click()
        sleep(random.uniform(0.5, 2.0))
    except Exception as e:
        print("No more pages or an error occurred:", e)

    # Scroll using Selenium execute_script
    target_x, target_y = 2930, 980
    driver.execute_script(f"window.scrollTo({target_x}, {target_y});")

    # Visit each company on the page (9 companies per page)
    for j in range(0, 9):
        print("Company", j)
        sleep(random.uniform(0.5, 2.0))
        try:
            companies = driver.find_elements(By.CSS_SELECTOR, '#wrapper > main > div > div.page-members__content > article > div > div > ul > li')[j]
            print(companies.text)
            companies.click()
            sleep(random.uniform(0.5, 2.0))
        except Exception as e:
            print("No more pages or an error occurred:", e)

        # Scrape data for each company
        # Get company name
        company_name = driver.find_element(By.CSS_SELECTOR, '#top > div.container > div > div.page-member-single__info__title').text
        data.append(company_name)

        # Get company information
        company_infos = driver.find_elements(By.CSS_SELECTOR, '#top > div.container > div > div.page-member-single__info__content > ul > li')
        for company_info in company_infos:
            temp = company_info.text.split("\n")
            data.append(temp)

        # Go back to previous page
        back_button = driver.find_element(By.CSS_SELECTOR, '#top > div.container > div > div.page-member-single__info-btn > div')
        back_button.click()
        sleep(random.uniform(0.5, 2.0))

        # Scroll back using Selenium execute_script
        driver.execute_script("window.scrollTo(0, 0);")

# Save data to JSON file
with open('company_info.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

# Quit the driver
driver.quit()
