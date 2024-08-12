import requests
import pandas as pd
from bs4 import BeautifulSoup
import re

def scrape_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        section = soup.find('section', class_='cp padding-left p-top mt-0')
        if not section:
            print(f"No matching section found on {url}")
            return ''
        
        # Remove elements related to WeChat and QR codes
        for wechat_element in section.find_all(string=re.compile(r'WeChat|QR', re.IGNORECASE)):
            wechat_element.extract()
        
        for qr_element in section.find_all(['img', 'div'], class_=lambda c: c and ('qr' in c.lower() or 'wechat' in c.lower())):
            qr_element.extract()
        
        for share_element in section.find_all(string=re.compile(r'Share to WeChat', re.IGNORECASE)):
            share_element.extract()

        text = section.get_text(separator='\n', strip=True)
        
        return text if text.strip() else ''
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return ''

def process_links(filename, output_filename):
    base_url = 'https://www.computextaipei.com.tw/'
    
    try:
        df = pd.read_csv(filename)
    except Exception as e:
        print(f"Error reading the CSV file: {e}")
        return
    
    if df.empty:
        print("The input CSV file is empty. Exiting the process.")
        return

    all_text = []
    unique_rows = {}
    combined_rows = {}

    for index, row in df.iterrows():
        try:
            relative_url = row['Links']
            url = base_url + relative_url
            print(f"Scraping {url}...")
            
            text = scrape_text(url)
            if text:
                text_items = text.split('\n')
                row_dict = {'URL': url}
                
                aggregate_after_trigger = False
                aggregate_text = []
                
                for item in text_items:
                    if "下一則：" in item:
                        aggregate_after_trigger = True
                    if aggregate_after_trigger:
                        aggregate_text.append(item)
                    else:
                        # Directly add the content to a list without naming columns
                        row_dict[len(row_dict)] = item  # Using numbers as temporary keys
                
                if aggregate_text:
                    row_dict['after_next'] = '\n'.join(aggregate_text).strip()  # Combine text after "下一則："

                if url in unique_rows:
                    existing_row = unique_rows[url]
                    
                    for key, value in row_dict.items():
                        if key not in existing_row or not existing_row[key]:
                            existing_row[key] = value
                else:
                    unique_rows[url] = row_dict

            print(f"Processed row {index + 1} of {len(df)}")
        except Exception as e:
            print(f"Error processing row {index}: {e}")

    if not unique_rows:
        print("No valid data was scraped. Exiting the process.")
        return

    # Identify the 17th column for merging rows
    merge_column_label = None
    sample_row = list(unique_rows.values())[0]
    for key in sample_row.keys():
        if isinstance(key, int) and key == 16:
            merge_column_label = key
            break

    for url, data in unique_rows.items():
        if merge_column_label and merge_column_label in data:
            key = data[merge_column_label]
            if key in combined_rows:
                existing_row = combined_rows[key]
                
                for column_label, value in data.items():
                    if column_label != merge_column_label and column_label not in existing_row:
                        existing_row[column_label] = value
            else:
                combined_rows[key] = data
        else:
            combined_rows[url] = data

    expanded_data = list(combined_rows.values())
    
    # Convert the dictionary list to a DataFrame
    expanded_df = pd.DataFrame(expanded_data)

    # Remove all columns that are entirely empty
    expanded_df = expanded_df.dropna(axis=1, how='all')

    # Remove all rows that are entirely empty (except the URL column)
    expanded_df = expanded_df.dropna(how='all', subset=expanded_df.columns.difference(['URL']))

    # Reorder columns to ensure URL is the first column and 'after_next' is the last column
    columns = expanded_df.columns.tolist()
    if 'URL' in columns:
        columns.remove('URL')
        columns.insert(0, 'URL')
    if 'after_next' in columns:
        columns.remove('after_next')
        columns.append('after_next')
    expanded_df = expanded_df[columns]

    # Save the DataFrame to an Excel file
    try:
        expanded_df.to_excel(output_filename, index=False)
        print(f"Scraped data saved to {output_filename}")
    except Exception as e:
        print(f"Error saving the output file: {e}")

if __name__ == "__main__":
    input_filename = 'Computex_Taipei_scraping_links.csv' 
    output_filename = 'scraped_text.xlsx'  # Output Excel file
    process_links(input_filename, output_filename)
