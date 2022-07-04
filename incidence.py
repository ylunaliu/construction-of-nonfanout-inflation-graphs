from turtle import shape
from autoray import numpy
import networkx as nx 
import numpy as np
import scipy.sparse
import pandas as pd
from nonfanout import make_switching_vector
 #example2: Instrumental graph
instrumental = nx.DiGraph()
instrumental.add_edges_from([("A1", "D1"), ("D1", "B1"), ("U1", "D1"), ("U1", "B1")])
instrumental_hidden = list(["U1"])
# incidence_instrumental = scipy.sparse.coo_matrix(nx.incidence_matrix(instrumental,nodelist=instrumental.nodes, edgelist=instrumental.edges,oriented=True))

# Generate the incidence matrix
incidence_instrumental_dense_q1 = scipy.sparse.csr_matrix.todense(nx.incidence_matrix(instrumental,nodelist=instrumental.nodes, edgelist=instrumental.edges,oriented=True))
# The second copy of the incidence matrix
incidence_instrumental_q4 = incidence_instrumental_dense_q1.copy()
# Get the shape of the incidence matrix
shape_incidence_original = np.shape(incidence_instrumental_dense_q1)
incidence_adjust_q3 = np.zeros((shape_incidence_original[0], shape_incidence_original[1]))
incidence_adjust_q2 = np.zeros((shape_incidence_original[0], shape_incidence_original[1])) 
#I need to expand the matrix
# Get the index of non_zero value in the incidence matrix
index = np.array(incidence_instrumental_dense_q1.nonzero())

def rewiring_given_switching_vector(incidence_instrumental_dense_q1, switching_vector):
    q1_new = incidence_instrumental_dense_q1.copy()
    shape_incidence_original = np.shape(incidence_instrumental_dense_q1)
    q2 = np.zeros((shape_incidence_original[0], shape_incidence_original[1])) 
    q3 = np.zeros((shape_incidence_original[0], shape_incidence_original[1])) 
    q4 = incidence_instrumental_dense_q1.copy()
    index = np.array(incidence_instrumental_dense_q1.nonzero())
    counter = 0
    for i in range(len(index[0])):
        if(incidence_instrumental_dense_q1[index[:,i][0], index[:,i][1]]==1):
            if(switching_vector[counter]==1):
                q1_new[index[:,i][0], index[:,i][1]]=0
                q2[index[:,i][0], index[:,i][1]] = 1
                q4[index[:,i][0], index[:,i][1]]=0
                q3[index[:,i][0], index[:,i][1]]=1
            counter+=1
    
    new_incidence = np.vstack((q1_new, q3))
    new_incidence2 = np.vstack((q2, q4))
    final = np.hstack((new_incidence, new_incidence2))
    return final

for switching_vector in make_switching_vector(len(instrumental.edges)):
    print(f"This is the switching vector {switching_vector}")
    incidence_new = rewiring_given_switching_vector(incidence_instrumental_dense_q1, switching_vector)
    print(f"This is the new incidence matrix\n{incidence_new}")

# print(rewiring_given_switching_vector(incidence_instrumental_dense_q1, list([1,0,1,0])))