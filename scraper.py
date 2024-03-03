import requests
from bs4 import BeautifulSoup

page = requests.get('https://www.bcv.org.ve/', verify=False)
soup = BeautifulSoup(page.text, 'html.parser')
dolar_price = str(soup.find('div',id='dolar').find('strong'))
print(f'{dolar_price[dolar_price.find('>')+2:dolar_price.find(' </strong>')]}')