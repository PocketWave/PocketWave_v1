import tkinter as tk

class PowerSupply(tk.Frame):
    def __init__(self,parent):
        super().__init__(master=parent)
       
        self.layout()
    
    def layout(self):

        label_Title = tk.Label(self, text="Power Supply",font=("Helvetica", 20))
        label_Title.pack()
        
        label_volts = tk.Label(self, text="Volts:",font=("Helvetica", 12))
        label_volts.pack()

        self.Voltage=tk.DoubleVar()
        entry_volts = tk.Entry(self,textvariable=self.Voltage)
        entry_volts.pack()

        label_current = tk.Label(self, text="Current:",font=("Helvetica", 12))
        label_current.pack()

        self.Current=tk.DoubleVar()
        entry_current = tk.Entry(self,textvariable=self.Current)
        entry_current.pack()

    
