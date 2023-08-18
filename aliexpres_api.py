import json
import requests
import loader

ALIEXPRESS_API_KEY = loader.ALIEXPRESS_API_KEY


class AliExpressAPI:
    def __init__(self, api_key):
        self.base_url = "https://aliexpress-datahub.p.rapidapi.com"
        self.headers = {
            "X-RapidAPI-Key": api_key,
            "X-RapidAPI-Host": "aliexpress-datahub.p.rapidapi.com"
        }

    def search_items(self, query, sort, region, currency='EUR', start_price='0', end_price='0'):
        url = f"{self.base_url}/item_search_2"
        querystring = {
            "q": query,
            "sort": sort,
            "startPrice": start_price,
            "endPrice": end_price,
            "region": region,
            "currency": currency,
            'locale': 'ru_RU',
        }
        print(querystring)
        response = requests.get(url, headers=self.headers, params=querystring)
        with open('products.json', 'w', encoding='utf-8') as file:
            json.dump(response.json(), file, ensure_ascii=False, indent=4)
        return response.json()
