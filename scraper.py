import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO

class Scraper():

    def __init__(self, link: str, currencies: list) -> None:
        self.link = link
        self.currencies: dict[str, int] = {}
        self.currencies_images: dict[str, str] = {}
        for currency in currencies:
            self.currencies[currency] = 0
            self.currencies_images[currency] = ''
        self.page = None
        self.connect_to_currencie_page()

    def connect_to_currencie_page(self) -> None:
        self.page = requests.get(self.link, verify=False)

    def get_currency_image(self, tag_names: list, id: str) -> str:
        
        def format_link(currency_link: str) -> str:
            
            img_link = currency_link[currency_link.find('src=')+5:currency_link.find('png')+3]            
            img_link = self.link+img_link

            return img_link
        
        soup = BeautifulSoup(self.page.text, 'html.parser')
        currency_link = str()
        for i in range(len(tag_names)):
            if i == 0:
                currency_link = soup.find(tag_names[i],id=id)
            else:
                currency_link = currency_link.find(tag_names[i])

        return format_link(str(currency_link))
    

    def retrieve_img(self, url) -> Image:
        response = requests.get(url, verify=False)
        img_data = response.content
        img = Image.open(BytesIO(img_data))
        return img

    def download_currencies_images(self):

        images: dict[str:Image] = {}

        for currency in self.currencies_images:
            url = self.currencies_images[currency]
            img = self.retrieve_img(url=url)
            images[currency] = img

        return images

    def get_currency_price(self, tag_names: list, id: str) -> str:
        
        def format_price(currency_price: str) -> str:
            i = 0
            while str(currency_price[i]).isdigit() == False:
                i += 1

            actual_price = ''
            while str(currency_price[i]).isdigit() == True or str(currency_price[i]) == ',' or str(currency_price[i]) == '.':
                actual_price += currency_price[i]
                i += 1

            return actual_price

        soup = BeautifulSoup(self.page.text, 'html.parser')
        currency_price = str()
        for i in range(len(tag_names)):
            if i == 0:
                currency_price = soup.find(tag_names[i],id=id)
            else:
                currency_price = currency_price.find(tag_names[i])

        return format_price(str(currency_price))
    
    def set_currencies_prices(self, tag_names: list):
        for currency in self.currencies:
            self.currencies[currency] = self.get_currency_price(tag_names, currency)

    def set_currencies_images(self, tag_names: list):
        for currency in self.currencies_images:
            self.currencies_images[currency] = self.get_currency_image(tag_names, currency)
        self.currencies_images = self.download_currencies_images()