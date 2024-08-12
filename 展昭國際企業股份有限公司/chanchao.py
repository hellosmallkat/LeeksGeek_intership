import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to scrape data from the website
def scrape_company_data(url):
    # Send a GET request to the URL
    response = requests.get(url)
    response.raise_for_status()  # Check that the request was successful
    response.encoding = 'utf-8'  # Ensure the response is interpreted as UTF-8

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all the <div class="right"> elements
    right_divs = soup.find_all('div', class_='right')

    # Initialize lists to store company names and booth numbers
    company_names = []
    booth_numbers = []

    # Iterate through each <div class="right"> element
    for div in right_divs:
        # Find the company name
        company_name_tag = div.find('h4').find('a')
        if company_name_tag:
            company_name = company_name_tag.get_text(strip=True)
        else:
            company_name = None

        # Find the booth number
        booth_number_tag = div.find('p', string=lambda x: x and '攤位號碼' in x)
        if booth_number_tag:
            booth_number = booth_number_tag.get_text(strip=True).split('：')[-1]
        else:
            booth_number = None

        # Append the data to the lists
        company_names.append(company_name)
        booth_numbers.append(booth_number)

    # Create a DataFrame from the scraped data
    data = {'Company Name': company_names, 'Booth Number': booth_numbers}
    df = pd.DataFrame(data)

    # Save the DataFrame to a spreadsheet
    df.to_excel('company_data.xlsx', index=False)

# URL of the website to scrape
url = 'https://www.chanchao.com.tw/healthcos/visitorExhibitor.asp'

# Scrape the company data from the website
scrape_company_data(url)

print("Data has been scraped and saved to company_data.xlsx")
