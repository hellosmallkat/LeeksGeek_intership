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

# Step 2: Load the webpage
driver.get("https://tsa.org.tw/members/")

# Step 3: Wait for the elements to be clickable and click to reveal information
wait = WebDriverWait(driver, 10)
member_items = driver.find_elements(By.CLASS_NAME, 'memberlist')
for member_item in member_items:
    # Click on each member to reveal the detailed information
    actions = ActionChains(driver)
    actions.move_to_element(member_item).click().perform()
    time.sleep(2)  # Wait for the content to load

# Step 4: Parse the HTML content
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Step 5: Locate the memberlist items
member_items = soup.find_all('li', class_='memberlist')
if not member_items:
    raise ValueError("No memberlist items found on the web page")

# Step 6: Extract the data from each memberlist item
data = []
for item in member_items:
    data_id = item['data-id']
    divs = item.find_all('div')
    company_name = divs[0].text.strip() if len(divs) > 0 else ''
    products = divs[1].text.strip() if len(divs) > 1 else ''
    contact = divs[2].text.strip() if len(divs) > 2 else ''

    # Locate the detailed information section
    open_member = item.find_next_sibling('div', class_='open_member')
    if open_member:
        details = open_member.find_all('li')
        responsible_person = details[0].find_all('div')[1].text.strip() if len(details) > 0 else ''
        capital = details[1].find_all('div')[1].text.strip() if len(details) > 1 else ''
        main_products = details[2].find_all('div')[1].text.strip() if len(details) > 2 else ''
        address = details[3].find_all('div')[1].text.strip() if len(details) > 3 else ''
        phone = details[4].find_all('div')[1].text.strip() if len(details) > 4 else ''
        fax = details[5].find_all('div')[1].text.strip() if len(details) > 5 else ''
        website = details[6].find('a').get('href') if len(details) > 6 else ''
        email = details[7].find('a').get('href').replace('mailto:', '') if len(details) > 7 else ''
    else:
        responsible_person = capital = main_products = address = phone = fax = website = email = ''

    data.append([
        data_id, company_name, products, contact, responsible_person, capital, main_products,
        address, phone, fax, website, email
    ])

# Close the browser
driver.quit()

# Debug: Print the first few data items to ensure data extraction is correct
print("First few data items extracted:", data[:5])

# Step 7: Store data in a pandas DataFrame
columns = [
    'ID', 'Company Name', 'Products', 'Contact', 'Responsible Person', 'Capital', 'Main Products',
    'Address', 'Phone', 'Fax', 'Website', 'Email'
]
df = pd.DataFrame(data, columns=columns)

# Step 8: Write DataFrame to an Excel file
df.to_excel('TSA_member_data.xlsx', index=False)

print("Data has been successfully written to TSA_member_data.xlsx")
