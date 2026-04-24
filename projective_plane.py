"""
Scripts used to plot the PG(2,3) projective plane. 

0 1 2 3
0 4 5 6
0 8 9 12
0 7 10 11
1 4 7 8
1 6 9 11
1 5 10 12
3 4 9 10
2 4 11 12
2 5 7 9
3 6 7 12
3 5 8 11
2 6 8 10
"""
import numpy as np 
import matplotlib.pyplot as plt 
import math 
from matplotlib.textpath import TextPath
from matplotlib.patches import PathPatch
from matplotlib.transforms import Affine2D

# vertex coords
r = 3
vertex_coordinates = {0:(r, 0),
                      1:(-1, 1),
                      2:(0, 1),
                      3:(1,1),
                      4:(-1, 0),
                      5:(0, 0),
                      6:(1, 0),
                      7:(-1, -1),
                      8:(0, -1),
                      9:(1, -1),
                      10:(-r/np.sqrt(2), -r/np.sqrt(2)),
                      11:(0, -r),
                      12:(r/np.sqrt(2), -r/np.sqrt(2))}

def parabola(point1, point2, direction = np.array([1,-1]), c = 0.6, n_points = 100): 
    # rotate things so direction is the new y axis
    d_norm = direction/np.linalg.norm(direction)
    d_right = np.array([[0,1],[-1,0]])@d_norm
    r_mat = np.array([d_right, d_norm])
    print(r_mat)

    p1_coords = vertex_coordinates[point1]
    p1_coords_rotated = r_mat@np.array(p1_coords)

    p2_coords = vertex_coordinates[point2]
    p2_coords_rotated = r_mat@np.array(p2_coords)

    # sets up the linear system of equations for the coefficients of this parabola
    x1 = p1_coords_rotated[0]
    y1 = p1_coords_rotated[1]

    x2 = p2_coords_rotated[0]
    y2 = p2_coords_rotated[1]

    # this is the x_coordinate of the parabola's apex (in the rotated system of coordinates)
    x_crit = x1*c + x2*(1 - c)

    A = np.array([[x1**2, x1, 1],
                  [x2**2, x2, 1],
                  [2*x_crit, 1, 0]])
    b = np.array([y1, y2, 0])
    coefficients = np.linalg.inv(A)@b

    # take th
    x =  np.arange(np.min([x1,x2]),np.max([x1,x2]),np.abs(x1 - x2)/n_points)
    y = coefficients[0]*x**2 + coefficients[1]*x + coefficients[2]
    points = np.array([x,y])
    print(np.min([x1,x2]),np.max([x1,x2]),n_points)
    print('x', x)
    rotated_points = np.linalg.inv(r_mat)@points
    return rotated_points 


def Bezier_curve(P_list, N = 10):
    # parametrer _t
    N = len(P_list) - 1
    t = np.arange(0, 1, 0.02)
    t = np.append(t,1)
    T = len(t)

    T_mat = np.zeros((N + 1,T))
    for i in range(N + 1):
        T_mat[i][:] = math.comb(N, i)*t**i * (1 - t)**(N - i)

    P_mat = np.array(P_list).T
    b_curve = P_mat@T_mat 
    return b_curve 

def straight_line(index_1, index_2):
    return [[vertex_coordinates[index_1][0], vertex_coordinates[index_2][0]],[vertex_coordinates[index_1][1],vertex_coordinates[index_2][1]]]

def circle_arc(index_1, index_2, centre = np.array([0,0])):
    p1 = np.array(vertex_coordinates[index_1])
    p2 = np.array(vertex_coordinates[index_2])
    r = np.linalg.norm(p1 - centre)
    normalised_p1 = p1 - centre
    normalised_p2 = p2 - centre
    theta1 = np.arccos(normalised_p1[0]/r)*np.sign(normalised_p1[1])
    theta2 = np.arccos(normalised_p2[0]/r)*np.sign(normalised_p2[1])
    theta = np.linspace(theta1, theta2, 20)
    x_coords = centre[0] + r*np.cos(theta)
    y_coords = centre[1] + r*np.sin(theta)
    return [x_coords, y_coords]

