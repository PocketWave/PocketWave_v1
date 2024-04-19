import tkinter as tk
from PIL import Image, ImageTk
from MainWindow import *
import webbrowser
class Root(tk.Tk):
    def __init__(self):
        super().__init__()
        self.wm_title('')
        self.iconbitmap("Images/Icon.ico")
        self.resizable(False,False)
        self.Menu()
        self.centrar()
        MainWindow(self)
        self.mainloop()

    def centrar(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        window_width = 800
        window_height = 700

        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.geometry(f'{window_width}x{window_height}+{x}+{y}')

    def Menu(self):
        #menu
        Menu=tk.Menu(self)
        #sub-menu
        file_menu=tk.Menu(Menu,tearoff=False)
        help_menu=tk.Menu(Menu,tearoff=False)
        help_menu.add_command(label='GUI Manual')
        Menu.add_cascade(label="Help",menu=help_menu)

        contacts_menu=tk.Menu(Menu,tearoff=False)
        contacts_menu.add_command(label='Go to Pocketwave website',command=self.OpenWebSite)
        Menu.add_cascade(label="Contacts",menu=contacts_menu)
        


        self.configure(menu=Menu)

    def OpenWebSite(self):
        webbrowser.open_new("https://pocketwave.web.ua.pt/")    
if __name__ == '__main__':
    Root()
