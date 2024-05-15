import serial
import tkinter as tk
import serial.tools.list_ports
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# Função para encontrar a porta serial
def find_serial_port():
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        if "STMicroelectronics STLink Virtual COM Port" in p.description:
            return p.device
    return None

# Função para atualizar o valor na janela e no gráfico
def update_values():
    data = ser.readline().decode().strip()
    try:
        data1 = float(data)
        raw = 4*(data1 / 4095 * 3.3 - 1.6)
        add_data_point(raw)  # Adiciona o novo valor ao gráfico
    except ValueError:
        pass
    root.after(1, update_values)  # Atualiza a cada 100 milissegundos

# Função para adicionar um ponto de dados ao gráfico
def add_data_point(value):
    x_data.append(len(x_data))
    y_data.append(value)
    ax.clear()
    ax.plot(x_data, y_data)
    ax.set_xlabel('Tempo')
    ax.set_ylabel('Tensão (V)')
    canvas.draw()

# Encontrar a porta serial
port = find_serial_port()

# Se uma porta for encontrada, configura a comunicação serial
if port:
    ser = serial.Serial(port, 115200)
else:
    print("Nenhuma porta serial encontrada.")
    exit()

# Criar a janela
root = tk.Tk()
root.title("Valores em tempo real")

# Configuração do gráfico
fig = Figure(figsize=(6, 4), dpi=100)
ax = fig.add_subplot(111)
x_data = []
y_data = []

# Criar o canvas do gráfico e adicioná-lo à janela
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Iniciar a atualização dos valores
update_values()

# Iniciar a execução da interface gráfica
root.mainloop()
