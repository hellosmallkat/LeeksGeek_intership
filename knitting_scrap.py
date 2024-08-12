import requests
from bs4 import BeautifulSoup
import pandas as pd

base_url = "https://knitting.org.tw/members"

def scrape_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    company_data = []
    
    # Find all company items directly
    company_items = soup.find_all('li', class_='page-members__content__right__info-item')
    
    if not company_items:
        print(f"No company items found on page: {url}")
        return company_data
    
    for item in company_items:
        company_name_elem = item.find_all('div')
        
        if len(company_name_elem) >= 4:  # Ensure there are enough elements to extract
            company_name = company_name_elem[1].text.strip()  # Assuming the second div contains company name
            phone = company_name_elem[2].text.strip()  # Assuming the third div contains phone
            contact_person = company_name_elem[3].text.strip()  # Assuming the fourth div contains contact person
        else:
            company_name = 'N/A'
            phone = 'N/A'
            contact_person = 'N/A'
        
        company_data.append({
            'Company Name': company_name,
            'Phone': phone,
            'Contact Person': contact_person
        })
    
    return company_data

def scrape_all_pages(base_url):
    all_company_data = []
    page_num = 1
    
    while page_num < 35:
        url = f"{base_url}?posts_per_page=9&page={page_num}&city_name=&company_name=&lang=zh"
        print(f"Scraping {url}")
        response = requests.get(url)
        
        if response.status_code != 200:
            print(f"Failed to retrieve page: {url}")
            break
        
        page_data = scrape_page(url)
        all_company_data.extend(page_data)
        
        # Check if there are no more company items
        if not page_data:
            break
        
        page_num += 1
    
    return all_company_data

def save_to_excel(data, filename='knitting_companies.xlsx'):
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)
    print(f"Company data saved to {filename}")

if __name__ == "__main__":
    all_company_data = scrape_all_pages(base_url)
    save_to_excel(all_company_data)
