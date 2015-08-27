__author__ = 'Butikk'



import math

class HeapQueue:
    def __init__(self):
        self.length = 0
        self.queue = []

    def parent(self, node):
        return self.queue[int(math.floor((self.queue.index(node) - 1) / 2))]

    def leftChild(self, node):
        if (self.queue.index(node) * 2) + 1 < self.length:
            return self.queue[(self.queue.index(node) * 2) + 1]
        return None

    def rightChild(self, node):
        if (self.queue.index(node) * 2) + 2 < self.length:
            return self.queue[(self.queue.index(node) * 2) + 2]
        return None

    def insert(self, node):
        self.queue.append(node)
        self.length += 1

        currentNode = self.queue[self.length - 1]
        parentNode = self.parent(currentNode)

        #compares parent with the new node, and performs potential switching until heap property is reached
        while self.queue.index(currentNode) > 0 and parentNode.value > currentNode.value:
            currentNode.value, parentNode.value = parentNode.value, currentNode.value
            currentNode = parentNode
            parentNode = self.parent(currentNode)


    #maintains heap property by switching nodes downwards
    def maintainHeapProperty(self, currentNode):
        leftChild = self.leftChild(currentNode)
        rightChild = self.rightChild(currentNode)

        smallestNode = currentNode
        if leftChild != None:
            if self.queue.index(leftChild) < self.length and leftChild.value < currentNode.value:
                smallestNode = leftChild

        if rightChild != None:
            if self.queue.index(rightChild) < self.length and rightChild.value < smallestNode.value:
                smallestNode = rightChild

        if smallestNode == currentNode:
            return
        else:
            currentNode.value, smallestNode.value = smallestNode.value, currentNode.value
            currentNode = smallestNode
            self.maintainHeapProperty(currentNode)

    def get(self):
        node = self.queue[0]
        if self.length > 1:
            self.queue[0] = self.queue.pop(self.length - 1)
        else:
            self.queue.pop(0)
            self.length -= 1
            return node
        self.length -= 1

        self.maintainHeapProperty(self.queue[0])

        return node



