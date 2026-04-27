import numpy as np
 
# define the permutation class
def tuple_order(t1, t2):
    for i in range(len(t1)):
        if t1[i]< t2[i]:
            return True
        elif t1[i]> t2[i]:
            return False
    return False

class permutation:
    def __init__(self, arr):
        is_list_of_tuples = isinstance(arr, list) and all(isinstance(item, tuple) for item in arr)

        for i in range(len(arr)):
            if i not in arr:
                raise Exception('Inputs needs to be an array of the integers 0 through to N')
        self.arr = tuple(arr)
        self.len = len(arr)

    @staticmethod
    def cyclic_notation_to_array(cyclic_notation, n):
        arr = list(range(n))
        for cycle in cyclic_notation:
            for i in range(len(cycle)):
                arr[cycle[i]] = cycle[(i + 1) % len(cycle)]
        return arr
        
    def inv(self):
        return permutation([self.arr.index(i) for i in range(self.len)])

    def __repr__(self):
        return f"permutation({self.arr})"

    def __mul__(self, other):
        """Handles operations like vector * scalar or vector * vector"""
        if isinstance(other, permutation) and self.len == other.len:
            # Scalar multiplication
            return permutation([other.arr[self.arr[i]] for i in range(self.len)])
        elif isinstance(other, int):
            pass
        elif self.len != other.len:
            raise ValueError('input permutations must be of the same length')
        else:
            return NotImplemented # Signal Python to try __rmul__ on the other operand's type
        
    def __eq__(self, other):
        if not isinstance(other, permutation):
            return NotImplemented
        return self.arr == other.arr
    
    def __hash__(self):
        # Combine hashable attributes into a tuple and hash the tuple
        return hash((self.arr, self.len))
    
    def __lt__(self, other):
        if not isinstance(other, permutation):
            return NotImplemented
        # Define the primary sorting order: age, then grade, then name
        return tuple_order(self.arr, other.arr)
    
    def __le__(self, other):
        """
        Defines the behavior for the less than or equal to (<=) operator.
        Compares students based on their 'score' attribute.
        """
        if isinstance(other, permutation):
            return tuple_order(self.arr, other.arr) or self.arr == other.arr
        else:
            # Optional: handle cases where 'other' is not a Student instance
            # by raising an error or returning NotImplemented.
            return NotImplemented

def identity(n):
    X = list(range(n))
    return permutation(X)

def create_supergenerator(generators, n = 13, t = 4):
    """
    Docstring for create_supergenerators
    
    :param generators: Description
    :param n: Length of the word we are searching for 
    :param t: number of supergenerators we search over
    """
    # compose n/t generators from our generator set to obtain L1
    # dictionary of words from the generator words in the generator set indexed by permutations
    L = {}
    q = max(generators[0].arr) # number of elements we are permuting
    e = permutation(list(range(q+1))) # creates the identity permutation. 
    
    L[e] = []
    nt = n//t 
    e*generators[1]
    perms_to_check = []
    perms_to_check.append(e)
    checked_perms = [e]

    for i in range(len(generators)):
        # appends the inverses of the generators 
        generators.append(generators[i].inv())

    for j in range(nt):# goes through the words of length up to nt 
        new_perms = []
        for p in perms_to_check:
            for i in range(len(generators)):
                new_perm = generators[i]*p
                if new_perm in checked_perms:
                    pass
                else:
                    L[new_perm] = L[p] + [i]
                    checked_perms.append(new_perm)
                    new_perms.append(new_perm)
        perms_to_check = new_perms
    return dict(sorted(L.items(), reverse=False)), generators



generators = [permutation([11,0,1,2,3,4,5,6,7,8,9,10]),
              permutation([9,4,6,7,1,8,2,3,5,0,11,10]),
              permutation([0,9,3,2,8,6,5,7,4,1,10,11])]

L, generators = create_supergenerator(generators)
g = permutation([5,2,8,3,0,1,4,7,6,9,10,11])
g = g