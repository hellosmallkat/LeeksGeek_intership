import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to scrape a website for all links
def scrape_website_for_links(url):
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
            if href:  # Only consider links with a non-empty href
                link_list.append({
                    'Text': text,
                    'URL': href
                })
                
        return link_list
    
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return []

# Function to save links to an Excel file
def save_links_to_excel(links, file_name):
    # Create a DataFrame from the list of links
    df = pd.DataFrame(links)
    
    # Save the DataFrame to an Excel file
    df.to_excel(file_name, index=False)
    print(f"Links saved to {file_name}")

# Example usage
if __name__ == "__main__":
    website_url = 'https://www.bags.org.tw/company_all#m9'  # Replace with the URL you want to scrape
    links = scrape_website_for_links(website_url)
    if links:
        save_links_to_excel(links, 'bag_links.xlsx')
    else:
        print("No links found or an error occurred.")
