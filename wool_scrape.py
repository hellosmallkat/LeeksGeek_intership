import requests
from bs4 import BeautifulSoup
import pandas as pd

# Initialize lists to store data
company_names = []
responsible_persons = []
product_intros = []
contact_details = []

# Iterate through each page
for page_number in range(5):  # Loop through pages 0 to 4
    url = f'https://www.wool.org.tw/mod/staff/index.php?REQUEST_ID=aa01d123095ece4cbe36082e47c36062&pn={page_number}'
    
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the content with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all rows in the table
        rows = soup.find_all('tr', class_=['show1', 'show2'])
        
        # Iterate through each row
        for row in rows:
            columns = row.find_all('td')  # Find all columns in the row
            if columns:
                if len(columns) == 1:  # Handling for 'show2' rows
                    details = columns[0].find_all('div', class_='area')
                    if details:
                        company_names.append(details[0].find('div', class_='txt1').text.strip())
                        responsible_persons.append(details[1].find('div', class_='txt1').text.strip())
                        product_intros.append(details[2].find('div', class_='txt1').text.strip())
                        contact_details.append(details[3].text.strip().replace('\n', ' '))
                else:  # Handling for 'show1' rows
                    company_name = columns[0].find('div', class_='txt1').text.strip()
                    responsible_person = columns[1].find('div', class_='txt1').text.strip()
                    product_intro = columns[2].find('div', class_='txt1').text.strip()
                    contact_detail = columns[3].text.strip().replace('\n', ' ')
                    
                    company_names.append(company_name)
                    responsible_persons.append(responsible_person)
                    product_intros.append(product_intro)
                    contact_details.append(contact_detail)
        
        print(f'Page {page_number} scraped successfully')
    else:
        print(f'Failed to retrieve page {page_number}. Status code: {response.status_code}')

# Create a DataFrame
df = pd.DataFrame({
    '會員廠商名稱': company_names,
    '負責人': responsible_persons,
    '產品簡介': product_intros,
    '聯絡方式': contact_details  # Removed leading space for column name
})

# Export to Excel
output_file = 'wool_companies.xlsx'
df.to_excel(output_file, index=False)

print(f'Data successfully scraped from 5 pages and saved to {output_file}')
