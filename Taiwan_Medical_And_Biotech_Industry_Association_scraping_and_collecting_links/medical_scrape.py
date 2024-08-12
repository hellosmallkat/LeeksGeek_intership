import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

def scrape_company_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', {"class": "member_Table"})
    
    company_info = {}
    
    if table:
        rows = table.find_all('tr', class_='member_Table_List')
        for row in rows:
            th = row.find('th', class_='member_Table_Th')
            td = row.find('td', class_='member_Table_Td')
            if th and td:
                key = th.get_text(strip=True)
                value = td.get_text(strip=True)
                link = td.find('a')
                if link and link.get('href'):
                    value = link.get('href').replace('mailto:', '')
                company_info[key] = value
    
    return company_info

def sanitize_data(data):
    # Function to remove illegal characters from a string
    def clean_string(s):
        if isinstance(s, str):
            # Remove non-printable and control characters, while keeping Chinese characters
            s = re.sub(r'[^\u4e00-\u9fff\x20-\x7e]', '', s)
            return s
        return str(s)  # Convert non-strings to strings

    # Apply cleaning to all string values in the data
    sanitized_data = [{k: clean_string(v) for k, v in item.items()} for item in data]
    return sanitized_data

def save_to_excel(data, filename='company_details.xlsx'):
    # Sanitize the data
    sanitized_data = sanitize_data(data)
    # Create a DataFrame with the sanitized data
    df = pd.DataFrame(sanitized_data)
    # Save the DataFrame to an Excel file
    df.to_excel(filename, index=False)
    print(f"Company details saved to {filename}")

if __name__ == "__main__":
    # Load the links from the Excel file
    links_df = pd.read_excel('links_comp.xlsx')
    links = links_df['URL'].tolist()

    all_company_details = []
    
    # Loop over each link to scrape company details
    for link in links:
        print(f"Scraping link: {link}")
        company_info = scrape_company_info(link)
        all_company_details.append(company_info)

    # Save all company details to Excel
    save_to_excel(all_company_details)
