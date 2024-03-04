import customtkinter as ctk
from PIL import Image

class Interface():
    
    def __init__(self, reference_page_logo: Image,national_currency: str,currencies: dict, currencies_imgs: dict):
        self.root = ctk.CTk()
        self.root.title('Currency Scraper')
        self.root.geometry('350x450')
        self.root.minsize(320,450)
        self.root.resizable(False, False)     
        self.root.iconbitmap('logo_currency_scraper.ico')   

        self.main_frame=ctk.CTkFrame(self.root)
        self.reference_page_frame=ctk.CTkFrame(self.main_frame)
        page_logo = ctk.CTkImage(reference_page_logo)
        self.logo_label = ctk.CTkLabel(self.reference_page_frame,image=page_logo, text='')
        self.logo_label.place(relwidth=1, relheight=1)
        self.reference_page_frame.place(relx=0.15, rely=0.15,relwidth=1, relheight=0.15)

        rel_y_pos = 0.15
        for currency in currencies:
            img = ctk.CTkImage(currencies_imgs[currency])
            currency_img = ctk.CTkLabel(self.main_frame, image=img, text='')
            currency_img.place(relx = 0.3, rely=rel_y_pos)
            currency_price = ctk.CTkLabel(self.main_frame, text=f'{currencies[currency]} {national_currency}')
            currency_price.place(relx = 0.45, rely=rel_y_pos)
            rel_y_pos+=rel_y_pos

        self.main_frame.place(relx = 0.3, relwidth=0.4, relheight=1)