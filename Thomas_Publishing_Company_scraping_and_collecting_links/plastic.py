from bs4 import BeautifulSoup
import requests

# Define the URL to scrape
url = "https://www.thomasnet.com/suppliers/usa/plastic-containers-17810805?coverage_area=NA"

# Define headers to mimic a regular browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'
}

# Fetch the webpage content
response = requests.get(url, headers=headers)

# Check if the response was successful
response.raise_for_status()

# Parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')

# Find all instances of the desired HTML structure
items = soup.find_all('div', class_='css-10wpnqb')

# Iterate over each instance and extract the desired information
for item in items:
    # Find the link within each item
    link = item.find('a', href=True)
    if link:
        link_url = link['href']  # Extract the link URL
        # If the link is relative, you may need to prepend the base URL
        # link_url = urljoin(base_url, link['href'])
        
        # Print or process the extracted link URL
        print("Link URL:", link_url)

    # Optionally, extract other information from the item as needed
    # For example, you might extract the company name or logo image URL
