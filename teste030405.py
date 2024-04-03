import serial
import tkinter as tk
import serial.tools.list_ports
import matplotlib.pyplot as plt

# Variável para armazenar os valores de raw
raw_values = []

# Função para encontrar a porta serial
def find_serial_port():
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        if "STMicroelectronics STLink Virtual COM Port" in p.description:
            return p.device
    return None

# Função para atualizar o valor na janela e adicionar ao array
def update_label():
    data = ser.readline().decode().strip()
    try:
        data1 = float(data)
        raw = data1 / 4095 * 3.3
        raw_values.append(raw)  # Adiciona ao array
        label.config(text="Tensão: {:.2f}".format(raw))
    except ValueError:
        pass
    root.after(1, update_label)  # Atualiza a cada 100 milissegundos

# Função para fechar o array e gerar o gráfico
def close_array():
    plt.plot(raw_values)
    plt.xlabel('Amostras')
    plt.ylabel('Tensão (V)')
    plt.title('Gráfico de Tensão em Função das Amostras')
    plt.grid(True)
    plt.show()
    # Programa um autoclick no botão a cada 2 segundos
    root.after(2000, close_button.invoke)

# Função para realizar um autoclick no botão
def autoclick():
    close_button.invoke()
    # Programa um novo autoclick a cada 2 segundos
    root.after(2000, autoclick)

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

# Criar o rótulo para exibir os valores
label = tk.Label(root, text="Valor: ")
label.pack(padx=20, pady=20)

# Botão para fechar o array e gerar o gráfico
close_button = tk.Button(root, text="Fechar Array e Gerar Gráfico", command=close_array)
close_button.pack(pady=10)

# Iniciar a atualização dos valores
update_label()

# Programa o primeiro autoclick após 2 segundos
root.after(2000, autoclick)

# Iniciar a execução da interface gráfica
root.mainloop()
