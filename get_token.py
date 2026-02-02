import time

from seleniumbase import Driver

class CookiesWB:
    USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36'
    URL = "https://www.wildberries.ru/"
    COOKIE_NEED = "x_wbaas_token"

    def __init__(self, user_agent: str = None, url: str = None, cookie_need: str = None):
        self.user_agent = user_agent or CookiesWB.USER_AGENT
        self.url = url or CookiesWB.URL
        self.cookie_need = cookie_need or CookiesWB.COOKIE_NEED
    
    def get_token(self) -> str:
        driver = Driver(
        uc=True,
        # headed=True,
        headless=True,
        agent = self.user_agent)

        try:
            driver.open("https://www.wildberries.ru/")
            for _ in range(3):
                cookies = driver.execute_cdp_cmd("Network.getAllCookies", {})
                for cookie in cookies.get("cookies"):
                    if cookie.get("name") == self.cookie_need:
                        return cookie.get("value")
                time.sleep(5)
            return None
        finally:
            driver.quit()

def get_token() -> str:
    return CookiesWB().get_token()

if __name__ == "__main__":
    token = CookiesWB().get_token()
    print(token)