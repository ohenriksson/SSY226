from PointPlotter import PointPlotter
from TaskReader import TaskReader
import numpy as np
import modelspec as ms
from enum import Enum
import random as rn

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
    def __init__(self,startNode:int,endNode:int,length:int):
        self.start = startNode
        self.end = endNode
        self.dist = length

    def __str__(self):
        return str(self.start) +' ' +str(self.end) +' ' +str(int(np.divide(self.dist,ms.agv_velocity)))

class Task:
    counter = 1
    def __init__(self,startNode:Node,endNode:Node):
        self.sNode = startNode
        self.eNode = endNode
        self.index = Task.counter
        Task.counter+= 1

    def printStart(self) -> str:
        return str(self.index) +' ' +str(self.sNode)

    def printEnd(self) -> str:
        return str(self.index) +' ' +str(self.eNode)


class AmplDataWriter:
    bigNumber = 1000000
    separator = " "

    tau_complete = ""
    tasks_complete = ""
    allowed_tasks_complete = ""

    path = ""
    input_tasks = "tasks.txt"
    input_layout = "layout.txt"
    output_ampl = "test_data.dat"

    def __init__(self,use_modelspec:bool, path=""):
        self.use_modelspec = use_modelspec
        AmplDataWriter.path = path
        self.numberNodes = ms.pickup_stations + ms.place_stations + ms.intermidiate_nodes

        self.arcs = []
        self.taskList = []
        self.generateLayout()
        self.createAllTasks()

    def generateLayout(self):
        self.interLayers = []
        self.masterSourceNode = Node()
        self.pickupNodes = [Node() for i in range(ms.pickup_stations)]
        for layers in range(ms.intermidiate_layers):
            interNodes = [Node() for i in range(ms.intermidiate_nodes)]
            self.interLayers.append(interNodes)
        self.placeNodes = [Node() for i in range(ms.place_stations)]
        self.masterSinkNode = Node()
        self.generateAllArcs()

    def writeDatFile(self,filename):
        setup = self.setParameter('startNode',str(self.masterSourceNode))
        setup += self.setParameter('endNode',str(self.masterSinkNode))
        setup += self.setParameter('T',str(ms.timeframe))
        setup += self.setParameter('nrAGVs',str(ms.n_agvs))
        setup += self.setParameter('nTasks',str(ms.unique_tasks))
        setup += self.setParameter('travelTask',str(0))
        setup += self.setParameter('edgeCap',str(ms.edge_capacity))
        arcs = self.setParameter('ARCS: TAU :','\n'.join([str(a) for a in self.arcs]))
        task_src = self.setParameter('task_src :', '\n'.join(t.printStart() for t in self.taskList) )
        task_snk = self.setParameter('task_snk :', '\n'.join(t.printEnd() for t in self.taskList) )
        config = '\n'.join([setup,arcs,task_src,task_snk])
        self.print_to_file(filename,config)

    @staticmethod
    def setParameter(parameter,value):
        return 'param ' +parameter +' = ' +value +';\n'

    def generateAllArcs(self):
        self.generateArcsBetween([self.masterSourceNode],self.pickupNodes,distance=Dist.Zero)

        for (index,layer) in enumerate(self.interLayers):
            if index == 0:
                self.generateArcsBetween(self.pickupNodes,layer,distance=Dist.Euclidian)
            elif index == self.interLayers.__len__() -1:
                self.generateArcsBetween(self.interNodes,self.placeNodes,distance=Dist.Euclidian)
            else:
                self.generateArcsBetween(self.interLayers[index-1],layer)

        self.generateArcsBetween(self.placeNodes,[self.masterSinkNode],distance=Dist.Zero)

        if ms.allow_tel_back_to_pickup:
            self.generateArcsBetween(self.placeNodes,self.pickupNodes,distance=Dist.Zero)


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
        stop = rn.randint(0,ms.place_stations)
        stop += self.placeNodes.__len__()
        return Task(start,stop)

    @classmethod
    def main(cls):
        pp = PointPlotter(cls.input_layout)
        tr = TaskReader(cls.input_tasks)

        cls.aggregate_nodes(pp)
        cls.aggregate_tasks(tr)
        cls.alowed_tasks_list(tr)
        cls.print_to_file(cls.tau_complete + cls.tasks_complete + cls.allowed_tasks_complete)

    @classmethod
    def aggregate_nodes(cls, pp):
        nNodes = len(pp.points_id)
        header = ''.join([str(i) + cls.separator for i in range(nNodes)])

        TAU = np.ones([nNodes,nNodes])*cls.bigNumber

        for l,(i,j) in enumerate(pp.segment_ids):
            i1 = pp.points_id.index(str(i))
            i2 = pp.points_id.index(str(j))
            TAU[i1,i2] = pp.segment_distance[l]

        cls.tau_complete = header + "\n" + ''.join(
            [str(l) + cls.separator + ''.join([str(int(cell)) + cls.separator for cell in i])
             + '\n' for l, i in enumerate(TAU)])

    @classmethod
    def aggregate_tasks(cls, tr):
        header = ''.join([str(i) + cls.separator for i in range(tr.tasks.__len__())])
        tasks = ''.join([str(i) + cls.separator for i,j in tr.tasks])
        cls.tasks_complete = header + '\n' + tasks

    #
    # @classmethod
    # def allowed_tasks_list(cls,tr):
    #     node_header = ''.join([str(i) + cls.separator for i in range(tr.tasks.__len__()])
    #     tasks = [range()]
    #     cls.tasks_complete = node_header + '\n' + tasks

    @classmethod
    def print_to_file(cls,output_string,content_string):
        f = open(output_string,'w')
        f.write(content_string)
        f.close()
        return
