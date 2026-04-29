import numpy as np 
import matplotlib.pyplot as plt 
import math 
from matplotlib.textpath import TextPath
from matplotlib.patches import PathPatch
from matplotlib.transforms import Affine2D
from permutation import * 
from projective_plane import straight_line


def PG23_rotationally_symmetric():
    """
    Draws the rotaionally symmetric projective plane PG(2,3)

    inputs: none
    outputs:
        -fig:The top-level container for all plot elements. Think of it as the canvas or window that holds everything.
        -ax: The actual plotting area or "cell" where data is drawn. Despite the plural name, an Axes object refers to
             a single individual plot within the figure. It contains the x and y axes, title, labels, and the plotted 
             data points.
        -label_node_map: dictionary indexed by the nodes (0 to 12), and the objects are the labels assigned the nodes (also 
            the integers 0 to 12). This dictionary gets permuted as we solve the puzzle. 
        -vertex_dict: A dictionary indexed by the nodes (i.e. 0 to 12) the objects are the circles given by the 
            "circle = plt.Circle()" command
        -edge_dict: A dictionary of dictionaries indexed by nodes and the internal dictionaries are also indexed by nodes. 
            The objects of the dictionary are the lines creates by commands like 
            ax.plot(b_curve[0,:], b_curve[1,:], color="black", linestyle="-")
        -label_dict: dictionary indexed by nodes whose objects are the text patches created with the "text_patch()" command 
        -lines: list of the lists used in the projective plane lines[0] = [0,1,5,11] (Jacob Seihler's enumeration)
        -line_to_edge_dict: dictionary indexed by the lines (i.e. tuples of the form (0,1,5,11)) whose objects are lists of the 
         edges (i.e. the lines created by the ax.plot() command) that are relevant to that line in the projective plane. 
         We use this to determine which edges to flash when we click on a node in the interactive visualization.
    """

    # initialises the figure 
    fig, ax = plt.subplots()  

    label_node_map = {i:i for i in range(13)}
    vertex_dict = {}
    label_dict = {}
    line_to_edge_dict = {}  

    # storing the edges in a dictionary of dictionaries
    edge_dict = {}
    for i in range(13):
        edge_dict[i] = {}

    # vertex coordinates 
    r = 2 # radius of circle for node placement
    vertex_coordinates = {}
    for i in range(13):
        angle = np.pi * (-2*i / 13 + 1/2) # angle for node placement, the 1/2 is to rotate the whole thing by 90 degrees so that node 0 is at the top
        vertex_coordinates[i] = np.array((r * np.cos(angle), r * np.sin(angle)))

    # label coordinates, which are slightly shifted from the vertex coordinates so that the labels are not on top of the vertices.
    r = 2.4 # radius of circle for node placement
    label_coordinates = {}
    for i in range(13):
        angle = np.pi * (-2*i / 13 + 1/2) # angle for node placement, the 1/2 is to rotate the whole thing by 90 degrees so that node 0 is at the top
        label_coordinates[i] = np.array((r * np.cos(angle), r * np.sin(angle)))

    for i in vertex_coordinates:
        print(i, vertex_coordinates[i])

    # the intermediate nodes are the midpoints of the edges between the vertices. We will use these to plot the lines in the projective plane.
    intermediate_coordinates = {}
    for i in range(13):
        intermediate_coordinates[i] = (vertex_coordinates[i] + vertex_coordinates[(i+1)%13])/2

    # replacing the lines from the above Seihler's enumeration 
    lines = []
    for i in range(13):
        lines.append((i, (i+1)%13, (i+5)%13, (i-2)%13))
    

    for line in lines:
        edge_list = []
        # plot the edges relevant to the line
        # line between point line[0] and point line[1]
        p0 = line[0]
        p1 = line[1]
        b_line = straight_line(p0, p1, vertex_coordinates1=vertex_coordinates, vertex_coordinates2=vertex_coordinates)
        plotted_line, = ax.plot(b_line[0], b_line[1], color="black", linestyle="-")
        min_node = min(line[0], line[1])
        max_node = max(line[0], line[1])    
        edge_dict[min_node][max_node] = plotted_line
        edge_list.append(plotted_line)

        # plot the lines from the intermediate node between line[0] and line[1] to line[2] and line[3]
        p_intermediate = line[0]
        p2 = line[2]
        b_line = straight_line(p_intermediate, p2, vertex_coordinates1=intermediate_coordinates, vertex_coordinates2=vertex_coordinates)
        plotted_line, = ax.plot(b_line[0], b_line[1], color="black", linestyle="-")
        min_node = min(line[0], line[2])
        max_node = max(line[0], line[2])    
        edge_dict[min_node][max_node] = plotted_line
        edge_list.append(plotted_line)

        p3 = line[3]
        b_line = straight_line(p_intermediate, p3, vertex_coordinates1=intermediate_coordinates, vertex_coordinates2=vertex_coordinates)
        plotted_line, = ax.plot(b_line[0], b_line[1], color="black", linestyle="-")
        min_node = min(line[0], line[3])
        max_node = max(line[0], line[3])    
        edge_dict[min_node][max_node] = plotted_line
        edge_list.append(plotted_line)

        line_to_edge_dict[line] = edge_list
        
    # plot the vertices and labels
    mapping = list(range(13)) 
    # optional permutation if we wish to plot the labels in a different order. By default, the labels are plotted in the same order as the nodes 
    # (i.e. label 0 is plotted at node 0, label 1 at node 1, etc.)
    for vertex in vertex_coordinates.keys():
        if vertex == 0:
            circle = plt.Circle(
                        (vertex_coordinates[vertex][0],vertex_coordinates[vertex][1]),      # centre coordinates (x, y)
                        radius=0.15,      # Radius
                        facecolor= 'white',   # Fill color
                        edgecolor='red',   # Outline color
                        linewidth=2,      # Outline width
                        zorder = 24,       # plots the circle on top
                        label = 'asdf'
                    )

        else:
            circle = plt.Circle(
                        (vertex_coordinates[vertex][0],vertex_coordinates[vertex][1]),      # centre coordinates (x, y)
                        radius=0.15,      # Radius
                        facecolor='black',   # Fill color
                        edgecolor='black',   # Outline color
                        linewidth=2,      # Outline width
                        zorder = 24,      # plots the circle on top
                        label = 'asdf'
                    )
        ax.add_patch(circle)

        # plotting the intermediate circle here. 
        intermediate_circle = plt.Circle(
                        (intermediate_coordinates[vertex][0],intermediate_coordinates[vertex][1]),      # centre coordinates (x, y)
                        radius=0.05,      # Radius
                        facecolor= 'black',   # Fill color
                        edgecolor='black',   # Outline color
                        linewidth=2,      # Outline width
                        zorder = 24,       # plots the circle on top
                        label = 'asdf'
                    )
        ax.add_patch(intermediate_circle)

        #label = ax.annotate(str(vertex), xy=(vertex_coordinates[vertex][0],vertex_coordinates[vertex][1]), fontsize=5, fontweight='bold', ha="centre", color = 'white', zorder =30)
        if mapping[vertex] > 9:
            epsx = 0.13
        else:
            epsx = 0.07
        epsy = 0.07
        coords = np.array([vertex_coordinates[vertex][0],vertex_coordinates[vertex][1]]) - np.array([epsx, epsy])
        
        # altered this line to plot labels in the Siehler enumeration.
        # change made 27/4/26
        text = TextPath((0,0), str(mapping[vertex]), size = 0.2)
        trans = Affine2D().translate(*coords)
        """
        # Get bounding box of tex
        bbox = text.get_extents()
        # Compute centre of the text
        cx = (bbox.x0 + bbox.x1) / 4
        cy = (bbox.y0 + bbox.y1) / 4
        shifted_coords = coords + np.array(-cx, -cy)
        transform = (
                Affine2D()
                .translate(shifted_coords[0], 0)   # centre text geometry
                + ax.transData
            )
        text_patch = PathPatch(text, transform = transform, color='white', zorder = 30)
        """
        text_patch = PathPatch(text, color='white', transform=trans + ax.transData, zorder = 30)
        if vertex == 0:
            print('setting invisible')
            text_patch.set_visible(False)
        ax.add_patch(text_patch)
        vertex_dict[vertex] = circle
        label_dict[vertex] = text_patch
        label_node_map[vertex] = vertex

        # plotting the original labels 
        coords = np.array([label_coordinates[vertex][0],label_coordinates[vertex][1]]) - np.array([epsx, epsy])
        text = TextPath((0,0), str(vertex), size = 0.2)
        trans = Affine2D().translate(*coords)
        text_patch = PathPatch(text, color='red', transform=trans + ax.transData, zorder = 30)
        ax.add_patch(text_patch)


    print('vertex dict')
    for i in vertex_dict:
        print(i, vertex_dict[i])
    print(' ')
    print('edge dict')
    for i in edge_dict:
        for j in edge_dict[i]:
            print(i, j, edge_dict[i][j])
    print(' ')
    print('label dict')
    for i in label_dict:
        print(i, label_dict[i]) 
    print(' ')
    print('line to edge dict')
    for i in line_to_edge_dict:
        print(i, line_to_edge_dict[i])
    return fig, ax, label_node_map, vertex_dict, edge_dict, label_dict, lines, line_to_edge_dict


if __name__ == "__main__":
    fig, *_ = PG23_rotationally_symmetric()
    plt.show()