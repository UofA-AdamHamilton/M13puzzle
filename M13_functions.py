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


# Update node colors
def update_node_colors(nodes, canvas):
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
def draw_selection_outline(node ,pos, canvas):
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
def remove_selection_outline(canvas, root):
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

    for _ in range(3):
        nodes._facecolors[idx1] = (1, 1, 1, 1)
        nodes._facecolors[idx2] = (1, 1, 1, 1)
        if edge_flash:
            edges._edgecolors[ide1] = (0, 1, 1, 0)
        #fig.canvas.draw_idle()
        canvas.draw()
        root.update()
        root.after(100)
        #time.sleep(0.1)
        #plt.pause(0.1) #this will render the figur ein a new window
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