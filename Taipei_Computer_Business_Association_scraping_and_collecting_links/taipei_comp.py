import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_table(page_url):
    response = requests.get(page_url)
    
    # Ensure correct encoding
    response.encoding = response.apparent_encoding
    
    # Use BeautifulSoup to parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Debugging: Print the raw HTML content to check structure
    #print("HTML content:")
    #print(soup.prettify())

    # Find the table
    table = soup.find('table', {'width': '70%', 'border': '1'})
    
    # Handle case where the table is not found
    if table is None:
        print(f"Table not found on page: {page_url}")
        return []

    rows = table.find_all('tr')
    data = []
    for row in rows[1:]:  # Skip header row
        cols = row.find_all('td')
        
        # Handle cases where columns might be missing
        if len(cols) < 3:
        #    print(f"Skipping row with insufficient columns: {row}")
            continue

        # Debugging: Print the raw HTML content of the row
       # print("Raw HTML of row:")
        #(row.prettify())

        member_id = cols[0].get_text(strip=True)
        
        # Get company name directly from text and verify the content
        company_name_tag = cols[1].find('a')
        if company_name_tag:
            company_name = company_name_tag.get_text(strip=True)
            # Debugging: Print extracted company name
    #        print(f"Extracted company name: {company_name}")
        else:
            company_name = cols[1].get_text(strip=True)
            # Debugging: Print extracted company name
     #       print(f"Extracted company name (without a tag): {company_name}")
        
        contact_number = cols[2].get_text(strip=True)
        data.append([member_id, company_name, contact_number])
    
    return data

# Base URL for the pages
base_url = "https://www.tca.org.tw/tcaprdqc.asp?bytype=pcode&PRODUCT_CNAME=Z999&page="

all_data = []

# Loop through the 12 pages
for page_num in range(1, 13):
    page_url = f"{base_url}{page_num}"
    page_data = scrape_table(page_url)
    all_data.extend(page_data)

# Print data for debugging
#for item in all_data:
#    print(item)

# Create a DataFrame and save it to an Excel file
columns = ['會員編號', '公司名稱', '聯絡電話']
df = pd.DataFrame(all_data, columns=columns)

df.to_excel('scraped_data.xlsx', index=False)

print("Data has been scraped and saved to 'scraped_data.xlsx'.")
