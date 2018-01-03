from enum import Enum


class ModelData(Enum):
    epsilonTravel = 1
    useEpsilon = 2
    startNode = 3
    endNode = 4
    travelTask = 5
    taskLowerBound = 6
    nodeCap = 7
    edgeCap = 8
    T = 9
    agv = 10
    snk_tasks = 11
    src_tasks = 12
    arcs = 13

