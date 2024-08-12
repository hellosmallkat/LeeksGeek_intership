import requests
from bs4 import BeautifulSoup
import pandas as pd

# Base URL of the website
base_url = 'https://tsa.org.tw/members/page/'

# Initialize empty lists to store the data
companies = []
products = []
phones = []

# Function to scrape a single page
def scrape_page(page_number):
    url = base_url + str(page_number) + '/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all memberlist items
    memberlist_items = soup.find_all('li', class_='memberlist')
    
    for item in memberlist_items:
        company = item.find_all('div')[0].text.strip()
        product = item.find_all('div')[1].text.strip()
        phone = item.find_all('div')[2].text.strip()
        
        companies.append(company)
        products.append(product)
        phones.append(phone)

# Loop through the specified number of pages
for page in range(1, 5):  # There are 4 pages in total
    scrape_page(page)

# Create a DataFrame from the lists
data = {
    '公司': companies,
    '主要產品': products,
    '聯絡電話': phones
}
df = pd.DataFrame(data)

# Save the DataFrame to an Excel file
df.to_excel('company_info.xlsx', index=False)
print('Data has been written to company_info.xlsx')
