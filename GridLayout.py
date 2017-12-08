from LayoutTypes import *
from typing import List
import modelspec as ms


class GridLayout:
    @staticmethod
    def generateArcsInLayer(layer: List[Node])->List[Arc]:
        arcList = []
        for (i,n) in enumerate(layer):
            if i < (layer.__len__() -1):
                arcList.append(Arc(i,i+1,ms.node_spacing_y))
                if ms.allow_tel_back_to_pickup:
                    arcList.append(Arc(i+1,i,ms.node_spacing_y))
        return arcList

    def arcsBetweenLayers(self,layer1: List[Node],layer2: List[Node])->[Arc]:
        arcList = []
        shortest = layer1.__len__() if layer1.__len__() < layer2.__len__() else layer2.__len__()
        for i in range(shortest):
            arcList.append(Arc(layer1[i].number,layer2[i].number))
        return arcList


