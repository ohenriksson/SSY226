from GridLayout import GridLayout
from LayoutTypes import *
from typing import List

import numpy as np
import modelspec as ms
import random as rn


class AmplDataWriter:
    path = ""
    input_tasks = "tasks.txt"
    input_layout = "layout.txt"
    output_ampl = "test_data.dat"

    def __init__(self, use_modelspec:bool, path=""):
        self.use_modelspec = use_modelspec
        AmplDataWriter.path = path
        self.numberNodes = ms.pickup_stations + ms.place_stations + ms.intermidiate_nodes

        self.arcs = []
        self.taskList = []
        self.interLayers = []
        self.generateNodes()
        self.generateArcs()
        self.createAllTasks()
        self.timeFrame = self.calculateTimeframe()

    def generateNodes(self):
        self.masterSourceNode = Node()
        self.pickupNodes = [Node() for i in range(ms.pickup_stations)]
        for layers in range(ms.intermidiate_layers):
            interNodes = [Node() for i in range(ms.intermidiate_nodes)]
            self.interLayers.append(interNodes)
        self.placeNodes = [Node() for i in range(ms.place_stations)]
        self.masterSinkNode = Node()


    def writeDatFile(self,filename):
        setup = ''.join(["#pickupNodes:", str(ms.pickup_stations) , " interNodes:", str(ms.intermidiate_nodes), " placeNodes:", str(ms.place_stations), '\n'])
        setup += self.setParameter('startNode',str(self.masterSourceNode))
        setup += self.setParameter('endNode',str(self.masterSinkNode))
        setup += self.setParameter('T',str(self.timeFrame))
        setup += self.setParameter('nrAGVs',str(ms.n_agvs))
        setup += self.setParameter('nTasks',str(ms.unique_tasks))
        setup += self.setParameter('travelTask',str(0))
        setup += self.setParameter('edgeCap',str(ms.edge_capacity))
        setup += self.setParameter('epsilon', str(ms.epsilon))
        setup += self.setParameter('taskLowerBound',str(ms.all_tasks))
        arcs = self.setParameter(': ARCS :TAU :', '\n'.join([str(a) for a in self.arcs]),True)
        task_src = self.setParameter(':src_tasks :','\n'.join(t.print_start() for t in self.taskList), True)
        task_snk = self.setParameter(':snk_tasks :', '\n'.join(t.print_end() for t in self.taskList), True)
        config = '\n'.join([setup,arcs,task_src,task_snk])
        self.print_to_file(filename,config)

    def calculateTimeframe(self):
        longestRoute = 0
        for arc in self.arcs:
            if longestRoute < arc.dist: longestRoute = arc.dist
        return longestRoute*ms.unique_tasks

    @staticmethod
    def setParameter(parameter, value, newLine=False,):
        sign = ' = '
        if newLine: sign = '=\n';
        return 'param ' +parameter +sign +value +';\n'

    def generateArcs(self):
        self.generateArcsBetween([self.masterSourceNode],self.pickupNodes,distance=Dist.Zero)

        if ms.grid_layout: self.arcs += GridLayout.generateGridArcs([self.pickupNodes] + self.interLayers + [self.placeNodes])
        else: self.generateAllArcs()

        self.generateArcsBetween(self.placeNodes,[self.masterSinkNode],distance=Dist.Zero)

        if ms.allow_tel_back_to_pickup:
            self.generateArcsBetween(self.placeNodes,self.pickupNodes,distance=Dist.Zero)


    def generateAllArcs(self):
        bdPaths = not ms.allow_tel_back_to_pickup
        for (index,layer) in enumerate(self.interLayers):
            if index == 0:
                self.generateArcsBetween(self.pickupNodes,layer,distance=Dist.Euclidian,bidirectional=bdPaths)
            if index == self.interLayers.__len__()-1:
                self.generateArcsBetween(layer,self.placeNodes,distance=Dist.Euclidian,bidirectional=bdPaths)
            elif index < self.interLayers.__len__():
                self.generateArcsBetween(self.interLayers[index-1],layer,distance=Dist.Euclidian,bidirectional=bdPaths)

    def generateArcsBetween(self, nodeLayer1:[Node], nodeLayer2:[Node], distance=Dist.Unit, bidirectional=False):
        for i1,n1 in enumerate(nodeLayer1):
            for (i2,n2) in enumerate(nodeLayer2):
                if distance.value == Dist.Euclidian.value:
                    d = self.getEuclidianDistance(i1,i2)
                else: d = distance.value
                self.arcs.append(Arc(n1,n2,d))
                if bidirectional: self.arcs.append(Arc(n2,n1,d))

    def getEuclidianDistance(self,y1,y2) ->int:
        x = np.divide(ms.delivery_distance,(ms.intermidiate_layers+1))
        y = np.abs(y1-y2)*ms.node_spacing_y
        return int(round(np.hypot(x,y),0))

    def createAllTasks(self):
         for t in range(ms.unique_tasks):
             self.taskList.append(self.createATask())

    def createATask(self)->Task:
        start = rn.randint(1,ms.pickup_stations)
        stop = rn.randint(1,ms.place_stations)
        stop += self.numberNodes - ms.place_stations
        return Task(start,stop)

    @classmethod
    def print_to_file(cls,output_string,content_string):
        f = open(output_string,'w')
        f.write(content_string)
        f.close()
        return
