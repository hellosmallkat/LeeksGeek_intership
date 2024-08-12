import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_links(url):
    # Send a GET request to the URL
    response = requests.get(url)
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    # Find all <a> tags with href attributes within <th> or <td> tags
    a_tags = soup.find_all(['th', 'td'])
    # Extract the href attribute from each <a> tag
    links = [a.find('a').get('href') for a in a_tags if a.find('a') and a.find('a').get('href')]
    return links

def save_to_excel(links, filename='links_comp.xlsx'):
    # Create a DataFrame with the links
    df = pd.DataFrame({'Links': links})
    # Save the DataFrame to an Excel file
    df.to_excel(filename, index=False)
    print(f"Links saved to {filename}")

if __name__ == "__main__":
    base_url = "https://www.prtdyeing.org.tw/basic/?node=5"
    all_links = []

    # Loop over each page to scrape links

    print(f"Scraping page {base_url}")
    links = scrape_links(base_url)
    all_links.extend(links)

    # Save all links to Excel
    save_to_excel(all_links)
