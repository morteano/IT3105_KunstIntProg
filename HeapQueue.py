__author__ = 'Butikk'

import math

class HeapQueue:
	def __init__(self):
		self.length = 0
		self.queue = []

	def parent(self, node):
		return int(math.floor((node - 1) / 2))

	def leftChild(self, node):
		return (node * 2) + 1

	def rightChild(self, node):
		return (node * 2) + 2

	def insert(self, value):
		self.queue.append(value)
		self.length += 1

		currentNode = self.length - 1

		#compares parent with the new node, and performs potential switching until heap property is reached
		while currentNode > 0 and self.queue[self.parent(currentNode)] > self.queue[currentNode]:
			self.queue[currentNode], self.queue[self.parent(currentNode)] = self.queue[self.parent(currentNode)], self.queue[currentNode]
			currentNode = self.parent(currentNode)

	#maintains heap property by switching nodes downwards
	def maintainHeapProperty(self, currentNode):
		leftChild = self.leftChild(currentNode)
		rightChild = self.rightChild(currentNode)

		largestNode = currentNode

		if leftChild < self.length and self.queue[leftChild] < self.queue[currentNode]:
			largestNode = leftChild

		if rightChild < self.length and self.queue[rightChild] < self.queue[largestNode]:
			largestNode = rightChild

		if largestNode == currentNode:
			return
		else:
			self.queue[currentNode], self.queue[largestNode] = self.queue[largestNode], self.queue[currentNode]
			currentNode = largestNode
			self.maintainHeapProperty(currentNode)

	def get(self):
		value = self.queue[0]
		self.queue[0] = self.queue.pop(self.length - 1)
		self.length -= 1

		print(self.queue)

		self.maintainHeapProperty(0)

		return value