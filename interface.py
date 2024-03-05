import customtkinter as ctk
from PIL import Image

class Interface():
    
    def __init__(self, national_currency: str,currencies: dict, currencies_imgs: dict):
        self.root = ctk.CTk()
        self.root.title('Currency Scraper')
        self.root.geometry('350x450')
        self.root.minsize(320,450)
        self.root.resizable(False, False)     
        self.root.iconbitmap('logo_currency_scraper.ico')   
        self.root.configure(fg_color="#174369")

        self.main_frame=ctk.CTkScrollableFrame(self.root)

        rel_y_pos = 0.1
        for currency in currencies:
            img = ctk.CTkImage(currencies_imgs[currency])
            currency_img = ctk.CTkLabel(self.main_frame, image=img, text=f'\n\n\n{str(currency).upper()}')
            currency_img.pack()
            currency_price = ctk.CTkLabel(self.main_frame, text=f'{currencies[currency]} {national_currency}')
            currency_price.pack()
            rel_y_pos+=rel_y_pos

        self.main_frame.place(relx = 0.27, relwidth=0.5, relheight=1)