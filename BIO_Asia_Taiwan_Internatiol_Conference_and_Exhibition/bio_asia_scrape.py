import pandas as pd
import requests
from bs4 import BeautifulSoup

# Function to extract information from a single page
def extract_info(url):
    print(f"Scraping page: {url}")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the <div id="right">
    right_div = soup.find('div', id='right')
    
    if not right_div:
        print(f"Could not find the right div for URL: {url}")
        return {
            "URL": url,
            "Company Name": "",
            "English Name": "",
            "Vendor Category": "",
            "Booth Number": "",
            "Website": "",
            "Company Profile": ""
        }

    # Extract information
    company_name = right_div.find('h1', class_='noPadding').get_text(strip=True)
    english_name = right_div.find('p', class_='italic').get_text(strip=True)
    
    vendor_category = ""
    booth_number = ""
    website = ""
    company_profile = ""
    
    p_tags = right_div.find_all('p')
    for p in p_tags:
        if '廠商分類：' in p.get_text():
            vendor_category = p.find('a').get_text(strip=True)
        if '攤位號碼：' in p.get_text():
            booth_number = p.get_text().replace('攤位號碼：', '').strip()
        if '公司網址：' in p.get_text():
            website = p.find('a')['href'].strip()
    
    # Find the <h3> tag with text "廠商介紹"
    intro_header = right_div.find('h3', text='廠商介紹')
    if intro_header:
        company_profile = intro_header.find_next_sibling(text=True).strip()

    # Return extracted data
    return {
        "URL": url,
        "Company Name": company_name,
        "English Name": english_name,
        "Vendor Category": vendor_category,
        "Booth Number": booth_number,
        "Website": website,
        "Company Profile": company_profile
    }

# Read URLs from the Excel file
input_file = 'links_bio_asia.xlsx'  # Replace with your file name
urls_df = pd.read_excel(input_file)
urls = urls_df['URL'].tolist()  # Replace 'URL' with the actual column name

# Initialize a list to hold data
data = []

# Scrape each URL and collect data
for url in urls:
    data.append(extract_info(url))

# Create a DataFrame from the list of data
df = pd.DataFrame(data)

# Save the DataFrame to an Excel file
output_file = 'scraped_data.xlsx'  # Replace with your desired file name
df.to_excel(output_file, index=False)

print(f"Data has been saved to {output_file}")
