from pulp import *


class Model2:
    startNode = 1
    endNode = 2
    travelTask = 0
    taskLowerBound = 1
    nodeCap = 1
    edgeCap = 1

    prob = LpProblem("Task Optimizer", LpMaximize)
    X = [3,2,1]
    Y = [2,2,2]
    x = LpVariable.dicts('table',X,lowBound=0, upBound=edgeCap ,cat=LpInteger)
    y = LpVariable.dicts('table',Y,lowBound=0, upBound=endNode ,cat=LpInteger)


