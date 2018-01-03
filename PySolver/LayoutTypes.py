from enum import Enum
import numpy as np
import modelspec as ms

class Dist(Enum):
    Euclidian = 'eucl'
    Zero = 0
    Unit = 1

class Node:
    counter = 0

    def __init__(self):
        self.number = int(Node.counter)
        Node.counter += 1

    def __str__(self):
        return str(self.number)


class Arc:
    velocity = ms.agv_velocity

    def __init__(self, start_node:int, end_node:int, length:int):
        self.start = start_node
        self.end = end_node
        self.dist = int(np.divide(length, Arc.velocity))

    def __array__(self)->[]:
        return [self.start, self.end, self.dist]

    def __str__(self):
        return str(self.start) +' ' +str(self.end) +' ' +str(int(self.dist))


class Task:
    counter = 1
    def __init__(self, start_node:Node, end_node:Node):
        self.sNode = start_node
        self.eNode = end_node
        self.index = Task.counter
        Task.counter += 1

    def printStart(self) -> str:
        return str(self.index) +' ' +str(self.sNode)

    def printEnd(self) -> str:
        return str(self.index) +' ' +str(self.eNode)
