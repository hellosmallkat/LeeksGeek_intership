import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urlparse, urljoin

def scrape_links(url):
    try:
        # Fetch the content from url
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        
        # Parse the content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all hyperlinks
        links = soup.find_all('a')
        
        # Extract the href attribute and text from each link
        link_list = []
        for link in links:
            href = link.get('href')
            text = link.get_text(strip=True)
            if href and is_valid_link(href):  # Check if it's a valid link
                full_url = urljoin(url, href)  # Make the link absolute
                if is_detail_mode_link(full_url):  # Check if it's a detail mode link
                    link_list.append({
                        'Text': text,
                        'URL': full_url
                    })
                
        return link_list
    
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return []

def is_valid_link(href):
    # Function to check if a link is valid (not an image file)
    parsed = urlparse(href)
    # Get the path of the URL
    path = parsed.path.lower()
    # Check if the path ends with an image extension
    if path.endswith('.png') or path.endswith('.jpg') or path.endswith('.jpeg') or path.endswith('.gif'):
        return False
    return True

def is_detail_mode_link(url):
    # Function to check if a URL contains "?mode=detail&"
    return '?mode=detail&' in url

def save_to_excel(links, filename='woven_links.xlsx'):
    # Create a DataFrame with the links
    df = pd.DataFrame(links)
    # Save the DataFrame to an Excel file
    df.to_excel(filename, index=False)
    print(f"Links saved to {filename}")

if __name__ == "__main__":
    base_url = "https://www.prtdyeing.org.tw/"
    all_links = []

    # Loop over each page to scrape links
    for page_num in range(1, 6):  # Assuming there are 5 pages
        page_url = f"{base_url}basic/?page={page_num}&node=5"
        print(f"Scraping page {page_num}: {page_url}")
        links = scrape_links(page_url)
        all_links.extend(links)

    # Save all links to Excel
    save_to_excel(all_links)
