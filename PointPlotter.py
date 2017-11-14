import matplotlib
import matplotlib.pyplot as plt


class PointPlotter:

    points = []
    segments = []
    def __init__(self ,filename):
        self.filename = filename
        self.main()

    def main(self):
        f = open(self.filename, "r")

        while f.readable():
            line = f.readline()
            cont_read = self.read_row(line)
            if not cont_read:
                break

        f.close()
        return

    def read_row(self, string_line):
        string_line = string_line.rstrip("\n")
        row = string_line.rsplit(" ")

        if row[0] == 'point':
            self.read_point(row)
            return True
        elif row[0] == 'segment':
            self.read_segment(row)
            return True
        else:
            return False

    def read_point(self ,arrayPoint):
        point = [arrayPoint[2] ,arrayPoint[3]]
        self.points.append(point)


    def read_segment(self ,arraySegment):  # not complete
        segment = [arraySegment[2] ,arraySegment[3]]
        self.segments.append(segment)

    def plot(self):
        fig, ax = plt.subplots()
        x = [x[0] for x in self.points]
        y = [x[1] for x in self.points]
        ax.scatter(x, y)
        ax.grid()
        plt.show()
        print(self.points)



pp = PointPlotter("~/Documents/layout.txt")
pp.plot()
