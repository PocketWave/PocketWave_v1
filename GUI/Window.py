import tkinter as tk
import webbrowser
from MultimeterFrame import *
from OscilloscopeFramr import *
from PSupllyFrame import *
from SGeneratorFrame import *

class Window(tk.Toplevel):
    def __init__(self,Title,Size): 
        super().__init__()
        self.wm_title('')
        self.iconbitmap("Imagens/Icon.ico")
        self.resizable(True,True)
        self.title(Title)
        self.geometry(Size)
        
        self.Show()
        self.Menu()

    def Show(self):
        if(self.title()=='Signal Generator'):
            self.rowconfigure(0,weight=1)
            self.columnconfigure(0,weight=1)
            self.SG=SignalGenerator(self)
            self.SG.grid(row=0,column=0,sticky="NWES")

        elif(self.title()=='Power Supply'):
            self.rowconfigure(0,weight=1)
            self.columnconfigure(0,weight=1)
            self.PS=PowerSupply(self)
            self.PS.grid(row=0,column=0,sticky="NWES")
        elif(self.title()=='Oscilloscope'):
            self.rowconfigure(0,weight=1)
            self.columnconfigure(0,weight=1)
            self.columnconfigure(1,weight=1)
            self.columnconfigure(2,weight=1)
            self.rowconfigure(1,weight=5)
            self.Oscil=Oscilloscope(self)
            self.Oscil.grid(row=0,column=0,sticky="NSWE",rowspan=2,columnspan=3)
            
        else:
            self.rowconfigure(0,weight=1)
            self.columnconfigure(0,weight=1)
            self.Mult=Multimeter(self)
            self.Mult.grid(row=0,column=0,sticky="NWES")
    def Menu(self):
        
        if(self.title()=='Signal Generator'):
            Menu=tk.Menu(self)

            Show_menu=tk.Menu(Menu,tearoff=False)
            self.OscilWindow1=tk.BooleanVar()
            self.MultWindow1=tk.BooleanVar()
            self.PSWindow1=tk.BooleanVar()
            Show_menu.add_checkbutton(label="Show Oscilloscope Window",command=self.ShowOscilWindow,variable=self.OscilWindow1)
            Show_menu.add_checkbutton(label="Show Multimeter Window",command=self.ShowMultWindow,variable=self.MultWindow1)
            Show_menu.add_checkbutton(label="Show Power Supply Window",command=self.ShowPSWindow,variable=self.PSWindow1)
            Menu.add_cascade(label="Show...",menu=Show_menu)

            help_menu=tk.Menu(Menu,tearoff=False)
            help_menu.add_command(label='GUI Manual',command=lambda:print('GUI Manual'))
            Menu.add_cascade(label="Help",menu=help_menu)

            contacts_menu=tk.Menu(Menu,tearoff=False)
            contacts_menu.add_command(label='Go to Pocketwave website',command=self.OpenWebSite)
            Menu.add_cascade(label="Contacts",menu=contacts_menu)

            self.configure(menu=Menu)
        elif(self.title()=='Multimeter'):
            Menu=tk.Menu(self)

            Show_menu=tk.Menu(Menu,tearoff=False)
            self.OscilWindow2=tk.BooleanVar()
            self.SGWindow1=tk.BooleanVar()
            self.PSWindow2=tk.BooleanVar()
            Show_menu.add_checkbutton(label="Show Oscilloscope Window",command=self.ShowOscilWindow,variable=self.OscilWindow2)
            Show_menu.add_checkbutton(label="Show Signal Generator Window",command=self.ShowSGWindow,variable=self.SGWindow1)
            Show_menu.add_checkbutton(label="Show Power Supply Window",command=self.ShowPSWindow,variable=self.PSWindow2)
            Menu.add_cascade(label="Show...",menu=Show_menu)

            help_menu=tk.Menu(Menu,tearoff=False)
            help_menu.add_command(label='GUI Manual',command=lambda:print('GUI Manual'))
            Menu.add_cascade(label="Help",menu=help_menu)

            contacts_menu=tk.Menu(Menu,tearoff=False)
            contacts_menu.add_command(label='Go to Pocketwave website',command=self.OpenWebSite)
            Menu.add_cascade(label="Contacts",menu=contacts_menu)

            self.configure(menu=Menu)
        elif(self.title()=='Power Supply'):
            Menu=tk.Menu(self)

            Show_menu=tk.Menu(Menu,tearoff=False)
            self.OscilWindow3=tk.BooleanVar()
            self.SGWindow2=tk.BooleanVar()
            self.MultWindow2=tk.BooleanVar()
            Show_menu.add_checkbutton(label="Show Oscilloscope Window",command=self.ShowOscilWindow,variable=self.OscilWindow3)
            Show_menu.add_checkbutton(label="Show Signal Generator Window",command=self.ShowSGWindow,variable=self.SGWindow2)
            Show_menu.add_checkbutton(label="Show Multimeter Window",command=self.ShowMultWindow,variable=self.MultWindow2)
            Menu.add_cascade(label="Show...",menu=Show_menu)

            help_menu=tk.Menu(Menu,tearoff=False)
            help_menu.add_command(label='GUI Manual',command=lambda:print('GUI Manual'))
            Menu.add_cascade(label="Help",menu=help_menu)

            contacts_menu=tk.Menu(Menu,tearoff=False)
            contacts_menu.add_command(label='Go to Pocketwave website',command=self.OpenWebSite)
            Menu.add_cascade(label="Contacts",menu=contacts_menu)

            self.configure(menu=Menu)
        else:
            Menu=tk.Menu(self)

            Show_menu=tk.Menu(Menu,tearoff=False)
            self.PSWindow3=tk.BooleanVar()
            self.SGWindow3=tk.BooleanVar()
            self.MultWindow3=tk.BooleanVar()
            Show_menu.add_checkbutton(label="Show Power Supply Window",command=self.ShowPSWindow,variable=self.PSWindow3)
            Show_menu.add_checkbutton(label="Show Signal Generator Window",command=self.ShowSGWindow,variable=self.SGWindow3)
            Show_menu.add_checkbutton(label="Show Multimeter Window",command=self.ShowMultWindow,variable=self.MultWindow3)
            Menu.add_cascade(label="Show...",menu=Show_menu)

            help_menu=tk.Menu(Menu,tearoff=False)
            help_menu.add_command(label='GUI Manual',command=lambda:print('GUI Manual'))
            Menu.add_cascade(label="Help",menu=help_menu)

            contacts_menu=tk.Menu(Menu,tearoff=False)
            contacts_menu.add_command(label='Go to Pocketwave website',command=self.OpenWebSite)
            Menu.add_cascade(label="Contacts",menu=contacts_menu)

            self.configure(menu=Menu)

    def OpenWebSite(self):
        webbrowser.open_new("https://pocketwave.web.ua.pt/")         


    def ShowPSWindow(self):
        
        if(self.title()=='Signal Generator'):
            botoes_ativosSG=int(self.OscilWindow1.get()) +int(self.MultWindow1.get())+int(self.PSWindow1.get())
            if(self.PSWindow1.get()==True):
                if(botoes_ativosSG==1 and self.OscilWindow1.get()==False):
                    
                    self.geometry("600x300")
                    self.rowconfigure(0,weight=1)
                    self.rowconfigure(1,weight=0)
                    self.columnconfigure(0,weight=1)
                    self.columnconfigure(1,weight=1)
                    self.columnconfigure(2,weight=0)
                    self.PS2=PowerSupply(self)
                    self.PS2.grid(row=0,column=1,sticky='NSWE',padx=2)
                   
                if(botoes_ativosSG==2 and self.OscilWindow1.get()==False):
                    self.Mult2.destroy()
                    self.geometry("900x300")
                    self.rowconfigure(0,weight=1)
                    self.columnconfigure(0,weight=1)
                    self.columnconfigure(1,weight=1)
                    self.columnconfigure(2,weight=1)
                    self.rowconfigure(1,weight=0)
                    self.Mult2=Multimeter(self)
                    self.Mult2.grid(row=0,column=1,sticky='NSWE')
                    self.PS2=PowerSupply(self)
                    self.PS2.grid(row=0,column=2,sticky='NSWE')
                if(botoes_ativosSG==3):
                    self.Mult2.destroy()
                    self.geometry("1000x700")
                    self.rowconfigure(0,weight=1)
                    self.columnconfigure(0,weight=1)
                    self.columnconfigure(1,weight=1)
                    self.columnconfigure(2,weight=1)
                    self.rowconfigure(1,weight=10)
                    self.Mult2=Multimeter(self)
                    self.Mult2.grid(row=0,column=1,sticky='NSWE')
                    self.PS2=PowerSupply(self)
                    self.PS2.grid(row=0,column=2,sticky='NSWE')
                if(botoes_ativosSG==2 and self.OscilWindow1.get()==True):
                    
                    self.geometry("1000x700")
                    self.rowconfigure(0,weight=1)
                    self.rowconfigure(1,weight=10)
                    self.columnconfigure(0,weight=1)
                    self.columnconfigure(1,weight=1)
                    self.columnconfigure(2,weight=1)
                    self.PS2=PowerSupply(self)
                    self.PS2.grid(row=0,column=1,sticky='NSWE')
            
            if(self.PSWindow1.get()==False):
                if(botoes_ativosSG==0):
                    
                    self.PS2.destroy()
                    self.geometry("300x300")
                    self.PS2=PowerSupply(self)
                    self.rowconfigure(0,weight=1)
                    self.rowconfigure(1,weight=0)
                    self.columnconfigure(0,weight=1)
                    self.columnconfigure(1,weight=0)
                    self.columnconfigure(2,weight=0)
                if(botoes_ativosSG==1 and self.OscilWindow1.get()==False):
                    self.PS2.destroy()
                    self.geometry("600x300")
                    self.rowconfigure(0,weight=1)
                    self.rowconfigure(1,weight=0)
                    self.columnconfigure(0,weight=1)
                    self.columnconfigure(1,weight=1)
                    self.columnconfigure(2,weight=0)
                if(botoes_ativosSG==1 and self.OscilWindow1.get()==True):
                    self.PS2.destroy()
                    self.geometry("1000x700")
                    self.columnconfigure(0,weight=1)
                    self.rowconfigure(0,weight=1)
                    self.columnconfigure(1,weight=1)
                    self.columnconfigure(2,weight=1)
                    self.rowconfigure(1,weight=10)
                if(botoes_ativosSG==2):
                    self.PS2.destroy()
                    self.geometry("1000x700")
                    self.columnconfigure(0,weight=1)
                    self.rowconfigure(0,weight=1)
                    self.rowconfigure(1,weight=10)
                    self.columnconfigure(1,weight=1)
                    self.columnconfigure(2,weight=1)
        if(self.title()=='Multimeter'):
            botoes_ativosMult=int(self.OscilWindow2.get()) +int(self.SGWindow1.get())+int(self.PSWindow2.get())
            if(self.PSWindow2.get()==True):
                if(botoes_ativosMult==1 and self.OscilWindow2.get()==False):
                    self.geometry("600x300")
                    self.rowconfigure(0,weight=1)
                    self.rowconfigure(1,weight=0)
                    self.columnconfigure(0,weight=1)
                    self.columnconfigure(1,weight=1)
                    self.columnconfigure(2,weight=0)
                    self.PS3=PowerSupply(self)
                    self.PS3.grid(row=0,column=1,sticky='NSWE')
                   
                if(botoes_ativosMult==2 and self.OscilWindow2.get()==False):
                    self.SG3.destroy()
                    self.geometry("900x300")
                    self.rowconfigure(0,weight=1)
                    self.rowconfigure(1,weight=0)
                    self.columnconfigure(0,weight=1)
                    self.columnconfigure(1,weight=1)
                    self.columnconfigure(2,weight=1)
                    self.SG3=SignalGenerator(self)
                    self.SG3.grid(row=0,column=1,sticky='NSWE')
                    self.PS3=PowerSupply(self)
                    self.PS3.grid(row=0,column=2,sticky='NSWE')
                if(botoes_ativosMult==3):
                    self.SG3.destroy()
                    self.geometry("1000x700")
                    self.rowconfigure(0,weight=1)
                    self.columnconfigure(0,weight=1)
                    self.columnconfigure(1,weight=1)
                    self.columnconfigure(2,weight=1)
                    self.rowconfigure(1,weight=10)
                    self.SG3=SignalGenerator(self)
                    self.SG3.grid(row=0,column=1,sticky='NSWE')
                    self.PS3=PowerSupply(self)
                    self.PS3.grid(row=0,column=2,sticky='NSWE')
                if(botoes_ativosMult==2 and self.OscilWindow2.get()==True):
                    
                    self.geometry("1000x700")
                    self.rowconfigure(0,weight=1)
                    self.rowconfigure(1,weight=10)
                    self.columnconfigure(0,weight=1)
                    self.columnconfigure(1,weight=1)
                    self.columnconfigure(2,weight=1)
                    self.PS3=PowerSupply(self)
                    self.PS3.grid(row=0,column=1,sticky='NSWE')
            
            if(self.PSWindow2.get()==False):
                if(botoes_ativosMult==0):
                    self.PS3.destroy()
                    self.geometry("300x300")
                    self.PS3=PowerSupply(self)
                    self.rowconfigure(0,weight=1)
                    self.rowconfigure(1,weight=0)
                    self.columnconfigure(0,weight=1)
                    self.columnconfigure(1,weight=0)
                    self.columnconfigure(2,weight=0)
                if(botoes_ativosMult==1 and self.OscilWindow2.get()==False):
                    self.PS3.destroy()
                    self.geometry("600x300")
                    self.rowconfigure(0,weight=1)
                    self.rowconfigure(1,weight=0)
                    self.columnconfigure(0,weight=1)
                    self.columnconfigure(1,weight=1)
                    self.columnconfigure(2,weight=0)
                if(botoes_ativosMult==1 and self.OscilWindow2.get()==True):
                    self.PS3.destroy()
                    self.geometry("1000x700")
                    self.columnconfigure(0,weight=1)
                    self.rowconfigure(0,weight=1)
                    self.rowconfigure(1,weight=10)
                    self.columnconfigure(1,weight=1)
                    self.columnconfigure(2,weight=1)
                if(botoes_ativosMult==2):
                    self.PS3.destroy()
                    self.geometry("1000x700")
                    self.columnconfigure(0,weight=1)
                    self.rowconfigure(0,weight=1)
                    self.rowconfigure(1,weight=10)
                    self.columnconfigure(1,weight=1)
                    self.columnconfigure(2,weight=1)

        if(self.title()=='Oscilloscope'):      
            botoes_ativosOscil=int(self.MultWindow3.get()) +int(self.SGWindow3.get())+int(self.PSWindow3.get())
            if(self.PSWindow3.get()==True):
                if(botoes_ativosOscil==1):
                    self.Oscil.destroy()
                    self.geometry("1000x700")
                    self.rowconfigure(0,weight=1)
                    self.columnconfigure(0,weight=1)
                    self.columnconfigure(1,weight=1)
                    self.columnconfigure(2,weight=1)
                    self.rowconfigure(1,weight=10)
                    self.Oscil=Oscilloscope(self)
                    self.Oscil.grid(row=1,column=0,columnspan=3,sticky="NSEW")
                    self.PS4=PowerSupply(self)
                    self.PS4.grid(row=0,column=0,sticky='NSWE')
                   
                   
                if(botoes_ativosOscil==2):
                    
                    self.geometry("1000x700")
                    self.rowconfigure(0,weight=1)
                    self.columnconfigure(0,weight=1)
                    self.columnconfigure(1,weight=1)
                    self.columnconfigure(2,weight=1)
                    self.rowconfigure(1,weight=10)
                    self.PS4=PowerSupply(self)
                    self.PS4.grid(row=0,column=0,sticky='NSWE')
                if(botoes_ativosOscil==3):
                    print(botoes_ativosOscil)
                    
                    self.geometry("1000x700")
                    self.rowconfigure(0,weight=1)
                    self.columnconfigure(0,weight=1)
                    self.columnconfigure(1,weight=1)
                    self.columnconfigure(2,weight=1)
                    self.rowconfigure(1,weight=10)
                    self.PS4=PowerSupply(self)
                    self.PS4.grid(row=0,column=0,sticky='NSWE')
            if(self.PSWindow3.get()==False):
                if(botoes_ativosOscil==0):
                    
                    self.PS4.destroy()
                    self.Oscil.destroy()
                    self.geometry("1000x700")
                    self.rowconfigure(0,weight=1)
                    self.columnconfigure(0,weight=1)
                    self.columnconfigure(1,weight=1)
                    self.columnconfigure(2,weight=1)
                    self.rowconfigure(1,weight=10)
                    self.Oscil=Oscilloscope(self)
                    
                    self.Oscil.grid(row=0,column=0,columnspan=3,rowspan=2,sticky="NSWE")
                if(botoes_ativosOscil==1):
                    
                    self.PS4.destroy()
                    self.Oscil.destroy()
                    self.geometry("1000x700")
                    self.rowconfigure(0,weight=1)
                    self.columnconfigure(0,weight=1)
                    self.columnconfigure(1,weight=1)
                    self.columnconfigure(2,weight=1)
                    self.rowconfigure(1,weight=10)
                    self.Oscil=Oscilloscope(self)
                    self.Oscil.grid(row=1,column=0,columnspan=3,sticky="NSEW")
                    
                if(botoes_ativosOscil==2):
                    print(botoes_ativosOscil)
                    self.PS4.destroy()
                    self.Oscil.destroy()
                    self.geometry("1000x700")
                    self.rowconfigure(0,weight=1)
                    self.columnconfigure(0,weight=1)
                    self.columnconfigure(1,weight=1)
                    self.columnconfigure(2,weight=1)
                    self.rowconfigure(1,weight=10)
                    self.Oscil=Oscilloscope(self)
                    self.Oscil.grid(row=1,column=0,columnspan=3,sticky="NSEW")
                    

    def ShowSGWindow(self):
        if(self.title()=='Oscilloscope'):
            botoes_ativosOscil=int(self.MultWindow3.get()) +int(self.SGWindow3.get())+int(self.PSWindow3.get())
            if(self.SGWindow3.get()==True):
                if(botoes_ativosOscil==1):
                    print(botoes_ativosOscil)
                    self.Oscil.destroy()
                    self.geometry("1000x700")
                    self.rowconfigure(0,weight=1)
                    self.columnconfigure(0,weight=1)
                    self.columnconfigure(1,weight=1)
                    self.columnconfigure(2,weight=1)
                    self.rowconfigure(1,weight=10)
                    self.Oscil=Oscilloscope(self)
                    self.Oscil.grid(row=1,column=0,columnspan=3,sticky="NSEW")
                    self.SG2=SignalGenerator(self)
                    self.SG2.grid(row=0,column=1,sticky='NSWE')
                   
                   
                if(botoes_ativosOscil==2):
                    
                    print(botoes_ativosOscil)
                    self.geometry("1000x700")
                    self.rowconfigure(0,weight=1)
                    self.columnconfigure(0,weight=1)
                    self.columnconfigure(1,weight=1)
                    self.columnconfigure(2,weight=1)
                    self.rowconfigure(1,weight=10)
                    self.SG2=SignalGenerator(self)
                    self.SG2.grid(row=0,column=1,sticky='NSWE')
                if(botoes_ativosOscil==3):
                    print(botoes_ativosOscil)
                    
                    self.geometry("1000x700")
                    self.rowconfigure(0,weight=1)
                    self.columnconfigure(0,weight=1)
                    self.columnconfigure(1,weight=1)
                    self.columnconfigure(2,weight=1)
                    self.rowconfigure(1,weight=10)
                    self.SG2=SignalGenerator(self)
                    self.SG2.grid(row=0,column=1,sticky='NSWE')
            if(self.SGWindow3.get()==False):
                if(botoes_ativosOscil==0):
                    
                    self.SG2.destroy()
                    self.Oscil.destroy()
                    self.geometry("1000x700")
                    self.rowconfigure(0,weight=1)
                    self.columnconfigure(0,weight=1)
                    self.columnconfigure(1,weight=1)
                    self.columnconfigure(2,weight=1)
                    self.rowconfigure(1,weight=10)
                    self.Oscil=Oscilloscope(self)
                    
                    self.Oscil.grid(row=0,column=0,rowspan=2,columnspan=3,sticky="NSWE")
                if(botoes_ativosOscil==1):
                    self.SG2.destroy()
                    
                    
                    self.Oscil.destroy()
                    self.geometry("1000x700")
                    self.rowconfigure(0,weight=1)
                    self.columnconfigure(0,weight=1)
                    self.columnconfigure(1,weight=1)
                    self.columnconfigure(2,weight=1)
                    self.rowconfigure(1,weight=10)
                    self.Oscil=Oscilloscope(self)
                    self.Oscil.grid(row=1,column=0,columnspan=3,sticky="NSEW")
                    
                if(botoes_ativosOscil==2):
                    print(botoes_ativosOscil)
                    self.SG2.destroy()
                    self.Oscil.destroy()
                    self.geometry("1000x700")
                    self.rowconfigure(0,weight=1)
                    self.columnconfigure(0,weight=1)
                    self.columnconfigure(1,weight=1)
                    self.columnconfigure(2,weight=1)
                    self.rowconfigure(1,weight=10)
                    self.Oscil=Oscilloscope(self)
                    self.Oscil.grid(row=1,column=0,columnspan=3,sticky="NSEW")


        if(self.title()=='Multimeter'):
            botoes_ativosMult=int(self.OscilWindow2.get()) +int(self.SGWindow1.get())+int(self.PSWindow2.get())
            if(self.SGWindow1.get()==True):
                if(botoes_ativosMult==1 and self.OscilWindow2.get()==False):
                    self.geometry("600x300")
                    self.rowconfigure(0,weight=1)
                    self.rowconfigure(1,weight=0)
                    self.columnconfigure(0,weight=1)
                    self.columnconfigure(1,weight=0)
                    self.columnconfigure(2,weight=0)
                    self.SG3=SignalGenerator(self)
                    self.SG3.grid(row=0,column=1,sticky='NSWE')
                   
                if(botoes_ativosMult==2 and self.OscilWindow2.get()==False):
                    self.PS3.destroy()
                    self.geometry("900x300")
                    self.rowconfigure(0,weight=1)
                    
                    self.rowconfigure(1,weight=0)
                    self.columnconfigure(0,weight=1)
                    self.columnconfigure(1,weight=1)
                    self.columnconfigure(2,weight=1)
                    self.PS3=PowerSupply(self)
                    self.PS3.grid(row=0,column=1,sticky='NSWE')
                    self.SG3=SignalGenerator(self)
                    self.SG3.grid(row=0,column=2,sticky='NSWE')
                if(botoes_ativosMult==3):
                    self.PS3.destroy()
                    self.geometry("1000x700")
                    self.rowconfigure(0,weight=1)
                    self.columnconfigure(0,weight=1)
                    self.columnconfigure(1,weight=1)
                    self.columnconfigure(2,weight=1)
                    self.rowconfigure(1,weight=10)
                    self.PS3=PowerSupply(self)
                    self.PS3.grid(row=0,column=1,sticky='NSWE')
                    self.SG3=SignalGenerator(self)
                    self.SG3.grid(row=0,column=2,sticky='NSWE')
                if(botoes_ativosMult==2 and self.OscilWindow2.get()==True):
                    
                    self.geometry("1000x700")
                    self.rowconfigure(0,weight=1)
                    self.rowconfigure(1,weight=10)
                    self.columnconfigure(0,weight=1)
                    self.columnconfigure(1,weight=1)
                    self.columnconfigure(2,weight=1)
                    self.SG3=SignalGenerator(self)
                    self.SG3.grid(row=0,column=1,sticky='NSWE')
            
            if(self.SGWindow1.get()==False):
                if(botoes_ativosMult==0):
                    self.SG3.destroy()
                    self.geometry("300x300")
                    self.SG3=SignalGenerator(self)
                    self.rowconfigure(0,weight=1)
                    self.rowconfigure(1,weight=0)
                    self.columnconfigure(0,weight=1)
                    self.columnconfigure(1,weight=0)
                    self.columnconfigure(2,weight=0)
                if(botoes_ativosMult==1 and self.OscilWindow2.get()==False):
                    self.SG3.destroy()
                    self.geometry("600x300")
                    self.rowconfigure(0,weight=1)
                    self.rowconfigure(1,weight=0)
                    self.columnconfigure(0,weight=1)
                    self.columnconfigure(1,weight=1)
                    self.columnconfigure(2,weight=0)
                if(botoes_ativosMult==1 and self.OscilWindow2.get()==True):
                    self.SG3.destroy()
                    self.geometry("1000x700")
                    self.columnconfigure(0,weight=1)
                    self.rowconfigure(0,weight=1)
                    self.rowconfigure(1,weight=10)
                    self.columnconfigure(1,weight=1)
                    self.columnconfigure(2,weight=1)
                if(botoes_ativosMult==2):
                    self.SG3.destroy()
                    self.geometry("1000x700")
                    self.columnconfigure(0,weight=1)
                    self.rowconfigure(0,weight=1)
                    self.rowconfigure(1,weight=10)
                    self.columnconfigure(1,weight=1)
                    self.columnconfigure(2,weight=1)



        if(self.title()=='Power Supply'):
            botoes_ativosPS=int(self.OscilWindow3.get()) +int(self.SGWindow2.get())+int(self.MultWindow2.get())
            if(self.SGWindow2.get()==True):
                if(botoes_ativosPS==1 and self.OscilWindow3.get()==False):
                    self.geometry("600x300")
                    self.rowconfigure(0,weight=1)
                    self.rowconfigure(1,weight=0)
                    self.columnconfigure(0,weight=1)
                    self.columnconfigure(1,weight=1)
                    self.columnconfigure(2,weight=0)
                    self.SG4=SignalGenerator(self)
                    self.SG4.grid(row=0,column=1,sticky='NSWE')
                   
                if(botoes_ativosPS==2 and self.OscilWindow3.get()==False):
                    self.Mult3.destroy()
                    self.geometry("900x300")
                    self.rowconfigure(0,weight=1)
                    self.rowconfigure(1,weight=0)
                    self.columnconfigure(0,weight=1)
                    self.columnconfigure(1,weight=1)
                    self.columnconfigure(2,weight=1)
                    self.Mult3=Multimeter(self)
                    self.Mult3.grid(row=0,column=1,sticky='NSWE')
                    self.SG4=SignalGenerator(self)
                    self.SG4.grid(row=0,column=2,sticky='NSWE')
                if(botoes_ativosPS==3):
                    self.Mult3.destroy()
                    self.geometry("1000x700")
                    self.rowconfigure(0,weight=1)
                    self.columnconfigure(0,weight=1)
                    self.columnconfigure(1,weight=1)
                    self.columnconfigure(2,weight=1)
                    self.rowconfigure(1,weight=10)
                    self.Mult3=Multimeter(self)
                    self.Mult3.grid(row=0,column=1,sticky='NSWE')
                    self.SG4=SignalGenerator(self)
                    self.SG4.grid(row=0,column=2,sticky='NSWE')
                if(botoes_ativosPS==2 and self.OscilWindow3.get()==True):
                    
                    self.geometry("1000x700")
                    self.rowconfigure(0,weight=1)
                    self.rowconfigure(1,weight=10)
                    self.columnconfigure(0,weight=1)
                    self.columnconfigure(1,weight=1)
                    self.columnconfigure(2,weight=1)
                    self.SG4=SignalGenerator(self)
                    self.SG4.grid(row=0,column=1,sticky='NSWE')
            
            if(self.SGWindow2.get()==False):
                if(botoes_ativosPS==0):
                    self.SG4.destroy()
                    self.geometry("300x300")
                    self.SG4=SignalGenerator(self)
                    self.rowconfigure(0,weight=1)
                    self.rowconfigure(1,weight=0)
                    self.columnconfigure(0,weight=1)
                    self.columnconfigure(1,weight=0)
                    self.columnconfigure(2,weight=0)
                if(botoes_ativosPS==1 and self.OscilWindow3.get()==False):
                    self.SG4.destroy()
                    self.geometry("600x300")
                    self.rowconfigure(0,weight=1)
                    self.rowconfigure(1,weight=0)
                    self.columnconfigure(0,weight=1)
                    self.columnconfigure(1,weight=1)
                    self.columnconfigure(2,weight=0)
                if(botoes_ativosPS==1 and self.OscilWindow3.get()==True):
                    self.geometry("1000x700")
                    self.columnconfigure(0,weight=1)
                    self.columnconfigure(1,weight=1)
                    self.columnconfigure(2,weight=1)
                    self.rowconfigure(0,weight=1)
                    self.rowconfigure(1,weight=10)
                    self.SG4.destroy()
                    
                if(botoes_ativosPS==2):
                    self.SG4.destroy()
                    self.geometry("1000x700")
                    self.columnconfigure(0,weight=1)
                    self.rowconfigure(0,weight=1)
                    self.rowconfigure(1,weight=10)
                    self.columnconfigure(1,weight=1)
                    self.columnconfigure(2,weight=1)
    def ShowMultWindow(self):
        if(self.title()=='Signal Generator'):
            botoes_ativosSG=int(self.OscilWindow1.get()) +int(self.MultWindow1.get())+int(self.PSWindow1.get())
            if(self.MultWindow1.get()==True):
                if(botoes_ativosSG==1 and self.OscilWindow1.get()==False):
                    self.geometry("600x300")
                    self.rowconfigure(0,weight=1)
                    self.rowconfigure(1,weight=0)
                    self.columnconfigure(0,weight=1)
                    self.columnconfigure(1,weight=1)
                    self.columnconfigure(2,weight=0)
                    self.Mult2=Multimeter(self)
                    self.Mult2.grid(row=0,column=1,sticky='NSWE')
                   
                if(botoes_ativosSG==2 and self.OscilWindow1.get()==False):
                    self.PS2.destroy()
                    self.geometry("900x300")
                    self.rowconfigure(0,weight=1)
                    self.rowconfigure(1,weight=0)
                    self.columnconfigure(0,weight=1)
                    self.columnconfigure(1,weight=1)
                    self.columnconfigure(2,weight=1)
                    self.PS2=PowerSupply(self)
                    self.PS2.grid(row=0,column=1,sticky='NSWE')
                    self.Mult2=Multimeter(self)
                    self.Mult2.grid(row=0,column=2,sticky='NSWE')
                if(botoes_ativosSG==3):
                    self.PS2.destroy()
                    self.geometry("1000x700")
                    self.rowconfigure(0,weight=1)
                    self.columnconfigure(0,weight=1)
                    self.columnconfigure(1,weight=1)
                    self.columnconfigure(2,weight=1)
                    self.rowconfigure(1,weight=10)
                    self.PS2=PowerSupply(self)
                    self.PS2.grid(row=0,column=1,sticky='NSWE')
                    self.Mult2=Multimeter(self)
                    self.Mult2.grid(row=0,column=2,sticky='NSWE')
                if(botoes_ativosSG==2 and self.OscilWindow1.get()==True):
                    
                    self.geometry("1000x700")
                    self.rowconfigure(0,weight=1)
                    self.rowconfigure(1,weight=10)
                    self.columnconfigure(0,weight=1)
                    self.columnconfigure(1,weight=1)
                    self.columnconfigure(2,weight=1)
                    self.Mult2=Multimeter(self)
                    self.Mult2.grid(row=0,column=1,sticky='NSWE')
            
            if(self.MultWindow1.get()==False):
                if(botoes_ativosSG==0):
                    self.Mult2.destroy()
                    self.geometry("300x300")
                    self.Mult2=Multimeter(self)
                    self.rowconfigure(0,weight=1)
                    self.rowconfigure(1,weight=0)
                    self.columnconfigure(0,weight=1)
                    self.columnconfigure(1,weight=0)
                    self.columnconfigure(2,weight=0)
                if(botoes_ativosSG==1 and self.OscilWindow1.get()==False):
                    self.Mult2.destroy()
                    self.geometry("600x300")
                    self.rowconfigure(0,weight=1)
                    self.rowconfigure(1,weight=0)
                    self.columnconfigure(0,weight=1)
                    self.columnconfigure(1,weight=1)
                    self.columnconfigure(2,weight=0)
                if(botoes_ativosSG==1 and self.OscilWindow1.get()==True):
                    self.Mult2.destroy()
                    self.geometry("1000x700")
                    self.rowconfigure(0,weight=1)
                    self.rowconfigure(1,weight=10)
                    self.columnconfigure(0,weight=1)
                    self.columnconfigure(1,weight=1)
                    self.columnconfigure(2,weight=1)
                if(botoes_ativosSG==2):
                    self.Mult2.destroy()
                    self.geometry("1000x700")
                    self.rowconfigure(0,weight=1)
                    self.rowconfigure(1,weight=10)
                    self.columnconfigure(0,weight=1)
                    self.columnconfigure(1,weight=1)
                    self.columnconfigure(2,weight=1)

        if(self.title()=='Power Supply'):
            print(self.SGWindow2.get())
            botoes_ativosPS=int(self.OscilWindow3.get()) +int(self.SGWindow2.get())+int(self.MultWindow2.get())
            if(self.MultWindow2.get()==True):
                if(botoes_ativosPS==1 and self.OscilWindow3.get()==False):
                    self.geometry("600x300")
                    self.rowconfigure(0,weight=1)
                    self.rowconfigure(1,weight=0)
                    self.columnconfigure(0,weight=1)
                    self.columnconfigure(1,weight=1)
                    self.columnconfigure(2,weight=0)
                    self.Mult3=Multimeter(self)
                    self.Mult3.grid(row=0,column=1,sticky='NSWE')
                   
                if(botoes_ativosPS==2 and self.OscilWindow3.get()==False):
                    self.SG4.destroy()
                    self.geometry("900x300")
                    self.rowconfigure(0,weight=1)
                    self.rowconfigure(1,weight=0)
                    self.columnconfigure(0,weight=1)
                    self.columnconfigure(1,weight=1)
                    self.columnconfigure(2,weight=1)
                    self.SG4=SignalGenerator(self)
                    self.SG4.grid(row=0,column=1,sticky='NSWE')
                    self.Mult3=Multimeter(self)
                    self.Mult3.grid(row=0,column=2,sticky='NSWE')
                if(botoes_ativosPS==3):
                    self.SG4.destroy()
                    self.geometry("1000x700")
                    self.rowconfigure(0,weight=1)
                    self.columnconfigure(0,weight=1)
                    self.columnconfigure(1,weight=1)
                    self.columnconfigure(2,weight=1)
                    self.rowconfigure(1,weight=10)
                    self.SG4=SignalGenerator(self)
                    self.SG4.grid(row=0,column=1,sticky='NSWE')
                    self.Mult3=Multimeter(self)
                    self.Mult3.grid(row=0,column=2,sticky='NSWE')
                if(botoes_ativosPS==2 and self.OscilWindow3.get()==True):
                    
                    self.geometry("1000x700")
                    self.rowconfigure(0,weight=1)
                    self.rowconfigure(1,weight=10)
                    self.columnconfigure(0,weight=1)
                    self.columnconfigure(1,weight=1)
                    self.columnconfigure(2,weight=1)
                    self.Mult3=Multimeter(self)
                    self.Mult3.grid(row=0,column=1,sticky='NSWE')
            
            if(self.MultWindow2.get()==False):
                if(botoes_ativosPS==0):
                    self.Mult3.destroy()
                    self.geometry("300x300")
                    self.rowconfigure(0,weight=1)
                    self.rowconfigure(1,weight=0)
                    self.columnconfigure(0,weight=1)
                    self.columnconfigure(1,weight=0)
                    self.columnconfigure(2,weight=0)
                if(botoes_ativosPS==1 and self.OscilWindow3.get()==False):
                    self.Mult3.destroy()
                    self.geometry("600x300")
                    self.rowconfigure(0,weight=1)
                    self.rowconfigure(1,weight=0)
                    self.columnconfigure(0,weight=1)
                    self.columnconfigure(1,weight=1)
                    self.columnconfigure(2,weight=0)
                if(botoes_ativosPS==1 and self.OscilWindow3.get()==True):
                    self.Mult3.destroy()
                    self.geometry("1000x700")
                    self.rowconfigure(0,weight=1)
                    self.rowconfigure(1,weight=10)
                    self.columnconfigure(0,weight=1)
                    self.columnconfigure(1,weight=1)
                    self.columnconfigure(2,weight=1)
                if(botoes_ativosPS==2):
                    self.Mult3.destroy()
                    self.geometry("1000x700")
                    self.rowconfigure(0,weight=1)
                    self.rowconfigure(1,weight=10)
                    self.columnconfigure(0,weight=1)
                    self.columnconfigure(1,weight=1)
                    self.columnconfigure(2,weight=1)

        if(self.title()=='Oscilloscope'):
            botoes_ativosOscil=int(self.MultWindow3.get()) +int(self.SGWindow3.get())+int(self.PSWindow3.get())
            if(self.MultWindow3.get()==True):
                if(botoes_ativosOscil==1):
                    self.Oscil.destroy()
                    self.geometry("1000x700")
                    self.rowconfigure(0,weight=1)
                    self.columnconfigure(0,weight=1)
                    self.columnconfigure(1,weight=1)
                    self.columnconfigure(2,weight=1)
                    self.rowconfigure(1,weight=10)
                    self.Oscil=Oscilloscope(self)
                    self.Oscil.grid(row=1,column=0,columnspan=3,sticky="NSEW")
                    self.Mult4=Multimeter(self)
                    self.Mult4.grid(row=0,column=2,sticky='NSWE')
                   
                   
                if(botoes_ativosOscil==2):
                    
            
                    self.geometry("1000x700")
                    self.rowconfigure(0,weight=1)
                    self.columnconfigure(0,weight=1)
                    self.columnconfigure(1,weight=1)
                    self.columnconfigure(2,weight=1)
                    self.rowconfigure(1,weight=10)
                    self.Mult4=Multimeter(self)
                    self.Mult4.grid(row=0,column=2,sticky='NSWE')
                if(botoes_ativosOscil==3):
                    
                    self.Mult4=Multimeter(self)
                    self.geometry("1000x700")
                    self.rowconfigure(0,weight=1)
                    self.columnconfigure(0,weight=1)
                    self.columnconfigure(1,weight=1)
                    self.columnconfigure(2,weight=1)
                    self.rowconfigure(1,weight=10)
                    self.Mult4=Multimeter(self)
                    self.Mult4.grid(row=0,column=2,sticky='NSWE')
            if(self.MultWindow3.get()==False):
                if(botoes_ativosOscil==0):
                    self.Mult4.destroy()
                    self.Oscil.destroy()
                    self.geometry("1000x700")
                    self.rowconfigure(0,weight=1)
                    self.columnconfigure(0,weight=1)
                    self.columnconfigure(1,weight=1)
                    self.columnconfigure(2,weight=1)
                    self.rowconfigure(1,weight=10)
                    self.Oscil=Oscilloscope(self)
                    
                    self.Oscil.grid(row=0,column=0,rowspan=2,columnspan=3,sticky="NSWE")
                if(botoes_ativosOscil==1):
                    self.Mult4.destroy()
                    self.Oscil.destroy()
                    self.geometry("1000x700")
                    self.rowconfigure(0,weight=1)
                    self.columnconfigure(0,weight=1)
                    self.columnconfigure(1,weight=1)
                    self.columnconfigure(2,weight=1)
                    self.rowconfigure(1,weight=10)
                    self.Oscil=Oscilloscope(self)
                    self.Oscil.grid(row=1,column=0,columnspan=3,sticky="NSEW")
                    
                if(botoes_ativosOscil==2):
                    self.Mult4.destroy()
                    self.Oscil.destroy()
                    self.geometry("1000x700")
                    self.rowconfigure(0,weight=1)
                    self.columnconfigure(0,weight=1)
                    self.columnconfigure(1,weight=1)
                    self.columnconfigure(2,weight=1)
                    self.rowconfigure(1,weight=10)
                    self.Oscil=Oscilloscope(self)
                    self.Oscil.grid(row=1,column=0,columnspan=3,sticky="NSEW")

    def ShowOscilWindow(self):
        if(self.title()=='Power Supply'):
            
            botoes_ativosPS=int(self.OscilWindow3.get()) +int(self.SGWindow2.get())+int(self.MultWindow2.get())
            if(self.OscilWindow3.get()==True):
                if(botoes_ativosPS==1):
                    self.PS.destroy()
                    self.geometry("1000x700")
                    self.rowconfigure(0,weight=1)
                    self.columnconfigure(0,weight=1)
                    self.columnconfigure(1,weight=1)
                    self.columnconfigure(2,weight=1)
                    self.rowconfigure(1,weight=10)
                    self.Oscil2=Oscilloscope(self)
                    self.Oscil2.grid(row=1,column=0,columnspan=3,sticky="NSEW")
                    self.PS=PowerSupply(self)
                    self.PS.grid(row=0,column=0,sticky='NSWE')
                   
                if(botoes_ativosPS==2):
                    self.geometry("1000x700")
                    self.rowconfigure(0,weight=1)
                    self.columnconfigure(0,weight=1)
                    self.columnconfigure(1,weight=1)
                    self.columnconfigure(2,weight=1)
                    self.rowconfigure(1,weight=10)
                    self.Oscil2=Oscilloscope(self)
                    self.Oscil2.grid(row=1,column=0,columnspan=3,sticky="NSEW")
                if(botoes_ativosPS==3):
                    self.geometry("1000x700")
                    self.rowconfigure(0,weight=1)
                    self.columnconfigure(0,weight=1)
                    self.columnconfigure(1,weight=1)
                    self.columnconfigure(2,weight=1)
                    self.rowconfigure(1,weight=10)
                    self.Oscil2=Oscilloscope(self)
                    self.Oscil2.grid(row=1,column=0,columnspan=3,sticky="NSEW")
                
            if(self.OscilWindow3.get()==False):
                if(botoes_ativosPS==0):
                    self.geometry("300x300")
                    self.Oscil2.destroy()
                    self.rowconfigure(0,weight=1)
                    self.rowconfigure(1,weight=0)
                    self.columnconfigure(0,weight=1)
                    self.columnconfigure(1,weight=0)
                    self.columnconfigure(2,weight=0)
                if(botoes_ativosPS==1):
                    self.Oscil2.destroy()
                    self.geometry("600x300")
                    self.rowconfigure(0,weight=1)
                    self.rowconfigure(1,weight=0)
                    self.columnconfigure(0,weight=1)
                    self.columnconfigure(1,weight=1)
                    self.columnconfigure(2,weight=0)
                if(botoes_ativosPS==2):
                    self.Oscil2.destroy()
                    self.geometry("900x300")
                    self.rowconfigure(0,weight=1)
                    self.rowconfigure(1,weight=0)
                    self.columnconfigure(0,weight=1)
                    self.columnconfigure(1,weight=1)
                    self.columnconfigure(2,weight=1)



        if(self.title()=='Multimeter'):

            botoes_ativosMult=int(self.OscilWindow2.get()) +int(self.SGWindow1.get())+int(self.PSWindow2.get())
            if(self.OscilWindow2.get()==True):
                if(botoes_ativosMult==1):
                    self.Mult.destroy()
                    self.geometry("1000x700")
                    self.rowconfigure(0,weight=1)
                    self.columnconfigure(0,weight=1)
                    self.columnconfigure(1,weight=1)
                    self.columnconfigure(2,weight=1)
                    self.rowconfigure(1,weight=10)
                    self.Oscil3=Oscilloscope(self)
                    self.Oscil3.grid(row=1,column=0,columnspan=3,sticky="NSEW")
                    self.Mult=Multimeter(self)
                    self.Mult.grid(row=0,column=0,sticky='NSWE')
                   
                   
                if(botoes_ativosMult==2):
                    self.geometry("1000x700")
                    self.rowconfigure(0,weight=1)
                    self.columnconfigure(0,weight=1)
                    self.columnconfigure(1,weight=1)
                    self.columnconfigure(2,weight=1)
                    self.rowconfigure(1,weight=10)
                    self.Oscil3=Oscilloscope(self)
                    self.Oscil3.grid(row=1,column=0,columnspan=3,sticky="NSEW")
                if(botoes_ativosMult==3):
                    self.geometry("1000x700")
                    self.rowconfigure(0,weight=1)
                    self.columnconfigure(0,weight=1)
                    self.columnconfigure(1,weight=1)
                    self.columnconfigure(2,weight=1)
                    self.rowconfigure(1,weight=10)
                    self.Oscil3=Oscilloscope(self)
                    self.Oscil3.grid(row=1,column=0,columnspan=3,sticky="NSEW")
                
            
            if(self.OscilWindow2.get()==False):
                if(botoes_ativosMult==0):
                    self.geometry("300x300")
                    self.rowconfigure(0,weight=1)
                    self.rowconfigure(1,weight=0)
                    self.columnconfigure(0,weight=1)
                    self.columnconfigure(1,weight=0)
                    self.columnconfigure(2,weight=0)
                    self.Oscil3.destroy()
                if(botoes_ativosMult==1):
                    self.Oscil3.destroy()
                    self.geometry("600x300")
                    self.rowconfigure(0,weight=1)
                    self.rowconfigure(1,weight=0)
                    self.columnconfigure(0,weight=1)
                    self.columnconfigure(1,weight=1)
                    self.columnconfigure(2,weight=0)
                if(botoes_ativosMult==2):
                    self.Oscil3.destroy()
                    self.geometry("900x300")
                    self.rowconfigure(0,weight=1)
                    self.rowconfigure(1,weight=0)
                    self.columnconfigure(0,weight=1)
                    self.columnconfigure(1,weight=1)
                    self.columnconfigure(2,weight=1)

        if(self.title()=='Signal Generator'):   
            botoes_ativosSG=int(self.OscilWindow1.get()) +int(self.MultWindow1.get())+int(self.PSWindow1.get())
            if(self.OscilWindow1.get()==True):
                if(botoes_ativosSG==1):
                    self.SG.destroy()
                    self.geometry("1000x700")
                    self.rowconfigure(0,weight=1)
                    self.columnconfigure(0,weight=1)
                    self.columnconfigure(1,weight=1)
                    self.columnconfigure(2,weight=1)
                    self.rowconfigure(1,weight=10)
                    self.Oscil4=Oscilloscope(self)
                    self.Oscil4.grid(row=1,column=0,columnspan=3,sticky="NSEW")
                    self.SG=SignalGenerator(self)
                    self.SG.grid(row=0,column=0,sticky='NSWE')
                   
                if(botoes_ativosSG==2):
                    self.geometry("1000x700")
                    self.rowconfigure(0,weight=1)
                    self.columnconfigure(0,weight=1)
                    self.columnconfigure(1,weight=1)
                    self.columnconfigure(2,weight=1)
                    self.rowconfigure(1,weight=10)
                    self.Oscil4=Oscilloscope(self)
                    self.Oscil4.grid(row=1,column=0,columnspan=3,sticky="NSEW")
                if(botoes_ativosSG==3):
                    self.geometry("1000x700")
                    self.rowconfigure(0,weight=1)
                    self.columnconfigure(0,weight=1)
                    self.columnconfigure(1,weight=1)
                    self.columnconfigure(2,weight=1)
                    self.rowconfigure(1,weight=10)
                    self.Oscil4=Oscilloscope(self)
                    self.Oscil4.grid(row=1,column=0,columnspan=3,sticky="NSEW")
                
            
            if(self.OscilWindow1.get()==False):
                if(botoes_ativosSG==0):
                    self.geometry("300x300")
                    self.rowconfigure(0,weight=1)
                    self.rowconfigure(1,weight=0)
                    self.columnconfigure(0,weight=1)
                    self.columnconfigure(1,weight=0)
                    self.columnconfigure(2,weight=0)
                    self.Oscil4.destroy()
                if(botoes_ativosSG==1):
                    self.Oscil4.destroy()
                    self.geometry("600x300")
                    self.rowconfigure(0,weight=1)
                    self.rowconfigure(1,weight=0)
                    self.columnconfigure(0,weight=1)
                    self.columnconfigure(1,weight=1)
                    self.columnconfigure(2,weight=0)
                if(botoes_ativosSG==2):
                    self.Oscil4.destroy()
                    self.geometry("900x300")
                    self.rowconfigure(0,weight=1)
                    self.rowconfigure(1,weight=0)
                    self.columnconfigure(0,weight=1)
                    self.columnconfigure(1,weight=1)
                    self.columnconfigure(2,weight=1)

        