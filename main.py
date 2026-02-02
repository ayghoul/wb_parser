import requests
import get_token
import pandas as pd

class WBParser:
    TOKEN = '1.1000.976cdc0ba129477893b052364c01d30a.MHwxMzYuMTY5LjE3NC4yNXxNb3ppbGxhLzUuMCAoV2luZG93cyBOVCAxMC4wOyBXaW42NDsgeDY0KSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBDaHJvbWUvMTQ0LjAuMC4wIFNhZmFyaS81MzcuMzZ8MTc3MTE1MzczOXxyZXVzYWJsZXwyfGV5Sm9ZWE5vSWpvaUluMD18MHwzfDE3NzA1NDg5Mzl8MQ==.MEUCIQDWSja8CSICPQm4xKqnNjJMoephQsPUyjlY1vK2lKXNBwIgTuR5/c3XlvHC41MhlINt/mGYYH0yszuzQxx+hLZNWAM='
    SEARCH_URL = 'https://www.wildberries.ru/__internal/u-search/exactmatch/ru/common/v18/search'

    HEADERS = {
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9',
    'priority': 'u=1, i',
    'referer': 'https://www.wildberries.ru/catalog/0/search.aspx?search=%D0%BF%D0%B0%D0%BB%D1%8C%D1%82%D0%BE%20%D0%B8%D0%B7%20%D0%BD%D0%B0%D1%82%D1%83%D1%80%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%D0%B9%20%D1%88%D0%B5%D1%80%D1%81%D1%82%D0%B8',
    'sec-ch-ua': '"Not(A:Brand";v="8", "Chromium";v="144", "Google Chrome";v="144"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    'x-spa-version': '13.21.4',
    'x-userid': '0',
    }

    PARAMS = {
    'ab_testing': 'false',
    'appType': '1',
    'curr': 'rub',
    'dest': '12358496',
    'hide_dtype': '9',
    'hide_vflags': '4294967296',
    'inheritFilters': 'false',
    'lang': 'ru',
    'query': 'пальто из натуральной шерсти',
    'resultset': 'catalog',
    'sort': 'popular',
    'spp': '30',
    'suppressSpellcheck': 'false',
}

    def __init__(self, products: dict):
        self.products = products
        self.token = WBParser.TOKEN

    def _update_token(self):
        self.token = get_token()

    def get_product_details(self, url: str):
        headers = {
            'sec-ch-ua-platform': '"Windows"',
            'Referer': 'https://www.wildberries.ru/catalog/462970157/detail.aspx?targetUrl=SP',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Not(A:Brand";v="8", "Chromium";v="144", "Google Chrome";v="144"',
            'sec-ch-ua-mobile': '?0',
         }
        for i in range(2):
            response = requests.get('https://basket-26.wbbasket.ru/vol4629/part462970/462970157/info/ru/card.json', headers=headers)
            if response.status_code == 498:
                self._update_token()
                continue
            if response.status_code != 200:
                return None
        product_data = response.json



        

    def parse(self) -> list:
        results = []

        price = self.products["price"]
        rating = self.products["rating"]

        data = self.get_fetch(self.SEARCH_URL)
        for product in data["products"]:
            print(product["feedbacks"])
            # if product["reviewRating"] >= rating:
            #     if product["sizes"][0]["price"]["product"] <= price:
                    # result.append({
                    #     "Ссылка на товар":"https://www.wildberries.ru/catalog/{}/detail.aspx".format(product[id]),
                    #     "Артикул": product[id],
                    #     "Название": product["name"], 
            #             "Цена, руб.": product["sizes"][0]["price"]["product"]/100, 
            #             "Описание":, 
            #             "Ссылки на изображения":[], 
            #             "Характеристики":[], 
            #             "Название селлера": product["brand"],
            #             "Ссылка на селлера": "https://www.wildberries.ru/brands/{}".format(product["brand"]),
            #             "Размеры товара":[],
            #             "Остатки по товару (число)":,
            #             "Рейтинг": product["reviewRating"],
            #             "Количество отзывов": product["feedbacks"]
                        # })



    def get_fetch(self, url: str, retries: int = 2):
        for _ in range(retries):
            response = requests.get(
                url,
                params=self.PARAMS,
                cookies={"x_wbaas_token": self.token},
                headers=self.HEADERS
            )
            if response.status_code == 498:
                self._update_token()
                continue
            if response.status_code != 200:
                return None
            try:
                return response.json()
            except Exception:
                return None
        return None

if __name__ == "__main__":
    input_data = {"rating": 4.5, "price": 10000}
    result = WBParser(input_data).parse()


        
# cookies = {
#     'x_wbaas_token': '1.1000.976cdc0ba129477893b052364c01d30a.MHwxMzYuMTY5LjE3NC4yNXxNb3ppbGxhLzUuMCAoV2luZG93cyBOVCAxMC4wOyBXaW42NDsgeDY0KSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBDaHJvbWUvMTQ0LjAuMC4wIFNhZmFyaS81MzcuMzZ8MTc3MTE1MzczOXxyZXVzYWJsZXwyfGV5Sm9ZWE5vSWpvaUluMD18MHwzfDE3NzA1NDg5Mzl8MQ==.MEUCIQDWSja8CSICPQm4xKqnNjJMoephQsPUyjlY1vK2lKXNBwIgTuR5/c3XlvHC41MhlINt/mGYYH0yszuzQxx+hLZNWAM=',
#     # '_wbauid': '9682191941769944141',
#     # '_cp': '1',
# }




# for i in range(105):
#     response = requests.get(
#         'https://www.wildberries.ru/__internal/u-search/exactmatch/ru/common/v18/search',
#         params=params,
#         cookies=cookies,
#         headers=headers,
#     )
#     print(i)
#     print(response.status_code)
# print(response.json())