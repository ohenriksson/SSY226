from pulp import *


class Model2:
    startNode = 1
    endNode = 2
    travelTask = 0
    taskLowerBound = 1
    nodeCap = 1
    edgeCap = 1
    T = 10

    snk_tasks = [0,1,3]
    src_tasks = [0,1,2]

    NODES = range(5)
    TASK = range(3)
    TASKLIST = TASK[1:]
    TIME = range(T)
    INTER = NODES[1:-1]
    ARCS = [[0, 1, 0], [1, 2, 1], [2, 3, 4], [3,4,0]]

    a_src = 0
    a_snk = 1
    a_dst = 2

    Y = LpVariable.dicts('Y', (NODES, TASK, TIME), lowBound=0, cat=LpInteger)
    X = LpVariable.dicts('X', (NODES, NODES, TASK, TIME), lowBound=0, upBound=edgeCap, cat=LpInteger)

    @classmethod
    def init(cls):
        prob = LpProblem("Task Optimizer", LpMaximize)
        cls.objective_f(prob)
        cls.detector(prob)
        cls.inflow_outflow(prob)
        cls.tasks_must_go_on(prob)
        cls.tasks_must_be_dropped(prob)
        cls.node_capacity(prob)

        #prob.writeLP("MinmaxProblem.lp")
        prob.solve()

        for v in prob.variables():
            print(v.name, "=", v.varValue)
        print( "Throughput :", pulp.value(prob.objective))

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
                   arcs = cls.arcs_ending_here(v0, k)
                   label = 'detector_' +str(k) + '_' +str(t) +'_' +str(v0)
                   incoming = [cls.X[a[cls.a_src]][v0][t][k-a[cls.a_dst]] for a in arcs]
                   prob += lpSum(incoming) == cls.Y[v0][t][k], label


    @classmethod
    def inflow_outflow(cls, prob):
        for k in cls.TIME:
            for v0 in cls.INTER:
                arcsIn = cls.arcs_ending_here(v0,k)
                arcsOut = cls.arcs_starting_here(v0,k)
                inArcs = [[ cls.X[a[cls.a_src]][a[cls.a_snk]][t][k-a[cls.a_dst]] for t in cls.TASK] for a in arcsIn]
                outArcs =[[ cls.X[a[cls.a_src]][a[cls.a_snk]][t][k] for t in cls.TASK] for a in arcsOut]
                prob += lpSum(inArcs) == lpSum(outArcs), ""

    @classmethod
    def tasks_must_go_on(cls, prob):
        for k in cls.TIME:
            for t in cls.TASKLIST:
                for v0 in cls.INTER:
                    arcsOut = cls.arcs_starting_here(v0,k)
                    constraint = cls.Y[v0][t][k] == lpSum([ cls.X[a[cls.a_src]][a[cls.a_snk]][t][k] for a in arcsOut])
                    prob += constraint, ""

    @classmethod
    def tasks_must_be_dropped(cls,prob):
        for k in cls.TIME:
            for t in cls.TASKLIST:
                for v0 in list(filter(lambda v: v == cls.snk_tasks[t],cls.INTER)):
                    arcsIn = cls.arcs_ending_here(v0,k)
                    prob += lpSum([cls.X[a[cls.a_src]][v0][t][k] for a in arcsIn]) == 0

    @classmethod
    def node_capacity(cls,prob):
        for k in cls.TIME:
            for v0 in cls.INTER:
                prob += lpSum([cls.Y[v0][t][k] for t in cls.TASK]) <= cls.nodeCap, ""

    @classmethod
    def arcs_ending_here(cls, v0, k)->[]:
        arcs = list(filter(lambda s: s[cls.a_snk] == v0 and k-s[cls.a_dst] >= 0, cls.ARCS))
        return arcs

    @classmethod
    def arcs_starting_here(cls, v0,k)->[]:
        arcs = list(filter(lambda s: s[cls.a_src] == v0 , cls.ARCS))
        return arcs
