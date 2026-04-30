import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import mplcursors
import matplotlib.colors as mcolors
import matplotlib.patches as patches
import time
import copy
import numpy as np
from projective_plane import PG23
from projectiveplane_rotationally_symmetric import PG23_rotationally_symmetric
from main_functions import open_markdown, swap_and_animate, close_window, set_permutation

# --- Create main window ---
root = tk.Tk()
root.title("M13 Groupoid")

# --- Layout frames ---
# Main container frames

# buttons to the left 
control_frame = ttk.Frame(root, padding=10)
control_frame.grid(row = 0, column=0 , sticky='nsew')

# exit button
control_frame_exit = ttk.Frame(root, padding=10)
control_frame_exit.grid(row = 1, column=0 , sticky='nsew')

# buttons below
control_frame_bottom = ttk.Frame(root, padding=10)
control_frame_bottom.grid(row = 1, column=1 , sticky='nsew')

# the matplotlib window
frame_plot = ttk.Frame(root)
frame_plot.grid(row=0, column=1, sticky="ns")

# the text widget to the right
frame_text = ttk.Frame(root)
frame_text.grid(row=0, column=2, sticky="nsew")

# Make the window resize properly
root.rowconfigure(0, weight=3)
root.columnconfigure(1, weight=3)
root.columnconfigure(2, weight=3)

# --- Matplotlib figure ---
#fig, ax, label_node_map, vertex_dict, edge_dict, label_dict, lines, line_to_edge_dict  = PG23()
fig, ax, label_node_map, vertex_dict, edge_dict, label_dict, lines, line_to_edge_dict  = PG23_rotationally_symmetric()
layout = "rotational 3-fold symmetry"

graph_data = {
        "label_node_map": label_node_map,
        "vertex_dict": vertex_dict,
        "lines": lines,
        "line_to_edge_dict": line_to_edge_dict,
        "ax": ax
    }


original_label_dict = copy.deepcopy(label_dict)
original_vertex_dict = copy.deepcopy(vertex_dict)


print('printing vertex dictionary')
print(vertex_dict)
ax.set_title("Interactive Plot")
ax.tick_params(
    #axis='',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom=False,      # ticks along the bottom edge are off
    top=False,         # ticks along the top edge are off
    labelbottom=False) # labels along the bottom edge are o
ax.set_yticks([])

canvas = FigureCanvasTkAgg(fig, master=frame_plot)
canvas.draw()
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# --- Dropdown callback ---
def change_color(event=None):
    color = color_var.get()
    for i in edge_dict.values():
        for j in i.values():
            print(type(j))
            j.set_color(color)
    canvas.draw_idle()

# --- Dropdown menu ---
ttk.Label(control_frame, text="Select line color:").pack(pady=(0, 5))

color_var = tk.StringVar(value="blue")
colors = ["black", "blue", "red", "green", "black", "orange", "purple"]

color_menu = ttk.Combobox(
    control_frame,
    textvariable=color_var,
    values=colors,
    state="readonly"
)
color_menu.pack()
color_menu.bind("<<ComboboxSelected>>", change_color)


# --- Dropdown callback ---
def change_layout(event=None):

    global canvas
    global layout 
    global on_click 
    
    # if the old layout matches the new layout, do nothing
    old_layout = copy.copy(layout)
    layout = layout_var.get()
    if layout == old_layout:
        print('no change in layout')
        return 

    #create a table mapping 
    dispatch_table = {
        "standard": PG23,
        "rotational 3-fold symmetry": PG23_rotationally_symmetric,
        "13-gon": 'not implemented yet sorry',
        "nonagon": 'not implemented yet sorry',
        "octagon": 'not implemented yet sorry'
    }

    # remove old canvas
    if canvas is not None:
        canvas.get_tk_widget().destroy()
    
    fig, ax, label_node_map, vertex_dict, edge_dict, label_dict, lines, line_to_edge_dict = dispatch_table.get(layout, PG23)()
    graph_data = {
        "label_node_map": label_node_map,
        "vertex_dict": vertex_dict,
        "lines": lines,
        "line_to_edge_dict": line_to_edge_dict,
        "ax": ax
    }

    ax.set_title("Interactive Plot")
    ax.tick_params(
        #axis='',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom=False,      # ticks along the bottom edge are off
        top=False,         # ticks along the top edge are off
        labelbottom=False) # labels along the bottom edge are ods
    
    ax.set_yticks([])

    # resets the clicked nodes and empty node when the layout is changed, to avoid confusion
    clicked_nodes = []
    empty_node = [0]
    clear_text()
    """
    def on_click(event):
        if event.inaxes != graph_data["ax"]:
            return
        # records coordinates in text box
        if event.inaxes == ax:
            x, y = event.xdata, event.ydata
            text_widget.insert(tk.END, f"Clicked at: ({x:.2f}, {y:.2f})\n")
            text_widget.see(tk.END)  # Auto-scroll to bottom
        if event.inaxes != ax:
            return
        x_click, y_click = event.xdata, event.ydata
        for i in vertex_dict.keys():
            x,y = vertex_dict[i].center
            dx, dy = x - x_click, y - y_click
            if (dx**2 + dy**2)**0.5 < 0.2 and i != empty_node[0]:
                text_widget.insert(tk.END, f"Clicked a node\n")
                clicked_nodes.append(i)
                print('clicked nodes:', clicked_nodes)
                if len(clicked_nodes) == 1:
                    print('animate')
                    swap_and_animate(i, empty_node[0], label_node_map, vertex_dict, edge_dict, label_dict, lines, root, canvas, ax, line_to_edge_dict,edge_flash = True)
                    clicked_nodes.clear()
                    empty_node[0] =  i
                    text_widget.insert(tk.END, f"empty node is now {i}\n")
                elif len(clicked_nodes) > 1:
                    clicked_nodes.clear()
                print('permutation')
                print(label_node_map)
                break
    """
            
    print(' ')
    canvas = FigureCanvasTkAgg(fig, master=frame_plot)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    # Connect click event
    canvas.mpl_connect("button_press_event", on_click)
    canvas.mpl_connect(
    "button_press_event",
    lambda event: on_click(event)
)

