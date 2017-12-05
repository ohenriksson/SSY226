from PointPlotter import PointPlotter
from TaskReader import TaskReader
import numpy as np
from modelspec import *


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
        self.__class__.path = path

    def writeDatFile(self,filename):
        self.print_to_file(filename,"teststring")

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
