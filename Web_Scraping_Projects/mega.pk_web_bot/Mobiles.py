from bs4 import BeautifulSoup
import requests
from _Proxies import ProxiesCrawler
import random
import pandas as pd
from fake_useragent import UserAgent
import json

def Read_Excel_Files(file_path : str):
    # Load the Excel file
    excel_file = pd.ExcelFile(file_path)

    # Dictionary to store data from each workbook
    workbooks_data = {}

    # Iterate over each sheet (workbook)
    for sheet_name in sorted(excel_file.sheet_names):
        # Read each sheet into a DataFrame (assuming there are two columns)
        df = pd.read_excel(excel_file, sheet_name=sheet_name, usecols=[0, 1])

        # Convert the DataFrame to a list of tuples
        data_as_tuples = [tuple(x) for x in df.values]

        # Store the DataFrame in the dictionary with the sheet name as the key
        workbooks_data[sheet_name] = data_as_tuples

    return workbooks_data

def Get_Mobiles_Specs(dicts : dict):
    print("Get_Mobiles_Specs() Started")
    JsonOutput = []
    try:
        i = 0
        for brand, contents in dicts.items():
            print(f"Started scraping the Brand: '{brand}'")
            temp_dict = {"brand": f"{str(brand).capitalize()}", "mobiles": []}
            JsonOutput.append(temp_dict)

            for i, content in enumerate(contents):
                name = content[0][1:] if content[0][0] == "'" else content[0]
                link = content[1].replace("'","").replace('"','')
                temp_dict2 = {"country": "", "data": {"name": f"{name}", "price": "N/A", "image": ""}}
                temp_dict["mobiles"].append(temp_dict2)
                ImgUrl = ""

                ua = UserAgent()
                headers = {'User-Agent': ua.random}
                RandomProxy = random.choice(ALL_PROXIES)
                print(f"Using Proxy: '{RandomProxy}', to Scrap Mobile: '{name}'")

                soup = BeautifulSoup(requests.get(link, proxies={RandomProxy[1]: RandomProxy[0]}, headers=headers).text,'html.parser')
                if "too many request" in soup.text.replace('\n', '').lower():
                    print("Server down")
                    break

                elif soup.find('div',attrs={'id':"specs"}) is None:
                    print(f"Passing this content: '{name}'")
                    del temp_dict['mobiles'][-1]
                    continue

                elif len(soup.find('div',attrs={'id':"specs"}).find_all('div',attrs = {'class':"_gry-bg _spctbl _ovfhide"})) > 0:
                    Categories = [cat.text for cat in soup.find('div', attrs={'id': "specs"}).find_all('div', attrs={'class': "_hd"})]
                    Tables = soup.find('div',attrs={'id':"specs"}).find_all('table')
                    ImgUrl = soup.find('div',attrs = {'class':'_pdmimg __arModalBtn _flx'}).find('img')['src'].strip()

                    for cat,table in zip(Categories, Tables):
                        CatName = cat.strip().lower()
                        temp_list = []

                        if len(table.find_all('tr')) > 0:
                            temp_tr = ''
                            for tr in table.find_all('tr'):
                                if len(tr.find_all('td')) != 0:
                                    if len(tr.find_all('td')) == 1:
                                        temp_tr = str(tr.find_all('td')[0].text.strip()) + ":"
                                        continue
                                    f1 = temp_tr +tr.find_all('td')[0].text.strip()
                                    f2 = tr.find_all('td')[1].text.strip().replace('\n', '').replace('\xa0','').replace('\u2009', '').replace('\r', ' ').replace(r'\u00b', ' ')
                                    if "price" in str(f1).strip().lower():
                                        temp_dict2["data"]["price"] = str(f2).strip()
                                        continue
                                    temp_list.append([f1, f2])

                        else:
                            print(f'NO ROWS FOUND FOR CATEGORY: "{CatName}"')
                        temp_dict2["data"].update({CatName: temp_list})
                        temp_dict2['data']["image"] = ImgUrl
        return JsonOutput

    except Exception as error:
        print(f"Error in function Get_Mobiles_Specs() -> '{error}'")
        return JsonOutput


if __name__ == "__main__":
    print("*-----------------Execution Started-----------------*")
    ALL_PROXIES = ProxiesCrawler().get_proxies(0,10)

    data = Read_Excel_Files('Extracted Excels/Mobiles.xlsx')
    Json_data = Get_Mobiles_Specs(data)
    print(f"Total Mobiles Brands Scrapped: '{len(Json_data)}'")

    # Directly exporting to JSON (Only for testing)
    file = open("Extracted Jsons/MobilesSpecs.json", 'w', encoding='utf-8')
    json.dump(Json_data, file, indent=4, ensure_ascii=False)
    file.close()

    #Exporting to text file (Recommended)
    # file = open("LaptopSpecs",'w', encoding = 'utf-8')
    # json.dump(Json_data, file, indent=4, ensure_ascii=False)
    # file.close()

    print("*-----------------Execution Ended-----------------*")
