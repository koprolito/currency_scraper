from scraper import Scraper
from interface import Interface

if __name__ == '__main__':
    scraper = Scraper('https://www.bcv.org.ve/',['dolar', 'euro'])
    scraper.set_currencies_prices(['div', 'strong'])
    scraper.set_currencies_images(['div', 'img'])
    print(scraper.currencies_images)
    window = Interface(scraper.currencies,None)
    window.root.mainloop()