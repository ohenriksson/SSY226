from pulp import *


class Model2:
    startNode = 1
    endNode = 2
    travelTask = 0
    taskLowerBound = 1
    nodeCap = 1
    edgeCap = 1
    T = 10

    snk_tasks = [0, 2,1]
    src_tasks = [0, 1,2]

    NODES = range(10)
    TASK = range(3)
    TASKLIST = TASK[1:]
    TIME = range(T)
    ARCS = [[3, 2, 2], [3, 2, 1], [3, 2, 1]]
    
    Y = LpVariable.dicts('Choice', (NODES, TASK, TIME), lowBound=0, upBound=0, cat=LpInteger)
    X = LpVariable.dicts('Choice', (NODES, NODES, TASK, TIME), lowBound=0, upBound=edgeCap, cat=LpInteger)

    @classmethod
    def init(cls):
        prob = LpProblem("Task Optimizer", LpMaximize)
        cls.objective_f(prob)
        cls.detector(prob)
        #print(prob)

    @classmethod
    def objective_f(cls, prob):
        for k in cls.TIME:
            for tsk in cls.TASKLIST:
                taskN = cls.snk_tasks[tsk]
                label = 'obj_' +str(taskN) + '_' +str(k) +'_' +str(tsk)
                prob += lpSum( cls.Y[taskN][tsk][k] )/cls.T , label

    @classmethod
    def detector(cls, prob):
        for k in cls.TIME:
            for t in cls.TASK:
                for v0 in cls.NODES:
                   label = 'detector_' +str(k) + '_' +str(t) +'_' +str(v0)
                   prob += lpSum(cls.X[v0][0][t][k]) == cls.Y[v0][t][k], label



