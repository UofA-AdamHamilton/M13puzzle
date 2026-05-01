def find_maximum_seq(tree, seq, perm):
    max_seq = []
    next_dict = tree
    base = max(perm.arr)
    inv_perm = perm.inv().arr
    for i in range(len(seq)):
        for j in range(len(inv_perm)):
            j_entry = inv_perm[j]
            if j_entry in next_dict.keys():
                pass
            else:
                break
        max_seq.append(inv_perm[j - 1])
        next_dict = next_dict[inv_perm[j - 1]]
    return max_seq
    
def next_leaf_node(tree, perm, seq, maximum_seq = None, max_iterations = 1000000):
    """
    """
    if maximum_seq is None:
        maximum_seq = find_maximum_seq(tree, perm)
    index = [-1]
    found_entry = False
    copunt = 0
    while not found_path:
        seq = next_seq(seq, perm)
        if path_in_tree(tree, seq):
            return path, leaf_node
        if seq == maximum_seq:
            return 
        count += 1
        if count > max_iterations:
            return 
        


def next_seq(seq, perm):
    # maps the digits to the permutation
    # so apply the permutations inverse to every entry 
    for i in range(len(seq)):
        seq[i] = perm.inv().arr[seq[i]]
    # adds one  in this base 
    base = max(perm.arr) + 1
    seq = next_path(seq, base)
    # maps back
    for i in range(len(seq)):
        seq[i] = perm.arr[seq[i]]
    return seq

def path_in_tree(tree, path):
    next_dict = tree
    for i in path:
        if i in next_dict.keys():
            next_dict = next_dict[i]
        else:
            return False
    return True


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