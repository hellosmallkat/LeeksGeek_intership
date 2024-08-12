import pandas as pd
from bs4 import BeautifulSoup

# HTML content
html_content = """
<table width="95%" align="center" border="0" cellpadding="0" cellspacing="1">
  <tbody><tr>
    <td>
      <form method="post" name="list">
        <input type="hidden" name="no">
        <table width="70%" border="1" align="center" cellpadding="3" cellspacing="0" bordercolor="#666666" style=" font-size:16px;border-collapse:collapse; line-height:1.5em;">
          <tbody><tr align="center" bgcolor="#2F64DF">
            <td width="17%"><font color="#FFFFFF"><strong>會員編號</strong></font></td>
            <td width="56%"><font color="#FFFFFF"><strong>公司名稱</strong></font></td>
            <td width="27%"><font color="#FFFFFF"><strong>聯絡電話</strong></font></td>
          </tr>

          <tr align="center" bgcolor="#EAF5FD">
            <td>11653</td>
            <td align="left"><a href="#" onclick="GoList('11653')">利陽資訊股份有限公司</a></td>
            <td>02-25463880</td>
          </tr>

          <tr align="center" bgcolor="#EBEBEB">
            <td>17431</td>
            <td align="left"><a href="#" onclick="GoList('17431')">聰明學習股份有限公司</a></td>
            <td>0916-852595</td>
          </tr>

          <tr align="center" bgcolor="#EAF5FD">
            <td>17482</td>
            <td align="left"><a href="#" onclick="GoList('17482')">學好好學人文教育有限公司</a></td>
            <td>02-28748586</td>
          </tr>

          <tr align="center" bgcolor="#EBEBEB">
            <td>17660</td>
            <td align="left"><a href="#" onclick="GoList('17660')">播種者數位股份有限公司</a></td>
            <td>02-2732-0798</td>
          </tr>

        </tbody></table>
      </form>
    </td>
  </tr>
</tbody></table>
"""

def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', {'width': '70%', 'border': '1'})
    
    if table is None:
        print("Table not found")
        return []

    rows = table.find_all('tr')
    data = []
    
    for row in rows[1:]:  # Skip header row
        cols = row.find_all('td')
        if len(cols) < 3:
            continue

        member_id = cols[0].get_text(strip=True)
        company_name_tag = cols[1].find('a')
        company_name = company_name_tag.get_text(strip=True) if company_name_tag else cols[1].get_text(strip=True)
        contact_number = cols[2].get_text(strip=True)
        
        data.append([member_id, company_name, contact_number])
    
    return data

# Parse the HTML content
data = parse_html(html_content)

# Define the DataFrame columns
columns = ['會員編號', '公司名稱', '聯絡電話']

# Create a DataFrame
df = pd.DataFrame(data, columns=columns)

# Save the DataFrame to an Excel file
df.to_excel('scraped_data.xlsx', index=False)

print("Data has been scraped and saved to 'scraped_data.xlsx'.")
