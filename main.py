from scraper import Scraper
from interface import Interface

'''Disclaimer:

    If your interest is to only see the prices of the currencies fast, you can 
    just use the print(scraper.currencies) that is right below scraper.save_currencies_data()
    and comment the rest of the code that is below the print. Otherwise you will load the whole
    GUI that contains the prices of each currency listed, including their symbols, however this
    might take a little more time depending on your internet connection.'''

if __name__ == '__main__':

    #The first value of the constructor is the link of the web page to be scraped,
    #the second one consists of a list with the names of the currencies that the web page has registered.
    scraper = Scraper('https://www.bcv.org.ve/',['dolar', 'euro', "rublo", "yuan", "lira"])
    
    scraper.set_currencies_prices(['div', 'strong'])
    scraper.save_currencies_data()
    print(scraper.currencies)

'''    scraper.set_currencies_images(['div', 'img'])

    window = Interface('Bs.',scraper.currencies,scraper.currencies_images)
    window.root.mainloop()'''