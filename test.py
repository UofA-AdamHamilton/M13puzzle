import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np

# import the functions
from test_function import change_color, change_linestyle

root = tk.Tk()
root.title("Matplotlib Style Controls")

control_frame = ttk.Frame(root, padding=10)
control_frame.pack(side=tk.LEFT, fill=tk.Y)

plot_frame = ttk.Frame(root)
plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

fig, ax = plt.subplots(figsize=(5, 4))
x = np.linspace(0, 10, 100)
line, = ax.plot(x, np.sin(x), color="blue", linestyle="-") # this is how you will store the edges of PG(2,3)
canvas = FigureCanvasTkAgg(fig, master=plot_frame)
canvas.draw()
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# color dropdown
color_var = tk.StringVar(value="blue")
color_menu = ttk.Combobox(
    control_frame,
    textvariable=color_var,
    values=["blue", "red", "green", "black", "orange", "purple"],
    state="readonly"
)
color_menu.pack(fill="x")
color_menu.bind(
    "<<ComboboxSelected>>",
    lambda event: change_color(line, color_var, canvas)
)

# linestyle dropdown
linestyle_var = tk.StringVar(value="solid")
style_menu = ttk.Combobox(
    control_frame,
    textvariable=linestyle_var,
    values=["solid", "dashed"],
    state="readonly"
)
style_menu.pack(fill="x")
style_menu.bind(
    "<<ComboboxSelected>>",
    lambda event: change_linestyle(line, linestyle_var, canvas)
)

root.mainloop()
