# -*- coding: utf-8 -*-
from collections import defaultdict
from asciitree import LeftAligned


class SimplexTree:
    
    def __init__(self):
        self.root = SimplexTreeNode("root", None,-1)
        self.sibling_tree = defaultdict(lambda : defaultdict(list))
        self.depth = 0
        
    def add_simplex(self, nodes):
        nodes = sorted(nodes)
        
        #TODO: this is busted
        #we only update the leftmost branch
        parent = self.root  
        
        to_add = []
        to_add.append((self.root, 0))
        
        while to_add:
            parent, depth = to_add.pop()
            subnodes = nodes[depth:]
            parent.add_children(subnodes)
            for node in subnodes:
                to_add.append((parent.children[node], depth + 1))
                self.sibling_tree[depth][node] = parent.children[node]
      
        if self.depth < len(nodes):
            self.depth = len(nodes)
                    
    def _remove_from_sibling_tree(self, node):
        for child in node.children.values():
            self._remove_from_sibling_tree(child)
        self.sibling_tree[node.dimension][node.name].remove(node)  
        
    def delete_simplex(self, simplex):
        node = self.find_simplex(simplex)
        cofaces = self.find_cofaces(simplex)
        
        self._remove_from_sibling_tree(node)
        node.parent.remove_child(node.name)
        for coface in cofaces:
            self._remove_from_sibling_tree(coface)
            coface.parent.remove_child(coface.name)
            
    #TODO: at least some of thse should be in SimplexTreeNode               
    def find_simplex(self, simplex):
        return self.root.find_simplex(simplex)
    
    def find_cofaces(self, simplex):
        #find all simplices that have the same final vertex
        #nb this doesn't actually return ALL cofaces - things of larger dim
        #may just be implied
        final_node = self.find_simplex(simplex)
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
        
    def find_facets(self, simplex):
        #TODO: figure out why we need this, i don't think
        #i'm understanding the terminology correctly
        #also this is really pointing out that i need to do something about
        #equality testing for nodes
        facets = []
        node = self.find_simplex(simplex)
        path = node.path_to_root()
        remaining = []
        for child,parent in zip(path,path[1:]):
            facet = parent.find_simplex(remaining)
            if facet is not None:
                facets.append(facet)
            remaining.append(child.name)
        return facets



class SimplexTreeNode:
    
    def __init__(self, name, parent, dim):
        self.name = name
        self.parent = parent
        self.dimension = dim
        self.children = {}
        
    def find_simplex(self, simplex):
        current = self
        try:
            for node in simplex:
                current = current.children[node]
            return current
        except KeyError:
            return None
        
    def path_to_root(self):
        path = []
        current = self
        while current is not None:
            path.append(current)
            current = current.parent
        return path
        
    def get_children(self):
        return list(self.children.values())

    def add_children(self, names):
        for name in names:
            self.add_child(name)
    
    def add_child(self, name):
        if name not in self.children:
            self.children[name] = SimplexTreeNode(name, self, self.dimension+1)
        
    def remove_child(self, name):
        del self.children[name]
    
    def __str__(self):
        try:
            return "{}^{} : {}".format(self.name, self.dimension, len(self.children))
        except AttributeError:
            return "root"
    def pretty(self):
        path = self.path_to_root()
        return "-".join([str(p.name) for p in path])
        
    def to_dictionary(self):
        child_dictionary = {c.name : c.to_dictionary() for c in self.children.values()}

        if self.parent is None:
            return {self.name : child_dictionary}
        return child_dictionary#{self.name : child_dictionary}

if __name__ == "__main__":
    simplices = [[1,2,3,4],[3,4,5]]
    
    tree = SimplexTree()
    #tree.add_simplex(simplices[0])
    tree.add_simplex(simplices[1])
    #tree.add_simplex([1])
    #print(tree.root)
    #print(tree.sibling_tree)
    #print(tree.find_simplex([1,2,3]))
    #print("-")
    #print(tree.find_cofaces([3,4]))
    #for i in range(4):
    #    siblings = tree.sibling_tree[i]
    #    for name in siblings:
    #        print(i, name, len(siblings[name]))
    #tree.delete_simplex([3,4])
    #print("---")
    #print(tree.root)
    #print(tree.sibling_tree)
    #for i in range(4):
    #    siblings = tree.sibling_tree[i]
    #    for name in siblings:
    #        print(i, name, len(siblings[name]))
    #facets = tree.find_facets([3,4,5])
    #print([f.pretty() for f in facets])
    #print(tree.find_simplex([4,5]))
    
    print(LeftAligned()(tree.root.to_dictionary()))
    #print(tree.root.to_dictionary())
    print(tree.root.to_dictionary())