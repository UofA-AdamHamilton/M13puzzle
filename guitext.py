import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Set up the main Tkinter window
root = tk.Tk()
root.title("Clickable Matplotlib Plot with Scrollable Text")

# Main container frames
frame_plot = ttk.Frame(root)
frame_plot.grid(row=0, column=0, sticky="nsew")

frame_text = ttk.Frame(root)
frame_text.grid(row=0, column=1, sticky="nsew")

# Make the window resize properly
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=3)
root.columnconfigure(1, weight=1)

# Create a Matplotlib figure and axes
fig, ax = plt.subplots(figsize=(5, 4))
ax.set_title("Click inside the plot")
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)

# Embed the plot in the Tkinter GUI
canvas = FigureCanvasTkAgg(fig, master=frame_plot)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
canvas.draw()

# Create the scrollable Text widget
text_frame = ttk.Frame(frame_text)
text_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

text_widget = tk.Text(text_frame, wrap="none", height=20)
text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=text_widget.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

text_widget.configure(yscrollcommand=scrollbar.set)

# Clear button
def clear_text():
    text_widget.delete("1.0", tk.END)

clear_button = ttk.Button(frame_text, text="Clear Text", command=clear_text)
clear_button.pack(pady=5)

# Handle mouse click on the plot
def on_click(event):
    if event.inaxes == ax:
        x, y = event.xdata, event.ydata
        text_widget.insert(tk.END, f"Clicked at: ({x:.2f}, {y:.2f})\n")
        text_widget.see(tk.END)  # Auto-scroll to bottom

# Connect click event
canvas.mpl_connect("button_press_event", on_click)

# Start the Tkinter event loop
root.mainloop()

