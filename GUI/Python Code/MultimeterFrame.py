import tkinter as tk
from tkinter import ttk


class Multimeter(tk.Frame):
    def __init__(self,parent):
        super().__init__(master=parent)
        self.layout()
        
    def layout(self):
        #label
        label_Title = tk.Label(self, text="Multimeter:",font=("Helvetica", 20))
        label_Title.pack()

        label1 = tk.Label(self, text="Choose one of the multimeter's measuring options", font=("Helvetica", 9))
        label1.pack(side='top')

        #NOTEBOOK
        notebook=ttk.Notebook(self)
        notebook.pack()
        tab1=ttk.Frame(notebook)#VOLTAGE
        self.Voltage=tk.DoubleVar(value=5)
        label_tensao=ttk.Label(tab1,text=f'V: {self.Voltage.get()}',font=("Helvetica", 20))
        label_tensao.pack(side='bottom')

        tab2=ttk.Frame(notebook)#CURRENT
        self.Current=tk.DoubleVar(value=5)
        label_current=ttk.Label(tab2,text=f'I: {self.Current.get()}',font=("Helvetica", 20))
        label_current.pack(side='bottom')

        tab3=ttk.Frame(notebook)#RESISTANCE
        self.Resistance=tk.DoubleVar(value=5)
        label_resistance=ttk.Label(tab3,text=f'R: {self.Resistance.get()}',font=("Helvetica", 20))
        label_resistance.pack(side='bottom')


        tab4=ttk.Frame(notebook)#CAPACITANCE
        self.Capacitance=tk.DoubleVar(value=5)
        label_capacitance=ttk.Label(tab4,text=f'C: {self.Capacitance.get()}',font=("Helvetica", 20))
        label_capacitance.pack(side='bottom')


        notebook.add(tab1,text= 'Voltage')  
        notebook.add(tab2,text= 'Current')
        notebook.add(tab3,text= 'Resistance')
        notebook.add(tab4,text= 'Capacitance')

  