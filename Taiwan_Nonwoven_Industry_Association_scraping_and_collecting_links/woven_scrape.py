import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Base URL to combine with relative URLs from the spreadsheet
base_url = 'https://www.nonwoven.org.tw/'

# Load Excel file with list of unique websites (adjust filename as needed)
excel_file = 'links_comp.xlsx'
sheet_name = 'Sheet1'  # Adjust sheet name if necessary

# Read Excel into a DataFrame
df = pd.read_excel(excel_file, sheet_name=sheet_name)

# Function to scrape data from a webpage
def scrape_website(url):
    # Combine base_url with relative URL from the spreadsheet
    full_url = urljoin(base_url, url)
    
    # Fetch the webpage content
    response = requests.get(full_url)
    html_content = response.content
    
    # Parse the HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find the table element
    table = soup.find('table', class_='table')  # Adjust class name as per your HTML
    
    if table is None:
        print(f"Table not found on page: {full_url}")
        return [url, 'Table not found']
    
    # Initialize list to store extracted data from the second cells
    data = [url]  # Start with the URL as the first item
    
    # Loop through table rows and extract data from the second cell
    for row in table.find_all('tr'):
        cells = row.find_all(['th', 'td'])
        if len(cells) >= 2:
            # Extract the text from the second cell
            second_cell_text = cells[1].text.strip()
            if not second_cell_text:
                second_cell_text = 'X'
            data.append(second_cell_text)
    
    return data

# List to store all scraped data lists
all_data = []

# Iterate through each unique URL in the DataFrame
unique_urls = df['URL'].unique()  # Get unique URLs
for url in unique_urls:
    print(f"Scraping data for: {url}")
    data = scrape_website(url)
    all_data.append(data)

# Convert list of lists to DataFrame
result_df = pd.DataFrame(all_data)

# Save the DataFrame to a new Excel file
output_file = 'scraped_data_second_cells.xlsx'
with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    result_df.to_excel(writer, index=False, sheet_name='Sheet1', startrow=0, startcol=0)

print(f"Scraped data saved to {output_file}")
