from distutils.command import check
from venv import create
from os import dup
from platform import node
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import itertools
def split_anynode(node):
    """
    Descrption: used to split the node name

    Parameter:
    ------------
    node: str

    Return:
    ------------
    A list containing the first and the rest of the characters in the node.
    """
    first, rest = node[0], node[1:]
    return [first,rest]

def get_unique_index(nodes:list):
    """
    Descrption: get the unique index for a graph

    Parameter:
    ------------
    nodes: list of nodes

    Return:
    ------------
    A list contains the unique elements
    """
    empty_test = []
    for node in nodes:
        split_node = split_anynode(node)
        empty_test.extend(split_node[1])
    
    return(np.unique(np.array(empty_test).astype(int)))

def modify_copy_inflation(number_of_copy, unique_index, edges:list):
    """
    Description: get the new edges for a non-fanout inflation

    Parameter:
    ------------
    number_of_copy: The number of copy that you want to make the non-fanout inflation graph
    unique_index: A list contains the unique elements
    edges: The edges of the original graph

    Return:
    ------------
    all_new_edges: The new edges for a nonfanout inflated graph
    """
    number_of_index = len(unique_index) #get the number of index
    all_new_edges = []
    all_new_edges.extend(edges)
    for i in range(number_of_copy):
        copy_of_edges = np.array(edges.copy())
        new_edges = []    
        for each_pair in copy_of_edges:
            new_pair = []
            for each_node in each_pair:
                split_node = split_anynode(each_node)
                index = split_node[1]
                new_index = int(index) + (i+1)* number_of_index
                split_node[1]=new_index
                new_node_pair = [split_node[0]+ str(split_node[1])]
                new_pair.extend(new_node_pair)
            new_edges.append(tuple(new_pair))
        all_new_edges.extend(new_edges)
    return all_new_edges

def make_switching_vector(number_of_edges, unique_element=[0,1]):
    """
    Description: produces the switching vector for non-fanout inflation, TODO: This only works for 2 copies
                 1 means switch, 0 nmeans not switch

    Parameter:
    ------------
    number_of_edges: int, number of edges of the original graph

    Return:
    ------------
    all ways of making the switch
    """
    return(np.array(list(itertools.product(unique_element,repeat=number_of_edges))))

def generate_non_fanout_inflation_edges(non_fanout_edges, num_orginal_egdes:int, switching_vector, number_of_copy):
    """
    Description: produces all the possible non-fanout inflation(only edges but you can use edges to construct the graphs)

    Parameter:
    ------------
    non_fanout_edges: The edges for the non_fanout_graph (independent copy)
    num_orginal_egdes: number of edges of the original graph
    switching_vector: a list containg all the way to make the switch

    Return:
    ------------
    all_non_fanout: a list containg all edges for all possible way for non-fanout inflation
    """
    all_non_fanout = []
    for each_switching_vector in switching_vector:
        new = non_fanout_edges.copy()
        print(f"here is the switch vector{each_switching_vector}")
        print(f"here is the original egdes{new}")
        for index, switch in enumerate(each_switching_vector):
            if (switch==1):
                pair1 = new[index]
                pair2 = new[index + num_orginal_egdes]
                new_pair1, new_pair2 = switching_nodes(list(pair1), list(pair2))
                new[index] = new_pair1
                new[index + num_orginal_egdes] = new_pair2
        print(f"here is the edges after switching{new}")
        all_non_fanout.append(new)
        
    print(f"This is the number of possible non fanout inflation: {len(all_non_fanout)}")
    return all_non_fanout

def switching_nodes(pair1, pair2):
    node_pair1 = pair1[1]
    node_pair2 = pair2[1]

    pair1[1] = node_pair2
    pair2[1] = node_pair1

    return tuple(pair1), tuple(pair2)

if __name__ == "__main__": 
    ring_six_inflation = nx.DiGraph()
    ring_six_inflation.add_edges_from([("X1", "A1"), ("X1", "B1"), ("Y1", "B1"), ("Y1", "C1"), 
                                       ("Z1", "C1"), ("Z1", "A2"), ("X2", "A2"), ("X2", "B2"),
                                       ("Y2", "B2"), ("Y2", "C2"), ("Z2", "C2"), ("Z2", "A1")])
    ring_six_inflation_hidden = list(["X1", "X2", "Y1", "Y2", "Z1", "Z2"])

    edges = list(ring_six_inflation.edges)
    nodes = ring_six_inflation.nodes
    unique = get_unique_index(nodes)
    all_copy = modify_copy_inflation(1, unique, edges)
    switching_vector = make_switching_vector(len(edges))

    generate_non_fanout_inflation_edges(all_copy, len(edges), switching_vector,1)