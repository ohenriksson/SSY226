import matplotlib.pyplot as plt
from matplotlib import collections
import numpy as np

class SolutionPlot:

    nodeCoords = [(0,0),(0,1),(0,2),(3,3)]

    x = [[0,0,0,1],
         [0,0,1,0]] #x[i,j] #there exists one x for each task and each time

    tasks = [x,x]
    time = [tasks,tasks,tasks,tasks,tasks]

    points = [0,1,2]
    segments = [] # time ordered travelling segments [from,to,taskNo]

    @classmethod
    def init(cls):
        cls.constructSegments(cls.time)
        cls.plot()

    @classmethod
    def constructSegments(cls,timeTable):
       [cls.checkTasks(t,tasklist) for t,tasklist in enumerate(timeTable)]

    @classmethod
    def checkTasks(cls,timeStamp,tasklist):
        [cls.checkNodes(tNo,task) for tNo,task in enumerate(tasklist)]

    @classmethod
    def checkNodes(cls,taskNo,task):
        [cls.checkRow(row,j,taskNo) for row,j in enumerate(task)]

    @classmethod
    def checkRow(cls,rownum,row,taskNo):
        for colnum,c in enumerate(row):
            if c > 0:
                cls.segments.append([rownum,colnum,taskNo])

    @classmethod
    def getSegmentCoords(cls,start,end):
        return [cls.nodeCoords[start],cls.nodeCoords[end]]

    @classmethod
    def plot(cls):
        fig, ax = plt.subplots()
        x = [x[0] for x in cls.nodeCoords]
        y = [x[1] for x in cls.nodeCoords]

        labels = [i[2] for i in cls.segments]
        segments = [cls.getSegmentCoords(i[0],i[1]) for i in cls.segments]
        print(segments)

        line_segments = collections.LineCollection(segments, colors='black', linewidths=0.5)
        line_segments.set_label(''.join(str(labels)))

        ax.scatter(x, y)
        ax.add_collection(line_segments)
        ax.grid()
        plt.show()

SolutionPlot.init()