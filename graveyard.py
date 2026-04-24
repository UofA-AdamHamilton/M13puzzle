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