import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()

class ProxiesCrawler:

    def get_proxies(self, start_proxies : int, end_proxies : int):
        '''
        It will fetch the (number_of_proxies) free working proxies to utilize in the code, in order to avoid getting BAN.
        :return: (list) -> A 2D list that contains the Proxy and its protocol which is used for scrapping
        '''
        print("get_proxies() Started")

        valid_proxies = []
        try:
            link = os.getenv("PROXY_URL")
            response = requests.get(link)
            if response.status_code == 200:
                raw_proxies = json.loads(response.text)
                proxies = [x['ip'].strip() + ":" + x['port'].strip() for x in raw_proxies['data']]
                proxies_protocols = [x['protocols'][0] for x in raw_proxies['data']]
                for proxies_protocol,proxy in zip(proxies_protocols,proxies):
                    try:
                        # check proxy is valid or not
                        res = requests.get('https://ifconfig.me/', proxies={proxies_protocol:proxy})
                        if res.status_code == 200:
                            print(f"Valid Proxy: {proxy} with protocol: {proxies_protocol}")
                            valid_proxies.append([proxy,proxies_protocol])

                        if len(valid_proxies) == end_proxies:
                            valid_proxies = valid_proxies[start_proxies : end_proxies]
                            break

                    except Exception as er:
                        continue

                print(f"Total Valid Proxies we get: {len(valid_proxies)}")
                return valid_proxies

            else:
                return valid_proxies

        except Exception as error:
            print(f"get_proxies() Error -> {error}")
            return valid_proxies