from typing import List

import pickle
import numpy as np
import modelspec as ms
import random as rn

from LayoutTypes import *
from GridLayout import *
from DataTypes import ModelData as md

class ModelSpecParser:
    numberNodes = ms.pickup_stations + ms.place_stations + ms.intermidiate_nodes

    arcs = []
    taskList = []
    interLayers = []

    @classmethod
    def parse(cls)->None:
        cls.generateNodes()
        cls.generateArcs()
        cls.createAllTasks()
        cls.timeFrame = cls.calculateTimeFrame(cls.arcs)
        cls.savePickle(cls.generateDataStruct())
        return

    @classmethod
    def savePickle(cls, data)->None:
        pickle_out = open('model1.pickle','wb')
        pickle.dump(data,pickle_out)
        pickle_out.close()

    @classmethod
    def generateNodes(cls):
        cls.masterSourceNode = Node()
        cls.pickupNodes = [Node() for i in range(ms.pickup_stations)]
        for layers in range(ms.intermidiate_layers):
            interNodes = [Node() for i in range(ms.intermidiate_nodes)]
            cls.interLayers.append(interNodes)
        cls.placeNodes = [Node() for i in range(ms.place_stations)]
        cls.masterSinkNode = Node()

    @classmethod
    def generateDataStruct(cls):
        data = {}
        data[md.epsilonTravel] = ms.epsilon
        data[md.useEpsilon] = ms.use_epsilon
        data[md.startNode] = cls.masterSourceNode
        data[md.endNode] = cls.masterSinkNode
        data[md.T] = cls.timeFrame
        data[md.agv] = ms.n_agvs
        data[md.taskLowerBound] = ms.all_tasks * ms.unique_tasks
        data[md.nodeCap] = ms.node_capacity
        data[md.edgeCap] = ms.edge_capacity
        data[md.travelTask] = 0
        data[md.snk_tasks] = [t.eNode for t in cls.taskList]
        data[md.src_tasks] = [t.sNode for t in cls.taskList]
        data[md.arcs] = [a.__array__() for a in cls.arcs]
        return data

    @staticmethod
    def calculateTimeFrame(arcs:[Arc])->int:
        longestRoute = 0
        for arc in arcs:
            if longestRoute < arc.dist: longestRoute = arc.dist
        return int(longestRoute*ms.unique_tasks)

    @staticmethod
    def setParameter(parameter, value, newLine=False,):
        sign = ' = '
        if newLine: sign = '=\n';
        return 'param ' +parameter +sign +value +';\n'

    @classmethod
    def generateArcs(cls):
        cls.generateArcsBetween([cls.masterSourceNode], cls.pickupNodes, distance=Dist.Zero)

        if ms.grid_layout: cls.arcs += GridLayout.generateGridArcs([cls.pickupNodes] + cls.interLayers + [cls.placeNodes])
        else: cls.generateAllArcs()

        cls.generateArcsBetween(cls.placeNodes, [cls.masterSinkNode], distance=Dist.Zero)

        if ms.allow_tel_back_to_pickup:
            cls.generateArcsBetween(cls.placeNodes, cls.pickupNodes, distance=Dist.Zero)

    @classmethod
    def generateAllArcs(cls):
        bdPaths = not ms.allow_tel_back_to_pickup
        for (index,layer) in enumerate(cls.interLayers):
            if index == 0:
                cls.generateArcsBetween(cls.pickupNodes, layer, distance=Dist.Euclidian, bidirectional=bdPaths)
            if index == cls.interLayers.__len__()-1:
                cls.generateArcsBetween(layer, cls.placeNodes, distance=Dist.Euclidian, bidirectional=bdPaths)
            elif index < cls.interLayers.__len__():
                cls.generateArcsBetween(cls.interLayers[index - 1], layer, distance=Dist.Euclidian, bidirectional=bdPaths)

    @classmethod
    def generateArcsBetween(cls, nodeLayer1:[Node], nodeLayer2:[Node], distance=Dist.Unit, bidirectional=False):
        for i1,n1 in enumerate(nodeLayer1):
            for (i2,n2) in enumerate(nodeLayer2):
                if distance.value == Dist.Euclidian.value:
                    d = cls.getEuclidianDistance(i1, i2)
                else: d = distance.value
                cls.arcs.append(Arc(n1.number, n2.number, d))
                if bidirectional: cls.arcs.append(Arc(n2.number, n1.number, d))

    @staticmethod
    def getEuclidianDistance(y1,y2) ->int:
        x = np.divide(ms.delivery_distance,(ms.intermidiate_layers+1))
        y = np.abs(y1-y2)*ms.node_spacing_y
        return int(round(np.hypot(x,y),0))

    @classmethod
    def createAllTasks(cls):
        for t in range(ms.unique_tasks):
            cls.taskList.append(cls.createATask())

    @classmethod
    def createATask(cls)->Task:
        start = rn.randint(1,ms.pickup_stations)
        stop = rn.randint(1,ms.place_stations)
        stop += cls.numberNodes - ms.place_stations
        return Task(start,stop)

    @staticmethod
    def print_to_file(output_string,content_string):
        f = open(output_string,'w')
        f.write(content_string)
        f.close()
        return
