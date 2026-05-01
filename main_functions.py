import os 
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
from markdown import markdown
from tkhtmlview import HTMLLabel
from matplotlib.widgets import Button
import matplotlib.colors as mcolors
import matplotlib.patches as patches
import time
import numpy as np
from matplotlib.transforms import Affine2D
import copy 

def is_identity(permutation_dictionary):
    for i in permutation_dictionary:
        if permutation_dictionary[i] != i:
            return False
    return True

def open_markdown(root, md_path):
    #md_path = "example.md"
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

# creating a line to edges mapping for the animation


def get_edges(node1, node2, line_to_edge_dict, lines):
    print('line to edge dict')
    print(line_to_edge_dict)
    print('getting edges for nodes', node1, node2)
    for line in lines:
        if node1 in line and node2 in line:
            break # by the axioms of projective geometry, this will always break
    edges = line_to_edge_dict[line]
    return edges, line

def epsilon(node_label):
    if node_label > 9:
        epsx = 0.13
    else:
        epsx = 0.07
    epsy = 0.07
    return np.array([epsx, epsy])

def move_label_location(node_1, node_2, label_node_map, vertex_dict, label_dict, canvas, ax, root):
    """
    takes the counter at node_1, moves it to node 2
    """
    label_node_map[node_1] # get the label value of node 1

    node_1_coords = vertex_dict[node_1].center

    node_2_coords = vertex_dict[node_2].center
    label_value_1 = label_node_map[node_1] # get the label value of node 1
    eps = epsilon(label_value_1)
    coords = np.array([node_2_coords[0],node_2_coords[1]]) - eps
    patch1 = label_dict[label_value_1] # get the corresponding path patch object
    patch1.set_transform(Affine2D().translate(*coords) + ax.transData) # move the label at node_1 to node_2's location
    canvas.draw()
    root.update()
    
    pass

def swap_node_labels_and_colors(node_1, node_2, label_node_map, vertex_dict, label_dict, canvas, ax, root):
    # move label 2 to node1's location
    node_1_coords = vertex_dict[node_1].center
    label_value_2 = label_node_map[node_2] # get the label value of node 2
    eps = epsilon(label_value_2)
    coords = np.array([node_1_coords[0],node_1_coords[1]]) - eps
    patch2 = label_dict[label_value_2] # get the corresponding path patch object
    patch2.set_transform(Affine2D().translate(*coords) + ax.transData) # move the label at node_2 to node 1's location
    canvas.draw()
    root.update()

    # move label 2 to node1's location
    node_2_coords = vertex_dict[node_2].center
    label_value_1 = label_node_map[node_1] # get the label value of node 1
    eps = epsilon(label_value_1)
    coords = np.array([node_2_coords[0],node_2_coords[1]]) - eps
    patch1 = label_dict[label_value_1] # get the corresponding path patch object
    patch1.set_transform(Affine2D().translate(*coords) + ax.transData) # move the label at node_1 to node_2's location
    canvas.draw()
    root.update()
    """
    node_2_coords = vertex_dict[node_2][0].center
    # New transforms (swap positions)
    patch1.set_transform(Affine2D().translate(*pos2) + ax.transData)
    patch2.set_transform(Affine2D().translate(*pos1) + ax.transData)
    node_1_text = vertex_dict[node_1][1]
    original_path = node_1_text.get_path()

    node_2_coords = vertex_dict[node_2][0].center
    node_2_text = vertex_dict[node_1][1]

    path1 = node_1_text.get_path()
    path2 = node_2_text.get_path() 

    v1 = path1.vertices.copy()
    v2 = path2.vertices.copy()  

    node_1_text.set_path(type(path1)(v2, path2.codes))
    node_2_text.set_path(type(path2)(v1, path1.codes))
    
    
    path1 = node_1_text.get_path()
    path2 = node_2_text.get_path()

    v1 = path1.vertices.copy()
    v2 = path2.vertices.copy()

    node_1_text.set_path(type(path1)(v2, path2.codes))
    node_2_text.set_path(type(path2)(v1, path1.codes))

    translate_21 = np.array(node_1_coords) - np.array(node_2_coords)
    translate_12 = np.array(node_2_coords) - np.array(node_1_coords)


    transform21 = Affine2D().translate(translate_21[0], translate_21[1]) + ax.transData
    node_1_text.set_transform(transform21)
    transformed_path = node_1_text.get_path()

    transform12 = Affine2D().translate(translate_12[0], translate_12[1]) + ax.transData
    node_2_text.set_transform(transform12)

    node_1_text_copy = copy.deepcopy(node_1_text)
    #vertex_dict[node_1][1] = node_2_text
    #vertex_dict[node_2][1] = node_1_text_copy

    """
    # swap the colors 
    face_color_1 = vertex_dict[node_1].get_facecolor()
    edge_color_1 = vertex_dict[node_1].get_edgecolor()
    face_color_2 = vertex_dict[node_2].get_facecolor()
    edge_color_2 = vertex_dict[node_2].get_edgecolor()

    vertex_dict[node_1].set_facecolor(face_color_2)
    vertex_dict[node_1].set_edgecolor(edge_color_2)
    vertex_dict[node_2].set_facecolor(face_color_1)
    vertex_dict[node_2].set_edgecolor(edge_color_1)

    # swap the labels in the label list 
    label_copy = label_node_map[node_1]
    label_node_map[node_1] = label_node_map[node_2]
    label_node_map[node_2] = label_copy
    canvas.draw()
    root.update()


