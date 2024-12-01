import os
from bs4 import BeautifulSoup
import pandas as pd

def extract_details():
    try:
        data = {"bank":[], "city":[], "branch": [], "swift_code": []}
        for i in os.listdir("data"):
            with open(f"data/{i}", "r", encoding="utf-8") as f:
                html_doc = f.read()
            soup = BeautifulSoup(html_doc,'html.parser')
            table = soup.find('table', attrs={'class':'swift-country'}).tbody
            table_row = table.find_all("tr")
            for tr in table_row:
                table_data = tr.find_all("td")
                bank = table_data[1].get_text().strip()
                city = table_data[2].get_text().strip()
                branch = table_data[3].get_text().strip()
                swift_code = table_data[4].a.get_text().strip()
                # print(f"Bank: '{bank}',  City: '{city}',  Swift_Code: '{swift_code}'")
                data["bank"].append(bank)
                data["city"].append(city)
                data["branch"].append(branch)
                data["swift_code"].append(swift_code)

        return data
        
    except Exception as err:
        print(err)
        return data

data = extract_details()
if(data):
    df = pd.DataFrame(data=data)
    df.to_excel("swift_codes.xlsx")
    print("Successfully created excel file")

# Delete HTML files after extracting data
try:
    files = os.listdir("data")
    for file in files:
       file_path = os.path.join("data", file)
       if os.path.isfile(file_path):
        os.remove(file_path)
    print("All HTML files deleted successfully.")
except OSError:
     print("Error occurred while deleting files.")