import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

# Function to scrape data from a single page
def scrape_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        companies = []
        seen_names = set()  # Track seen company names to avoid duplicates

        for row in soup.find_all('tr', class_=['show1', 'show2']):
            areas = row.find_all('div', class_='area')

            if len(areas) < 3:
                continue  # Skip rows that don't have the expected number of 'area' divs

            # Extracting company name and description
            try:
                name_area = areas[1]
                company_name = name_area.find('div', class_='txt1').text.strip()
                company_description = name_area.find('div', class_='txt2').text.strip()
            except AttributeError:
                continue  # Skip if any expected text elements are missing

            # Extracting contact details
            contact_details = []
            contact_div = areas[-1]  # Assume the last 'area' div contains contact details

            for item in contact_div.find_all('div'):
                if item.find('i', class_='icon fas fa-map-marker-alt'):
                    contact_details.append(item.text.strip())
                elif item.find('i', class_='icon fas fa-phone'):
                    contact_details.append(item.find('a').text.strip())
                elif item.find('i', class_='icon fas fa-fax'):
                    contact_details.append(item.text.strip())
                elif item.find('i', class_='icon fas fa-envelope-square'):
                    contact_details.append(item.text.strip())
                elif item.find('i', class_='icon fas fa-link'):
                    contact_details.append(item.find('a').text.strip())
                elif item.find('i', class_='icon fas fa-industry'):
                    contact_details.append(item.text.strip())

            # Flatten contact details based on spaces and create separate columns
            flat_contact_details = [part.strip() for detail in contact_details for part in detail.split(' ') if part.strip()]

            # Add to companies list if company name is unique
            if company_name not in seen_names:
                seen_names.add(company_name)
                company_data = {
                    'Company Name': company_name,
                    'Description': company_description
                }

                # Dynamically add contact detail columns
                for idx, detail in enumerate(flat_contact_details):
                    column_name = f'Contact Detail {idx + 1}'
                    company_data[column_name] = detail

                companies.append(company_data)

        return companies
    else:
        print(f"Failed to fetch page: {url}")
        return []

# Main function to iterate over multiple pages
def main():
    base_url = 'https://www.taiwan-garment.org.tw/mod/staff/index.php?REQUEST_ID=774b0483831c0f2dac209eba4b544646&pn='
    num_pages = 10  # Number of pages to scrape

    all_companies = []
    for page in range(1, num_pages + 10):
        url = f"{base_url}{page}"
        companies = scrape_page(url)
        all_companies.extend(companies)
