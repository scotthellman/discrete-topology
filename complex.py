# -*- coding: utf-8 -*-

class SimplexTree:
    
    def __init__(self):
        self.root = SimplexTreeNode("root", None)
        
    def add_simplex(self, nodes):
        nodes = sorted(nodes)
        for i in range(len(nodes)):
            subnodes = nodes[i:]
            parent = self.root
            for node in subnodes:
                current = parent.children
                if node not in current:
                    current[node] = SimplexTreeNode(node, parent)
                parent = current[node]
            


class SimplexTreeNode:
    
    def __init__(self, name, parent):
        self.name = name
        self.siblings = []
        self.parent = parent
        self.children = {}
        
    def __str__(self):
        return "{}: {}".format(self.name, [str(c) for c in self.children.values()])
        


if __name__ == "__main__":
    simplices = [[1,2,3,4],[3,4,5]]
    
    tree = SimplexTree()
    tree.add_simplex(simplices[0])
    tree.add_simplex(simplices[1])
    print(tree.root)