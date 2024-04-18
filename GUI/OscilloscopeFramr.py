import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk, Canvas, Label, Entry, Button, StringVar, OptionMenu, PhotoImage

class Oscilloscope(tk.Frame):
    def __init__(self,parent):
        super().__init__(master=parent)
        

        self.canvas = Canvas(self, width=800, height=400, bg="white")
        self.canvas.place(relx=0,rely=0,relheight=1,relwidth=1)

    



       
        
        plt.xlabel('Tempo (s)')
        plt.ylabel('Amplitude')
        plt.grid(True)
        plt.savefig("temp_plot.png")

    
        img = PhotoImage(file="temp_plot.png")
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        self.canvas.create_image(0, 0, anchor="nw", image=img)
        self.canvas.image = img

   



    
    
    