def set_permutation(permutation, label_node_map, vertex_dict, label_dict, root, canvas, ax):
    """
    Docstring for set_permutation
    Function that changes the M13 plot so that the labels are assigned based on a permutation inputted by the user. 
    
    :param permutation: Description
    :param vertex_dict: Description
    :param label_dict: Description
    :param root: Description
    :param canvas: Description
    :param ax: Description
    """
    # make a copy of the label_dict
    for node in vertex_dict:
        # get the original color of the vertex 
        label_node_map[node] = permutation[node]
    canvas.draw()
    root.update()

    pass

# Swap node colors with animation
def swap_and_animate(node1, node2, label_node_map, vertex_dict, edge_dict, label_dict, lines, root, canvas, ax, line_to_edge_dict, edge_flash = True):
    # find the edges 
    flashing_edges, flashing_nodes = get_edges(node1, node2, line_to_edge_dict, lines)
    print('line in the projective plane', flashing_nodes)
    for _ in range(2):
        # m
        if edge_flash:
            for edge in flashing_edges:
                edge.set_visible(False)
        #fig.canvas.draw_idle()
        canvas.draw()
        root.update()
        root.after(50)
        #time.sleep(0.1)
        #plt.pause(0.1) #this will render the figur ein a new window
        if edge_flash:
            for edge in flashing_edges:
                edge.set_visible(True)
        canvas.draw()
        root.update()
        root.after(50)
        #fig.canvas.draw_idle()
        #plt.pause(0.1)
        #time.sleep(0.1)

    """
    # Swap colors
    node_colors[node1], node_colors[node2] = node_colors[node2], node_colors[node1]
    update_node_colors()
    # Remove outline
    remove_selection_outline()
    """
    flashing_nodes = list(flashing_nodes)
    flashing_nodes.remove(node1)
    flashing_nodes.remove(node2)

    swap_node_labels_and_colors(node1, node2, label_node_map, vertex_dict, label_dict, canvas, ax, root)
    swap_node_labels_and_colors(flashing_nodes[0], flashing_nodes[1], label_node_map, vertex_dict, label_dict, canvas, ax, root)





# function to close the window
def close_window(root):
    # note you need to close both matplotlib and tkinter 
    plt.close()
    root.destroy()