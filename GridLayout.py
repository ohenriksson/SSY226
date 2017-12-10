from LayoutTypes import *
from typing import List
import modelspec as ms


class GridLayout:
    @staticmethod
    def generateArcsInLayer(layer: List[Node]) -> List[Arc]:
        arcList = []
        for (i,n) in enumerate(layer):
            if i < layer.__len__()-1:
                arcList.append(Arc(n.number,n.number+1,ms.node_spacing_y))
                arcList.append(Arc(n.number+1,n.number,ms.node_spacing_y))
        return arcList

    @staticmethod
    def arcsBetweenLayers(layer1: List[Node],layer2: List[Node])->[Arc]:
        xDist = ms.delivery_distance/(ms.intermidiate_layers+1)
        arcList = []
        shortest = layer1.__len__() if layer1.__len__() < layer2.__len__() else layer2.__len__()
        for i in range(shortest):
            arcList.append(Arc(layer1[i].number,layer2[i].number, xDist ))
            if not ms.allow_tel_back_to_pickup:
                arcList.append(Arc(layer2[i].number,layer1[i].number, xDist ))
        return arcList

    @classmethod
    def generateGridArcs(cls,interLayers:List[List[Node]]):
        arcs = []
        for (index,layer) in enumerate(interLayers):
            arcs += cls.generateArcsInLayer(layer)
            if index+1 < interLayers.__len__():
                arcs += cls.arcsBetweenLayers(layer,(interLayers[index+1]))
        return arcs


