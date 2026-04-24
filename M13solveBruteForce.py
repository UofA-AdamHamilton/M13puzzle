import networkx as nx
import itertools
import copy 
import json 

def solve_M13(perm):
    """
    Docstring for solve_M13
    Function that calculates the inverse of a permutation 

    output: 
        node_list: a list of numbers between 0 and 12, such that you swap the empty node with the node at these positions
        label_list: a list of numbers between one and 
    
    :param perm: Description
    """
    pass

# define the complementary pair dictionary
def complementary_pair():
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
    complementary_pairs = {}
    for line in lines:
        permutations_iterator = itertools.permutations(line)
        for p in permutations_iterator:
            complementary_pairs[(p[0], p[1])] = (p[2], p[3])
    return complementary_pairs

def M13_graph():
    # initialiase the M13 graph
    G = nx.Graph()
    complete = False #set to true once every edge has been discovered. 
    G.add_node(tuple([0,1,2,3,4,5,6,7,8,9,10,11,12])) # initialises the 
    nodes_to_check = [[0,1,2,3,4,5,6,7,8,9,10,11,12]] # list of permutations that correspond to the nodes we wish to check
    complementary_pairs = complementary_pair()
    count = 0
    route_dict = {}
    depth_dict = {tuple([0,1,2,3,4,5,6,7,8,9,10,11,12]):0}
    max_depth = 0

    while nodes_to_check:
        current_node = nodes_to_check.pop(0)
        for i in range(13):
            found_new_node = False
            # swap the node labelled with 0 with the node at position i 
            loc = current_node.index(0)
            if loc == i:
                pass 
            else:
                node_copy = copy.copy(current_node)
                c = node_copy[loc]
                node_copy[loc] = node_copy[i]
                node_copy[i] = c

                # let a and b be the complementary pairs to i and 0's position
                # swap positions i and j

                a,b = complementary_pairs[(loc, i)]
                c = node_copy[a]
                node_copy[a] = node_copy[b]
                node_copy[b] = c

                if tuple(node_copy) in G.nodes():
                    pass
                else:
                    # These BFS edges to a new node appear in the tree of shortest paths so we add the link to the rout dictionary
                    # each entry to the dictionary is the location of entry with label 0 and the location and 
                    # value of the entry we  swap it with
                    depth_dict[tuple(node_copy)] = depth_dict[tuple(current_node)] + 1
                    if depth_dict[tuple(node_copy)] > max_depth:
                        max_depth = depth_dict[tuple(node_copy)]
                        print('new maximum depth', depth_dict[tuple(node_copy)])
                    route_dict[str(current_node)] = str(node_copy)
                    G.add_node(tuple(node_copy))
                    found_new_node = True
                    G.add_edge(tuple(current_node), tuple(node_copy))
                    nodes_to_check.append(node_copy)
        if not found_new_node:
            complete = True
        count += 1
    override = True
    if override:
        nx.write_gml(G, "M13_graph.gml")
    with open('data.json', 'w') as json_file:
        json.dump(route_dict, json_file, indent=4) # 'indent=4' makes the file human-readabl

    print(len(G.nodes()))
    print(len(G.edges()))

    pass


complementary_pair()
M13_graph()