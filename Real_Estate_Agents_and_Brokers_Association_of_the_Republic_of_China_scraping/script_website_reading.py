import requests
from bs4 import BeautifulSoup
import pandas as pd

# Step 1: Fetch the webpage content
url = "https://www.taiwanhouse.org.tw/a/blogs/static/4923"  # Replace with the actual URL
response = requests.get(url)
response.raise_for_status()  # Ensure we notice bad responses

# Step 2: Parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')

# Step 3: Locate the table
# Adjust the selector to match the actual HTML structure of the table
table = soup.find('table')  # Assuming there is only one table and it's the first one
if table is None:
    raise ValueError("No table found on the web page")

# Debug: Print the table's HTML to ensure we're selecting the correct one
print("Table HTML:", table.prettify())

# Step 4: Extract the rows
rows = []
for row in table.find_all('tr'):
    cells = row.find_all('td')
    rows.append([cell.text.strip() for cell in cells])

# Debug: Print the first few rows to ensure data extraction is correct
print("First few rows extracted:", rows[:5])

# Step 5: Store data in a pandas DataFrame
df = pd.DataFrame(rows)

# Step 6: Write DataFrame to an Excel file
df.to_excel('Taiwan_house_information.xlsx', index=False, header=False)

print("Data has been successfully written to Taiwan_house_information.xlsx")
