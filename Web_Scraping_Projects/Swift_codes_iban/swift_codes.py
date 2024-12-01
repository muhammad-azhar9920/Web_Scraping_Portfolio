import pandas as pd
import json
from bs4 import BeautifulSoup
import requests
from _Proxies import ProxiesCrawler
from fake_useragent import UserAgent
import random

def read_excel_files(file_path):
    # Load excel file
    excel_file = pd.ExcelFile(file_path)

    # Dictionary to store data from each workbook
    workbooks_data = {}

    # Iterate over each sheet (workbook)
    for sheet_name in sorted(excel_file.sheet_names):
        # Read each sheet into a DataFrame (assuming there are four columns)
        df = pd.read_excel(excel_file, sheet_name=sheet_name, usecols=[0,1,2,3])
        df = df.fillna(' ')

        # Convert the DataFrame to a list of tuples
        data_as_tuples = [tuple(x) for x in df.values]

        # Store the DataFrame in the dictionary with the sheet name as the key
        workbooks_data[sheet_name] = data_as_tuples
    
    return workbooks_data

def convert_data_into_json(dicts: dict):
    JsonOutput = []
    try:
        for country, contents in dicts.items():
            temp_dict = {"country": f"{str(country).capitalize()}", "iban_structure": "", "data": []}

            JsonOutput.append(temp_dict)

            for content in contents:
                bank = content[0][1:] if content[0][0] == "'" else content[0]
                city = content[1][1:] if content[1][0] == "'" else content[1]
                branch = content[2][1:] if content[2][0] == "'" else content[2]
                swift_code = content[3][1:] if content[3][0] == "'" else content[3]

                temp_dict_2 = {"bank": f"{bank}", "city": f"{city}", "branch": f"{branch}", "swift_code": f"{swift_code}"}
                temp_dict["data"].append(temp_dict_2)

        return JsonOutput


    except Exception as er:
        print(er)
        return JsonOutput

if __name__ == '__main__':
    data = read_excel_files('All_swift_codes.xlsx')
    json_data = convert_data_into_json(data)

    # Directly exporting to JSON (Only for testing)
    with open("data.json", "w", encoding='utf-8') as file:
        json.dump(json_data, file, indent=4, ensure_ascii=False)
