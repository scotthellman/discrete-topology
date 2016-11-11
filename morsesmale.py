import networkx as nx
import numpy as np
import scipy
import graph

def generate_morse_smale(G, pdist, function_vals):
    #TODO: throw exception when 2 values are the same
    maxima, minima, ascent, descent = find_extrema(G, function_vals)
    max_labels = assign_extrema(G, maxima, ascent)
    min_labels = assign_extrema(G, minima, descent)
    
    return list(zip(min_labels, max_labels))
    
def assign_extrema(G, extrema, path):
    assignments = [0] * len(G.nodes())
    print(extrema)
    print(path)
    for node in G:
        traverser = node
        while traverser not in extrema:
            traverser = path[traverser]
        assignments[node] = traverser
    return assignments
    
def find_extrema(G, function_vals):
    ascent = {}
    descent = {}
    maxima = []
    minima = []
    for i,value in enumerate(function_vals):
        neighbors = np.array(G.neighbors(i))
        differences = np.array([function_vals[n] - value for n in neighbors]).T[0]
        ordered = np.argsort(differences)
        if np.all(differences < 0):
            maxima.append(i)
            ascent[i] = i
            descent[i] = neighbors[ordered[0]]
        elif np.all(differences > 0):
            minima.append(i)
            ascent[i] = neighbors[ordered[-1]]
            descent[i] = i
        else:
            ascent[i] = neighbors[ordered[-1]]
            descent[i] = neighbors[ordered[0]]
    return maxima, minima, ascent, descent
    

def get_filtrations(pdist, function_vals, k=2):
    if k is None:
        G = graph.generate_gabriel_graph(pdist)
    else:
        G = graph.generate_knn_graph(pdist, k)
    
    msc = generate_morse_smale(G, pdist, function_vals)
    filtrations = generate_filtrations(msc, G, function_vals)
    
    return filtrations
    
if __name__ == "__main__":
    import scipy.spatial
    values = np.array(range(20)).reshape(20,1)
    pairs = scipy.spatial.distance.pdist(values)
    pdist = scipy.spatial.distance.squareform(pairs)
    G = graph.generate_knn_graph(pdist, 2)
    
    func_vals = values % 5
    
    maxs, mins, ascent, descent = find_extrema(G, func_vals)
    
    print(assign_extrema(G, maxs, ascent))
    print(generate_morse_smale(G, pdist, func_vals))
    