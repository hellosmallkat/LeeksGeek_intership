import requests
from bs4 import BeautifulSoup
import pandas as pd

# Base URL
base_url = 'https://www.filaweaving.org.tw/list/member-information.htm#/'

# Initialize lists to store data
company_names = []
phone_numbers = []
emails = []
websites = []

# Function to scrape data from the single URL
def scrape_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table', class_='table')
        if table:
            rows = table.find_all('tr')
            for row in rows:
                columns = row.find_all('td')
                if len(columns) >= 4:
                    company_name = columns[0].a.text.strip()
                    phone_number = columns[1].a.text.strip()
                    email = columns[2].a.get('href').replace('mailto:', '').strip()
                    website = columns[3].a.get('href').strip()

                    company_names.append(company_name)
                    phone_numbers.append(phone_number)
                    emails.append(email)
                    websites.append(website)
        else:
            print(f"No table found on {url}")
    else:
        print(f"Failed to retrieve data from {url}")

# Start scraping from the base URL
scrape_data(base_url)

# Create a DataFrame
data = {
    '公司名稱': company_names,
    '電話': phone_numbers,
    'Email': emails,
    '網址': websites
}
df = pd.DataFrame(data)

# Save to Excel
output_file = 'weaving_companies.xlsx'
df.to_excel(output_file, index=False)
print(f"Data saved to {output_file}")
