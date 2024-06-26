import tkinter as tk

# dummy data
sin_array1 = [2048, 2098, 2148, 2199, 2249, 2299, 2349, 2399, 2448, 2498, 2547, 2596, 2644, 2692, 2740,
              2787, 2834, 2880, 2926, 2971, 3016, 3060, 3104, 3147, 3189, 3230, 3271, 3311, 3351, 3389,
              3427, 3464, 3500, 3535, 3569, 3602, 3635, 3666, 3697, 3726, 3754, 3782, 3808, 3833, 3857,
              3880, 3902, 3923, 3943, 3961, 3979, 3995, 4010, 4024, 4036, 4048, 4058, 4067, 4074, 4081,
              4086, 4090, 4093, 4095, 4095, 4094, 4092, 4088, 4084, 4078, 4071, 4062, 4053, 4042, 4030,
              4017, 4002, 3987, 3970, 3952, 3933, 3913, 3891, 3869, 3845, 3821, 3795, 3768, 3740, 3711,
              3681, 3651, 3619, 3586, 3552, 3517, 3482, 3445, 3408, 3370, 3331, 3291, 3251, 3210, 3168,
              3125, 3082, 3038, 2994, 2949, 2903, 2857, 2811, 2764, 2716, 2668, 2620, 2571, 2522, 2473,
              2424, 2374, 2324, 2274, 2224, 2174, 2123, 2073, 2022, 1972, 1921, 1871, 1821, 1771, 1721,
              1671, 1622, 1573, 1524, 1475, 1427, 1379, 1331, 1284, 1238, 1192, 1146, 1101, 1057, 1013,
              970, 927, 885, 844, 804, 764, 725, 687, 650, 613, 578, 543, 509, 476, 444,
              414, 384, 355, 327, 300, 274, 250, 226, 204, 182, 162, 143, 125, 108, 93,
              78, 65, 53, 42, 33, 24, 17, 11, 7, 3, 1, 0, 0, 2, 5,
              9, 14, 21, 28, 37, 47, 59, 71, 85, 100, 116, 134, 152, 172, 193,
              215, 238, 262, 287, 313, 341, 369, 398, 429, 460, 493, 526, 560, 595, 631,
              668, 706, 744, 784, 824, 865, 906, 948, 991, 1035, 1079, 1124, 1169, 1215, 1261,
              1308, 1355, 1403, 1451, 1499, 1548, 1597, 1647, 1696, 1746, 1796, 1846, 1896, 1947, 1997,
              2047]

# Function to update the label with real-time values
def update_label():
    global index
    data = sin_array1[index]
    data1 = float(data)
    raw = data1 / 4095 * 3.3
    label.config(text="Valor: {:.2f}V".format(raw))
    index = (index + 1) % len(sin_array1)
    root.after(10, update_label)  # Update every 100 milliseconds

# Create the window
root = tk.Tk()
root.title("Real-time Values")

# Create the label to display the values
label = tk.Label(root, text="Value: ")
label.pack(padx=100, pady=20)

# init index
index = 0

# Start updating the label with real-time values
update_label()

# Start the Tkinter event loop
root.mainloop()
