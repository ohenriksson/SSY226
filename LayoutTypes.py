from enum import Enum
import numpy as np
import modelspec as ms

class Dist(Enum):
    Euclidian = 'eucl',
    Zero = 0,
    Unit = 1,



class Node:
    counter = 0
    def __init__(self):
        self.number = int(Node.counter)
        Node.counter += 1

    def __str__(self):
        return str(self.number)


class Arc:
    def __init__(self,startNode:int, endNode:int,length:int):
        self.start = startNode
        self.end = endNode
        self.dist = np.divide(length,ms.agv_velocity)

    def __str__(self):
        return str(self.start) +' ' +str(self.end) +' ' +str(int(self.dist))


class Task:
    counter = 1
    def __init__(self,startNode:Node, endNode:Node):
        self.sNode = startNode
        self.eNode = endNode
        self.index = Task.counter
        Task.counter+= 1

    def printStart(self) -> str:
        return str(self.index) +' ' +str(self.sNode)

    def printEnd(self) -> str:
        return str(self.index) +' ' +str(self.eNode)
