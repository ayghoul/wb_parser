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
    
    def get_qty(self, nm: int):
        search_url = "https://www.wildberries.ru/__internal/card/cards/v4/detail"
        params = {
        'appType': '1',
        'curr': 'rub',
        'dest': '12358496',
        'spp': '30',
        'hide_dtype': '9',
        'ab_testing': 'false',
        'lang': 'ru',
        'nm': str(nm)
        }
        response = requests.get(
                search_url,
                params=params,
                cookies={"x_wbaas_token": self.token})
        result = response.json()

        return result['products'][0]['totalQuantity']
        
    def get_product_details(self, id):
        headers = {
            'sec-ch-ua-platform': '"Windows"',
            'Referer': 'https://www.wildberries.ru/catalog/462970157/detail.aspx?targetUrl=SP',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Not(A:Brand";v="8", "Chromium";v="144", "Google Chrome";v="144"',
            'sec-ch-ua-mobile': '?0',
         }
        url = self.get_card_url(id)
        for _ in range(2):
            response = requests.get(url, headers=headers)
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
    
    def get_image_url(self, count: int, id: int) -> list:
        part = id // 1000
        vol = id // 100000
        r = self.get_busket(vol)
        link = f"https://basket-{r}.wbbasket.ru/vol{vol}/part{part}/{id}/images"
        result = [f"{link}/big/{i}.webp" for i in range(1, count + 1)]
        return result

    def get_card_url(self, id: int) -> str:
        part = id // 1000
        vol = id // 100000
        r = self.get_busket(vol)
        return f"https://basket-{r}.wbbasket.ru/vol{vol}/part{part}/{id}/info/ru/card.json"

    def get_busket(self, vol: int):
        if vol >= 0 and vol <= 143:
            r = "01"
        elif vol <= 287:
            r = "02"
        elif vol <= 431:
            r = "03"
        elif vol <= 719:
            r = "04"
        elif vol <= 1007:
            r = "05"
        elif vol <= 1061:
            r = "06"
        elif vol <= 1115:
            r = "07"
        elif vol <= 1169:
            r = "08"
        elif vol <= 1313:
            r = "09"
        elif vol <= 1601:
            r = "10"
        elif vol <= 1655:
            r = "11"
        elif vol <= 1919:
            r = "12"
        elif vol <= 2045:
            r = "13"
        elif vol <= 2189:
            r = "14"
        elif vol <= 2405:
            r = "15"
        elif vol <= 2621:
            r = "16"
        elif vol <= 2837:
            r = "17"
        elif vol <= 3053:
            r = "18"
        elif vol <= 3269:
            r = "19"
        elif vol <= 3485:
            r = "20"
        elif vol <= 3701:
            r = "21"
        elif vol <= 3917:
            r = "22"
        elif vol <= 4133:
            r = "23"
        elif vol <= 4349:
            r = "24"
        elif vol <= 4565:
            r = "25"
        elif vol <= 4877:
            r = "26"
        elif vol <= 5189:
            r = "27"
        elif vol <= 5501:
            r = "28"
        elif vol <= 5813:
            r = "29"
        elif vol <= 6125:
            r = "30"
        elif vol <= 6437:
            r = "31"
        elif vol <= 6749:
            r = "32"
        elif vol <= 7061:
            r = "33"
        elif vol <= 7373:
            r = "34"
        elif vol <= 7685:
            r = "35"
        elif vol <= 7997:
            r = "36"
        elif vol <= 8309:
            r = "37"
        else:
            r = "38"
        return r

    def parse(self):
        results = []

        price = self.products["price"]*100
        rating = self.products["rating"]
        data = self.get_fetch(self.SEARCH_URL)
        for product in data["products"]:
            
            if product["reviewRating"] >= rating:
                if product["sizes"][0]["price"]["product"] <= price:
                    product_details = self.get_product_details(product["id"])
                    characteristics = {i["name"]: i["value"]for i in product_details["options"]}
                    sizes = [i["name"] for i in product["sizes"]]
                    links = self.get_image_url(product_details["media"]["photo_count"], product["id"])
                    results.append({
                        "Ссылка на товар":"https://www.wildberries.ru/catalog/{}/detail.aspx".format(product["id"]),
                        "Артикул": str(product["id"]),
                        "Название": product["name"], 
                        "Цена, руб.": product["sizes"][0]["price"]["product"]/100, 
                        "Описание": product_details["description"], 
                        "Ссылки на изображения": ", ".join(links), 
                        "Характеристики":', '.join([f'{key}: {value}' for key, value in characteristics.items()]), 
                        "Название селлера": product["brand"],
                        "Ссылка на селлера": "https://www.wildberries.ru/brands/{}".format(product["brand"]),
                        "Размеры товара":", ".join(sizes),
                        "Остатки по товару (число)": self.get_qty(product["id"]),
                        "Рейтинг": product["reviewRating"],
                        "Количество отзывов": product["feedbacks"]
                        })
        return results



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
    result = pd.DataFrame(result)
    result.to_excel("results.xlsx")
    print("Результаты записаны в файл results.xlsx")