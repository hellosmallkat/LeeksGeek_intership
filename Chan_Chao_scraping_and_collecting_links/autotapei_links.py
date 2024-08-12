import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_links(url):
    # Send a GET request to the URL
    response = requests.get(url)
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    # Find all <li> tags with the specified class
    li_tags = soup.find_all('ul', class_='product')
    # Extract the href attribute from each anchor tag within the <li> tags
    links = [li.find('a').get('href') for li in li_tags if li.find('a')]
    return links

def save_to_excel(links, filename='展昭國際企業股份有限公司_links.xlsx'):
    # Create a DataFrame with the links
    df = pd.DataFrame({'Links': links})
    # Save the DataFrame to an Excel file
    df.to_excel(filename, index=False)
    print(f"Links saved to {filename}")

if __name__ == "__main__":
    base_url = "https://www.chanchao.com.tw/AutomationTaipei/"
    all_links = []

    # Loop over each page to scrape links
    for page_num in range(1, 41):  # Assuming there are 40 pages
        page_url = f"{base_url}visitorExhibitor.asp?page={page_num}&view=&Area=&sort=" # combines the base URL with the page number
        print(f"Scraping page {page_num}: {page_url}")
        links = scrape_links(page_url)
        all_links.extend(links)

    # Save all links to Excel
    save_to_excel(all_links)
