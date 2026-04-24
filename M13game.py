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
import numpy as np

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
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=3)

# Create a graph
G = nx.erdos_renyi_graph(n=6, p=0.5, seed=42)

# Assign unique colors to nodes
colors = ['red', 'green', 'blue', 'orange', 'purple', 'cyan']
original_node_colors = {node: colors[i % len(colors)] for i, node in enumerate(G.nodes)}
node_colors = original_node_colors.copy()

# Graph layout
pos = nx.spring_layout(G)


# Create figure and axis
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.2)  # Make space for reset button
plt.title("Hover to view, click two nodes to swap colors. Reset to restore.")
plt.gca().set_aspect('equal')

# Embed the plot in the Tkinter GUI
canvas = FigureCanvasTkAgg(fig, master=frame_plot)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
canvas.draw()

# Draw graph
nodes = nx.draw_networkx_nodes(G, pos, ax=ax, node_color=[node_colors[n] for n in G.nodes])
edges = nx.draw_networkx_edges(G, pos, ax=ax, edge_color=[[0,0,0,1]]*len(list(G.edges)))
labels = nx.draw_networkx_labels(G, pos, ax=ax)

# Track clicked nodes and selected outline
clicked_nodes = []
selection_outline = None  # This will hold the patch
#circleline = None

# Update node colors
def update_node_colors():
    nodes.set_color([node_colors[n] for n in G.nodes])
    #fig.canvas.draw_idle()
    canvas.draw()

"""
# Add hover with label and highlight
cursor = mplcursors.cursor(nodes, hover=True)
@cursor.connect("add")
def on_hover(sel):
    node_index = sel.index
    node2 = list(G.nodes)[node_index]
    print('hover on node', node_index, node2)
    sel.annotation.set_text(f"Node {node2}")
    sel.annotation.get_bbox_patch().set(fc="yellow")
    current_annotation["ann"] = sel.annotation  # store reference
    print(current_annotation)

# Keep track of the current annotation
current_annotation = {"ann": None}
print('current annotation', current_annotation)
@cursor.connect("remove")
def on_leave(sel):
    # Hide current annotation when the cursor leaves all nodes
    print('removing')
    ann = current_annotation.get("ann")
    if ann is not None:
        ann.set_visible(False)
        canvas.draw()
        current_annotation["ann"] = None
"""


# Function to draw red outline around first selected node
def draw_selection_outline(node):
    print('triggered draw')
    #global selection_outline
    global circleline
    x, y = pos[node]
    print(node, x, y)
    #outline = patches.Circle(
    #    (x, y), radius=0.07, edgecolor='red', facecolor='none', linewidth=3#, zorder=3
    #)
    def draw_circle(x_center, y_center, radius, ax, **kwargs):
        theta = np.linspace(0, 2 * np.pi, 100)
        x = x_center + radius * np.cos(theta)
        y = y_center + radius * np.sin(theta)
        circleline, = ax.plot(x, y, **kwargs, color = 'red', linewidth = 3)
        return circleline
        
    circleline = draw_circle(x, y, 0.07, ax)
    #selection_outline = outline
    #ax.add_patch(outline)
    #fig.canvas.draw()  # <- Force immediate redraw here
    canvas.draw()
    #root.update()
    #root.after(100)

# Remove the red outline
def remove_selection_outline():
    #global selection_outline
    #if selection_outline:
    #    selection_outline.remove()
    #    selection_outline = None
    #    #fig.canvas.draw_idle()
    #    #fig.canvas.draw()
    #    canvas.draw()
    #    root.update()
    global circleline
    if circleline:
        circleline.remove()
        circleline = None
        canvas.draw()
        root.update()

# Swap node colors with animation
def swap_and_animate(node1, node2):
    # Colors before swap
    c1 = mcolors.to_rgba(node_colors[node1])
    c2 = mcolors.to_rgba(node_colors[node2])
    # Flash animation
    edge_indices = list(G.edges)
    print(edge_indices)
    edge_flash = False
    if (node1, node2) in edge_indices:
        ide1 = edge_indices.index((node1, node2))
        edge_flash = True
    elif (node2, node1) in edge_indices:
        ide1 = edge_indices.index((node2, node1))
        edge_flash = True
    else:
        pass
    node_indices = list(G.nodes)
    idx1 = node_indices.index(node1)
    idx2 = node_indices.index(node2)

    for _ in range(2):
        nodes._facecolors[idx1] = (1, 1, 1, 1)
        nodes._facecolors[idx2] = (1, 1, 1, 1)
        if edge_flash:
            edges._edgecolors[ide1] = (0, 1, 1, 0)
        #fig.canvas.draw_idle()
        canvas.draw()
        root.update()
        root.after(100)
        #time.sleep(0.1)
        #plt.pause(0.1) #this will render the figure in a new window
        nodes._facecolors[idx1] = c1
        nodes._facecolors[idx2] = c2
        if edge_flash:
            edges._edgecolors[ide1] = (0, 0, 0, 1)
        canvas.draw()
        root.update()
        root.after(100)
        #fig.canvas.draw_idle()
        #plt.pause(0.1)
        #time.sleep(0.1)

    # Swap colors
    node_colors[node1], node_colors[node2] = node_colors[node2], node_colors[node1]
    update_node_colors()
    # Remove outline
    remove_selection_outline()

# Reset function
def reset(event):
    global node_colors
    node_colors = original_node_colors.copy()
    clicked_nodes.clear()
    remove_selection_outline()
    update_node_colors()

# Add reset button
reset_ax = plt.axes([0.4, 0.05, 0.2, 0.2])#075])
reset_button = Button(reset_ax, 'Reset Colors')
reset_button.on_clicked(reset)

# add close window button 
def close_window(event):
    # note you need to close both matplotlib and tkinter 
    plt.close()
    root.destroy()

# Add close window button
close_ax = plt.axes([0.1, 0.05, 0.2, 0.1])#075])
close_button = Button(close_ax, 'close window')
close_button.on_clicked(close_window)

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
def on_click(event):
    # records coordinates in text box
    if event.inaxes == ax:
        x, y = event.xdata, event.ydata
        text_widget.insert(tk.END, f"Clicked at: ({x:.2f}, {y:.2f})\n")
        text_widget.see(tk.END)  # Auto-scroll to bottom
    if event.inaxes != ax:
        return
    x_click, y_click = event.xdata, event.ydata
    for i, (node, (x, y)) in enumerate(pos.items()):
        dx, dy = x - x_click, y - y_click
        if (dx**2 + dy**2)**0.5 < 0.1:
            text_widget.insert(tk.END, f"Clicked a node\n")
            clicked_nodes.append(node)
            print('clicked nodes:', clicked_nodes)
            if len(clicked_nodes) == 1:
                print('drawing outline')
                draw_selection_outline(node)
            if len(clicked_nodes) >= 2:
                print('clicked nodes have length 2')
                swap_and_animate(clicked_nodes[0], clicked_nodes[1])
                clicked_nodes.clear()
            break
    print(' ')

# Connect click event
canvas.mpl_connect("button_press_event", on_click)

# Start the Tkinter event loop

root.mainloop()
print("Application closed.") # This will print after root.destroy() is called

