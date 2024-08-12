import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_table_data(url):
    try:
        # Fetch the content from URL
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        
        # Parse the content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the table with class 'table-bordered'
        table = soup.find('table', class_='table-bordered')
        
        if not table:
            print(f"No table found on {url}")
            return {}
        
        # Initialize dictionary to store table data
        table_data = {}
        
        # Find all rows (tr) in the table body (tbody)
        rows = table.find_all('tr')
        
        for row in rows:
            # Extract the text from th (header) and td (data) cells
            header = row.find('th')
            data = row.find('td')
            
            if header and data:
                header_text = header.get_text(strip=True)
                data_text = data.get_text(strip=True)
                
                # Store data in dictionary
                table_data[header_text] = data_text
        
        return table_data
    
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return {}

def combine_with_base_url(base_url, links):
    combined_links = []
    for link in links:
        combined_url = base_url.rstrip('/') + link.lstrip('/')
        combined_links.append(combined_url)
    return combined_links

def save_to_excel(data_list, filename='woven_scraped_data.xlsx'):
    # Create a DataFrame from list of dictionaries
    df = pd.DataFrame(data_list)
    
    # Save DataFrame to Excel
    df.to_excel(filename, index=False)
    print(f"Data saved to {filename}")

if __name__ == "__main__":
    # Assuming 'links_comp.xlsx' contains a column 'Links' with /basic/?node=xxxxx links
    input_filename = 'woven_links.xlsx'
    base_url = ""
    
    # Load links from Excel
    df = pd.read_excel(input_filename)
    links = df['URL'].tolist()
    
    # Combine links with base URL
    combined_links = combine_with_base_url(base_url, links)
    
    # Scraping data from each combined link
    scraped_data = []
    for url in combined_links:
        print(f"Scraping data from: {url}")
        data = scrape_table_data(url)
        scraped_data.append(data)
    
    # Save scraped data to Excel
    save_to_excel(scraped_data)


#flutter -> hello world
#
#