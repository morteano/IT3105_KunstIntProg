__author__ = 'MortenAlver'

from Map import Map
from HeapQueue import HeapQueue
from Node import Node


map = Map()
map.readMap("input0.txt")
map.printMap()

queue = HeapQueue()

node = Node(0, 0)
node.value = 5
queue.insert(node)
node = Node(1, 1)
node.value = 3
queue.insert(node)
node = Node(2, 2)
node.value = 6
queue.insert(node)
node = Node(3, 3)
node.value = 2
queue.insert(node)

for i in range(4):
    print(queue.queue[i].value)


