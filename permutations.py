import numpy as np
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics import Polyhedron
import itertools
import sys
np.set_printoptions(threshold=sys.maxsize)
#Consider 4 by 5 matrix, [] 12 edges
n = 8
permutation_array = np.arange(0,n,1)
# permutation_array1 = permutation_array.copy()
# permutation_array1[0]= permutation_array[1]
# permutation_array1[1]= permutation_array[0]
# permutation_array2 = permutation_array.copy()
# permutation_array2=np.roll(permutation_array2,-1)
# F = Permutation(permutation_array1)
# G = Permutation(permutation_array2)
# G1 = PermutationGroup(F,G)
# group_elements = list(G1.generate_dimino(af=True))
# print(group_elements)
# print(len(group_elements))

permutations = list(itertools.permutations(permutation_array))
print(len(permutations))