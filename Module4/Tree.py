import math

class Node:

    def __init__(self, object):
        self.parent = None
        self.children = []
        self.object = object

    def getParent(self):
        return self.parent

    def getChildren(self):
        return self.children

    def setParent(self, node):
        self.parent = node

    def addChild(self, node):
        self.children.append(node)

class Tree:

    def __init__(self):
        self.nodes = []
        self.root = None
        self.size = 0.0

        self.depth = 0

    def addNode(self, node, parentNode):
        self.nodes.append(node)
        self.size += 1

        if len(self.nodes) == 1:
            self.root = node
        else:
            node.parent = parentNode
            parentNode.children.append(node)

    def reset(self):
        for i in self.nodes:
            i.children = []
            i.parent = None
        self.nodes = []
        self.root = None
        self.size = 0.0
        self.depth = 0









