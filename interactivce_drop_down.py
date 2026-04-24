import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
from markdown import markdown
from tkhtmlview import HTMLLabel
import os

root = tk.Tk()
root.title("Matplotlib Style Controls")

# Frames
control_frame = ttk.Frame(root, padding=10)
control_frame.pack(side=tk.LEFT, fill=tk.Y)

plot_frame = ttk.Frame(root)
plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Matplotlib figure
fig, ax = plt.subplots(figsize=(5, 4))
x = np.linspace(0, 10, 100)
line, = ax.plot(x, np.sin(x), color="blue", linestyle="-")
ax.set_title("Interactive Plot")

canvas = FigureCanvasTkAgg(fig, master=plot_frame)
canvas.draw()
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

def change_color(event=None):
    line.set_color(color_var.get())
    canvas.draw_idle()

def change_linestyle(event=None):
    line.set_linestyle("-" if linestyle_var.get() == "solid" else "--")
    canvas.draw_idle()

def open_markdown():
    md_path = "example.md"
    if not os.path.exists(md_path):
        return

    with open(md_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    html = markdown(md_text)  # convert Markdown -> HTML

    md_window = tk.Toplevel(root)
    md_window.title("Documentation")
    md_window.geometry("600x500")

    html_label = HTMLLabel(md_window, html=html)
    html_label.pack(fill="both", expand=True, padx=10, pady=10)
    html_label.fit_height()

# Color control
ttk.Label(control_frame, text="Line color:").pack(anchor="w", pady=(0, 5))

color_var = tk.StringVar(value="blue")
color_menu = ttk.Combobox(
    control_frame,
    textvariable=color_var,
    values=["blue", "red", "green", "black", "orange", "purple"],
    state="readonly"
)
color_menu.pack(fill="x")
color_menu.bind("<<ComboboxSelected>>", change_color)

# Line style control
ttk.Label(control_frame, text="Line style:").pack(anchor="w", pady=(15, 5))

linestyle_var = tk.StringVar(value="solid")
style_menu = ttk.Combobox(
    control_frame,
    textvariable=linestyle_var,
    values=["solid", "dashed"],
    state="readonly"
)
style_menu.pack(fill="x")
style_menu.bind("<<ComboboxSelected>>", change_linestyle)

# Markdown button
ttk.Label(control_frame, text="Documentation:").pack(anchor="w", pady=(20, 5))

ttk.Button(
    control_frame,
    text="Open Markdown (rendered)",
    command=open_markdown
).pack(fill="x")

root.mainloop()
