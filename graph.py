# -*- coding: utf-8 -*-

import networkx as nx
import numpy as np

def generate_knn_graph(pdist, k):
    G = nx.Graph()
    for i,row in enumerate(pdist):
        nearest_neighbors = np.argsort(row)
        for neighbor in nearest_neighbors[1:k+1]:
            G.add_edge(i,neighbor)
    return G
    
def generate_gabriel_graph(pdist):
    #for every pair of nodes, see if anything 
    #is closer to both
    G = nx.Graph()
    for i,row in enumerate(pdist):
        for j,distance in enumerate(row):
            if i != j:
                for k in range(len(pdist)):
                    if pdist[i,k] < distance and pdist[j,k] < distance:
                        break
                else:
                    G.add_edge(i,j)
    return G
    
if __name__ == "__main__":
    import scipy.spatial
    values = np.array([[0,0],
                       [1,1],
                       [2,2],
                       [1,0],
                       [5,0]])
    pairs = scipy.spatial.distance.pdist(values)
    pdist = scipy.spatial.distance.squareform(pairs)
    
    print(generate_gabriel_graph(pdist).edges())
    print(generate_knn_graph(pdist, 2).edges())