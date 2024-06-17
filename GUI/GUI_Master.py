from tkinter import *
from tkinter import ttk
import webbrowser
from PIL import Image, ImageTk
from tkinter import messagebox
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
import os
import sys

class RootGUI:
    def __init__(self,serial,data):
        self.root=Tk()
        self.root.title('PocketWave')
        self.root.iconbitmap(self.resource_path("Images\\Icon.ico"))
        self.root.resizable(False,False)
        self.Menu()
        self.centrar()
        self.AddBackground()
        self.add_buttons()
        self.serial=serial
        self.data=data
        self.root.protocol("WM_DELETE_WINDOW",self.close_window)

        self.SG_Count=0
        self.PS_Count=0
        self.Mult_Count=0  
        self.Oscil_Count=0

        
        self.SignalGenerator=[]
        
        self.PowerSupply= []
        
        self.Multimeter=[]
        
        self.Oscilloscope =[]

        self.SG_SHOW_Flag=False
        self.PS_SHOW_Flag=False
        self.Oscil_SHOW_Flag=False
        self.Mult_SHOW_Flag=False

    def resource_path(self,relative_path):
        try:
            base_path = sys._MEIPASS2
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)
    def close_window(self):
            self.serial.OscilloscopeThreadFlag=False
            self.serial.MultimeterThreadFlag=False
            self.serial.PSThreadFlag=False
            self.serial.SGThreadFlag=False
            self.root.destroy()
       
        
    def centrar(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        window_width = 800
        window_height = 700

        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.root.geometry(f'{window_width}x{window_height}+{x}+{y}')

    def Menu(self):
        #menu
        self.Menu=Menu(self.root)
        #sub-menu
        help_menu=Menu(self.Menu,tearoff=False)
        help_menu.add_command(label='User Manual',command=self.OpenUserGuide)
        self.Menu.add_cascade(label="Help",menu=help_menu)

        contacts_menu=Menu(self.Menu,tearoff=False)
        contacts_menu.add_command(label='Go to Pocketwave website',command=self.OpenWebSite)
        self.Menu.add_cascade(label="Contacts",menu=contacts_menu)
        self.root.configure(menu=self.Menu)
    def OpenUserGuide(self):
        self.document_path = self.resource_path('usermanual.pdf')
        if os.path.exists(self.document_path):
            # Open the specified document using the default application
            os.startfile(self.document_path)
        else:
            print(f"File not found: {self.document_path}") 

    def OpenWebSite(self):
        webbrowser.open_new("https://pocketwave.web.ua.pt/")

    def AddBackground(self):
        def stretch_image(event):
            width = event.width
            height = event.height
            self.bg1 = Image.open(self.resource_path("Images\\Background_Image.jpg"))
            self.resized_image = self.bg1.resize((width, height))
            self.new_bg = ImageTk.PhotoImage(self.resized_image)
            self.Canvas.create_image(0, 0, image=self.new_bg, anchor="nw")

        self.Canvas = Canvas(self.root)
        self.Canvas.pack(expand=True, fill='both')
        self.bg_img = ImageTk.PhotoImage(file=self.resource_path("Images\\Background_Image.jpg"))
            # Set Image in Canvas
        self.Canvas.bind('<Configure>', lambda event: stretch_image(event))
        self.Canvas.create_image(0, 0, image=self.bg_img, anchor="nw")

    def add_buttons(self):

        def create_button(image_path, text, command, row, col,):
            img = Image.open(self.resource_path(image_path))
            resized_img = img.resize((250, 100))
            tk_img = ImageTk.PhotoImage(resized_img)
            if(text== 'Oscilloscope'):
                self.Oscilloscopebutton = Button(self.Canvas, text=text, image=tk_img, command=command, compound=TOP,
                               font=("Helvetica", 12), bg="white", fg="black", relief=FLAT, highlightthickness=0,state="normal")
                self.Oscilloscopebutton.image = tk_img
                self.Canvas.create_window(col, row, anchor=NW, window=self.Oscilloscopebutton)
            elif(text== 'Multimeter'):
                self.Multimeterbutton = Button(self.Canvas, text=text, image=tk_img, command=command, compound=TOP,
                               font=("Helvetica", 12), bg="white", fg="black", relief=FLAT, highlightthickness=0,state="normal")
                self.Multimeterbutton.image = tk_img
                self.Canvas.create_window(col, row, anchor=NW, window=self.Multimeterbutton)
            elif(text== 'Power Supply'):
                self.PSbutton = Button(self.Canvas, text=text, image=tk_img, command=command, compound=TOP,
                               font=("Helvetica", 12), bg="white", fg="black", relief=FLAT, highlightthickness=0,state="normal")
                self.PSbutton.image = tk_img
                self.Canvas.create_window(col, row, anchor=NW, window= self.PSbutton)
            else:
                self.SGbutton = Button(self.Canvas, text=text, image=tk_img, command=command, compound=TOP,
                               font=("Helvetica", 12), bg="white", fg="black", relief=FLAT, highlightthickness=0,state="normal")
                self.SGbutton.image = tk_img
                self.Canvas.create_window(col, row, anchor=NW, window=self.SGbutton)
        def create_connect_disconnect_button( text, command, row, col):  
            self.CDbutton = Button(self.Canvas, text=text,  command=command, compound=TOP,
                               font=("Helvetica", 12), bg="white", fg="black", relief=FLAT, highlightthickness=0)
            self.CDbutton_window=self.Canvas.create_window(col, row, anchor=NW, window=self.CDbutton )

        create_connect_disconnect_button('Connect STM',self.Connect_DisconnectSTM,360,350)
        create_button('Images\\Oscilloscope.png', 'Oscilloscope', self.open_Oscil_window, 400, 100)
        create_button('Images\\Multimeter.png', 'Multimeter', self.open_Mult_window, 550, 100)
        create_button('Images\\PowerSupply.png', 'Power Supply', self.open_PS_window, 400, 450)
        create_button('Images\\SignalGenerator.png', 'Signal Generator', self.open_SG_window , 550, 450)

    def Connect_DisconnectSTM(self):
        if self.CDbutton.cget('text') == "Connect STM" :
            self.serial.SerialOpen(self) 
            #try:
            #    if self.serial.ser.is_open:
            #        self.serial.Receive=threading.Thread(target=self.serial.Serial_Receive,args=(), daemon=True)
            #        self.serial.Receive.start()
            #except:
            #    pass

        else:
            self.serial.Receive_Thread=False
            self.serial.SerialClose()
            self.CDbutton.config(text="Connect STM")
            self.Canvas.coords(self.CDbutton_window,350,360)
                
    def open_SG_window(self):
        print('SignalGenerator')
        self.SG_Count +=1
        signalgenerator= SignalGenerator(self,self.data,self.serial)
        self.SignalGenerator.append( signalgenerator )
        
    def open_PS_window(self):
        print('PowerSupply')
        self.PS_Count +=1
        powersupply= PowerSupply(  self,self.data,self.serial)
        self.PowerSupply.append( powersupply )
        
    def open_Mult_window(self):
        print('Multimeter')
        self.Mult_Count +=1
        
        multimeter= Multimeter (self,self.data,self.serial )
        self.Multimeter.append ( multimeter )
        
    def open_Oscil_window(self):
        print('Oscilloscope')
        self.Oscil_Count +=1
        oscilloscope=Oscilloscope(self,self.data,self.serial)
        self.Oscilloscope.append( oscilloscope )
          
class Multimeter:
    def __init__(self,GUI,data,serial):
        self.GUI=GUI
        self.data=data
        self.serial=serial
        self.indice=self.GUI.Mult_Count -1
        if(self.GUI.Mult_SHOW_Flag==False):
            self.window=Toplevel()
            self.window.title("Multimeter")
            self.window.geometry("300x300")
            self.window.iconbitmap(self.resource_path("Images/Icon.ico"))
            self.window.resizable(True,True)
            self.Menu()
            self.Frame=LabelFrame(self.window)
            self.Frame.place(relheight=1,relwidth=1)
            self.layout()
            self.window.protocol("WM_DELETE_WINDOW",lambda: self.close_Mult_window(self.window))
        else:
            self.Frame=None

    def resource_path(self,relative_path):
        try:
            base_path = sys._MEIPASS2
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    def close_Mult_window(self,window):
        if(self.Show_PS_control.get()==True):
            if(len(self.GUI.PowerSupply)==1):
                self.serial.PSThreadFlag=False
            self.GUI.PowerSupply.pop(self.PS.indice)
            self.GUI.PS_Count-=1
            if(self.PS.indice < len(self.GUI.PowerSupply)):
                    for i in range(self.PS.indice,len(self.GUI.PowerSupply)):
                        self.GUI.PowerSupply[i].indice-=1 
        if(self.Show_SG_control.get()==True):
            if(len(self.GUI.SignalGenerator)==1):
                self.serial.SGThreadFlag=False
            self.GUI.SignalGenerator.pop(self.SG.indice)
            self.GUI.SG_Count-=1
            if(self.SG.indice < len(self.GUI.SignalGenerator)):
                    for i in range(self.SG.indice,len(self.GUI.SignalGenerator)):
                        self.GUI.SignalGenerator[i].indice-=1 
        if(self.Show_Oscil_control.get()==True):
            if(len(self.GUI.Oscilloscope)==1):
                self.serial.OscilloscopeThreadFlag=False
            self.GUI.Oscilloscope.pop(self.Oscil.indice)
            self.GUI.Oscil_Count-=1
            if(self.Oscil.indice < len(self.GUI.Oscilloscope)):
                    for i in range(self.Oscil.indice,len(self.GUI.Oscilloscope)):
                        self.GUI.Oscilloscope[i].indice-=1
         
        if(len(self.GUI.Multimeter)==1):
            try:
                self.serial.MultimeterThreadFlag=False
                window.destroy()
                self.GUI.Multimeter.pop(0)        
            except Exception as e:
                print(e)  
                     
        else:
            try:
                window.destroy()
                self.GUI.Multimeter.pop(self.indice)
                if(self.indice < len(self.GUI.Multimeter)):
                    for i in range(self.indice,len(self.GUI.Multimeter)):
                        self.GUI.Multimeter[i].indice-=1
            except Exception as e:
                print(e) 
        self.GUI.Mult_Count -=1
         
    def Menu(self):
        self.Menu=Menu(self.window)
        self.Show_menu=Menu(self.Menu,tearoff=False)
        self.Show_SG_control=BooleanVar()
        self.Show_Oscil_control=BooleanVar()
        self.Show_PS_control=BooleanVar()
        self.Show_menu.add_checkbutton(label="Show Oscilloscope",command=self.Show_Oscil,variable=self.Show_Oscil_control)
        self.Show_menu.add_checkbutton(label="Show Signal Generator",command=self.Show_SG,variable=self.Show_SG_control)
        self.Show_menu.add_checkbutton(label="Show Power Supply",command=self.Show_PS,variable=self.Show_PS_control)
        self.Menu.add_cascade(label="Show...",menu=self.Show_menu)

        help_menu=Menu(self.Menu,tearoff=False)
        help_menu.add_command(label='User Manual',command=self.OpenUserGuide)
        self.Menu.add_cascade(label="Help",menu=help_menu)

        contacts_menu=Menu(self.Menu,tearoff=False)
        contacts_menu.add_command(label='Go to Pocketwave website',command=self.OpenWebSite)
        self.Menu.add_cascade(label="Contacts",menu=contacts_menu)
        self.window.configure(menu=self.Menu)    

    def OpenUserGuide(self):
        self.document_path = self.resource_path('usermanual.pdf')
    
        if os.path.exists(self.document_path):
            os.startfile(self.document_path)
        else:
            print(f"File not found: {self.document_path}") 

    def layout(self):

        #Connect button 
        img = Image.open(self.resource_path('Images/BotaoOff.png'))
        resized_img = img.resize((40, 20))
        self.Botao_Off_Image = ImageTk.PhotoImage(resized_img)
        img = Image.open(self.resource_path('Images/BotaoOn.png'))
        resized_img = img.resize((40, 20))
        self.Botao_On_Image = ImageTk.PhotoImage(resized_img)
        if(self.serial.MultimeterThreadFlag==True):
            self.connect_button = Button(self.Frame,image=self.Botao_On_Image,
                                    command=self.Start_Stop_Multimeter, state="normal")
            self.connect_button.place(relx=0.85,rely=0)
        else:
             self.connect_button = Button(self.Frame,image=self.Botao_Off_Image,
                                    command=self.Start_Stop_Multimeter, state="normal")
             self.connect_button.place(relx=0.85,rely=0)
            
        #label
        label_Title = Label(self.Frame, text="Multimeter:",font=("Helvetica", 20))
        label_Title.pack()

        label1 = Label(self.Frame, text="Choose one of the multimeter's measuring options", font=("Helvetica", 9))
        label1.pack(side='top')

        #NOTEBOOK
        notebook=ttk.Notebook(self.Frame)
        notebook.pack()
        tab1=ttk.Frame(notebook)#VOLTAGE
        self.label_tensao=ttk.Label(tab1,text=f'V: ',font=("Helvetica", 20))
        self.label_tensao.pack(side='bottom')

        tab2=ttk.Frame(notebook)#CURRENT
        self.label_current=ttk.Label(tab2,text=f'I: ',font=("Helvetica", 20))
        self.label_current.pack(side='bottom')

        tab3=ttk.Frame(notebook)#RESISTANCE
        self.label_resistance=ttk.Label(tab3,text=f'R: ',font=("Helvetica", 20))
        self.label_resistance.pack(side='bottom')


        tab4=ttk.Frame(notebook)#CAPACITANCE
        self.label_capacitance=ttk.Label(tab4,text=f'C: ',font=("Helvetica", 20))
        self.label_capacitance.pack(side='bottom')


        notebook.add(tab1,text= 'Voltage')  
        notebook.add(tab2,text= 'Current')
        notebook.add(tab3,text= 'Resistance')
        notebook.add(tab4,text= 'Capacitance')
     
    def Show_SG(self):
        self.active_windows=int(self.Show_SG_control.get())+int(self.Show_Oscil_control.get())+int(self.Show_PS_control.get())
        if(self.Show_SG_control.get()==True):
            self.GUI.SG_Count +=1
            self.GUI.SG_SHOW_Flag=True
            self.SG=SignalGenerator(self.GUI,self.data,self.serial)
            self.GUI.SignalGenerator.append(self.SG)
            self.GUI.SG_SHOW_Flag=False
            self.SG.Frame=LabelFrame(master=self.window)
            if(self.active_windows==1):
                for widget in self.Frame.winfo_children():
                    widget.destroy()
                self.window.geometry("700x300")  
                self.window.rowconfigure(0,weight=1)
                self.window.rowconfigure(1,weight=0)
                self.window.columnconfigure(0,weight=1)
                self.window.columnconfigure(1,weight=1)
                self.window.columnconfigure(2,weight=0)
                self.SG.Frame.grid(row=0,column=1,sticky='nswe',padx=5,pady=5)
                self.SG.layout()
                self.Frame.grid(row=0,column=0,sticky='nswe',padx=5,pady=5)
                self.layout()
                
            elif(self.active_windows==2 and self.Show_Oscil_control.get()==False):
                self.window.geometry("900x300")  
                self.window.rowconfigure(0,weight=1)
                self.window.rowconfigure(1,weight=0)
                self.window.columnconfigure(0,weight=1)
                self.window.columnconfigure(1,weight=1)
                self.window.columnconfigure(2,weight=1)
                self.SG.Frame.grid(row=0,column=2,sticky='nswe',padx=5,pady=5)
                self.SG.layout()
            elif(self.active_windows==2 and self.Show_Oscil_control.get()==True):
                self.SG.Frame.grid(row=0,column=0,sticky='nswe',padx=5,pady=5)
                self.SG.layout()
            else:
                self.SG.Frame.grid(row=0,column=2,sticky='nswe',padx=5,pady=5)
                self.SG.layout()    
   
        else:
            self.GUI.SignalGenerator.pop(self.SG.indice)
            self.GUI.SG_Count -=1
            for widget in self.SG.Frame.winfo_children():
                widget.destroy()    
            self.SG.Frame.destroy()   
            if(self.SG.indice < len(self.GUI.SignalGenerator)):
                for i in range(self.SG.indice,len(self.GUI.SignalGenerator)):
                        self.GUI.SignalGenerator[i].indice-=1
            if(len(self.GUI.SignalGenerator)==0):
                self.serial.SGThreadFlag=False
            if(self.active_windows==0):
                self.window.geometry("300x300")
                self.window.rowconfigure(0,weight=1)
                self.window.rowconfigure(1,weight=0)
                self.window.columnconfigure(0,weight=1)
                self.window.columnconfigure(1,weight=0)
                self.window.columnconfigure(2,weight=0)
                self.Frame.grid(row=0,column=0,sticky="nswe")
            elif(self.active_windows==1 and self.Show_Oscil_control.get()==False):
                self.window.geometry("700x300")
                self.window.rowconfigure(0,weight=1)
                self.window.rowconfigure(1,weight=0)
                self.window.columnconfigure(0,weight=1)
                self.window.columnconfigure(1,weight=1)
                self.window.columnconfigure(2,weight=0)
                for widget in self.Frame.winfo_children():
                     widget.destroy()
                self.Frame.grid(row=0,column=0,sticky='nswe',padx=5,pady=5)
                self.layout()
                for widget in self.PS.Frame.winfo_children():
                    widget.destroy()
                self.PS.Frame.grid(row=0,column=1,sticky='nswe',padx=5,pady=5)
                self.PS.layout()
            elif(self.active_windows==1 and self.Show_Oscil_control.get()==True):
                for widget in self.Frame.winfo_children():
                     widget.destroy()
                self.Frame.grid(row=0,column=1,sticky='nswe',padx=5,pady=5)
                self.layout()
            else:
                for widget in self.Frame.winfo_children():
                     widget.destroy()
                self.Frame.grid(row=0,column=0,sticky='nswe',padx=5,pady=5)
                self.layout()

                for widget in self.PS.Frame.winfo_children():
                     widget.destroy()
                self.PS.Frame.grid(row=0,column=1,sticky='nswe',padx=5,pady=5)
                self.PS.layout()

    def Show_Oscil(self):
        self.active_windows=int(self.Show_Oscil_control.get())+int(self.Show_SG_control.get())+int(self.Show_PS_control.get())
        if(self.Show_Oscil_control.get()==True):
            self.GUI.Oscil_Count+=1
            self.GUI.Oscil_SHOW_Flag=True
            self.Oscil=Oscilloscope(self.GUI,self.data,self.serial)
            self.GUI.Oscilloscope.append(self.Oscil)
            self.GUI.Oscil_SHOW_Flag=False
            self.Oscil.Frame=LabelFrame(master=self.window)
            self.window.geometry("1200x800")  
            self.window.rowconfigure(0,weight=1)
            self.window.columnconfigure(0,weight=1)
            self.window.columnconfigure(1,weight=1)
            self.window.columnconfigure(2,weight=1)
            self.window.rowconfigure(1,weight=20)
            if(self.active_windows==1 ):
                for widget in self.Frame.winfo_children():
                    widget.destroy()
                self.Oscil.Frame.grid(row=1,column=0,columnspan=3,sticky='nswe',padx=5,pady=5)
                self.Oscil.CreateBackground()
                self.Frame.grid(row=0,column=1,columnspan=1,rowspan=1,sticky='nswe',padx=5,pady=5)
                self.layout()
            elif(self.active_windows==2):
                self.Oscil.Frame.grid(row=1,column=0,columnspan=3,sticky='nswe',padx=5,pady=5)
                self.Oscil.CreateBackground()
            else:
                self.Oscil.Frame.grid(row=1,column=0,columnspan=3,sticky='nswe',padx=5,pady=5)
                self.Oscil.CreateBackground()
        else:
            self.GUI.Oscilloscope.pop(self.Oscil.indice)
            self.GUI.Oscil_Count-=1  
            if(len(self.GUI.Oscilloscope)==0):
                self.serial.OscilloscopeThreadFlag=False
            if(self.Oscil.indice < len(self.GUI.Oscilloscope)):
                for i in range(self.Oscil.indice,len(self.GUI.Oscilloscope)):
                        self.GUI.Oscilloscope[i].indice-=1
            self.window.rowconfigure(1,weight=0)
            for widget in self.Oscil.Frame.winfo_children():
                    widget.destroy()
            self.Oscil.Frame.destroy()

            if(self.active_windows==0):
                self.window.geometry("300x300")
                for widget in self.Frame.winfo_children():
                    widget.destroy()
                self.Frame.grid(column=0,row=0,rowspan=2,columnspan=3,sticky="nswe",padx=5,pady=5)
                self.layout()
            elif(self.active_windows==1):
                self.window.geometry("700x300")
                self.window.columnconfigure(2,weight=0)
                if( self.Show_PS_control.get() == True):
                    for widget in self.Frame.winfo_children():
                        widget.destroy()
                    self.Frame.grid(column=0,row=0,columnspan=1,sticky="nswe",padx=5,pady=5)
                    self.layout()    
                    for widget in self.PS.Frame.winfo_children():
                        widget.destroy()
                    self.PS.Frame.grid(column=1,row=0,columnspan=1,sticky="nswe",padx=5,pady=5)
                    self.PS.layout()
                else:
                    for widget in self.Frame.winfo_children():
                        widget.destroy()
                    self.Frame.grid(column=0,row=0,columnspan=1,sticky="nswe",padx=5,pady=5)
                    self.layout()    
                    for widget in self.SG.Frame.winfo_children():
                        widget.destroy()
                    self.SG.Frame.grid(column=1,row=0,columnspan=1,sticky="nswe",padx=5,pady=5)
                    self.SG.layout()
            else:
                self.window.geometry("900x300")
                self.window.rowconfigure(1,weight=0)

    def Show_PS(self):
        self.active_windows=int(self.Show_Oscil_control.get())+int(self.Show_PS_control.get())+int(self.Show_SG_control.get())
        if(self.Show_PS_control.get()==True):
            self.GUI.PS_Count+=1
            self.GUI.PS_SHOW_Flag=True
            self.PS=PowerSupply(self.GUI,self.data,self.serial)
            self.GUI.PowerSupply.append(self.PS)
            self.GUI.PS_SHOW_Flag=False
            self.PS.Frame=LabelFrame(master=self.window)
            if(self.active_windows==1 ):
                for widget in self.Frame.winfo_children():
                    widget.destroy()
                self.window.geometry("700x300")  
                self.window.rowconfigure(0,weight=1)
                self.window.rowconfigure(1,weight=0)
                self.window.columnconfigure(0,weight=1)
                self.window.columnconfigure(1,weight=1)
                self.window.columnconfigure(2,weight=0)
                self.PS.Frame.grid(row=0,column=1,sticky='nswe',padx=5,pady=5)
                self.PS.layout()
                self.Frame.grid(row=0,column=0,sticky='nswe',padx=5,pady=5)
                self.layout()
            elif(self.active_windows==2 and self.Show_Oscil_control.get()==False):
                self.window.geometry("900x300")  
                self.window.rowconfigure(0,weight=1)
                self.window.rowconfigure(1,weight=0)
                self.window.columnconfigure(0,weight=1)
                self.window.columnconfigure(1,weight=1)
                self.window.columnconfigure(2,weight=1)
                self.PS.Frame.grid(row=0,column=2,sticky='nswe',padx=5,pady=5)
                self.PS.layout()
            elif(self.active_windows==2 and self.Show_Oscil_control.get()==True):
                self.PS.Frame.grid(row=0,column=0,sticky='nswe',padx=5,pady=5)
                self.PS.layout()
            else:
                self.PS.Frame.grid(row=0,column=2,sticky='nswe',padx=5,pady=5)
                self.PS.layout()
        else:
            self.GUI.PowerSupply.pop(self.PS.indice)
            self.GUI.PS_Count -=1
            for widget in self.PS.Frame.winfo_children():
                widget.destroy()    
            self.PS.Frame.destroy()  
            if(self.PS.indice < len(self.GUI.PowerSupply)):
                for i in range(self.PS.indice,len(self.GUI.PowerSupply)):
                        self.GUI.PowerSupply[i].indice-=1
            if(len(self.GUI.PowerSupply)==0):
                self.serial.PSThreadFlag=False
            if(self.active_windows==0):
                self.window.geometry("300x300")
                self.window.rowconfigure(0,weight=1)
                self.window.rowconfigure(1,weight=0)
                self.window.columnconfigure(0,weight=1)
                self.window.columnconfigure(1,weight=0)
                self.window.columnconfigure(2,weight=0)
                self.Frame.grid(row=0,column=0,sticky="nswe")
            elif(self.active_windows==1 and self.Show_Oscil_control.get()==False ):
                self.window.geometry("600x300")
                self.window.rowconfigure(0,weight=1)
                self.window.rowconfigure(1,weight=0)
                self.window.columnconfigure(0,weight=1)
                self.window.columnconfigure(1,weight=1)
                self.window.columnconfigure(2,weight=0)
                for widget in self.Frame.winfo_children():
                     widget.destroy()
                self.Frame.grid(row=0,column=0,sticky='nswe',padx=5,pady=5)
                self.layout()
                for widget in self.SG.Frame.winfo_children():
                    widget.destroy()
                self.SG.Frame.grid(row=0,column=1,sticky='nswe',padx=5,pady=5)
                self.SG.layout()
            elif(self.active_windows==1 and self.Show_Oscil_control.get()==True):
                for widget in self.Frame.winfo_children():
                     widget.destroy()
                self.Frame.grid(row=0,column=1,sticky='nswe',padx=5,pady=5)
                self.layout()
            else:
                for widget in self.Frame.winfo_children():
                     widget.destroy()
                self.Frame.grid(row=0,column=0,sticky='nswe',padx=5,pady=5)
                self.layout()

                for widget in self.SG.Frame.winfo_children():
                     widget.destroy()
                self.SG.Frame.grid(row=0,column=1,sticky='nswe',padx=5,pady=5)
                self.SG.layout()

    def OpenWebSite(self):
        webbrowser.open_new("https://pocketwave.web.ua.pt/")
        
    def Start_Stop_Multimeter(self):
            
        if(self.GUI.Mult_Count==1 and self.serial.MultimeterThreadFlag==False ):
            try:       
                    img = Image.open(self.resource_path('Images/BotaoOn.png'))
                    resized_img = img.resize((40, 20))
                    self.Botao_On_Image = ImageTk.PhotoImage(resized_img)
                                                                                                                                       
                    self.serial.MultimeterThread=threading.Thread(target=self.serial.SerialMultimeterData,args=(self.GUI,), daemon=True)
                    self.serial.MultimeterThread.start()
                    self.connect_button.config(image= self.Botao_On_Image)
            except Exception as e:
                print(e)   
                
        elif(self.GUI.Mult_Count==1 and self.serial.MultimeterThreadFlag==True):
            try:
                img = Image.open(self.resource_path('Images/BotaoOff.png'))
                resized_img = img.resize((40, 20))
                self.Botao_Off_Image = ImageTk.PhotoImage(resized_img)
                self.serial.MultimeterThreadFlag=False
                self.connect_button.config(image= self.Botao_Off_Image)
                    
            except Exception as e:
                print(e)
            
        elif(self.GUI.Mult_Count!=1 and self.serial.MultimeterThreadFlag==False):
            try:
                img = Image.open(self.resource_path('Images/BotaoOn.png'))
                resized_img = img.resize((40, 20))
                self.Botao_On_Image = ImageTk.PhotoImage(resized_img)
                self.serial.MultimeterThread=threading.Thread(target=self.serial.SerialMultimeterData,args=(self.GUI,), daemon=True)
                self.serial.MultimeterThread.start()
                for i in range(len(self.GUI.Multimeter)):
                    self.GUI.Multimeter[i].connect_button.config(image=self.GUI.Multimeter[i].Botao_On_Image)
            except Exception as e:
                print(e)
                
        elif(self.GUI.Mult_Count!=1 and self.serial.MultimeterThreadFlag==True):
            try:
                img = Image.open(self.resource_path('Images/BotaoOff.png'))
                resized_img = img.resize((40, 20))
                self.Botao_Off_Image = ImageTk.PhotoImage(resized_img)
                self.serial.MultimeterThreadFlag=False
                for i in range(len(self.GUI.Multimeter)):
                    self.GUI.Multimeter[i].connect_button.config(image=self.GUI.Multimeter[i].Botao_Off_Image)  
            except Exception as e:
                print(e) 
        else:
                print("\n")

class Oscilloscope:
    def __init__(self,GUI,data,serial):
        self.GUI=GUI
        self.indice=self.GUI.Oscil_Count -1
        self.data=data
        self.serial=serial   
        self.data_array = []
        if(self.GUI.Oscil_SHOW_Flag==False):
            self.window=Toplevel()
            self.window.title("Oscilloscope")
            self.window.geometry("1000x500")
            self.window.iconbitmap(self.resource_path("Images\\Icon.ico"))
            self.window.resizable(True,True)
            self.Frame=LabelFrame(self.window,bg='light gray')
            self.Frame.place(relheight=1,relwidth=1)
            self.Menu()
            self.CreateBackground()
            self.window.protocol("WM_DELETE_WINDOW",lambda: self.close_Oscil_window(self.window))

        else:
            self.Frame=None

    def resource_path(self,relative_path):
        try:
            base_path = sys._MEIPASS2
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    def close_Oscil_window(self,window):
        if(self.Show_Mult_control.get()==True):
            if(len(self.GUI.Multimeter)==1):
                self.serial.MultimeterThreadFlag=False
            self.GUI.Multimeter.pop(self.Mult.indice)
            self.GUI.Mult_Count-=1
            if(self.Mult.indice < len(self.GUI.Multimeter)):
                    for i in range(self.Mult.indice,len(self.GUI.Multimeter)):
                        self.GUI.Multimeter[i].indice-=1 
        if(self.Show_PS_control.get()==True):
            if(len(self.GUI.PowerSupply)==1):
                self.serial.PSThreadFlag=False
            self.GUI.PowerSupply.pop(self.PS.indice)
            self.GUI.PS_Count-=1
            if(self.PS.indice < len(self.GUI.PowerSupply)):
                    for i in range(self.PS.indice,len(self.GUI.PowerSupply)):
                        self.GUI.PowerSupply[i].indice-=1 
        if(self.Show_SG_control.get()==True):
            if(len(self.GUI.SignalGenerator)==1):
                self.serial.SGThreadFlag=False
            self.GUI.SignalGenerator.pop(self.SG.indice)
            self.GUI.SG_Count-=1
            if(self.SG.indice < len(self.GUI.SignalGenerator)):
                    for i in range(self.SG.indice,len(self.GUI.SignalGenerator)):
                        self.GUI.SignalGenerator[i].indice-=1 
        if(len(self.GUI.Oscilloscope)==1):
            try:
                self.serial.OscilloscopeThreadFlag=False 
                window.destroy()
                self.GUI.Oscilloscope.pop(0)  
            except Exception as e:
                print(e)
            
        else:
            try:
                window.destroy()
                self.GUI.Oscilloscope.pop(self.indice)    
                if(self.indice < len(self.GUI.Oscilloscope)):
                    for i in range(self.indice,len(self.GUI.Oscilloscope)):
                        self.GUI.Oscilloscope[i].indice-=1 
            except Exception as e:
                print(e)   
                
        self.GUI.Oscil_Count -=1

    def Menu(self):
        self.Menu=Menu(self.window)
        self.Show_menu=Menu(self.Menu,tearoff=False)
        self.Show_SG_control=BooleanVar()
        self.Show_Mult_control=BooleanVar()
        self.Show_PS_control=BooleanVar()
        self.Show_menu.add_checkbutton(label="Show Signal Generator",command=self.Show_SG,variable=self.Show_SG_control)
        self.Show_menu.add_checkbutton(label="Show Multimeter",command=self.Show_Mult,variable=self.Show_Mult_control)
        self.Show_menu.add_checkbutton(label="Show Power Supply",command=self.Show_PS,variable=self.Show_PS_control)
        self.Menu.add_cascade(label="Show...",menu=self.Show_menu)

        help_menu=Menu(self.Menu,tearoff=False)
        help_menu.add_command(label='User Manual',command=self.OpenUserGuide)
        self.Menu.add_cascade(label="Help",menu=help_menu)

        contacts_menu=Menu(self.Menu,tearoff=False)
        contacts_menu.add_command(label='Go to Pocketwave website',command=self.OpenWebSite)
        self.Menu.add_cascade(label="Contacts",menu=contacts_menu)
        self.window.configure(menu=self.Menu)
    def OpenUserGuide(self):
        self.document_path = self.resource_path('usermanual.pdf')
        if os.path.exists(self.document_path):
            # Open the specified document using the default application
            os.startfile(self.document_path)
        else:
            print(f"File not found: {self.document_path}") 

    def Show_SG(self):
        self.active_windows=int(self.Show_SG_control.get())+int(self.Show_PS_control.get())+int(self.Show_Mult_control.get())
        if(self.Show_SG_control.get()==True):
            self.GUI.SG_Count +=1
            self.GUI.SG_SHOW_Flag=True
            self.SG=SignalGenerator(self.GUI,self.data,self.serial)
            self.GUI.SignalGenerator.append(self.SG)
            self.GUI.SG_SHOW_Flag=False
            self.SG.Frame=LabelFrame(master=self.window)
            self.window.geometry("1200x800")  
            self.window.rowconfigure(0,weight=1)
            self.window.columnconfigure(0,weight=1)
            self.window.columnconfigure(1,weight=1)
            self.window.columnconfigure(2,weight=1)
            self.window.rowconfigure(1,weight=20)
            
            if(self.active_windows==1):
                for widget in self.Frame.winfo_children():
                    widget.destroy()
                self.SG.Frame.grid(row=0,column=1,sticky='nswe',padx=5,pady=5)
                self.SG.layout()
                self.Frame.grid(row=1,column=0,columnspan=3,sticky='nswe',padx=5,pady=5)
                self.CreateBackground()
                
            elif(self.active_windows==2):
                self.SG.Frame.grid(row=0,column=0,sticky='nswe',padx=5,pady=5)
                self.SG.layout()
            else:
                self.SG.Frame.grid(row=0,column=2,sticky='nswe',padx=5,pady=5)
                self.SG.layout()     

             
        else:
            self.GUI.SignalGenerator.pop(self.SG.indice)
            self.GUI.SG_Count -=1
            for widget in self.SG.Frame.winfo_children():
                widget.destroy()    
            self.SG.Frame.destroy()   
            if(self.SG.indice < len(self.GUI.SignalGenerator)):
                for i in range(self.SG.indice,len(self.GUI.SignalGenerator)):
                        self.GUI.SignalGenerator[i].indice-=1
            if(len(self.GUI.SignalGenerator)==0):
                self.serial.SGThreadFlag=False
            if(self.active_windows==0):
                self.window.geometry("1000x500")
                self.Frame.grid(row=0,column=0,rowspan=2,columnspan=3,sticky="nswe")
            elif(self.active_windows==1):
                if(self.Show_PS_control.get()==True):
                    for widget in self.PS.Frame.winfo_children():
                        widget.destroy()
                    self.PS.Frame.grid(row=0,column=1,sticky='nswe',padx=5,pady=5)
                    self.PS.layout()
                else:
                    for widget in self.Mult.Frame.winfo_children():
                        widget.destroy()
                    self.Mult.Frame.grid(row=0,column=1,sticky='nswe',padx=5,pady=5)
                    self.Mult.layout()
            else:
                for widget in self.PS.Frame.winfo_children():
                     widget.destroy()
                self.PS.Frame.grid(row=0,column=0,sticky='nswe',padx=5,pady=5)
                self.PS.layout()

                for widget in self.Mult.Frame.winfo_children():
                     widget.destroy()
                self.Mult.Frame.grid(row=0,column=1,sticky='nswe',padx=5,pady=5)
                self.Mult.layout()
                         
    def Show_Mult(self):
        self.active_windows=int(self.Show_SG_control.get())+int(self.Show_PS_control.get())+int(self.Show_Mult_control.get())
        if(self.Show_Mult_control.get()==True):
            self.GUI.Mult_SHOW_Flag=True
            self.GUI.Mult_Count+=1
            self.Mult=Multimeter(self.GUI,self.data,self.serial)
            self.GUI.Multimeter.append(self.Mult)
            self.GUI.Mult_SHOW_Flag=False
            self.Mult.Frame=LabelFrame(master=self.window)
            self.window.geometry("1200x800")  
            self.window.rowconfigure(0,weight=1)
            self.window.columnconfigure(0,weight=1)
            self.window.columnconfigure(1,weight=1)
            self.window.columnconfigure(2,weight=1)
            self.window.rowconfigure(1,weight=20)
            if(self.active_windows==1):
                for widget in self.Frame.winfo_children():
                    widget.destroy()
                self.Mult.Frame.grid(row=0,column=1,sticky='nswe',padx=5,pady=5)
                self.Mult.layout()
                self.Frame.grid(row=1,column=0,columnspan=3,sticky='nswe',padx=5,pady=5)
                self.CreateBackground()
            elif(self.active_windows==2):
                self.Mult.Frame.grid(row=0,column=0,sticky='nswe',padx=5,pady=5)
                self.Mult.layout()
            else:
                self.Mult.Frame.grid(row=0,column=2,sticky='nswe',padx=5,pady=5)
                self.Mult.layout() 
             
        else:
            self.GUI.Multimeter.pop(self.Mult.indice)
            self.GUI.Mult_Count-=1        
            for widget in self.Mult.Frame.winfo_children():
                widget.destroy()    
            self.Mult.Frame.destroy()
            if(self.Mult.indice < len(self.GUI.Multimeter)):
                for i in range(self.Mult.indice,len(self.GUI.Multimeter)):
                        self.GUI.Multimeter[i].indice-=1
            if(len(self.GUI.Multimeter)==0):
                self.serial.MultimeterThreadFlag=False
            if(self.active_windows==0):
                self.window.geometry("1000x500")
                self.Frame.grid(row=0,column=0,rowspan=2,columnspan=3,sticky="nswe")
            elif(self.active_windows==1):
                if(self.Show_SG_control.get()==True):
                    for widget in self.SG.Frame.winfo_children():
                        widget.destroy()
                    self.SG.Frame.grid(row=0,column=1,sticky='nswe',padx=5,pady=5)
                    self.SG.layout()
                else:
                    for widget in self.PS.Frame.winfo_children():
                        widget.destroy()
                    self.PS.Frame.grid(row=0,column=1,sticky='nswe',padx=5,pady=5)
                    self.PS.layout()
            else:
                for widget in self.SG.Frame.winfo_children():
                     widget.destroy()
                self.SG.Frame.grid(row=0,column=0,sticky='nswe',padx=5,pady=5)
                self.SG.layout()

                for widget in self.PS.Frame.winfo_children():
                     widget.destroy()
                self.PS.Frame.grid(row=0,column=1,sticky='nswe',padx=5,pady=5)
                self.PS.layout()

    def Show_PS(self):
        self.active_windows=int(self.Show_SG_control.get())+int(self.Show_PS_control.get())+int(self.Show_Mult_control.get())
        if(self.Show_PS_control.get()==True):
            self.GUI.PS_Count+=1
            self.GUI.PS_SHOW_Flag=True
            self.PS=PowerSupply(self.GUI,self.data,self.serial)
            self.GUI.PowerSupply.append(self.PS)
            self.GUI.PS_SHOW_Flag=False
            self.PS.Frame=LabelFrame(master=self.window)
            self.window.geometry("1200x800")  
            self.window.rowconfigure(0,weight=1)
            self.window.columnconfigure(0,weight=1)
            self.window.columnconfigure(1,weight=1)
            self.window.columnconfigure(2,weight=1)
            self.window.rowconfigure(1,weight=20)
        
            if(self.active_windows==1):
                for widget in self.Frame.winfo_children():
                    widget.destroy()
                self.PS.Frame.grid(row=0,column=1,sticky='nswe',padx=5,pady=5)
                self.PS.layout()
                self.Frame.grid(row=1,column=0,columnspan=3,sticky='nswe',padx=5,pady=5)
                self.CreateBackground()
            elif(self.active_windows==2):
                self.PS.Frame.grid(row=0,column=0,sticky='nswe',padx=5,pady=5)
                self.PS.layout()
            else:
                self.PS.Frame.grid(row=0,column=2,sticky='nswe',padx=5,pady=5)
                self.PS.layout() 
        else:
            self.GUI.PowerSupply.pop(self.PS.indice)
            self.GUI.PS_Count -=1
            for widget in self.PS.Frame.winfo_children():
                widget.destroy()    
            self.PS.Frame.destroy()  
            if(self.PS.indice < len(self.GUI.PowerSupply)):
                for i in range(self.PS.indice,len(self.GUI.PowerSupply)):
                        self.GUI.PowerSupply[i].indice-=1
            if(len(self.GUI.PowerSupply)==0):
                self.serial.PSThreadFlag=False
            if(self.active_windows==0):
                self.window.geometry("1000x500")
                self.Frame.grid(row=0,column=0,rowspan=2,columnspan=3,sticky="nswe")
            elif(self.active_windows==1):
                if(self.Show_SG_control.get()==True):
                    for widget in self.SG.Frame.winfo_children():
                        widget.destroy()
                    self.SG.Frame.grid(row=0,column=1,sticky='nswe',padx=5,pady=5)
                    self.SG.layout()
                else:
                    for widget in self.Mult.Frame.winfo_children():
                        widget.destroy()
                    self.Mult.Frame.grid(row=0,column=1,sticky='nswe',padx=5,pady=5)
                    self.Mult.layout()
            else:
                for widget in self.SG.Frame.winfo_children():
                     widget.destroy()
                self.SG.Frame.grid(row=0,column=0,sticky='nswe',padx=5,pady=5)
                self.SG.layout()

                for widget in self.Mult.Frame.winfo_children():
                     widget.destroy()
                self.Mult.Frame.grid(row=0,column=1,sticky='nswe',padx=5,pady=5)
                self.Mult.layout()

    def OpenWebSite(self):
        webbrowser.open_new("https://pocketwave.web.ua.pt/")
        
    def CreateBackground(self):

        self.DisplayFrame=Frame(master=self.Frame)
        self.DisplayFrame.place(relx=0,rely=0,relheight=1,relwidth=0.90)
         #Connect button 
        img = Image.open(self.resource_path('Images\\BotaoOff.png'))
        resized_img = img.resize((40, 20))
        self.Botao_Off_Image = ImageTk.PhotoImage(resized_img)
        img = Image.open(self.resource_path('Images\\BotaoOn.png'))
        resized_img = img.resize((40, 20))
        self.Botao_On_Image = ImageTk.PhotoImage(resized_img)
        if(self.serial.OscilloscopeThreadFlag==True):
            self.connect_button = Button(self.Frame,image=self.Botao_On_Image,
                                    command=self.StartOscilloscope, state="normal")
            self.connect_button.place(relx=0.95,rely=0)
        else:
             self.connect_button = Button(self.Frame,image=self.Botao_Off_Image,
                                    command=self.StartOscilloscope, state="normal")
             self.connect_button.place(relx=0.95,rely=0)

        self.figure=Figure(figsize=(10,8),dpi=100)
        self.ax_time = self.figure.add_subplot(211)
        self.ax_fft = self.figure.add_subplot(212)
        self.ax_time.grid(True)
        self.ax_fft.grid(True)
        self.canvas=FigureCanvasTkAgg(self.figure,master=self.DisplayFrame)
        self.canvas.get_tk_widget().pack(fill=BOTH,expand=True)

    
    
    def StartOscilloscope(self):
        if(self.GUI.Oscil_Count==1 and self.serial.OscilloscopeThreadFlag==False ):
                        
                        img = Image.open(self.resource_path('Images\\BotaoOn.png'))
                        resized_img = img.resize((40, 20))
                        self.Botao_On_Image = ImageTk.PhotoImage(resized_img)

                        self.serial.OscilloscopeThread=threading.Thread(target=self.serial.SerialOscilloscopeData,args=(self.GUI,), daemon=True)
                        self.serial.OscilloscopeThread.start()
                        self.connect_button.config(image= self.Botao_On_Image)
                        

        elif(self.GUI.Oscil_Count==1 and self.serial.OscilloscopeThreadFlag==True):

                img = Image.open(self.resource_path('Images\\BotaoOff.png'))
                resized_img = img.resize((40, 20))
                self.Botao_Off_Image = ImageTk.PhotoImage(resized_img)
               
                self.serial.OscilloscopeThreadFlag=False
                
                self.data_array=[]
                self.ax_time.clear()
                self.ax_fft.clear()
                self.connect_button.config(image= self.Botao_Off_Image)
        elif(self.GUI.Oscil_Count!=1 and self.serial.OscilloscopeThreadFlag==False):
                
                img = Image.open(self.resource_path('Images\\BotaoOn.png'))
                resized_img = img.resize((40, 20))
                self.Botao_On_Image = ImageTk.PhotoImage(resized_img)
                self.serial.OscilloscopeThread=threading.Thread(target=self.serial.SerialOscilloscopeData,args=(self.GUI,), daemon=True)
                self.serial.OscilloscopeThread.start()
                for i in range(len(self.GUI.Oscilloscope)):
                    
                    self.GUI.Oscilloscope[i].connect_button.config(image=self.GUI.Oscilloscope[i].Botao_On_Image)
                
        elif(self.GUI.Oscil_Count!=1 and self.serial.OscilloscopeThreadFlag==True):
                img = Image.open(self.resource_path('Images\\BotaoOff.png'))
                resized_img = img.resize((40, 20))
                self.Botao_Off_Image = ImageTk.PhotoImage(resized_img)
                
                self.serial.OscilloscopeThreadFlag=False
                
                for i in range(len(self.GUI.Oscilloscope)):
                    self.GUI.Oscilloscope[i].data_array=[]
                    self.GUI.Oscilloscope[i].ax_time.clear()
                    self.GUI.Oscilloscope[i].ax_fft.clear()
                    self.GUI.Oscilloscope[i].connect_button.config(image=self.GUI.Oscilloscope[i].Botao_Off_Image)
                    
               
        else:
            print('\n')

    def draw_array(self):
        self.ax_time.clear()
        self.ax_fft.clear()
        
        self.ax_time.plot(self.data_array)
        
        # Calcular e exibir valor pico a pico
        if len(self.data_array) > 0:
            peak_to_peak = np.ptp(self.data_array)
            self.ax_time.text(0.05, 0.95, f"Pico a Pico: {peak_to_peak:.2f} V", transform=self.ax_time.transAxes, verticalalignment='top')
        
        # Exibir frequência
        if self.serial.frequency:
            self.ax_time.text(0.05, 0.90, f"Frequência: {self.serial.frequency:.2f} Hz", transform=self.ax_time.transAxes, verticalalignment='top')
        
        self.ax_time.set_xlabel('Amostra')
        self.ax_time.set_ylabel('Tensão (V)')
        
        # FFT
        if len(self.data_array) > 1:
            N = len(self.data_array)
            T = 1.0 / 10e6  # 1ms interval
            yf = np.fft.fft(self.data_array)
            xf = np.fft.fftfreq(N, T)[:N//2]/1e3
            self.ax_fft.plot(xf, 2.0/N * np.abs(yf[:N//2]))
            self.ax_fft.set_xlabel('Frequência (KHz)')
            self.ax_fft.set_ylabel('Amplitude')
        
        self.canvas.draw()
class SignalGenerator:
    def __init__(self,GUI,data,serial):
        self.GUI=GUI
        self.serial=serial
        self.data=data
        self.indice=self.GUI.SG_Count -1
        if(self.GUI.SG_SHOW_Flag==False):
            self.window=Toplevel()
            self.window.title("Signal Generator")
            self.window.geometry("300x300")
            self.window.iconbitmap(self.resource_path("Images\\Icon.ico"))
            self.window.resizable(True,True)
            self.Menu()
            self.Frame=LabelFrame(self.window)
            self.Frame.place(relheight=1,relwidth=1)
            self.layout()
            self.window.protocol("WM_DELETE_WINDOW",lambda: self.close_Sg_window(self.window))
            self.Frequencia_input=self.Frequencia.get()
            self.Volts_input=self.Volts.get()
            self.Combo_input=self.Forma.get()

            self.Frequencia_last_input=self.Frequencia_input
            self.Volts_last_input=self.Volts_input
            self.Combo_last_input=self.Combo_input
        else:
            self.Frame=None
            if(self.serial.SGThreadFlag==True):
                self.Frequencia_input=self.GUI.SignalGenerator[0].Frequencia.get()
                self.Volts_input=self.GUI.SignalGenerator[0].Volts.get()
                self.Combo_input=self.GUI.SignalGenerator[0].Forma.get()

                self.Frequencia_last_input=self.Frequencia_input
                self.Volts_last_input=self.Volts_input
                self.Combo_last_input=self.Combo_input
            else:
                self.Frequencia_input=0
                self.Volts_input=0
                self.Combo_input='sine'

                self.Frequencia_last_input=self.Frequencia_input
                self.Volts_last_input=self.Volts_input
                self.Combo_last_input=self.Combo_input
        self.Frequencia_flag=0
        self.Volts_flag=0
        self.Combo_flag=0

    def resource_path(self,relative_path):
        try:
            base_path = sys._MEIPASS2
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)
    
    def Menu(self):
        self.Menu=Menu(self.window)
        self.Show_menu=Menu(self.Menu,tearoff=False)
        self.Show_Oscil_control=BooleanVar()
        self.Show_Mult_control=BooleanVar()
        self.Show_PS_control=BooleanVar()
        self.Show_menu.add_checkbutton(label="Show Oscilloscope",command=self.Show_Oscil,variable=self.Show_Oscil_control)
        self.Show_menu.add_checkbutton(label="Show Multimeter",command=self.Show_Mult,variable=self.Show_Mult_control)
        self.Show_menu.add_checkbutton(label="Show Power Supply",command=self.Show_PS,variable=self.Show_PS_control)
        self.Menu.add_cascade(label="Show...",menu=self.Show_menu)

        help_menu=Menu(self.Menu,tearoff=False)
        help_menu.add_command(label='User Manual',command=self.OpenUserGuide)
        self.Menu.add_cascade(label="Help",menu=help_menu)

        contacts_menu=Menu(self.Menu,tearoff=False)
        contacts_menu.add_command(label='Go to Pocketwave website',command=self.OpenWebSite)
        self.Menu.add_cascade(label="Contacts",menu=contacts_menu)
        self.window.configure(menu=self.Menu)   
        
    def OpenUserGuide(self):
        self.document_path = self.resource_path('usermanual.pdf')

        if os.path.exists(self.document_path):
            os.startfile(self.document_path)
        else:
            print(f"File not found: {self.document_path}")
    def close_Sg_window(self,window):
        if(self.Show_Mult_control.get()==True):
            if(len(self.GUI.Multimeter)==1):
                self.serial.MultimeterThreadFlag=False
            self.GUI.Multimeter.pop(self.Mult.indice)
            self.GUI.Mult_Count-=1
            if(self.Mult.indice < len(self.GUI.Multimeter)):
                    for i in range(self.Mult.indice,len(self.GUI.Multimeter)):
                        self.GUI.Multimeter[i].indice-=1 
        if(self.Show_PS_control.get()==True):
            if(len(self.GUI.PowerSupply)==1):
                self.serial.PSThreadFlag=False
            self.GUI.PowerSupply.pop(self.PS.indice)
            self.GUI.PS_Count-=1
            if(self.PS.indice < len(self.GUI.PowerSupply)):
                    for i in range(self.PS.indice,len(self.GUI.PowerSupply)):
                        self.GUI.PowerSupply[i].indice-=1 
        if(self.Show_Oscil_control.get()==True):
            if(len(self.GUI.Oscilloscope)==1):
                self.serial.OscilloscopeThreadFlag=False
            self.GUI.Oscilloscope.pop(self.Oscil.indice)
            self.GUI.Oscil_Count-=1
            if(self.Oscil.indice < len(self.GUI.Oscilloscope)):
                    for i in range(self.Oscil.indice,len(self.GUI.Oscilloscope)):
                        self.GUI.Oscilloscope[i].indice-=1 
        if(len(self.GUI.SignalGenerator)==1):
            try:
                self.serial.SGThreadFlag=False
                window.destroy()
                self.GUI.SignalGenerator.pop(0)
            except Exception as e:
                print(e)
                
        else:
            try:
                window.destroy()
                self.GUI.SignalGenerator.pop(self.indice)   
                if(self.indice < len(self.GUI.SignalGenerator)):
                    for i in range(self.indice,len(self.GUI.SignalGenerator)):
                        self.GUI.SignalGenerator[i].indice-=1
            except Exception as e:
                print(e) 
               
        self.GUI.SG_Count -=1
         
    def layout(self):
        img = Image.open(self.resource_path('Images\\BotaoOff.png'))
        resized_img = img.resize((40, 20))
        self.Botao_Off_Image = ImageTk.PhotoImage(resized_img)
        img = Image.open(self.resource_path('Images\\BotaoOn.png'))
        resized_img = img.resize((40, 20))
        self.Botao_On_Image = ImageTk.PhotoImage(resized_img)
        if(self.serial.SGThreadFlag==True):
            self.connect_button = Button(self.Frame,image=self.Botao_On_Image,
                                    command=self.StartSignalGenerator, state="normal")
            self.connect_button.place(relx=0.82,rely=0)
        else:
             self.connect_button = Button(self.Frame,image=self.Botao_Off_Image,
                                    command=self.StartSignalGenerator, state="normal")
             self.connect_button.place(relx=0.82,rely=0)
        label_Title = Label(self.Frame, text="Signal Generator",font=("Helvetica", 16))
        label_Title.pack()

        label_frequencia = Label(self.Frame, text="Frequency [10 Hz, 2 MHz]",font=("Helvetica", 10))
        label_frequencia.pack(expand=True,fill='both')
        if(self.serial.SGThreadFlag==True or self.GUI.SG_Count!=1):
            self.Frequencia=DoubleVar(value= self.GUI.SignalGenerator[0].Frequencia_last_input)
        else:
            self.Frequencia=DoubleVar(value=0.0)
        self.entry_frequencia = Entry(self.Frame,textvariable=self.Frequencia,font=("Helvetica", 15))
        self.entry_frequencia.pack(expand=True,fill='both')

        label_volts = Label(self.Frame, text="Amplitude (Vpp) [0 V, 3V]",font=("Helvetica", 10))
        label_volts.pack(expand=True,fill='both')

        if(self.serial.SGThreadFlag==True or self.GUI.SG_Count!=1):
            self.Volts=DoubleVar(value= self.GUI.SignalGenerator[0].Volts_last_input)
        else:
            self.Volts=DoubleVar(value=0.0)     
        
        self.entry_volts = Entry(self.Frame,textvariable=self.Volts,font=("Helvetica", 15))
        self.entry_volts.pack(expand=True,fill='both')

        label_forma_onda = Label(self.Frame, text="Waveform:",font=("Helvetica", 10))
        label_forma_onda.pack(expand=True,fill='both')
        if(self.serial.SGThreadFlag==True or self.GUI.SG_Count!=1):
            self.Forma=StringVar()
            self.combo_forma_onda = ttk.Combobox(self.Frame, values=["Sine", "Square", "Triangular"],textvariable=self.Forma, state="readonly")
            self.combo_forma_onda.set(self.GUI.SignalGenerator[0].Combo_last_input)
        else:
            self.Forma=StringVar()
            self.combo_forma_onda = ttk.Combobox(self.Frame, values=["Sine", "Square", "Triangular"],textvariable=self.Forma, state="readonly" )
            self.combo_forma_onda.set("Sine")
        self.combo_forma_onda.pack(expand=True,fill='both')
        self.entry_frequencia.bind ("<KeyRelease>", self.entry_freq_release)
        self.entry_volts.bind ("<KeyRelease>", self.entry_volts_release)
        self.combo_forma_onda.bind ("<KeyRelease>", self.combo_key_release) 
        self.combo_forma_onda.bind ("<FocusIn>", self.combo_selected)
        self.combo_forma_onda.bind ("<FocusOut>", self.combo_unselected)

    def Show_Oscil(self):
        self.active_windows=int(self.Show_Oscil_control.get())+int(self.Show_PS_control.get())+int(self.Show_Mult_control.get())
        if(self.Show_Oscil_control.get()==True):
            self.GUI.Oscil_Count+=1
            self.GUI.Oscil_SHOW_Flag=True
            self.Oscil=Oscilloscope(self.GUI,self.data,self.serial)
            self.GUI.Oscilloscope.append(self.Oscil)
            self.GUI.Oscil_SHOW_Flag=False
            self.Oscil.Frame=LabelFrame(master=self.window)
            self.window.geometry("1200x800")  
            self.window.rowconfigure(0,weight=1)
            self.window.columnconfigure(0,weight=1)
            self.window.columnconfigure(1,weight=1)
            self.window.columnconfigure(2,weight=1)
            self.window.rowconfigure(1,weight=20)
            if(self.active_windows==1 ):
                for widget in self.Frame.winfo_children():
                    widget.destroy()
                self.Oscil.Frame.grid(row=1,column=0,columnspan=3,sticky='nswe',padx=5,pady=5)
                self.Oscil.CreateBackground()
                self.Frame.grid(row=0,column=1,columnspan=1,rowspan=1,sticky='nswe',padx=5,pady=5)
                self.layout()
            elif(self.active_windows==2):
                self.Oscil.Frame.grid(row=1,column=0,columnspan=3,sticky='nswe',padx=5,pady=5)
                self.Oscil.CreateBackground()
            else:
                self.Oscil.Frame.grid(row=1,column=0,columnspan=3,sticky='nswe',padx=5,pady=5)
                self.Oscil.CreateBackground()
        else:
            self.GUI.Oscilloscope.pop(self.Oscil.indice)
            self.GUI.Oscil_Count-=1  
            if(len(self.GUI.Oscilloscope)==0):
                self.serial.OscilloscopeThreadFlag=False
            if(self.Oscil.indice < len(self.GUI.Oscilloscope)):
                for i in range(self.Oscil.indice,len(self.GUI.Oscilloscope)):
                        self.GUI.Oscilloscope[i].indice-=1
            self.window.rowconfigure(1,weight=0)
            for widget in self.Oscil.Frame.winfo_children():
                    widget.destroy()
            self.Oscil.Frame.destroy()

            if(self.active_windows==0):
                self.window.geometry("300x300")
                self.window.rowconfigure(0,weight=1)
                self.window.columnconfigure(0,weight=1)
                self.window.columnconfigure(1,weight=0)
                self.window.columnconfigure(2,weight=0)
                self.window.rowconfigure(1,weight=0)
                for widget in self.Frame.winfo_children():
                    widget.destroy()
                self.Frame.grid(column=0,row=0,sticky="nswe",padx=5,pady=5)
                self.layout()
            elif(self.active_windows==1):
                self.window.geometry("700x300")
                self.window.rowconfigure(0,weight=1)
                self.window.columnconfigure(0,weight=1)
                self.window.columnconfigure(1,weight=1)
                self.window.columnconfigure(2,weight=0)
                self.window.rowconfigure(1,weight=0)
                if( self.Show_PS_control.get() == True):
                    for widget in self.Frame.winfo_children():
                        widget.destroy()
                    self.Frame.grid(column=0,row=0,columnspan=1,sticky="nswe",padx=5,pady=5)
                    self.layout()    
                    for widget in self.PS.Frame.winfo_children():
                        widget.destroy()
                    self.PS.Frame.grid(column=1,row=0,columnspan=1,sticky="nswe",padx=5,pady=5)
                    self.PS.layout()
                else:
                    for widget in self.Frame.winfo_children():
                        widget.destroy()
                    self.Frame.grid(column=0,row=0,columnspan=1,sticky="nswe",padx=5,pady=5)
                    self.layout()    
                    for widget in self.Mult.Frame.winfo_children():
                        widget.destroy()
                    self.Mult.Frame.grid(column=1,row=0,columnspan=1,sticky="nswe",padx=5,pady=5)
                    self.Mult.layout()
            else:
                self.window.geometry("900x300")
                self.window.rowconfigure(0,weight=1)
                self.window.columnconfigure(0,weight=1)
                self.window.columnconfigure(1,weight=1)
                self.window.columnconfigure(2,weight=1)
                self.window.rowconfigure(1,weight=0)

    def Show_Mult(self):
        self.active_windows=int(self.Show_Oscil_control.get())+int(self.Show_PS_control.get())+int(self.Show_Mult_control.get())
        if(self.Show_Mult_control.get()==True):
            self.GUI.Mult_Count+=1
            self.GUI.Mult_SHOW_Flag=True
            self.Mult=Multimeter(self.GUI,self.data,self.serial)
            self.GUI.Multimeter.append(self.Mult)
            self.GUI.Mult_SHOW_Flag=False
            self.Mult.Frame=LabelFrame(master=self.window)
            if(self.active_windows==1 ):
                for widget in self.Frame.winfo_children():
                    widget.destroy()
                self.window.geometry("700x300")  
                self.window.rowconfigure(0,weight=1)
                self.window.rowconfigure(1,weight=0)
                self.window.columnconfigure(0,weight=1)
                self.window.columnconfigure(1,weight=1)
                self.window.columnconfigure(2,weight=0)
                self.Mult.Frame.grid(row=0,column=1,sticky='nswe',padx=5,pady=5)
                self.Mult.layout()
                self.Frame.grid(row=0,column=0,sticky='nswe',padx=5,pady=5)
                self.layout()
            elif(self.active_windows==2 and self.Show_Oscil_control.get()==False):
                self.window.geometry("900x300")  
                self.window.rowconfigure(0,weight=1)
                self.window.rowconfigure(1,weight=0)
                self.window.columnconfigure(0,weight=1)
                self.window.columnconfigure(1,weight=1)
                self.window.columnconfigure(2,weight=1)
                self.Mult.Frame.grid(row=0,column=2,sticky='nswe',padx=5,pady=5)
                self.Mult.layout()
            elif(self.active_windows==2 and self.Show_Oscil_control.get()==True):
                self.Mult.Frame.grid(row=0,column=0,sticky='nswe',padx=5,pady=5)
                self.Mult.layout()
            else:
                self.Mult.Frame.grid(row=0,column=2,sticky='nswe',padx=5,pady=5)
                self.Mult.layout()

             
        else:
            self.GUI.Multimeter.pop(self.Mult.indice)
            self.GUI.Mult_Count-=1        
            for widget in self.Mult.Frame.winfo_children():
                widget.destroy()    
            self.Mult.Frame.destroy()
            if(self.Mult.indice < len(self.GUI.Multimeter)):
                for i in range(self.Mult.indice,len(self.GUI.Multimeter)):
                        self.GUI.Multimeter[i].indice-=1
            if(len(self.GUI.Multimeter)==0):
                self.serial.MultimeterThreadFlag=False
            if(self.active_windows==0):
                self.window.geometry("300x300")
                self.window.rowconfigure(0,weight=1)
                self.window.rowconfigure(1,weight=0)
                self.window.columnconfigure(0,weight=1)
                self.window.columnconfigure(1,weight=0)
                self.window.columnconfigure(2,weight=0)
                self.Frame.grid(row=0,column=0,sticky="nswe")
            elif(self.active_windows==1 and self.Show_Oscil_control.get()==False):
                self.window.geometry("700x300")
                self.window.rowconfigure(0,weight=1)
                self.window.rowconfigure(1,weight=0)
                self.window.columnconfigure(0,weight=1)
                self.window.columnconfigure(1,weight=1)
                self.window.columnconfigure(2,weight=0)
                for widget in self.Frame.winfo_children():
                     widget.destroy()
                self.Frame.grid(row=0,column=0,sticky='nswe',padx=5,pady=5)
                self.layout()
                for widget in self.PS.Frame.winfo_children():
                    widget.destroy()
                self.PS.Frame.grid(row=0,column=1,sticky='nswe',padx=5,pady=5)
                self.PS.layout()
            elif(self.active_windows==1 and self.Show_Oscil_control.get()==True):
                for widget in self.Frame.winfo_children():
                     widget.destroy()
                self.Frame.grid(row=0,column=1,sticky='nswe',padx=5,pady=5)
                self.layout()
            else:
                for widget in self.Frame.winfo_children():
                     widget.destroy()
                self.Frame.grid(row=0,column=0,sticky='nswe',padx=5,pady=5)
                self.layout()

                for widget in self.PS.Frame.winfo_children():
                     widget.destroy()
                self.PS.Frame.grid(row=0,column=1,sticky='nswe',padx=5,pady=5)
                self.PS.layout()

    def Show_PS(self):
        self.active_windows=int(self.Show_Oscil_control.get())+int(self.Show_PS_control.get())+int(self.Show_Mult_control.get())
        if(self.Show_PS_control.get()==True):
            self.GUI.PS_Count+=1
            self.GUI.PS_SHOW_Flag=True
            self.PS=PowerSupply(self.GUI,self.data,self.serial)
            self.GUI.PowerSupply.append(self.PS)
            self.GUI.PS_SHOW_Flag=False
            self.PS.Frame=LabelFrame(master=self.window)
            if(self.active_windows==1 ):
                for widget in self.Frame.winfo_children():
                    widget.destroy()
                self.window.geometry("700x300")  
                self.window.rowconfigure(0,weight=1)
                self.window.rowconfigure(1,weight=0)
                self.window.columnconfigure(0,weight=1)
                self.window.columnconfigure(1,weight=1)
                self.window.columnconfigure(2,weight=0)
                self.PS.Frame.grid(row=0,column=1,sticky='nswe',padx=5,pady=5)
                self.PS.layout()
                self.Frame.grid(row=0,column=0,sticky='nswe',padx=5,pady=5)
                self.layout()
            elif(self.active_windows==2 and self.Show_Oscil_control.get()==False):
                self.window.geometry("900x300")  
                self.window.rowconfigure(0,weight=1)
                self.window.rowconfigure(1,weight=0)
                self.window.columnconfigure(0,weight=1)
                self.window.columnconfigure(1,weight=1)
                self.window.columnconfigure(2,weight=1)
                self.PS.Frame.grid(row=0,column=2,sticky='nswe',padx=5,pady=5)
                self.PS.layout()
            elif(self.active_windows==2 and self.Show_Oscil_control.get()==True):
                self.PS.Frame.grid(row=0,column=0,sticky='nswe',padx=5,pady=5)
                self.PS.layout()
            else:
                self.PS.Frame.grid(row=0,column=2,sticky='nswe',padx=5,pady=5)
                self.PS.layout()
        else:
            self.GUI.PowerSupply.pop(self.PS.indice)
            self.GUI.PS_Count -=1
            for widget in self.PS.Frame.winfo_children():
                widget.destroy()    
            self.PS.Frame.destroy()  
            if(self.PS.indice < len(self.GUI.PowerSupply)):
                for i in range(self.PS.indice,len(self.GUI.PowerSupply)):
                        self.GUI.PowerSupply[i].indice-=1
            if(len(self.GUI.PowerSupply)==0):
                self.serial.PSThreadFlag=False
            if(self.active_windows==0):
                self.window.geometry("300x300")
                self.window.rowconfigure(0,weight=1)
                self.window.rowconfigure(1,weight=0)
                self.window.columnconfigure(0,weight=1)
                self.window.columnconfigure(1,weight=0)
                self.window.columnconfigure(2,weight=0)
                self.Frame.grid(row=0,column=0,sticky="nswe")
            elif(self.active_windows==1 and self.Show_Oscil_control.get()==False ):
                self.window.geometry("700x300")
                self.window.rowconfigure(0,weight=1)
                self.window.rowconfigure(1,weight=0)
                self.window.columnconfigure(0,weight=1)
                self.window.columnconfigure(1,weight=1)
                self.window.columnconfigure(2,weight=0)
                for widget in self.Frame.winfo_children():
                     widget.destroy()
                self.Frame.grid(row=0,column=0,sticky='nswe',padx=5,pady=5)
                for widget in self.Mult.Frame.winfo_children():
                    widget.destroy()
                self.Mult.Frame.grid(row=0,column=1,sticky='nswe',padx=5,pady=5)
                self.Mult.layout()
            elif(self.active_windows==1 and self.Show_Oscil_control.get()==True):
                for widget in self.Frame.winfo_children():
                     widget.destroy()
                self.Frame.grid(row=0,column=1,sticky='nswe',padx=5,pady=5)
                self.layout()
            else:
                for widget in self.Frame.winfo_children():
                     widget.destroy()
                self.Frame.grid(row=0,column=0,sticky='nswe',padx=5,pady=5)
                self.layout()

                for widget in self.Mult.Frame.winfo_children():
                     widget.destroy()
                self.Mult.Frame.grid(row=0,column=1,sticky='nswe',padx=5,pady=5)
                self.Mult.layout()
        
    def OpenWebSite(self):
        webbrowser.open_new("https://pocketwave.web.ua.pt/")


    def combo_selected(self,event):
        self.Combo_selected = True
        print("combo_selected")

    def combo_unselected(self,event):
        if(self.serial.SGThreadFlag==True):
            try:
                if self.Combo_selected:  
                    self.Combo_selected = False
                    combo_input=(self.Forma.get())           
                    a=self.Frequencia.get()
                    b=self.Volts.get()
                    if(combo_input!=self.Combo_input and (a >0 and a<=2000000) and (b>0 and b<=3)):
                        self.Combo_input=combo_input
                        self.Combo_last_input=combo_input
                        self.Combo_flag=1     
            except Exception:
                print('\n')


    def combo_key_release(self,event):
        if(self.serial.SGThreadFlag==True):
            try:
                if event.keycode == 13:
                    combo_input=(self.Forma.get())           
                    a=self.Frequencia.get()
                    b=self.Volts.get()
                    if(combo_input!=self.Combo_input and (a >0 and a<=2000000) and (b>0 and b<=3)):
                        
                            self.Combo_input=combo_input
                            self.Combo_last_input=combo_input
                            self.Combo_flag=1
                            print(self.Forma.get())
            except Exception:
                print('\n')     
              
    def entry_freq_release(self,event):
        if(self.serial.SGThreadFlag==True):
            try:
                if event.keycode == 13:
                    freq_input=(self.Frequencia.get())           
                    b=self.Volts.get()
                    if(freq_input!=self.Frequencia_input ):
                        
                        if( freq_input <10 or  freq_input>2000000):
                            messagebox.showwarning("Frequency Input Error", "Check the Frequency value and adjust it") 
                        elif( (b>0 and b<=3) ):
                            self.Frequencia_last_input=freq_input
                            self.Frequencia_input=freq_input
                            self.Frequencia_flag=1
            except Exception:   
                print('\n')
    def entry_volts_release(self,event):
         if(self.serial.SGThreadFlag==True):
            try:
                if event.keycode == 13:
                    v_input=(self.Volts.get())           
                    a=self.Frequencia.get()
                    if(v_input!=self.Volts_last_input ):
                        
                        if( v_input <0 or  v_input>3):
                            messagebox.showwarning("Voltage Input Error", "Check the Voltage value and adjust it") 
                        elif( (a>0 and a<=2000000) ):
                            self.Volts_last_input=v_input
                            self.Volts_input=v_input
                            self.Volts_flag=1
            except Exception:
                print('\n')
 
    def StartSignalGenerator(self):

        if(self.GUI.SG_Count==1 and self.serial.SGThreadFlag==False ):
                        
                        img = Image.open(self.resource_path('Images\\BotaoOn.png'))
                        resized_img = img.resize((40, 20))
                        self.Botao_On_Image = ImageTk.PhotoImage(resized_img)

                        self.serial.SGThread=threading.Thread(target=self.serial.SerialSignalGeneratorData,args=(self.GUI,), daemon=True)
                        self.serial.SGThread.start()
                        self.connect_button.config(image= self.Botao_On_Image)
                        

        elif(self.GUI.SG_Count==1 and self.serial.SGThreadFlag==True):

                img = Image.open(self.resource_path('Images\\BotaoOff.png'))
                resized_img = img.resize((40, 20))
                self.Botao_Off_Image = ImageTk.PhotoImage(resized_img)
               
                self.serial.SGThreadFlag=False
                

                self.connect_button.config(image= self.Botao_Off_Image)
                
        elif(self.GUI.SG_Count!=1 and self.serial.SGThreadFlag==False):
                
                img = Image.open(self.resource_path('Images\\BotaoOn.png'))
                resized_img = img.resize((40, 20))
                self.Botao_On_Image = ImageTk.PhotoImage(resized_img)
                self.serial.SGThread=threading.Thread(target=self.serial.SerialSignalGeneratorData,args=(self.GUI,), daemon=True)
                self.serial.SGThread.start()
                for i in range(len(self.GUI.SignalGenerator)):
                    
                    self.GUI.SignalGenerator[i].connect_button.config(image=self.GUI.SignalGenerator[i].Botao_On_Image)
                
        elif(self.GUI.SG_Count!=1 and self.serial.SGThreadFlag==True):
                img = Image.open(self.resource_path('Images\\BotaoOff.png'))
                resized_img = img.resize((40, 20))
                self.Botao_Off_Image = ImageTk.PhotoImage(resized_img)
                
                self.serial.SGThreadFlag=False
               
                for i in range(len(self.GUI.SignalGenerator)):
            
                    self.GUI.SignalGenerator[i].connect_button.config(image=self.GUI.SignalGenerator[i].Botao_Off_Image)
                    
                print("Thread SignalGenerator Acabou")
        else:
                print('\n')

class PowerSupply:
    def __init__(self,GUI,data,serial):
        self.GUI=GUI
        self.indice=self.GUI.PS_Count -1
        self.data=data
        self.serial=serial
        if(self.GUI.PS_SHOW_Flag==False):
            self.window=Toplevel()
            self.window.title("Power Supply")
            self.window.geometry("300x300")
            self.window.iconbitmap(self.resource_path("Images\\Icon.ico"))
            self.window.resizable(True,True)
            self.Menu()
            self.Frame=LabelFrame(self.window)
            self.Frame.place(relheight=1,relwidth=1)
            self.layout()
            self.window.protocol("WM_DELETE_WINDOW",lambda: self.close_Ps_window(self.window))
            self.Current_input=self.Current.get()
            self.Voltage_input=self.Voltage.get()

            self.Current_last_input=self.Current_input
            self.Voltage_last_input=self.Voltage_input
        else:
            self.Frame=None
            if(self.serial.PSThreadFlag==True):
                self.Current_input=self.GUI.PowerSupply[0].Current.get()
                self.Voltage_input=self.GUI.PowerSupply[0].Voltage.get()
              

                self.Current_last_input=self.Current_input
                self.Voltage_last_input=self.Voltage_input
            else:
                self.Current_input=0
                self.Voltage_input=0

                self.Current_last_input=self.Current_input
                self.Voltage_last_input=self.Voltage_input
        self.voltage_flag=0
        self.current_flag=0

    def resource_path(self,relative_path):
        try:
            base_path = sys._MEIPASS2
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    def close_Ps_window(self,window):
        if(self.Show_Mult_control.get()==True):
            if(len(self.GUI.Multimeter)==1):
                self.serial.MultimeterThreadFlag=False
            self.GUI.Multimeter.pop(self.Mult.indice)
            self.GUI.Mult_Count-=1
            if(self.Mult.indice < len(self.GUI.Multimeter)):
                    for i in range(self.Mult.indice,len(self.GUI.Multimeter)):
                        self.GUI.Multimeter[i].indice-=1 
        if(self.Show_SG_control.get()==True):
            if(len(self.GUI.SignalGenerator)==1):
                self.serial.SGThreadFlag=False
            self.GUI.SignalGenerator.pop(self.SG.indice)
            self.GUI.SG_Count-=1
            if(self.SG.indice < len(self.GUI.SignalGenerator)):
                    for i in range(self.SG.indice,len(self.GUI.SignalGenerator)):
                        self.GUI.SignalGenerator[i].indice-=1 
        if(self.Show_Oscil_control.get()==True):
            if(len(self.GUI.Oscilloscope)==1):
                self.serial.OscilloscopeThreadFlag=False
            self.GUI.Oscilloscope.pop(self.Oscil.indice)
            self.GUI.Oscil_Count-=1
            if(self.Oscil.indice < len(self.GUI.Oscilloscope)):
                    for i in range(self.Oscil.indice,len(self.GUI.Oscilloscope)):
                        self.GUI.Oscilloscope[i].indice-=1
        if(len(self.GUI.PowerSupply)==1):
            try:
                self.serial.PSThreadFlag=False
                self.GUI.PowerSupply.pop(0)
                window.destroy()
            except Exception as e:
                print(e)
                
        else:
            try:
                self.GUI.PowerSupply.pop(self.indice)
                window.destroy()
                if(self.indice < len(self.GUI.PowerSupply)):
                    for i in range(self.indice,len(self.GUI.PowerSupply)):
                        self.GUI.PowerSupply[i].indice-=1
            except Exception as e:
                print(e)
        self.GUI.PS_Count -=1

    def Menu(self):
        self.Menu=Menu(self.window)
        self.Show_menu=Menu(self.Menu,tearoff=False)
        self.Show_Oscil_control=BooleanVar()
        self.Show_Mult_control=BooleanVar()
        self.Show_SG_control=BooleanVar()
        self.Show_menu.add_checkbutton(label="Show Oscilloscope",command=self.Show_Oscil,variable=self.Show_Oscil_control)
        self.Show_menu.add_checkbutton(label="Show Multimeter",command=self.Show_Mult,variable=self.Show_Mult_control)
        self.Show_menu.add_checkbutton(label="Show Signal Generator",command=self.Show_SG,variable=self.Show_SG_control)
        self.Menu.add_cascade(label="Show...",menu=self.Show_menu)

        help_menu=Menu(self.Menu,tearoff=False)
        help_menu.add_command(label='User Manual',command=self.OpenUserGuide)
        self.Menu.add_cascade(label="Help",menu=help_menu)

        contacts_menu=Menu(self.Menu,tearoff=False)
        contacts_menu.add_command(label='Go to Pocketwave website',command=self.OpenWebSite)
        self.Menu.add_cascade(label="Contacts",menu=contacts_menu)
        self.window.configure(menu=self.Menu)

    def OpenUserGuide(self):
        self.document_path = self.resource_path('usermanual.pdf')
        if os.path.exists(self.document_path):
            os.startfile(self.document_path)
        else:
            print(f"File not found: {self.document_path}")
    def layout(self):
            
        img = Image.open(self.resource_path('Images\\BotaoOff.png'))
        resized_img = img.resize((40, 20))
        self.Botao_Off_Image = ImageTk.PhotoImage(resized_img)
        img = Image.open(self.resource_path('Images\\BotaoOn.png'))
        resized_img = img.resize((40, 20))
        self.Botao_On_Image = ImageTk.PhotoImage(resized_img)
        if(self.serial.PSThreadFlag==True):
            self.connect_button = Button(self.Frame,image=self.Botao_On_Image,
                                    command=self.StartPowerSupply, state="normal")
            self.connect_button.place(relx=0.82,rely=0)
        else:
             self.connect_button = Button(self.Frame,image=self.Botao_Off_Image,
                                    command=self.StartPowerSupply, state="normal")
             self.connect_button.place(relx=0.82,rely=0)


        label_Title = Label(self.Frame, text="Power Supply",font=("Helvetica", 20))
        label_Title.pack()
        
        label_volts = Label(self.Frame, text="Volts  [-12V , 12V]",font=("Helvetica", 10))
        label_volts.pack()
        if(self.serial.PSThreadFlag==True or  self.GUI.PS_Count!=1):
            self.Voltage=DoubleVar(value=self.GUI.PowerSupply[0].Voltage_last_input)    
        else:
            self.Voltage=DoubleVar(value=0.0)    

        
        self.entry_volts = Entry(self.Frame,textvariable=self.Voltage,font=("Helvetica", 20))
        self.entry_volts.pack()
        self.voltage_slider = Scale(self.Frame, from_=-12, to=12, orient="horizontal", 
                             variable=self.Voltage, command=self.Update_Voltage,
                             resolution=0.1)  
        self.voltage_slider.pack(fill='x',padx=50)


        label_current = Label(self.Frame, text="Current  [0 A , 0.001 A]",font=("Helvetica", 10))
        label_current.pack()
        if(self.serial.PSThreadFlag==True or  self.GUI.PS_Count!=1):
            self.Current=DoubleVar(value=self.GUI.PowerSupply[0].Current_last_input)    
        else:
            self.Current=DoubleVar(value=0.0)     
        
        self.entry_current = Entry(self.Frame,textvariable=self.Current,font=("Helvetica", 20))
        self.entry_current.pack()
        self.voltage_slider = Scale(self.Frame, from_=0, to=0.001, orient="horizontal", 
                             variable=self.Current, command=self.Update_Current,
                             resolution=0.00001)  
        self.voltage_slider.pack(fill='x',padx=50)
       
        
        self.entry_current.bind("<KeyRelease>", self.current_key_release)

        
        self.entry_volts.bind("<KeyRelease>", self.voltage_key_release)
    def Update_Voltage(self,value):
            self.Voltage.set(value)
            self.Voltage_input=value 
            self.Voltage_last_input=value 
            self.voltage_flag=1
    def Update_Current(self,value):
            self.Current.set(value)
            self.Current_input=value
            self.Current_last_input=value
            self.current_flag=1

    def Show_Oscil(self):
        self.active_windows=int(self.Show_Oscil_control.get())+int(self.Show_SG_control.get())+int(self.Show_Mult_control.get())
        if(self.Show_Oscil_control.get()==True):
            self.GUI.Oscil_Count+=1
            self.GUI.Oscil_SHOW_Flag=True
            self.Oscil=Oscilloscope(self.GUI,self.data,self.serial)
            self.GUI.Oscilloscope.append(self.Oscil)
            self.GUI.Oscil_SHOW_Flag=False
            self.Oscil.Frame=LabelFrame(master=self.window)
            self.window.geometry("1200x800")  
            self.window.rowconfigure(0,weight=1)
            self.window.columnconfigure(0,weight=1)
            self.window.columnconfigure(1,weight=1)
            self.window.columnconfigure(2,weight=1)
            self.window.rowconfigure(1,weight=20)
            if(self.active_windows==1 ):
                for widget in self.Frame.winfo_children():
                    widget.destroy()
                self.Oscil.Frame.grid(row=1,column=0,columnspan=3,sticky='nswe',padx=5,pady=5)
                self.Oscil.CreateBackground()
                
                self.Frame.grid(row=0,column=1,columnspan=1,rowspan=1,sticky='nswe',padx=5,pady=5)
                self.layout()
            elif(self.active_windows==2):
                self.Oscil.Frame.grid(row=1,column=0,columnspan=3,sticky='nswe',padx=5,pady=5)
                self.Oscil.CreateBackground()

            else:
                self.Oscil.Frame.grid(row=1,column=0,columnspan=3,sticky='nswe',padx=5,pady=5)
                self.Oscil.CreateBackground()
     
        else:
            self.GUI.Oscilloscope.pop(self.Oscil.indice)
            self.GUI.Oscil_Count-=1  
            if(len(self.GUI.Oscilloscope)==0):
                self.serial.OscilloscopeThreadFlag=False
            if(self.Oscil.indice < len(self.GUI.Oscilloscope)):
                for i in range(self.Oscil.indice,len(self.GUI.Oscilloscope)):
                        self.GUI.Oscilloscope[i].indice-=1
            self.window.rowconfigure(1,weight=0)
            for widget in self.Oscil.Frame.winfo_children():
                    widget.destroy()
            self.Oscil.Frame.destroy()

            if(self.active_windows==0):
                self.window.geometry("300x300")
                self.window.rowconfigure(0,weight=1)
                self.window.columnconfigure(0,weight=1)
                self.window.columnconfigure(1,weight=0)
                self.window.columnconfigure(2,weight=0)
                self.window.rowconfigure(1,weight=0)
                for widget in self.Frame.winfo_children():
                    widget.destroy()
                self.Frame.grid(column=0,row=0,sticky="nswe",padx=5,pady=5)
                self.layout()
            elif(self.active_windows==1):
                self.window.geometry("700x300")
                self.window.rowconfigure(0,weight=1)
                self.window.columnconfigure(0,weight=1)
                self.window.columnconfigure(1,weight=1)
                self.window.columnconfigure(2,weight=0)
                self.window.rowconfigure(1,weight=0)
                if( self.Show_SG_control.get() == True):
                    for widget in self.Frame.winfo_children():
                        widget.destroy()
                    self.Frame.grid(column=0,row=0,columnspan=1,sticky="nswe",padx=5,pady=5)
                    self.layout()    
                    for widget in self.SG.Frame.winfo_children():
                        widget.destroy()
                    self.SG.Frame.grid(column=1,row=0,columnspan=1,sticky="nswe",padx=5,pady=5)
                    self.SG.layout()
                else:
                    for widget in self.Frame.winfo_children():
                        widget.destroy()
                    self.Frame.grid(column=0,row=0,columnspan=1,sticky="nswe",padx=5,pady=5)
                    self.layout()    
                    for widget in self.Mult.Frame.winfo_children():
                        widget.destroy()
                    self.Mult.Frame.grid(column=1,row=0,columnspan=1,sticky="nswe",padx=5,pady=5)
                    self.Mult.layout()
            else:
                self.window.geometry("900x300")
                self.window.rowconfigure(0,weight=1)
                self.window.columnconfigure(0,weight=1)
                self.window.columnconfigure(1,weight=1)
                self.window.columnconfigure(2,weight=1)
                self.window.rowconfigure(1,weight=0)

    def Show_Mult(self):
        self.active_windows=int(self.Show_Oscil_control.get())+int(self.Show_SG_control.get())+int(self.Show_Mult_control.get())
        if(self.Show_Mult_control.get()==True):
            self.GUI.Mult_Count+=1
            self.GUI.Mult_SHOW_Flag=True
            self.Mult=Multimeter(self.GUI,self.data,self.serial)
            self.GUI.Multimeter.append(self.Mult)
            self.GUI.Mult_SHOW_Flag=False
            self.Mult.Frame=LabelFrame(master=self.window)
            if(self.active_windows==1 ):
                for widget in self.Frame.winfo_children():
                    widget.destroy()
                self.window.geometry("700x300")  
                self.window.rowconfigure(0,weight=1)
                self.window.rowconfigure(1,weight=0)
                self.window.columnconfigure(0,weight=1)
                self.window.columnconfigure(1,weight=1)
                self.window.columnconfigure(2,weight=0)
                self.Mult.Frame.grid(row=0,column=1,sticky='nswe',padx=5,pady=5)
                self.Mult.layout()
                self.Frame.grid(row=0,column=0,sticky='nswe',padx=5,pady=5)
                self.layout()
            elif(self.active_windows==2 and self.Show_Oscil_control.get()==False):
                self.window.geometry("900x300")  
                self.window.rowconfigure(0,weight=1)
                self.window.rowconfigure(1,weight=0)
                self.window.columnconfigure(0,weight=1)
                self.window.columnconfigure(1,weight=1)
                self.window.columnconfigure(2,weight=1)
                self.Mult.Frame.grid(row=0,column=2,sticky='nswe',padx=5,pady=5)
                self.Mult.layout()
            elif(self.active_windows==2 and self.Show_Oscil_control.get()==True):
                self.Mult.Frame.grid(row=0,column=0,sticky='nswe',padx=5,pady=5)
                self.Mult.layout()
            else:
                self.Mult.Frame.grid(row=0,column=2,sticky='nswe',padx=5,pady=5)
                self.Mult.layout()

             
        else:
            self.GUI.Multimeter.pop(self.Mult.indice)
            self.GUI.Mult_Count-=1        
            for widget in self.Mult.Frame.winfo_children():
                widget.destroy()    
            self.Mult.Frame.destroy()
            if(self.Mult.indice < len(self.GUI.Multimeter)):
                for i in range(self.Mult.indice,len(self.GUI.Multimeter)):
                        self.GUI.Multimeter[i].indice-=1
            if(len(self.GUI.Multimeter)==0):
                self.serial.MultimeterThreadFlag=False
            if(self.active_windows==0):
                self.window.geometry("300x300")
                self.window.rowconfigure(0,weight=1)
                self.window.rowconfigure(1,weight=0)
                self.window.columnconfigure(0,weight=1)
                self.window.columnconfigure(1,weight=0)
                self.window.columnconfigure(2,weight=0)
                self.Frame.grid(row=0,column=0,sticky="nswe")
            elif(self.active_windows==1 and self.Show_Oscil_control.get()==False):
                self.window.geometry("700x300")
                self.window.rowconfigure(0,weight=1)
                self.window.rowconfigure(1,weight=0)
                self.window.columnconfigure(0,weight=1)
                self.window.columnconfigure(1,weight=1)
                self.window.columnconfigure(2,weight=0)
                for widget in self.Frame.winfo_children():
                     widget.destroy()
                self.Frame.grid(row=0,column=0,sticky='nswe',padx=5,pady=5)
                self.layout()
                for widget in self.SG.Frame.winfo_children():
                    widget.destroy()
                self.SG.Frame.grid(row=0,column=1,sticky='nswe',padx=5,pady=5)
                self.SG.layout()
            elif(self.active_windows==1 and self.Show_Oscil_control.get()==True):
                for widget in self.Frame.winfo_children():
                     widget.destroy()
                self.Frame.grid(row=0,column=1,sticky='nswe',padx=5,pady=5)
                self.layout()
            else:
                for widget in self.Frame.winfo_children():
                     widget.destroy()
                self.Frame.grid(row=0,column=0,sticky='nswe',padx=5,pady=5)
                self.layout()

                for widget in self.SG.Frame.winfo_children():
                     widget.destroy()
                self.SG.Frame.grid(row=0,column=1,sticky='nswe',padx=5,pady=5)
                self.SG.layout()
                
    def Show_SG(self):
        self.active_windows=int(self.Show_SG_control.get())+int(self.Show_Oscil_control.get())+int(self.Show_Mult_control.get())
        if(self.Show_SG_control.get()==True):
            self.GUI.SG_Count +=1
            self.GUI.SG_SHOW_Flag=True
            self.SG=SignalGenerator(self.GUI,self.data,self.serial)
            self.GUI.SignalGenerator.append(self.SG)
            self.GUI.SG_SHOW_Flag=False
            self.SG.Frame=LabelFrame(master=self.window) 
            self.window.rowconfigure(0,weight=1)
            self.window.columnconfigure(0,weight=1)
            self.window.columnconfigure(1,weight=1)
            self.window.columnconfigure(2,weight=1)
            self.window.rowconfigure(1,weight=20)
            
            if(self.active_windows==1):
                for widget in self.Frame.winfo_children():
                    widget.destroy()
                self.window.geometry("700x300")  
                self.window.rowconfigure(0,weight=1)
                self.window.rowconfigure(1,weight=0)
                self.window.columnconfigure(0,weight=1)
                self.window.columnconfigure(1,weight=1)
                self.window.columnconfigure(2,weight=0)
                self.SG.Frame.grid(row=0,column=1,sticky='nswe',padx=5,pady=5)
                self.SG.layout()
                self.Frame.grid(row=0,column=0,sticky='nswe',padx=5,pady=5)
                self.layout()
                
            elif(self.active_windows==2 and self.Show_Oscil_control.get()==False):
                self.window.geometry("900x300")  
                self.window.rowconfigure(0,weight=1)
                self.window.rowconfigure(1,weight=0)
                self.window.columnconfigure(0,weight=1)
                self.window.columnconfigure(1,weight=1)
                self.window.columnconfigure(2,weight=1)
                self.SG.Frame.grid(row=0,column=2,sticky='nswe',padx=5,pady=5)
                self.SG.layout()
            elif(self.active_windows==2 and self.Show_Oscil_control.get()==True):
                self.SG.Frame.grid(row=0,column=0,sticky='nswe',padx=5,pady=5)
                self.SG.layout()
            else:
                self.SG.Frame.grid(row=0,column=2,sticky='nswe',padx=5,pady=5)
                self.SG.layout()    

             
        else:
            self.GUI.SignalGenerator.pop(self.SG.indice)
            self.GUI.SG_Count -=1
            for widget in self.SG.Frame.winfo_children():
                widget.destroy()    
                self.SG.Frame.destroy()   
            if(self.SG.indice < len(self.GUI.SignalGenerator)):
                for i in range(self.SG.indice,len(self.GUI.SignalGenerator)):
                        self.GUI.SignalGenerator[i].indice-=1
            if(len(self.GUI.SignalGenerator)==0):
                self.serial.SGThreadFlag=False
            if(self.active_windows==0):
                self.window.geometry("300x300")
                self.window.rowconfigure(0,weight=1)
                self.window.rowconfigure(1,weight=0)
                self.window.columnconfigure(0,weight=1)
                self.window.columnconfigure(1,weight=0)
                self.window.columnconfigure(2,weight=0)
                self.Frame.grid(row=0,column=0,sticky="nswe")
            elif(self.active_windows==1 and self.Show_Oscil_control.get()==False):
                self.window.geometry("700x300")
                self.window.rowconfigure(0,weight=1)
                self.window.rowconfigure(1,weight=0)
                self.window.columnconfigure(0,weight=1)
                self.window.columnconfigure(1,weight=1)
                self.window.columnconfigure(2,weight=0)
                for widget in self.Frame.winfo_children():
                     widget.destroy()
                self.Frame.grid(row=0,column=0,sticky='nswe',padx=5,pady=5)
                self.layout()
                for widget in self.Mult.Frame.winfo_children():
                    widget.destroy()
                self.Mult.Frame.grid(row=0,column=1,sticky='nswe',padx=5,pady=5)
                self.Mult.layout()
            elif(self.active_windows==1 and self.Show_Oscil_control.get()==True):
                for widget in self.Frame.winfo_children():
                     widget.destroy()
                self.Frame.grid(row=0,column=1,sticky='nswe',padx=5,pady=5)
                self.layout()
            else:
                for widget in self.Frame.winfo_children():
                     widget.destroy()
                self.Frame.grid(row=0,column=0,sticky='nswe',padx=5,pady=5)
                self.layout()

                for widget in self.Mult.Frame.winfo_children():
                     widget.destroy()
                self.Mult.Frame.grid(row=0,column=1,sticky='nswe',padx=5,pady=5)
                self.Mult.layout()

    def OpenWebSite(self):
        webbrowser.open_new("https://pocketwave.web.ua.pt/")
      
    def voltage_key_release(self, event):
        if(self.serial.PSThreadFlag==True):
            try:
                if event.keycode == 13:
                   
                    v_input=(self.Voltage.get())           

                    if(v_input!=self.Voltage_input):
                            self.Voltage_input=v_input 
                            self.Voltage_last_input=v_input 
                            self.voltage_flag=1
            except:
                messagebox.showwarning("Voltage Input Error", "Check the voltage value and adjust it")
            
    def current_key_release(self, event):
        if(self.serial.PSThreadFlag==True):
            try:
                if event.keycode == 13:
                    
                    i_input=(self.Current.get())           

                    if(i_input!=self.Current_input):
                            self.Current_input=i_input
                            self.Current_last_input=i_input
                            self.current_flag=1
            except:
                messagebox.showwarning("Current Input Error", "Check the Current value and adjust it") 
        
    def StartPowerSupply(self):
        
        if(self.GUI.PS_Count==1 and self.serial.PSThreadFlag==False ):
                        
                        img = Image.open(self.resource_path('Images\\BotaoOn.png'))
                        resized_img = img.resize((40, 20))
                        self.Botao_On_Image = ImageTk.PhotoImage(resized_img)

                        self.serial.PSThread=threading.Thread(target=self.serial.SerialPowerSupplyData,args=(self.GUI,), daemon=True)
                        self.serial.PSThread.start()
                        self.connect_button.config(image= self.Botao_On_Image)
                        

        elif(self.GUI.PS_Count==1 and self.serial.PSThreadFlag==True):

                img = Image.open(self.resource_path('Images\\BotaoOff.png'))
                resized_img = img.resize((40, 20))
                self.Botao_Off_Image = ImageTk.PhotoImage(resized_img)
               
                self.serial.PSThreadFlag=False
                

                self.connect_button.config(image= self.Botao_Off_Image)
    
        elif(self.GUI.PS_Count!=1 and self.serial.PSThreadFlag==False):
                
                img = Image.open(self.resource_path('Images\\BotaoOn.png'))
                resized_img = img.resize((40, 20))
                self.Botao_On_Image = ImageTk.PhotoImage(resized_img)
                self.serial.PSThread=threading.Thread(target=self.serial.SerialPowerSupplyData,args=(self.GUI,), daemon=True)
                self.serial.PSThread.start()
                for i in range(len(self.GUI.PowerSupply)):
                    
                    self.GUI.PowerSupply[i].connect_button.config(image=self.GUI.PowerSupply[i].Botao_On_Image)
                
        elif(self.GUI.PS_Count!=1 and self.serial.PSThreadFlag==True):
                img = Image.open(self.resource_path('Images\\BotaoOff.png'))
                resized_img = img.resize((40, 20))
                self.Botao_Off_Image = ImageTk.PhotoImage(resized_img)
                
                self.serial.PSThreadFlag=False
               
                for i in range(len(self.GUI.PowerSupply)):
            
                    self.GUI.PowerSupply[i].connect_button.config(image=self.GUI.PowerSupply[i].Botao_Off_Image)
                    
                
        else:
            pass

if __name__=="__main__":   # Garante  so é executada quando é chamada pela Main(Master.py)
    RootGUI()
    Multimeter()
    Oscilloscope()
    PowerSupply()
    SignalGenerator()
