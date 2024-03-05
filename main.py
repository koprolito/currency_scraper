from scraper import Scraper
from interface import Interface

if __name__ == '__main__':
    
    scraper = Scraper('https://www.bcv.org.ve/',['dolar', 'euro', "rublo", "yuan", "lira"])
    scraper.set_currencies_prices(['div', 'strong'])
    scraper.set_currencies_images(['div', 'img'])

    window = Interface('Bs.',scraper.currencies,scraper.currencies_images)
    scraper.save_currencies_data()
    window.root.mainloop()