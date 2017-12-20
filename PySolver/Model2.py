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
    ARCS = [[3, 1, 2], [3, 2, 1], [3, 2, 1]]
    a_src = 0
    a_snk = 1
    a_dst = 2

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
        taskSum = []
        for k in cls.TIME:
            for tsk in cls.TASKLIST:
                taskN = cls.snk_tasks[tsk]
                taskSum += [cls.Y[taskN][tsk][k]]
        label = 'obj_'
        prob += lpSum(taskSum)/cls.T , label

    @classmethod
    def detector(cls, prob):
        for k in cls.TIME:
            for t in cls.TASK:
                for v0 in cls.NODES:
                   arcs = list(filter(lambda s: s[cls.a_snk] == v0 and k-s[cls.a_dst] >= 0, cls.ARCS))
                   label = 'detector_' +str(k) + '_' +str(t) +'_' +str(v0)
                   incoming = [cls.X[a[cls.a_src]][v0][t][k-a[cls.a_dst]] for a in arcs]
                   prob += lpSum(incoming) == cls.Y[v0][t][k], label



