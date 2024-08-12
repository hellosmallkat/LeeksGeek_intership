import pandas as pd
import requests
from bs4 import BeautifulSoup

def scrape_company_info(url):
    # Send a GET request to the URL
    response = requests.get(url)
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    # Find the table with the specified attributes
    table = soup.find('table', {'width': '96%', 'border': '0', 'align': 'center', 'cellpadding': '0', 'cellspacing': '0'})
    
    company_info = {}
    
    if table:
        rows = table.find_all('tr')
        for row in rows:
            cells = row.find_all('td')
            if len(cells) == 2:
                key = cells[0].get_text(strip=True)
                value = cells[1].get_text(strip=True)
                company_info[key] = value
    
    return company_info

def save_to_excel(data, filename='company_details.xlsx'):
    # Create a DataFrame with the data
    df = pd.DataFrame(data)
    # Save the DataFrame to an Excel file
    df.to_excel(filename, index=False)
    print(f"Company details saved to {filename}")

if __name__ == "__main__":
    # Load the links from the Excel file
    links_df = pd.read_excel('links_comps.xlsx')
    links = links_df['Links'].tolist()

    all_company_details = []
    
    # Loop over each link to scrape company details
    for link in links:
        print(f"Scraping link: {link}")
        company_info = scrape_company_info(link)
        all_company_details.append(company_info)

    # Save all company details to Excel
    save_to_excel(all_company_details)
