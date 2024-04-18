import tkinter as tk
from tkinter import ttk


class SignalGenerator(tk.Frame):
    def __init__(self,parent):
        super().__init__(master=parent)
        self.layout()
        
    def layout(self):
         #Adicione widgets para configurar frequência, volts e forma da onda
        # Exemplo de widgets; personalize conforme necessário
        label_Title = tk.Label(self, text="Signal Generator",font=("Helvetica", 20))
        label_Title.pack(expand=True,fill='both')

        label_frequencia = tk.Label(self, text="Frequency:")
        label_frequencia.pack(expand=True,fill='both')

        self.Frequencia=tk.DoubleVar()
        entry_frequencia = tk.Entry(self,textvariable=self.Frequencia)
        entry_frequencia.pack(expand=True,fill='both')

        label_volts = tk.Label(self, text="Volts:")
        label_volts.pack(expand=True,fill='both')

        self.Volts=tk.DoubleVar()
        entry_volts = tk.Entry(self,textvariable=self.Volts)
        entry_volts.pack(expand=True,fill='both')

        label_forma_onda = tk.Label(self, text="Waveform:")
        label_forma_onda.pack(expand=True,fill='both')

        self.Forma=tk.StringVar()
        combo_forma_onda = ttk.Combobox(self, values=["Sine", "Square", "Triangular"],textvariable=self.Forma)
        combo_forma_onda.set("Sine")
        combo_forma_onda.pack(expand=True,fill='both')

        # Botão para confirmar as configurações
        btn_confirmar = tk.Button(self, text="Confirmar", command=self.confirmar_configuracoes)
        btn_confirmar.pack(expand=True,fill='both')

    def confirmar_configuracoes(self):
        # Adicione lógica para processar as configurações aqui
        print("Configurações confirmadas!")
        

    