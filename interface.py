import customtkinter as ctk

class Interface():
    
    def __init__(self, currencies: dict, currencies_imgs: dict):
        self.root = ctk.CTk()
        self.root.title('Currency Scraper')
        self.root.geometry('350x450')
        self.root.minsize(320,450)

        self.main_frame=ctk.CTkScrollableFrame(self.root)
        self.main_frame.pack(fill=ctk.BOTH, expand=True)
        
        for currency in currencies:
            label = ctk.CTkLabel(self.main_frame, text=f'{currency}\t{currencies[currency]}')
            label.pack()