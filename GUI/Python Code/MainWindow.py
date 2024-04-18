import tkinter as tk
import serial
import serial.tools.list_ports
from PIL import Image, ImageTk
from Window import *
from tkinter import messagebox


class MainWindow(tk.Canvas):
    def __init__(self, parent):
        super().__init__(master=parent)
        self.pack(expand=True,fill='both')
        self.bg_image()
        self.add_buttons()
        

    def bg_image(self):
        self.bg_img = ImageTk.PhotoImage(file="Imagens/Background_Image.png")
        # Set Image in Canvas
        self.bind('<Configure>', self.stretch_image)
        self.create_image(0, 0, image=self.bg_img, anchor="nw")

    def stretch_image(self, event):
        width = event.width
        height = event.height
        self.bg1 = Image.open("Imagens/Background_Image.png")
        self.resized_image = self.bg1.resize((width, height))
        self.new_bg = ImageTk.PhotoImage(self.resized_image)
        self.create_image(0, 0, image=self.new_bg, anchor="nw")   

    

    def add_buttons(self):
        def create_button(image_path, text, command, row, col,state):
            img = Image.open(image_path)
            resized_img = img.resize((250, 100))
            tk_img = ImageTk.PhotoImage(resized_img)
            if(text== 'Oscilloscope'):
                self.Oscilloscopebutton = tk.Button(self, text=text, image=tk_img, command=command, compound=tk.TOP,
                               font=("Helvetica", 12), bg="white", fg="black", relief=tk.FLAT, highlightthickness=0,state=state)
                self.Oscilloscopebutton.image = tk_img
                self.create_window(col, row, anchor=tk.NW, window=self.Oscilloscopebutton)
            elif(text== 'Multimeter'):
                self.Multimeterbutton = tk.Button(self, text=text, image=tk_img, command=command, compound=tk.TOP,
                               font=("Helvetica", 12), bg="white", fg="black", relief=tk.FLAT, highlightthickness=0,state=state)
                self.Multimeterbutton.image = tk_img
                self.create_window(col, row, anchor=tk.NW, window=self.Multimeterbutton)
            elif(text== 'Power Supply'):
                self.PSbutton = tk.Button(self, text=text, image=tk_img, command=command, compound=tk.TOP,
                               font=("Helvetica", 12), bg="white", fg="black", relief=tk.FLAT, highlightthickness=0,state=state)
                self.PSbutton.image = tk_img
                self.create_window(col, row, anchor=tk.NW, window= self.PSbutton)
            else:
                self.SGbutton = tk.Button(self, text=text, image=tk_img, command=command, compound=tk.TOP,
                               font=("Helvetica", 12), bg="white", fg="black", relief=tk.FLAT, highlightthickness=0,state=state)
                self.SGbutton.image = tk_img
                self.create_window(col, row, anchor=tk.NW, window=self.SGbutton)
        def create_connect_disconnect_button( text, command, row, col):  
            self.CDbutton = tk.Button(self, text=text,  command=command, compound=tk.TOP,
                               font=("Helvetica", 12), bg="white", fg="black", relief=tk.FLAT, highlightthickness=0)
            self.CDbutton_window=self.create_window(col, row, anchor=tk.NW, window=self.CDbutton )

        create_connect_disconnect_button('Connect STM',self.Connect_DisconnectSTM,360,350)
        create_button('Imagens/Oscilloscope.png', 'Oscilloscope', self.open_Oscil_window, 400, 100,"disabled")
        create_button('Imagens/Multimeter.png', 'Multimeter', self.open_Mult_window, 550, 100,"disabled")
        create_button('Imagens/PowerSupply.png', 'Power Supply', self.open_PS_window, 400, 450,"disabled")
        create_button('Imagens/SignalGenerator.png', 'Signal Generator', self.open_SG_window , 550, 450,"disabled")

    def Connect_DisconnectSTM(self):
        def find_serial_port():
            ports = list(serial.tools.list_ports.comports())
            for p in ports:
                if "STMicroelectronics STLink Virtual COM Port" in p.description:
                    return p.device
            return None
        self.port = find_serial_port()

        if self.CDbutton.cget('text') == "Connect STM" :
            if self.port:
                self.ser = serial.Serial(self.port, 115200)
                messagebox.showinfo("Connection successful !","STM device connected to the PC")
                self.Oscilloscopebutton.config(state="normal")
                self.Multimeterbutton.config(state="normal")
                self.PSbutton.config(state="normal")
                self.SGbutton.config(state="normal")
                self.CDbutton.config(text="Disconnect STM")
                self.coords(self.CDbutton_window,340,360)

            else:
                messagebox.showwarning("Connection Error", "No STM device founded")
        else:
            self.ser.close()
            self.Oscilloscopebutton.config(state="disabled")
            self.Multimeterbutton.config(state="disabled")
            self.PSbutton.config(state="disabled")
            self.SGbutton.config(state="disabled")
            self.CDbutton.config(text="Connect STM")
            self.coords(self.CDbutton_window,350,360)
            


    def open_SG_window(self):
        print('SignalGenerator')
        self.SG_window=Window("Signal Generator","300x300")
        
        
    def open_PS_window(self):
        print('PowerSupply')
        self.PS_window=Window("Power Supply","300x300")
        
        
    def open_Mult_window(self):
        print('Multimeter')
        self.Mult_window=Window("Multimeter","300x300")
        
        
    def open_Oscil_window(self):
        print('Oscilloscope')
        self.Oscil_window=Window("Oscilloscope","1000x600")
        
        

              

        