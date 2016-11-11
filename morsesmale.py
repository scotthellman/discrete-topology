import networkx as nx
import numpy as np
import scipy
import graph
import itertools
from collections import defaultdict

def calculate_persistence(crystal, other, minimum_value, G, function_vals):
    minimums = []
    min_vertices = []
    for vertex in crystal:
        neighbors = G.neighbors(vertex)
        value = function_vals[vertex]
        worst_case = minimum_value - value
        minimum_dist = None
        minimum_node = None
        for n in neighbors:
            diff = minimum_value - function_vals[n]
            if minimum_dist is None or diff > worst_case and diff < minimum_dist:
                minimum_dist = diff
                minimum_node = n
        if minimum_dist < worst_case:
            minimum_dist = worst_case
            minimum_node = vertex
        minimums.append(minimum_dist)
        min_vertices.append(minimum_node)
    chosen_index = np.argmin(minimums)
    return minimums[chosen_index], min_vertices[chosen_index]

def find_filtration(G, function_vals, msc):
    #TODO: throw exception when 2 values are the same
    # minkP(X) mines(pa,pk) maxxiekamin − xik.   
    crystals = defaultdict(list)
    for i,label in enumerate(msc):
        crystals[label].append(i)
    filtration = [crystals] 
    while len(crystals) > 1:
        #find the crystal with the smalled persistence
        best_pair = None
        best_persistence = None
        for crystal in crystals:
            print(crystal)
            print(crystals)
            minimum_val = function_vals[crystal[0]]
            for other in crystals:
                if other != crystal:
                    persistence = calculate_persistence(crystals[crystal], crystals[other],
                                                        minimum_val, G, function_vals)[0]
                    if best_persistence is None or persistence < best_persistence:
                        best_pair = (crystal, other)
                        best_persistence = persistence
        new_crystals = defaultdict(list)
        for crystal,values in crystals.items():
            if crystal != best_pair[0]:
                new_crystals[crystal].extend(values)
            else:
                new_crystals[best_pair[1]].extend(values)
        filtration.append(new_crystals)
        crystals = new_crystals
    return filtration

def generate_morse_smale(G, pdist, function_vals):
    maxima, minima, ascent, descent = find_extrema(G, pdist, function_vals)
    max_labels = assign_extrema(G, maxima, ascent)
    min_labels = assign_extrema(G, minima, descent)
    
    return list(zip(min_labels, max_labels))
    
def assign_extrema(G, extrema, path):
    assignments = [0] * len(G.nodes())
    for node in G:
        traverser = node
        while traverser not in extrema:
            traverser = path[traverser]
        assignments[node] = traverser
    return assignments
    
def find_extrema(G, pdist, function_vals):
    ascent = {}
    descent = {}
    maxima = []
    minima = []
    for i,value in enumerate(function_vals):
        neighbors = np.array(G.neighbors(i))
        distances = np.array([d for n,d in enumerate(pdist[i]) if n in neighbors])
        differences = np.array([function_vals[n] - value for n in neighbors]).T[0]
        normalized = differences / distances
        ordered = np.argsort(normalized)
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
    
    maxs, mins, ascent, descent = find_extrema(G, pdist, func_vals)
    
    msc = generate_morse_smale(G, pdist, func_vals)
    print(msc)
    filtration = find_filtration(G, func_vals, msc)
    print("-"*20)
    for f in filtration:
        print(f)
    