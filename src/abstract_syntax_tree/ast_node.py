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
    def set(self, type = None, children = None, val = None):
        if type:
            self.type = type
        if children:
            self.children = children
        if val:
            self.val = val

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