# --- Dropdown menu ---
ttk.Label(control_frame, text="Select projective plane layout:").pack(pady=(0, 5))
layout_var = tk.StringVar(value="rotational 3-fold symmetry")
layouts = ["standard", "rotational 3-fold symmetry", "13-gon", "nonagon", "octagon"] 

layout_menu = ttk.Combobox(
    control_frame,
    textvariable=layout_var,
    values=layouts,
    state="readonly"
)
layout_menu.pack()
layout_menu.bind("<<ComboboxSelected>>", change_layout)

# Markdown button
ttk.Label(control_frame, text="Documentation:").pack(anchor="w", pady=(20, 5))
ttk.Button(
    control_frame,
    text="Instructions",
    command=lambda: open_markdown(root, 'documentation/instructions.md')
).pack(fill="x")


# other markdown button 
ttk.Button(
    control_frame,
    text="About M13",
    command=lambda: open_markdown(root, 'documentation/M13groupoid.md')
).pack(fill="x")


# save_button
ttk.Button(
    control_frame,
    text="Save",
    command=lambda: open_markdown(root, 'documentation/instructions')
).pack(fill="x")

# load_button
ttk.Button(
    control_frame,
    text="Load Permutation",
    command=lambda: open_markdown(root, 'documentation/instructions')
).pack(fill="x")

# reset button
def reset():
    open_markdown(root, 'documentation/instructions')
    for i in range(13):
        label_node_map[i] = i
    vertex_dict = original_label_dict
    label_dict = original_label_dict
    print('resetting permutation')
    canvas.draw()
    root.update()
ttk.Button(
    control_frame,
    text="Reset",
    command=reset
).pack(fill="x")

# exit button
ttk.Button(
    control_frame_exit,
    text="close",
    command= lambda: close_window(root)
).pack(fill="x")


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

# On click: handle selection and swapping
# Track clicked nodes and selected outline
clicked_nodes = []
empty_node = [0]
def on_click(event):
    if event.inaxes != graph_data["ax"]:
        return
    # records coordinates in text box
    if event.inaxes == ax:
        x, y = event.xdata, event.ydata
        text_widget.insert(tk.END, f"Clicked at: ({x:.2f}, {y:.2f})\n")
        text_widget.see(tk.END)  # Auto-scroll to bottom
    if event.inaxes != ax:
        return
    x_click, y_click = event.xdata, event.ydata
    for i in vertex_dict.keys():
        x,y = vertex_dict[i].center
        dx, dy = x - x_click, y - y_click
        if (dx**2 + dy**2)**0.5 < 0.2 and i != empty_node[0]:
            text_widget.insert(tk.END, f"Clicked a node\n")
            clicked_nodes.append(i)
            print('clicked nodes:', clicked_nodes)
            if len(clicked_nodes) == 1:
                print('animate')
                swap_and_animate(i, empty_node[0], label_node_map, vertex_dict, edge_dict, label_dict, lines, root, canvas, ax, line_to_edge_dict,edge_flash = True)
                clicked_nodes.clear()
                empty_node[0] =  i
                text_widget.insert(tk.END, f"empty node is now {i}\n")
            elif len(clicked_nodes) > 1:
                clicked_nodes.clear()
            print('permutation')
            print(label_node_map)
            break
            
    print(' ')

# Connect click event
canvas.mpl_connect("button_press_event", on_click)
print(empty_node)


# --- Start GUI ---
root.mainloop()
