import requests
from bs4 import BeautifulSoup
import pandas as pd

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
            # Extracting company name and description
            name_area = row.find_all('div', class_='area')[1]
            company_name = name_area.find('div', class_='txt1').text.strip()
            company_description = name_area.find('div', class_='txt2').text.strip()

            # Initialize contact details
            contact_details = {
                'Address': '',
                'Phone': '',
                'Fax': '',
                'Email': '',
                'Website': '',
                'Overseas Factory': ''
            }

            # Extracting contact details
            contact_div = row.find_all('div', class_='area')[-1]
            contact_items = contact_div.find_all('div')
            for item in contact_items:
                if item.find('i', class_='icon fas fa-map-marker-alt'):
                    contact_details['Address'] = item.text.strip()
                elif item.find('i', class_='icon fas fa-phone'):
                    contact_details['Phone'] = item.find('a').text.strip()
                elif item.find('i', class_='icon fas fa-fax'):
                    contact_details['Fax'] = item.text.strip()
                elif item.find('i', class_='icon fas fa-envelope-square'):
                    contact_details['Email'] = item.text.strip()
                elif item.find('i', class_='icon fas fa-link'):
                    contact_details['Website'] = item.find('a').text.strip()
                elif item.find('i', class_='icon fas fa-industry'):
                    contact_details['Overseas Factory'] = item.text.strip()

            # Add to companies list if company name is unique
            if company_name not in seen_names:
                seen_names.add(company_name)
                companies.append({
                    'Company Name': company_name,
                    'Description': company_description,
                    'Address': contact_details['Address'],
                    'Phone': contact_details['Phone'],
                    'Fax': contact_details['Fax'],
                    'Email': contact_details['Email'],
                    'Website': contact_details['Website'],
                    'Overseas Factory': contact_details['Overseas Factory']
                })

        return companies
    else:
        print(f"Failed to fetch page: {url}")
        return []

# Main function to iterate over multiple pages
def main():
    base_url = 'https://www.taiwan-garment.org.tw/mod/staff/index.php?REQUEST_ID=774b0483831c0f2dac209eba4b544646&pn='
    num_pages = 10  # Number of pages to scrape

    all_companies = []
    for page in range(1, num_pages + 1):
        url = f"{base_url}{page}"
        companies = scrape_page(url)
        all_companies.extend(companies)

    # Convert to DataFrame
    df = pd.DataFrame(all_companies)

    # Remove duplicates based on 'Company Name', keeping the first occurrence
    df = df.drop_duplicates(subset=['Company Name'], keep='first')

    # Save to Excel
    df.to_excel('garment_companies_with_contact_details.xlsx', index=False)
    print("Data saved to garment_companies_with_contact_details.xlsx")

if __name__ == '__main__':
    main()
