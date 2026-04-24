"""
Docstring for Shamir_algorithm
Implementation 
"""

class permutation:
    def __init__(self, arr):
        for i in range(len(arr)):
            if i not in arr:
                raise Exception('Inputs needs to be an array of the integers 0 through to N')
        self.arr = list(arr)
        self.len = len(arr)

    def __repr__(self):
        return f"permutation({self.arr})"

    def __mul__(self, other):
        """Handles operations like vector * scalar or vector * vector"""
        if isinstance(other, permutation) and self.len == other.len:
            # Scalar multiplication
            return permutation([self.arr[other[i]] for i in range(self.len)])
        else:
            return NotImplemented # Signal Python to try __rmul__ on the other operand's type

class Node(object):
    def __init__(self, data):
        self.data = data
        self.depth = 0
        self.children = []

    def add_child(self, obj):
        self.children.append(obj)


def permutation_tree(generators, nt):
    pass

def compose_permutation_tree(generators, nt):
    pass



def create_supergenerator(generators, n = 20, t = 4):
    """
    Docstring for create_supergenerators
    
    :param generators: Description
    :param n: Length of the word we are searching for 
    :param t: number of supergenerators we search over
    """
    # compose n/t generators from our generator set to obtain L1
    # dictionary of words from the generator words in the generator set indexed by permutations
    L = {}
    q = max(generators[0]) # numbe rof elements we are permuting
    e = permutation(list(range(N)))
    L[permutation(e)] = []
    nt = n//t 

    new_perms = []
    new_perms.append(e)

    for i in generators:
        # appends the inverses of the generators 
        generators.append(i.inv())

    for _ in range(nt):
        # goes through the words of length nt 
        for p in new_perms:
            for i in range(len(generators)):
                new_perm = p*generators[i]
                if new_perm not in L.keys():
                    L[new_perm] = L[p] + [i]
                pass
        for p in L.keys():
            
            pass
        pass
    pass


def solve_t_list(generators, g, t = 4):
    
    pass

if __name__ == '__main__':
    # generators of the M12 group
    generators = [(11,0,1,2,3,4,5,6,7,8,9,10),
                  (9,4,6,7,1,8,2,3,5,0,11,10),
                  (0,9,3,2,8,6,5,7,4,1,10,11)]
    create_supergenerators(generators)