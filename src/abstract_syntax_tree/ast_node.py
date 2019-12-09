from anytree import Node, RenderTree
from anytree.exporter import DotExporter

class ASTNode:
    def __init__(self, type, children=None, val=None, toTable=None, cgen=None):
        self.type = type
        self.val = val
        self.toTable = toTable
        self.cgen = cgen
        if children:
            self.children = children
        else:
            self.children = []
    def set(self, type = None, children = None, val = None, cgen = None):
        if type:
            self.type = type
        if children:
            self.children = children
        if val:
            self.val = val
        if cgen:
            self.cgen = cgen

    def children_length(self):
        if (self.children == None or len(self.children) == 0):
            return 0
        
        acc = 0
        for son in self.children:
            if isinstance(son, str) or isinstance(son, int):
                acc = acc + 1
            # else:
            #     acc = acc + son.children_length()

def create_tree(info, parent):
    if(info != None):
        if info.children != None:
            index = 0
            for item in info.children:
                if not type(item) is ASTNode:
                    Node(str(item), parent=parent)
                else:
                    new = Node(item.type, parent=parent)
                    create_tree(item, new)
