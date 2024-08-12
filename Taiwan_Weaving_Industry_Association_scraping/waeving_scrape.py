import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook

# URL pattern for the pages
base_url = 'https://weaving.org.tw/members/page/{}'

# Number of pages to scrape (adjust this based on actual number of pages)
num_pages = 16

# List to store extracted data
results = []

# Loop through each page
for page_num in range(1, num_pages + 1):
    url = base_url.format(page_num)
    print(f"Scraping page {page_num}/{num_pages} - {url}")
    
    # Fetch the page content
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all list items with class 'member'
        items = soup.find_all('li', class_='member')
        
        # Extract data from each item
        for item in items:
            # Check if 'data-id' attribute exists
            if 'data-id' in item.attrs:
                data_id = item['data-id']
                company_name = item.find('h3').text.strip()
                phone_1 = item.find_all('div')[1].text.strip()
                phone_2 = item.find_all('div')[2].text.strip()
                
                # Store the extracted data
                results.append({
                    'data_id': data_id,
                    'company_name': company_name,
                    'phone_1': phone_1,
                    'phone_2': phone_2
                })
            else:
                print("Warning: 'data-id' attribute not found in an <li> element.")
    else:
        print(f"Failed to retrieve page {page_num}")

# Write data to Excel
if results:
    wb = Workbook()
    ws = wb.active
    ws.append(['Data ID', 'Company Name', 'Phone 1', 'Phone 2'])
    
    for result in results:
        ws.append([result['data_id'], result['company_name'], result['phone_1'], result['phone_2']])
    
    wb.save('weaving_data.xlsx')
    print("Data saved to weaving_data.xlsx")
else:
    print("No data to save.")

