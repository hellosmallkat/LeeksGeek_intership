import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def scrape_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    a_tags = soup.find_all(['th', 'td'])
    links = set(a.find('a').get('href') for a in a_tags if a.find('a') and a.find('a').get('href').startswith('/about/exhibitor/ex'))
    return list(links)

def scrape_website(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all('article')
    
    # Define the labels we are looking for
    labels = ['攤位號碼', '公司網址', '公司簡介', '展出品牌', '產品介紹', '廠商影音']
    
    article_data_list = []
    
    for article in articles:
        title = article.find('h1') or article.find('h2') or article.find('h3')
        title_text = title.get_text(strip=True) if title else 'No Title'
        
        content = article.get_text(separator='\n').strip()
        
        # Initialize a dictionary to store the data with desired column names
        article_data = {}
        
        # Split the content into lines for easier processing
        lines = content.split('\n')
        
        current_label = None
        current_data = []
        
        for line in lines:
            line = line.strip()
            
            if any(line.startswith(label) for label in labels):
                if current_label:
                    # Save the collected data for the previous label without the title
                    if current_data:
                        article_data[current_label] = ' '.join(current_data).strip()
                    else:
                        article_data[current_label] = ' '  # Set empty label to " "
                
                # Find the label and start collecting data for the new label
                current_label = next(label for label in labels if line.startswith(label))
                # Start collecting data after the label
                current_data = [line.replace(f"{current_label}:", "").strip()]
            else:
                if current_label:
                    current_data.append(line)
        
        # Save any remaining data for the last label encountered
        if current_label:
            if current_data:
                article_data[current_label] = ' '.join(current_data).strip()
            else:
                article_data[current_label] = ' '  # Set empty label to " "
        
        # Add the dictionary to the list of article data
        article_data_list.append(article_data)
    
    return article_data_list

def clean_data(data):
    # Function to clean each column
    for article_data in data:
        # Clean 攤位號碼 column
        if '攤位號碼' in article_data:
            article_data['攤位號碼'] = re.sub(r'^攤位號碼\s+', '', article_data['攤位號碼'])
        else:
            article_data['攤位號碼'] = ' '  # Set empty label to " "
        
        # Clean 公司網址 column
        if '公司網址' in article_data:
            article_data['公司網址'] = re.sub(r'^公司網址\s+', '', article_data['公司網址'])
        else:
            article_data['公司網址'] = ' '  # Set empty label to " "
        
        # Clean 公司簡介 column
        if '公司簡介' in article_data:
            article_data['公司簡介'] = re.sub(r'^公司簡介\s+', '', article_data['公司簡介'])
        else:
            article_data['公司簡介'] = ' '  # Set empty label to " "
        
        # Clean 展出品牌 column
        if '展出品牌' in article_data:
            article_data['展出品牌'] = re.sub(r'^展出品牌\s+', '', article_data['展出品牌'])
        else:
            article_data['展出品牌'] = ' '  # Set empty label to " "
        
        # Clean 產品介紹 column
        if '產品介紹' in article_data:
            article_data['產品介紹'] = re.sub(r'^產品介紹\s+', '', article_data['產品介紹'])
        else:
            article_data['產品介紹'] = ' '  # Set empty label to " "
        
        # Clean 廠商影音 column
        if '廠商影音' in article_data:
            article_data['廠商影音'] = re.sub(r'^廠商影音\s+', '', article_data['廠商影音'])
        else:
            article_data['廠商影音'] = ' '  # Set empty label to " "
    
    return data

def save_to_excel(data, filename='exhibitors_data.xlsx'):
    # Clean the data
    cleaned_data = clean_data(data)
    
    # Create a DataFrame directly from the list of dictionaries
    df = pd.DataFrame(cleaned_data)
    
    # Save to Excel with specific header handling
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Sheet1', index=False)
        # Remove default header and write custom header
        worksheet = writer.sheets['Sheet1']
        for col_idx, col in enumerate(df.columns):
            cell = worksheet.cell(row=1, column=col_idx + 1)
            cell.value = col

    print(f"Data saved to {filename}")

if __name__ == "__main__":
    base_url = "https://www.tide.com.tw/about/exhibitor/"
    all_links = []

    # Loop over each page to scrape links
    for page_num in range(1, 9):  # Assuming there are 8 pages
        page_url = f"{base_url}ex0{page_num}"
        print(f"Scraping page {page_num}: {page_url}")
        links = scrape_links(page_url)
        all_links.extend(links)

    # Remove duplicate links
    unique_links = list(set(all_links))

    # Initialize a list to store all structured article data
    all_article_data = []

    # Loop over each unique link to scrape website data
    for link in unique_links:
        website_url = f"{link}"
        print(f"Scraping data from {website_url}")
        article_data = scrape_website(website_url)
        all_article_data.extend(article_data)  # Extend with list of dicts for each article

    # Save all scraped structured data to Excel
    save_to_excel(all_article_data)
# get rid of title name in all columen before and after the items
# save to excel