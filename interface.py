import customtkinter as ctk
from PIL import Image

class Interface():
    
    def __init__(self, reference_page_logo: Image,national_currency: str,currencies: dict, currencies_imgs: dict):
        self.root = ctk.CTk()
        self.root.title('Currency Scraper')
        self.root.geometry('350x450')
        self.root.minsize(320,450)
        self.root.resizable(False, False)

        self.main_frame=ctk.CTkFrame(self.root)
        self.reference_page_frame=ctk.CTkFrame(self.main_frame)
        page_logo = ctk.CTkImage(reference_page_logo)
        self.logo_label = ctk.CTkLabel(self.reference_page_frame,image=page_logo, text='')
        self.logo_label.pack(expand=True)
        self.reference_page_frame.pack(anchor='n', expand=True)

        for currency in currencies:
            img = ctk.CTkImage(currencies_imgs[currency])
            currency_img = ctk.CTkLabel(self.main_frame, image=img, text='')
            currency_img.pack()
            currency_price = ctk.CTkLabel(self.main_frame, text=f'{currencies[currency]} {national_currency}')
            currency_price.pack()


        self.main_frame.pack(fill=ctk.BOTH, expand=True)