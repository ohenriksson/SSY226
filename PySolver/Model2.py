from pulp import *
import model1 as data
from enum import IntEnum


class A(IntEnum):
    SRC = 0
    SNK = 1
    DST = 2


def count_nodes(arcs):
    highestnum = 0
    for a in arcs:
        if a[A.SNK] > highestnum:
            highestnum = a[A.SNK]
        elif a[A.SRC] > highestnum:
            highestnum = a[A.SRC]
    return highestnum+1


class Model2:
    epsilonTravel = data.epsilonTravel
    useEpsilon = data.useEpsilon

    startNode = data.startNode
    endNode = data.endNode
    travelTask = data.travelTask
    taskLowerBound = data.taskLowerBound
    nodeCap = data.nodeCap
    edgeCap = data.edgeCap
    T = data.T
    agvMax = data.agv

    snk_tasks = data.snk_tasks
    src_tasks = data.src_tasks

    ARCS = data.arcs
    TASK = range(snk_tasks.__len__())
    TASKLIST = TASK[1:]
    TIME = range(T)

    NODES = range(count_nodes(ARCS))
    INTER = NODES[1:-1]

    Y = LpVariable.dicts('Y', (NODES, TASK, TIME), lowBound=0, cat=LpInteger)
    X = LpVariable.dicts('X', (NODES, NODES, TASK, TIME), lowBound=0, upBound=edgeCap, cat=LpInteger)
    AGVS = LpVariable('AGVS', lowBound=0, upBound=agvMax, cat=LpInteger)

    @classmethod
    def init(cls):
        prob = LpProblem("Task Optimizer", LpMaximize)
        cls.objective_f(prob)
        cls.detector(prob)
        cls.inflow_outflow(prob)
        cls.arctravel_capacity(prob)
        cls.tasks_must_go_on(prob)
        cls.tasks_must_be_dropped(prob)
        cls.node_capacity(prob)
        cls.tasks_lower_bound(prob)
        cls.start_node_task(prob) #does not seem to restrict further
        cls.agv_number_restrictions(prob)

        #prob.writeLP("MinmaxProblem.lp")
        prob.solve()

        for v in prob.variables():
            if v.varValue > 0:
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
                   arcs = cls.arcs_ending_at(v0, k)
                   label = 'detector_' +str(k) + '_' +str(t) +'_' +str(v0)
                   incoming = [cls.X[a[A.SRC]][v0][t][k-a[A.DST]] for a in arcs]
                   prob += lpSum(incoming) == cls.Y[v0][t][k], label


    @classmethod
    def inflow_outflow(cls, prob):
        for k in cls.TIME:
            for v0 in cls.INTER:
                arcsIn = cls.arcs_ending_at(v0, k)
                arcsOut = cls.arcs_starting_here(v0,k)
                inArcs = [[ cls.X[a[A.SRC]][a[A.SNK]][t][k-a[A.DST]] for t in cls.TASK] for a in arcsIn]
                outArcs =[[ cls.X[a[A.SRC]][a[A.SNK]][t][k] for t in cls.TASK] for a in arcsOut]
                prob += lpSum(inArcs) == lpSum(outArcs), ""


    @classmethod
    def arctravel_capacity(cls, prob):
        for k in cls.TIME:
            for a in cls.ARCS:
                useTime = k+cls.epsilonTravel if cls.useEpsilon else k+a[A.DST]-1
                travelWindow = range(k, min(useTime, cls.T))
                prob += lpSum([[cls.X[a[A.SRC]][a[A.SNK]][t][k_win] for k_win in travelWindow] for t in cls.TASK]) <= cls.edgeCap

    @classmethod
    def tasks_must_go_on(cls, prob):
        for k in cls.TIME:
            for t in cls.TASKLIST:
                for v0 in list(filter(lambda v: v != cls.src_tasks[t] and v != cls.snk_tasks[t], cls.INTER)):
                    arcsOut = cls.arcs_starting_here(v0, k)
                    prob += cls.Y[v0][t][k] == lpSum([ cls.X[a[A.SRC]][a[A.SNK]][t][k] for a in arcsOut])

    @classmethod
    def tasks_must_be_dropped(cls, prob):
        for k in cls.TIME:
            for t in cls.TASKLIST:
                for v0 in list(filter(lambda v: v == cls.snk_tasks[t], cls.INTER)):
                    arcsOut = cls.arcs_starting_here(v0)
                    prob += lpSum([cls.X[a[A.SRC]][v0][t][k] for a in arcsOut]) == 0

    @classmethod
    def tasks_lower_bound(cls, prob):
        for t in cls.TASKLIST:
            taskSum = [cls.Y[cls.snk_tasks[t]][t][k] for k in cls.TIME]
            prob += lpSum(taskSum) >= cls.taskLowerBound

    @classmethod
    def node_capacity(cls,prob):
        for k in cls.TIME:
            for v0 in cls.INTER:
                prob += lpSum([cls.Y[v0][t][k] for t in cls.TASK]) <= cls.nodeCap, ""

    @classmethod
    def start_node_task(cls, prob):
        for k in cls.TIME:
            for t in cls.TASKLIST:
                for v0 in cls.arcs_starting_here(cls.startNode):
                    arcDest = v0[A.SNK]
                    prob += cls.X[cls.startNode][arcDest][t][k] == 0, ""

    @classmethod
    def agv_number_restrictions(cls, prob):
        cls.agv_counter(prob)

    @classmethod
    def agv_counter(cls,prob):
         startArcs = cls.arcs_starting_here(cls.startNode)
         endArcs = cls.arcs_ending_here(cls.endNode)
         startSum = list(cls.X[a[A.SRC]][a[A.SNK]] for a in startArcs)
         endSum = [cls.X[a[A.SRC]][a[A.SNK]] for a in endArcs]
         prob += lpSum(startSum) == lpSum(endSum), "agv restrictor"
         prob += lpSum(startSum) == cls.AGVS, "counter"


    @classmethod
    def arcs_ending_at(cls, v0, k)->[]:
        arcs = cls.arcs_ending_here(v0)
        return list(filter(lambda s: k-s[A.DST] >= 0, arcs))

    @classmethod
    def arcs_ending_here(cls,v0)->[]:
        return list(filter(lambda s: s[A.SNK] == v0, cls.ARCS))

    @classmethod
    def arcs_starting_here(cls, v0, k=0)->[]:
        return list(filter(lambda s: s[A.SRC] == v0 , cls.ARCS))
