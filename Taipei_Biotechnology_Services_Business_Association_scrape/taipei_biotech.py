import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_data(page_url):
    response = requests.get(page_url)
    
    # Ensure correct encoding
    response.encoding = response.apparent_encoding
    
    # Use BeautifulSoup to parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the <ul> element
    ul = soup.find('ul', {'id': 'guildmemberul'})
    
    # Handle case where the <ul> is not found
    if ul is None:
        print(f"UL element not found on page: {page_url}")
        return []

    # Find all <li> elements within the <ul>
    lis = ul.find_all('li')
    
    data = []
    for li in lis[1:]:  # Skip the first <li> which is the header
        divs = li.find_all('div', class_='data')
        
        # Handle cases where divs might be missing
        if len(divs) < 3:
            continue

        company_name = divs[0].get_text(strip=True)
        representative = divs[1].get_text(strip=True)
        company_address = divs[2].get_text(strip=True)
        
        data.append([company_name, representative, company_address])
    
    return data

# Base URL for the pages
base_url = "https://tbsa.org.tw/tc/guildmember?page="

all_data = []

# Loop through the pages
for page_num in range(1, 9):  # Adjust the range according to the number of pages
    page_url = f"{base_url}{page_num}"
    page_data = scrape_data(page_url)
    all_data.extend(page_data)

# Create a DataFrame and save it to an Excel file
columns = ["公司名稱", "代表人", "公司地址"]
df = pd.DataFrame(all_data, columns=columns)

df.to_excel('Biotech_scraped_data.xlsx', index=False)

print("Data has been scraped and saved to 'Biotech_scraped_data.xlsx'.")
