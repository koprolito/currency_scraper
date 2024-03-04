from scraper import Scraper, requests
from interface import Interface

if __name__ == '__main__':
    
    scraper = Scraper('https://www.bcv.org.ve/',['dolar', 'euro'])
    scraper.set_currencies_prices(['div', 'strong'])
    scraper.set_currencies_images(['div', 'img'])

    reference_page_logo = scraper.retrieve_img("https://www.bcv.org.ve/sites/default/files/default_images/logo_bcv-04_2.png")

    window = Interface(reference_page_logo,'Bs.',scraper.currencies,scraper.currencies_images)
    window.root.mainloop()