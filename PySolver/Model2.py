from pulp import *
from enum import IntEnum
from DataTypes import ModelData as md
import pickle

class A(IntEnum):
    SRC = 0
    SNK = 1
    DST = 2

class Model2:

    @staticmethod
    def count_nodes(arcs):
        highestnum = 0
        for a in arcs:
            if a[A.SNK] > highestnum:
                highestnum = a[A.SNK]
            elif a[A.SRC] > highestnum:
                highestnum = a[A.SRC]
        return highestnum+1

    @classmethod
    def load(cls, modelName = 'model1.pickle'):
        indata_pickle = open(modelName,'rb')
        data = pickle.load(indata_pickle)
        print(data)

        cls.epsilonTravel = data[md.epsilonTravel]
        cls.useEpsilon = data[md.useEpsilon]

        cls.startNode = data[md.startNode]
        cls.endNode = data[md.endNode]
        cls.travelTask = data[md.travelTask]
        cls.taskLowerBound = data[md.taskLowerBound]
        cls.nodeCap = data[md.nodeCap]
        cls.edgeCap = data[md.edgeCap]
        cls.T = data[md.T]
        cls.agvMax = data[md.agv]

        cls.snk_tasks = data[md.snk_tasks]
        cls.src_tasks = data[md.src_tasks]

        cls.ARCS = data[md.arcs]
        cls.TASK = range(cls.snk_tasks.__len__())
        cls.TASKLIST = cls.TASK[1:]
        cls.TIME = range(cls.T)

        cls.NODES = range(cls.count_nodes(cls.ARCS))
        cls.INTER = cls.NODES[1:-1]

        cls.Y = LpVariable.dicts('Y', (cls.NODES, cls.TASK,cls.TIME), lowBound=0, cat=LpInteger)
        cls.X = LpVariable.dicts('X', (cls.NODES, cls.NODES, cls.TASK, cls.TIME), lowBound=0, upBound=cls.agvMax, cat=LpInteger)
        cls.AGVS = LpVariable('AGVS', lowBound=0, upBound=cls.agvMax, cat=LpInteger)


    @classmethod
    def solve(cls):
        prob = LpProblem("Task Optimizer", LpMaximize)
        cls.objective_f(prob)
        cls.detector(prob)
        cls.prevent_early_start(prob)
        cls.inflow_outflow(prob)
        #cls.task_travel(prob)
        cls.arctravel_capacity(prob)
        cls.tasks_must_go_on(prob)
        cls.tasks_must_be_dropped(prob)
        cls.node_capacity(prob)
        cls.tasks_lower_bound(prob)
        cls.start_node_task(prob) #does not seem to restrict further
        cls.agv_number_restrictions(prob)

        prob.writeLP("MinmaxProblem.lp")
        prob.solve()

        cls.print_result(prob)

    @classmethod
    def print_result(cls, prob):
        if prob.status != pulp.LpStatusOptimal:
            print('FAILED: ', pulp.LpStatus[prob.status])
        else:
            for v in prob.variables():
                if v.varValue > 0:
                    print(v.name, "=", v.varValue)
            print("AGVS: ", pulp.value(cls.AGVS))
            print("Throughput: ", pulp.value(prob.objective))
        print("Constraints: ", prob.constraints.__len__() )
        print("Variables: ",prob.variables().__len__() )

    @classmethod
    def objective_f(cls, prob):
        taskSum = []
        for k in cls.TIME:
            for tsk in cls.TASKLIST:
                taskN = cls.snk_tasks[tsk]
                taskSum += [cls.Y[taskN][tsk][k]]
        prob += lpSum(taskSum)/cls.T

    @classmethod
    def detector(cls, prob):
        for k in cls.TIME:
            for t in cls.TASK:
                for v0 in cls.NODES:
                   arcs = cls.arcs_ending_at(v0, k)
                   label = 'detector_' +str(k) + '_' +str(t) +'_' +str(v0)
                   incoming = [cls.X[a[A.SRC]][v0][t][k-a[A.DST]] for a in arcs]
                   if incoming.__len__() == 0: incoming = [0]
                   prob += lpSum(incoming) == cls.Y[v0][t][k], label
    @classmethod
    def prevent_early_start(cls, prob):
        for k in cls.TIME:
            for a in cls.ARCS:
                for t in cls.TASK:
                    if k-a[A.DST] < 0:
                      prob += cls.Y[a[A.SNK]][t][k] == 0

    @classmethod
    def inflow_outflow(cls, prob):
        for k in cls.TIME:
            for v0 in cls.INTER:
                label = 'inout_flow_' +str(k) + '_' +str(v0)
                arcsIn = cls.arcs_ending_at(v0, k)
                arcsOut = cls.arcs_starting_here(v0, k)
                in_arcs = [[ cls.X[a[A.SRC]][a[A.SNK]][t][k-a[A.DST]] for t in cls.TASK] for a in arcsIn]
                out_arcs =[[ cls.X[a[A.SRC]][a[A.SNK]][t][k] for t in cls.TASK] for a in arcsOut]
                if in_arcs.__len__() == 0: in_arcs = [0]
                if out_arcs.__len__() == 0: out_arcs = [0]
                prob += lpSum(in_arcs) == lpSum(out_arcs), label

    #if the task ends here, the sum of outgoing tasks which do not orgin here has to be zero
    @classmethod
    def task_travel(cls, prob):
        for k in cls.TIME:
            for t in cls.TASKLIST:
                for v0 in cls.NODES:
                    if v0 == cls.snk_tasks[t]:
                        for a in cls.ARCS:
                            for t2 in cls.TASKLIST:
                                if a[A.SRC] != cls.src_tasks[t2]:
                                    prob += cls.X[a[A.SRC]][a[A.SNK]][t2][k] == 0

    @classmethod
    def arctravel_capacity(cls, prob):
        for k in cls.TIME:
            for a in cls.ARCS:
                useTime = min(k+a[A.DST]-1, cls.epsilonTravel) if cls.useEpsilon else k+a[A.DST]-1
                travelWindow = range(k, min(useTime, cls.T))
                if travelWindow.__len__() > 0:
                    arcWindow = [[cls.X[a[A.SRC]][a[A.SNK]][t][k_win] for k_win in travelWindow] for t in cls.TASK]
                    if arcWindow.__len__() == 0: arcWindow = [0]
                    prob += lpSum(arcWindow) <= cls.edgeCap, "arctravel_" +str(k) +'_' +str(a)

    @classmethod
    def tasks_must_go_on(cls, prob):
        for k in cls.TIME:
            for t in cls.TASKLIST:
                for v0 in list(filter(lambda v: v != cls.src_tasks[t] and v != cls.snk_tasks[t], cls.INTER)):
                    arcsOut = cls.arcs_starting_here(v0, k)
                    arcsum = [ cls.X[a[A.SRC]][a[A.SNK]][t][k] for a in arcsOut]
                    if arcsum.__len__() == 0:
                        arcsum = [0]
                    prob += cls.Y[v0][t][k] == lpSum(arcsum), 'tasks_go_on_' +str(k) +'_' +str(t) + '_' +str(v0)

    @classmethod
    def tasks_must_be_dropped(cls, prob):
        for k in cls.TIME:
            for t in cls.TASKLIST:
                for v0 in list(filter(lambda v: v == cls.snk_tasks[t], cls.INTER)):
                    arcsOut = cls.arcs_starting_here(v0)
                    arcsum = [cls.X[a[A.SRC]][v0][t][k] for a in arcsOut]
                    if arcsum.__len__() == 0: arcsum = [0]
                    prob += lpSum(arcsum) == 0, 'tasks_dropped_' +str(k) +'_' +str(t) + '_' +str(v0)

    @classmethod
    def tasks_lower_bound(cls, prob):
        for t in cls.TASKLIST:
            taskSum = [cls.Y[cls.snk_tasks[t]][t][k] for k in cls.TIME]
            prob += lpSum(taskSum) >= cls.taskLowerBound

    @classmethod
    def node_capacity(cls, prob):
        for k in cls.TIME:
            for v0 in cls.INTER:
                nodeSum = [cls.Y[v0][t][k] for t in cls.TASK]
                if nodeSum.__len__() == 0: nodeSum = [0]
                prob += lpSum(nodeSum) <= cls.nodeCap

    @classmethod
    def start_node_task(cls, prob):
        for k in cls.TIME:
            for t in cls.TASKLIST:
                for v0 in cls.arcs_starting_here(cls.startNode):
                    arcDest = v0[A.SNK]
                    prob += cls.X[cls.startNode][arcDest][t][k] == 0

    @classmethod
    def agv_number_restrictions(cls, prob):
        cls.agv_counter(prob)

    @classmethod
    def agv_counter(cls, prob):
         startArcs = cls.arcs_starting_here(cls.startNode)
         endArcs = cls.arcs_ending_here(cls.endNode)
         startSum = [cls.X[a[A.SRC]][a[A.SNK]] for a in startArcs]
         endSum = [cls.X[a[A.SRC]][a[A.SNK]] for a in endArcs]
         prob += lpSum(startSum) == lpSum(endSum)
         prob += lpSum(startSum) == cls.AGVS

    @classmethod
    def arcs_ending_at(cls, v0, k)->[]:
        arcs = cls.arcs_ending_here(v0)
        return list(filter(lambda s: k-s[A.DST] >= 0, arcs))

    @classmethod
    def arcs_ending_here(cls, v0:int)->[]:
        return list(filter(lambda s: s[A.SNK] == v0, cls.ARCS))

    @classmethod
    def arcs_starting_here(cls, v0:int, k=0)->[]:
        return list(filter(lambda s: s[A.SRC] == v0, cls.ARCS))
