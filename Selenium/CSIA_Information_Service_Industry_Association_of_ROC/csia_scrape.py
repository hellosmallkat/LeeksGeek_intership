import pandas as pd
import requests
from bs4 import BeautifulSoup

# Function to extract information from a single page
def extract_info(url):
    print(f"Scraping page: {url}")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    def find_next_text(soup, text):
        element = soup.find(string=text)
        if element:
            return element.find_next().get_text(strip=True)
        return ""
    
    def find_next_link(soup, text):
        element = soup.find(string=text)
        if element:
            link = element.find_next('a')
            if link:
                return link['href'].strip()
        return ""
    
    # Extract information
    vendor_category = find_next_text(soup, "Vendor Category:")
    booth_number = find_next_text(soup, "Booth number:")
    website = find_next_link(soup, "Company website:")
    company_profile = find_next_text(soup, "Manufacturer introduction")
    service_intro = find_next_text(soup, "Service introduction")
    
    # Return extracted data
    return {
        "URL": url,
        "Vendor Category": vendor_category,
        "Booth Number": booth_number,
        "Website": website,
        "Company Profile": company_profile,
        "Service Introduction": service_intro
    }

# Read URLs from the Excel file
input_file = 'links_cisanet.xlsx'  # Replace with your file name
urls_df = pd.read_excel(input_file)
urls = urls_df['Link'].tolist()  # Replace 'Links' with the actual column name

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
