import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import mplcursors
import matplotlib.colors as mcolors
import matplotlib.patches as patches
import time

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

# Draw graph
nodes = nx.draw_networkx_nodes(G, pos, ax=ax, node_color=[node_colors[n] for n in G.nodes])
edges = nx.draw_networkx_edges(G, pos, ax=ax, edge_color=[[0,0,0,1]]*len(list(G.edges)))
labels = nx.draw_networkx_labels(G, pos, ax=ax)

# Track clicked nodes and selected outline
clicked_nodes = []
selection_outline = None  # This will hold the patch

# Update node colors
def update_node_colors():
    nodes.set_color([node_colors[n] for n in G.nodes])
    fig.canvas.draw_idle()

# Add hover with label and highlight
#cursor = mplcursors.cursor(nodes, hover=True)
#@cursor.connect("add")
#def on_hover(sel):
#    node_index = sel.index
#    node2 = list(G.nodes)[node_index]
#    sel.annotation.set_text(f"Node {node2}")
#    sel.annotation.get_bbox_patch().set(fc="yellow")

# Function to draw red outline around first selected node
def draw_selection_outline(node):
    print('triggered draw')
    global selection_outline
    x, y = pos[node]
    outline = patches.Circle(
        (x, y), radius=0.07, edgecolor='red', facecolor='none', linewidth=3#, zorder=3
    )
    selection_outline = outline
    ax.add_patch(outline)
    fig.canvas.draw()  # <- Force immediate redraw here

# Remove the red outline
def remove_selection_outline():
    global selection_outline
    if selection_outline:
        selection_outline.remove()
        selection_outline = None
        #fig.canvas.draw_idle()
        fig.canvas.draw()

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
        fig.canvas.draw_idle()
        plt.pause(0.1)
        nodes._facecolors[idx1] = c1
        nodes._facecolors[idx2] = c2
        if edge_flash:
            edges._edgecolors[ide1] = (0, 0, 0, 1)
        fig.canvas.draw_idle()
        plt.pause(0.1)

    # Swap colors
    node_colors[node1], node_colors[node2] = node_colors[node2], node_colors[node1]
    update_node_colors()

    # Remove outline
    remove_selection_outline()

# On click: handle selection and swapping
def on_click(event):
    if event.inaxes != ax:
        return
    x_click, y_click = event.xdata, event.ydata
    for i, (node, (x, y)) in enumerate(pos.items()):
        print(i, node, x,y)
        dx, dy = x - x_click, y - y_click
        if (dx**2 + dy**2)**0.5 < 0.05:
            clicked_nodes.append(node)
            print('clicked nodes:', clicked_nodes)
            if len(clicked_nodes) == 1:
                draw_selection_outline(node)

            if len(clicked_nodes) >= 2:
                print('clicked nodes have length 2')
                swap_and_animate(clicked_nodes[0], clicked_nodes[1])
                clicked_nodes.clear()
            break
    print(' ')

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

# Connect mouse clicks
fig.canvas.mpl_connect("button_press_event", on_click)

# Finalize plot
plt.title("Hover to view, click two nodes to swap colors. Reset to restore.")
plt.gca().set_aspect('equal')
plt.axis('equal')
ax.set_aspect('equal', adjustable='box') # Key to making it a circle
plt.axis("off")
plt.show()
