import csv
import socket
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
from datetime import datetime
import os
import pandas as pd

class Scraper():

    def __init__(self, link: str, currencies: list) -> None:
        self.link = link
        self.page = None
        self.connect_to_currencie_page()
        self.currencies: dict[str, int] = {}
        self.currencies_images: dict[str, str] = {}
        for currency in currencies:
            self.currencies[currency] = 0
            self.currencies_images[currency] = ''

    def connect_to_currencie_page(self) -> None:
        '''Connects to the web page from which the prices and images are going
        to be processed later.
        
        WARNING: the verify value of request.get DOES NOT use SSL verification 
        in this phase of the project. 
        Only connect to web pages that you consider trustful, otherwise you may expose
        to \'man in the middle\' attacks under your own risk.'''
        self.page = requests.get(self.link, verify=False)

    def get_currency_image(self, tag_names: list, id: str) -> str:
        '''Gets the images of the currencies in their respective web page.'''
        
        def format_link(currency_link: str) -> str:
            '''Returns an str of the currency_link so that its format
            is appropiate for an image request'''
            
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
        '''Retrieves an image from a given URL and returns it as an Image object.'''

        response = requests.get(url, verify=False)
        img_data = response.content
        img = Image.open(BytesIO(img_data))
        return img

    def download_currencies_images(self) -> dict[str:Image]:
        ''''Downloads the images of a currencies in their respective web page 
        and returns a dictionary of structure 
        str (name of the currency): Image (an Image object of the currency)'''

        images: dict[str:Image] = {}

        for currency in self.currencies_images:
            url = self.currencies_images[currency]
            img = self.retrieve_img(url=url)
            images[currency] = img

        return images

    def get_currency_price(self, tag_names: list, id: str) -> str:
        ''''Gets the prices of the currencies in their respective web page.
        tag_names refers to a list of HTML tags of the web page that contains 
        the value of an specific currency. The way the tags are listed matters.'''
        
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

        return float(format_price(str(currency_price).replace(",",".")))
    
    def set_currencies_prices(self, tag_names: list):
        '''Sets the values of the prices for the currencies that are listed in self.currencies.
        For this, it takes all the prices of the currencies in their respective web page (as
        it has to be set while intializing the object).''' 
        for currency in self.currencies:
            self.currencies[currency] = self.get_currency_price(tag_names, currency)

    def set_currencies_images(self, tag_names: list) -> None: 
        '''Sets the images for the currencies that are listed in self.currencies. For
        this, it takes all the images of the currencies in their respective web page (as
        it has to be set while intializing the object).'''       
        for currency in self.currencies_images:
            self.currencies_images[currency] = self.get_currency_image(tag_names, currency)
        self.currencies_images = self.download_currencies_images()

    def save_currencies_data(self) -> None:
        '''Saves the prices of the currencies in the prices.csv file'''

        def get_previous_prices() -> list[float]:
            '''Returns the last price registered in the prices.csv file'''

            df = pd.read_csv('prices.csv', sep="|")
            # Get last row
            last_row = df.iloc[-1]
            previous_prices: list[float] = []
            for i in range(len(last_row)):
                if i > 0:
                    previous_prices.append(float(last_row.iloc[i]))
            return previous_prices
        
        def compare_previous_prices(previous_prices:list[float],new_prices:list[float]) -> bool:
            '''Compares a given previous prices list of float values with a new prices list.
             
              If there is one single price in previous prices
              that does not match with the new prices it returns True, otherwise returns False '''
            flag = False
            for i in range(len(previous_prices)):
                if previous_prices[i] != new_prices[i]:
                    flag = True
            return flag

        csv_headers = None
        new_file = False
        # Creaes the file "prices.csv" if it does not already exists,
        #if it does it opens it in appending mode
        if not os.path.exists('prices.csv'):
            csv_file = open('prices.csv', 'w', encoding='utf-8', newline='')

             # writing the header of the CSV file
            csv_headers = ['DATE,HOUR']
            for currency in self.currencies:
                csv_headers.append(currency.upper())
            new_file = True
        else:
            csv_file = open('prices.csv', 'a', encoding='utf-8', newline='')

        # initializing the writer object to insert data
        # in the CSV file
        writer = csv.writer(csv_file, delimiter="|")

        # initialize a list that will contain the current date, current time and
        # the prices of the currencies
        prices_row = [f"{datetime.now().strftime("%d/%m/%Y")},{datetime.now().strftime("%H:%M")}"]
        new_prices: list[float] = []
        for currency in self.currencies:
            currency_price = float(str(self.currencies[currency]).replace(",","."))
            prices_row.append(currency_price)
            new_prices.append(currency_price)

        # if the file has been created now, the write both its headers and
        # the current prices of the currencies, else compare their previous prices
        # with the new ones to know if there is any need to update the file with a new row
        if new_file:
            writer.writerow(csv_headers)        
            writer.writerow(prices_row)
        else:
            previous_prices = get_previous_prices()
            if compare_previous_prices(previous_prices=previous_prices, new_prices=new_prices):
                writer.writerow(prices_row)

        # terminating the operation and releasing the resources
        csv_file.close()