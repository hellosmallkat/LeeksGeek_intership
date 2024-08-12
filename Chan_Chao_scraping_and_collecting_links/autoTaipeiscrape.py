import openpyxl
import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
from urllib.parse import urlparse

# Function to extract host (main domain) from URL
def get_host_name(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc

# Function to scrape website links and specific company name from a website
def scrape_company_info(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all <a> tags with an href attribute that is a valid URL and does not contain unwanted domains
        live_links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            # Parse the URL to extract the host name
            parsed_url = urlparse(href)
            if parsed_url.scheme in ['http', 'https'] and parsed_url.netloc not in ['www.chanchao.com.tw', 'www.facebook.com']:
                live_links.append((href, get_host_name(href)))  # Store tuple of (link, host name)

        return live_links
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return []

# Function to combine base URL with parts from Excel file and scrape each website
def scrape_websites_from_excel(base_url, excel_file):
    try:
        # Generating an output file name
        output_file = f"展昭國際企業股份有限公司_scraped.csv"

        workbook = openpyxl.load_workbook(excel_file)
        sheet = workbook.active

        with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(['Company Name', 'Company Website'])  # Adding header row

            for row in sheet.iter_rows(min_row=2, min_col=1, max_col=1, values_only=True):
                part = row[0]
                if isinstance(part, str):  # Check if part is a string
                    url = f"{base_url}/{part}"
                    links_with_hosts = scrape_company_info(url)
                    for link, host_name in links_with_hosts:
                        # Create hyperlink for Excel in CSV
                        hyperlink = f'=HYPERLINK("{link}", "Link")'
                        writer.writerow([host_name, hyperlink])

        print(f"Scraping completed. Data written to '{output_file}'.")
    except Exception as e:
        print(f"Error: {e}")

# Example usage
base_url = "https://www.chanchao.com.tw/AutomationTaipei/"
excel_file = "展昭國際企業股份有限公司_links.xlsx"
scrape_websites_from_excel(base_url, excel_file)