# wrapping all this together into a function. 
def PG23():
    # returns
    """
    (vertices)
    - vertices: coordinates of teh
    - edges: doubly indexed dictionary of edges between vertices
    - lines: list of tuples of vert5ices that make up 
    """
    # initialises the figure 
    fig, ax = plt.subplots() 

    # storing the edges in a dictionary of dictionaries
    edge_dict = {}
    for i in range(13):
        edge_dict[i] = {}

    lines = []
    lines.append((1,6,8,10))
    lines.append((1,2,3,0))
    lines.append((1,5,9, 12))
    lines.append((1,4,7,11))
    lines.append((2,5,8,11))
    lines.append((3,5,7,10))
    lines.append((3,6,9,11))
    lines.append((4,5,6,0))
    lines.append((7,8,9,0))
    lines.append((9,2,4,10))
    lines.append((10,11,12,0))
    lines.append((3,4,8,12))
    lines.append((7,2,6,12))

    #  you want bezier edges between (2,7), (4,3), (1,6), (2,9)
    direction = np.array([-1,1])
    P_list = []
    r_1 = 2
    c = 0.8/np.sqrt(2)
    P_list.append(vertex_coordinates[7])
    P_list.append(vertex_coordinates[7] + (r_1+c)*direction)
    P_list.append(vertex_coordinates[2] + (r_1*direction))
    P_list.append(vertex_coordinates[2])
    b_curve = Bezier_curve(P_list)
    line, = ax.plot(b_curve[0,:], b_curve[1,:], color="black", linestyle="-")
    edge_dict[2][7] = line

    P_list = []
    r_1 = 2
    P_list.append(vertex_coordinates[4])
    P_list.append(vertex_coordinates[4] + (r_1+c)*direction)
    P_list.append(vertex_coordinates[3] + (r_1*direction))
    P_list.append(vertex_coordinates[3])
    b_curve = Bezier_curve(P_list)
    line, = ax.plot(b_curve[0,:], b_curve[1,:], color="black", linestyle="-")
    edge_dict[3][4] = line
    
    direction = np.array([1,1])
    P_list = []
    r_1 = 2
    P_list.append(vertex_coordinates[1])
    P_list.append(vertex_coordinates[1] + (r_1+c)*direction)
    P_list.append(vertex_coordinates[6] + (r_1*direction))
    P_list.append(vertex_coordinates[6])
    b_curve = Bezier_curve(P_list)
    line, = ax.plot(b_curve[0,:], b_curve[1,:], color="black", linestyle="-")
    edge_dict[1][6] = line

    P_list = []
    r_1 = 2
    P_list.append(vertex_coordinates[2])
    P_list.append(vertex_coordinates[2] + (r_1+c)*direction)
    P_list.append(vertex_coordinates[9] + (r_1*direction))
    P_list.append(vertex_coordinates[9])
    b_curve = Bezier_curve(P_list)
    line, = ax.plot(b_curve[0,:], b_curve[1,:], color="black", linestyle="-")
    edge_dict[2][9] = line


    # plotting one of the curved lines between 7 and 11
    P_list = []
    r_1 = 2
    P_list.append(vertex_coordinates[7])
    P_list.append(vertex_coordinates[7] + (2*r/4)*np.array([0,-1]))
    P_list.append(vertex_coordinates[11])
    b_curve = Bezier_curve(P_list)
    line, = ax.plot(b_curve[0,:], b_curve[1,:], color="black", linestyle="-")
    edge_dict[7][11] = line

    # plotting one of the curved lines between 9 and 11
    P_list = []
    r_1 = 2
    P_list.append(vertex_coordinates[9])
    P_list.append(vertex_coordinates[9] + (2*r/4)*np.array([0,-1]))
    P_list.append(vertex_coordinates[11])
    b_curve = Bezier_curve(P_list)
    line, = ax.plot(b_curve[0,:], b_curve[1,:], color="black", linestyle="-")
    edge_dict[9][11] = line

    # plotting one of the curved lines between 3 and 0
    P_list = []
    r_1 = 2
    P_list.append(vertex_coordinates[3])
    P_list.append(vertex_coordinates[3] + (2*r/4)*np.array([1,0]))
    P_list.append(vertex_coordinates[0])
    b_curve = Bezier_curve(P_list)
    line, = ax.plot(b_curve[0,:], b_curve[1,:], color="black", linestyle="-")
    edge_dict[0][3] = line

    # plotting one of the curved lines between 9 and 0
    P_list = []
    r_1 = 2
    P_list.append(vertex_coordinates[9])
    P_list.append(vertex_coordinates[9] + (2*r/4)*np.array([1,0]))
    P_list.append(vertex_coordinates[0])
    b_curve = Bezier_curve(P_list)
    line, = ax.plot(b_curve[0,:], b_curve[1,:], color="black", linestyle="-")
    edge_dict[0][9] = line

    # plotting one of the curved lines between 4 and 10
    P_list = []
    r_1 = 2
    P_list.append(vertex_coordinates[4])
    P_list.append(vertex_coordinates[4] + (0.4*r)*np.array([-1,-1]))
    P_list.append(vertex_coordinates[10])
    b_curve = Bezier_curve(P_list)
    line, = ax.plot(b_curve[0,:], b_curve[1,:], color="black", linestyle="-")
    edge_dict[4][10] = line

    # plotting one of the curved lines between 8 and 10
    P_list = []
    r_1 = 2
    P_list.append(vertex_coordinates[8])
    P_list.append(vertex_coordinates[8] + (0.4*r)*np.array([-1,-1]))
    P_list.append(vertex_coordinates[10])
    b_curve = Bezier_curve(P_list)
    line, = ax.plot(b_curve[0,:], b_curve[1,:], color="black", linestyle="-")
    edge_dict[8][10] = line

    # plotting one of the curved lines between 8 and 12
    P_list = []
    r_1 = 2
    P_list.append(vertex_coordinates[8])
    P_list.append(vertex_coordinates[8] + (0.4*r)*np.array([1,-1]))
    P_list.append(vertex_coordinates[12])
    b_curve = Bezier_curve(P_list)
    line, = ax.plot(b_curve[0,:], b_curve[1,:], color="black", linestyle="-")
    edge_dict[8][12] = line

    # plotting one of the curved lines between 6 and 12
    P_list = []
    r_1 = 2
    P_list.append(vertex_coordinates[6])
    P_list.append(vertex_coordinates[6] + (0.4*r)*np.array([1,-1]))
    P_list.append(vertex_coordinates[12])
    b_curve = Bezier_curve(P_list)
    line, = ax.plot(b_curve[0,:], b_curve[1,:], color="black", linestyle="-")
    edge_dict[6][12] = line


    # plotting the straightlines
    #(1,2)
    pair_list = [(1,2),(1,4),(1,5),(2,3),(2,4),(2,5),(2,6),(3,5),(3,6),(4,5),(4,7),(4,8),(5,6),(5,7),(5,8),(5,9),(6,8),(6,9),(7,8),(7,10),(8,9),(8,11),(9,12),(6,0)]
    for pair in pair_list:
        p0 = min(pair)
        p1 = max(pair)
        b_line = straight_line(p0, p1)
        line, = ax.plot(b_line[0], b_line[1], color="black", linestyle="-")
        edge_dict[p0][p1] = line

    # plotting the circular arc lines 
    index_1, index_2 = 10, 11
    x_coords, y_coords = circle_arc(index_1, index_2)
    line, = ax.plot(x_coords, y_coords, color="black", linestyle="-")
    edge_dict[index_1][index_2] = line

    index_1, index_2 = 11, 12
    x_coords, y_coords = circle_arc(index_1, index_2)
    line, = ax.plot(x_coords, y_coords, color="black", linestyle="-")
    edge_dict[index_1][index_2] = line

    index_1, index_2 = 0, 12
    x_coords, y_coords = circle_arc(index_1, index_2)
    line, = ax.plot(x_coords, y_coords, color="black", linestyle="-")
    edge_dict[index_1][index_2] = line
    
    # plotting the points
    vertex_dict = {}
    label_dict = {}
    label_node_map = {}
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
        #label = ax.annotate(str(vertex), xy=(vertex_coordinates[vertex][0],vertex_coordinates[vertex][1]), fontsize=5, fontweight='bold', ha="centre", color = 'white', zorder =30)
        if vertex > 9:
            epsx = 0.13
        else:
            epsx = 0.07
        epsy = 0.07
        coords = np.array([vertex_coordinates[vertex][0],vertex_coordinates[vertex][1]]) - np.array([epsx, epsy])
        text = TextPath((0,0), str(vertex), size = 0.2)
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

    return fig, ax, label_node_map, vertex_dict, edge_dict, label_dict, lines 

def draw_PG23_conway_layout():
    pass

if __name__ == "__main__":
    fig, *_ = PG23()
    plt.show()