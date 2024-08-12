import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook
from urllib.parse import urljoin

# Function to scrape links and company details from a single page
def scrape_page(url, headers):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    companies = []

    # Find all rows containing company information
    for div_row in soup.find_all('div', class_='row mt-3 pt-2') + soup.find_all('div', class_='row align-items-center'):
        company_info = {}

        # Extract company name and profile link
        profile_link_tag = div_row.find('a', href=lambda href: href and href.startswith('member_info.php?id='))
        if profile_link_tag:
            company_info['Profile Link'] = urljoin(url, profile_link_tag['href'])
            company_info['Name'] = profile_link_tag.text.strip()

            # Visit each profile link and scrape additional information
            profile_page_url = company_info['Profile Link']
            profile_page_response = requests.get(profile_page_url, headers=headers)
            profile_soup = BeautifulSoup(profile_page_response.content, 'html.parser')

            # Find the specific div containing detailed information
            detail_div = profile_soup.find('div', class_='col-md-5')
            if detail_div:
                details = detail_div.find_all('li')
                for detail in details:
                    strong_tag = detail.find('strong', class_='text-color-primary')
                    if strong_tag:
                        key = strong_tag.text.strip(' :')
                        if key == '網站':
                            website_tag = detail.find('a')
                            if website_tag:
                                company_info[key] = website_tag['href']
                        else:
                            value = detail.text.split(':')[1].strip()
                            company_info[key] = value

            companies.append(company_info)

    return companies

# Function to scrape all pages until no more data is found
def scrape_all_pages(base_url, headers):
    all_data = []
    page_num = 1

    while page_num < 11:
        url = f"{base_url}&page={page_num}"
        print(f"Scraping {url}")

        try:
            page_data = scrape_page(url, headers)
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            break

        if not page_data:
            break  # Exit the loop if no data is found

        all_data.extend(page_data)
        page_num += 1

    return all_data

# Function to save the scraped data to an Excel file
def save_to_excel(data, filename):
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Company Details"

    # Add headers
    headers = ["Name", "Profile Link", "電話", "傳真", "網站", "信箱", "地址"]
    sheet.append(headers)

    for item in data:
        row = [
            item.get('Name', ''),
            item.get('Profile Link', ''),
            item.get('電話', ''),
            item.get('傳真', ''),
            item.get('網站', ''),
            item.get('信箱', ''),
            item.get('地址', '')
        ]
        sheet.append(row)

    workbook.save(filename)
    print(f"All data have been written to {filename}")

# Main execution
if __name__ == "__main__":
    base_url = "https://www.hosiery.org.tw/member.php?id="  # Base URL without page number
    output_file = 'company_details.xlsx'

    # Define headers to mimic a browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    }

    all_company_data = scrape_all_pages(base_url, headers)
    save_to_excel(all_company_data, output_file)
