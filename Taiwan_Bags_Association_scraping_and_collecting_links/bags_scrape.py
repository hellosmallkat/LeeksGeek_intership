import requests
from bs4 import BeautifulSoup
import pandas as pd

# Define the URL of the webpage
url = 'https://expo.bioasiataiwan.com/visitorExhibitorDetail.asp?comNo=130700&sno=195416'

# Send a request to fetch the content
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Initialize a dictionary to store the scraped data
data = {
    'Company Name': None,
    'Vendor Category': None,
    'Booth Number': None,
    'Company Website': None,
    'Manufacturer Introduction': None,
    'Exhibited Brands': None
}

# Extract company name
company_name_h1 = soup.find('h1', class_='noPadding')
if company_name_h1:
    data['Company Name'] = company_name_h1.get_text(strip=True)

# Extract vendor category
vendor_category_p = soup.find('p', text=lambda text: text and 'Manufacturer Category:' in text)
if vendor_category_p:
    data['Vendor Category'] = vendor_category_p.get_text(strip=True).replace('Manufacturer Category:', '').strip()

# Extract booth number
booth_number_p = soup.find('p', text=lambda text: text and 'Booth number:' in text)
if booth_number_p:
    data['Booth Number'] = booth_number_p.get_text(strip=True).replace('Booth number:', '').strip()

# Extract company website
website_p = soup.find('p', text=lambda text: text and 'Company website:' in text)
if website_p:
    website_link = website_p.find('a')
    if website_link:
        data['Company Website'] = website_link.get('href', '').strip()

# Extract manufacturer introduction
introduction_header = soup.find('h3', text=lambda text: text and 'Manufacturer introduction' in text)
if introduction_header:
    next_p = introduction_header.find_next_sibling('p')
    if next_p:
        data['Manufacturer Introduction'] = next_p.get_text(strip=True)

# Extract exhibited brands
exhibited_brands_header = soup.find('h3', text=lambda text: text and 'Exhibited brands' in text)
if exhibited_brands_header:
    next_p = exhibited_brands_header.find_next_sibling('p')
    if next_p:
        data['Exhibited Brands'] = next_p.get_text(strip=True)

# Print the scraped data
print(data)

# Save the data to a DataFrame and then to an Excel file
df = pd.DataFrame([data])
df.to_excel('bags_scraped_data.xlsx', index=False)


#needs more work