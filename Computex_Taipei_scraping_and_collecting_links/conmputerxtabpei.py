from bs4 import BeautifulSoup
import pandas as pd
import requests
import re

# Function to scrape links from a page
def scrape_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('li')
    link_list = []
    for link in links:
        a_tag = link.find('a')
        if a_tag:
            href = a_tag['href']
            if re.match(r'/zh-tw/exhibitor/.*/info\.html\?lt=data&vt=show-area&cr=\d+', href):
                link_list.append(href)
    return link_list

# Starting page and number of pages to scrape
start_page = 1
num_pages = 127

# Base URL for the pages
base_url = 'https://www.computextaipei.com.tw/zh-tw/exhibitor/show-area-data/index.html'

# Initialize an empty list to store all links
all_links = []

# Loop through each page
for page in range(start_page, num_pages + 1):
    # Construct the URL for the current page
    url = f"{base_url}?pageSize=10&currentPage={page}#"
    print(f"Scraping page {page}...")

    # Scrape links from the current page
    page_links = scrape_links(url)

    # Add the links from the current page to the list of all links
    all_links.extend(page_links)

# Create a DataFrame from the list of all links
df = pd.DataFrame({'Links': all_links})

# Export DataFrame to a CSV file
df.to_csv('Computex_Taipei_scraping_links.csv', index=False)

print("All links saved to 'Computex_Taipei_scraping_links.csv'")
