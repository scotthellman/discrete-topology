# -*- coding: utf-8 -*-
from collections import defaultdict


class SimplexTree:
    
    def __init__(self):
        self.root = SimplexTreeNode("root", None,-1)
        self.sibling_tree = defaultdict(lambda : defaultdict(list))
        self.depth = 0
        
    def add_simplex(self, nodes):
        nodes = sorted(nodes)
        for i in range(len(nodes)):
            subnodes = nodes[i:]
            parent = self.root
            for j,node in enumerate(subnodes):
                #j is depth
                current = parent.children
                if node not in current:
                    current[node] = SimplexTreeNode(node, parent, j)
                self.sibling_tree[j][node].append(current[node])
                parent = current[node]   
                if i+j > self.depth:
                    self.depth = j
                    
    def _remove_from_sibling_tree(self, node):
        for child in node.children.values():
            self._remove_from_sibling_tree(child)
        self.sibling_tree[node.dimension][node.name].remove(node)  
        
    def delete_simplex(self, simplex):
        node = self.find_node(simplex)
        cofaces = self.find_cofaces(simplex)
        
        self._remove_from_sibling_tree(node)
        node.parent.remove_child(node.name)
        for coface in cofaces:
            self._remove_from_sibling_tree(coface)
            coface.parent.remove_child(coface.name)
        
                
    def find_node(self, simplex):
        current = self.root
        for node in simplex:
            current = current.children[node]
        return current
    
    def find_cofaces(self, simplex):
        #find all simplices that have the same final vertex
        #nb this doesn't actually return ALL cofaces - things of larger dim
        #may just be implied
        final_node = self.find_node(simplex)
        cofaces = []
        for dim in range(final_node.dimension, self.depth + 1):
            siblings = self.sibling_tree[dim][final_node.name]
            for sibling in siblings:
                if sibling == final_node:
                    continue
                path = sibling.path_to_root()
                names = set([p.name for p in path])
                if all([s in names for s in simplex]):
                    cofaces.append(sibling)
        return cofaces


class SimplexTreeNode:
    
    def __init__(self, name, parent, dim):
        self.name = name
        self.parent = parent
        self.dimension = dim
        self.children = {}
        
    def __str__(self):
        return "{}: {}".format(self.name, [str(c) for c in self.children.values()])
        
    def path_to_root(self):
        path = []
        current = self
        while current is not None:
            path.append(current)
            current = current.parent
        return path
        
    def remove_child(self, name):
        del self.children[name]

if __name__ == "__main__":
    simplices = [[1,2,3,4],[3,4,5]]
    
    tree = SimplexTree()
    tree.add_simplex(simplices[0])
    tree.add_simplex(simplices[1])
    #print(tree.root)
    #print(tree.sibling_tree)
    #print(tree.find_node([1,2,3]))
    #print("-")
    #print(tree.find_cofaces([3,4]))
    for i in range(4):
        siblings = tree.sibling_tree[i]
        for name in siblings:
            print(i, name, len(siblings[name]))
    tree.delete_simplex([3,4])
    print("---")
    #print(tree.root)
    #print(tree.sibling_tree)
    for i in range(4):
        siblings = tree.sibling_tree[i]
        for name in siblings:
            print(i, name, len(siblings[name]))