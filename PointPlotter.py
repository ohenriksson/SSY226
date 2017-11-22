import matplotlib.pyplot as plt
from matplotlib import collections


class PointPlotter:

    points_id = []
    points = []
    segments = []

    def __init__(self, filename):
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

    def read_point(self, arrayPoint):
        point_id = arrayPoint[1]
        point = [arrayPoint[2], arrayPoint[3]]
        self.points_id.append(point_id)
        self.points.append(point)

    def read_segment(self, arraySegment):  # not complete
        segment = [arraySegment[2], arraySegment[3]]
        coords = []
        for i in segment:
            index = self.points_id.index(i)
            coords.append((self.points[index][0], self.points[index][1]))

        self.segments.append(coords)

    def plot(self):
        fig, ax = plt.subplots()
        x = [x[0] for x in self.points]
        y = [x[1] for x in self.points]
        line_segments = collections.LineCollection(self.segments, colors='grey', linewidths=0.5)
        ax.scatter(x, y)
        ax.add_collection(line_segments)
        ax.grid()
        plt.show()
        #print(self.points)

pp = PointPlotter("/home/oskar/Desktop/layout.txt")
pp.plot()
print(pp.segments)
