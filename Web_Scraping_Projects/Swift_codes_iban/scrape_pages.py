import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from _Proxies import ProxiesCrawler
import random

def extract_pages():
    page_no = 1
    try:
        # while page_no <= 13:
            print(f"--------------Start Product Scraping page {page_no}--------------------")
            # link = "https://www.theswiftcodes.com/cameroon/"
            # link = f"https://www.theswiftcodes.com/vietnam/page/{page_no}/"
            if(page_no == 1):
                link = "https://www.theswiftcodes.com/zimbabwe/"
            ua = UserAgent()
            headers = {'User-Agent': ua.random}
            RandomProxy = random.choice(ALL_PROXIES)
            print(f"Using Proxy: '{RandomProxy}', to scrape data: ")
            html_doc = requests.get(link, proxies={RandomProxy[1]:RandomProxy[0]}, headers=headers).text

            soup = BeautifulSoup(html_doc, 'html.parser')

            with open(f"data/file_{page_no}.html","w", encoding='utf-8') as f:
                f.write(str(soup.prettify()))
            print(f"--------------Successfully Scraped page {page_no}--------------------")
            page_no += 1

    except Exception as er:
        print(er)

    

if __name__ == "__main__":
    ALL_PROXIES = ProxiesCrawler().get_proxies(0,10)
    extract_pages()