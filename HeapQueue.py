__author__ = 'Butikk'

import math

class HeapQueue:
    def __init__(self):
        self.length = 0
        self.queue = []

    def parent(self, node):
        return self.queue[int(math.floor((self.queue.index(node) - 1) / 2))]

    def leftChild(self, node):
        return self.queue[(self.queue.index(node) * 2) + 1]

    def rightChild(self, node):
        return self.queue[(self.queue.index(node) * 2) + 2]

    def insert(self, node):
        self.queue.append(node)
        self.length += 1

        currentNode = self.queue[self.length - 1]
        parentNode = self.parent(currentNode)

        #compares parent with the new node, and performs potential switching until heap property is reached
        while self.queue.index(currentNode) > 0 and parentNode.value > currentNode.value:
            currentNode, parentNode = parentNode, currentNode
            currentNode = parentNode

    #maintains heap property by switching nodes downwards
    def maintainHeapProperty(self, currentNode):
        leftChild = self.leftChild(currentNode)
        rightChild = self.rightChild(currentNode)

        largestNode = currentNode

        if self.queue.index(leftChild) < self.length and leftChild.value < currentNode.value:
            largestNode = leftChild

        if self.queue.index(rightChild) < self.length and rightChild.value < largestNode.value:
            largestNode = rightChild

        if largestNode == currentNode:
            return
        else:
            currentNode, largestNode = largestNode, currentNode
            self.maintainHeapProperty(currentNode)

    def get(self):
        node = self.queue[0]
        self.queue[0] = self.queue.pop(self.length - 1)
        self.length -= 1

        self.maintainHeapProperty(self.queue[0])

        return node



