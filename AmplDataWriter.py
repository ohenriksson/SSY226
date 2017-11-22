from PointPlotter import PointPlotter
import numpy as np


class AmplDataWriter:

    bigNumber = 1000000;
    header = []
    separator = " "
    TAUcomplete = ""
    path = "/home/oskar/Desktop/"

    @classmethod
    def main(cls):
        pp = PointPlotter(cls.path + "layout.txt")
        cls.aggrigate(pp)
        cls.print_to_file(cls.TAUcomplete)

        #pp.plot()
        #print(pp.segment_coords)

    @classmethod
    def aggrigate(cls,pp):

        nNodes = len(pp.points_id)

        header = ""
        for i in range(nNodes):
            header += str(i) + cls.separator
        cls.header = header
        print(header)

        TAU = np.ones([nNodes,nNodes])*cls.bigNumber;

        for l,(i,j) in enumerate(pp.segment_ids):
            i1 = pp.points_id.index(str(i))
            i2 = pp.points_id.index(str(j))
            TAU[i1,i2] = pp.segment_distance[l]

        #print(TAU[0:10,0:10])

        row1 = header + "\n"
        for l,i in enumerate(TAU):
            row1 += str(l) + cls.separator
            for cell in i:
                row1 += str(int(cell)) + cls.separator
            row1 += "\n"
        #print(row1)
        cls.TAUcomplete = row1;



    @classmethod
    def print_to_file(cls,string):
        f = open(cls.path + 'helloworld.txt','w')
        f.write(string)
        f.close()
        return

AmplDataWriter.main()

