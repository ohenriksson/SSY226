import matplotlib.pyplot as plt
from matplotlib import collections


class PointPlotter:

    points_id = []
    points = []
    segment_ids = []
    segment_coords = []
    segment_distance = []

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

    def read_point(self, array_point):
        point_id = array_point[1]
        point = [array_point[2], array_point[3]]
        self.points_id.append(point_id)
        self.points.append(point)

    def read_segment(self, array_segment):
        segment = [array_segment[2], array_segment[3]]

        coords = []
        ids = []
        for i in segment:
            index = self.points_id.index(i)
            coords.append((self.points[index][0], self.points[index][1]))
            ids.append(int(self.points_id[index]))

        self.segment_ids.append(ids)
        self.segment_distance.append(array_segment[4])
        self.segment_coords.append(coords)

    def plot(self):
        fig, ax = plt.subplots()
        x = [x[0] for x in self.points]
        y = [x[1] for x in self.points]
        line_segments = collections.LineCollection(self.segment_coords, colors='grey', linewidths=0.5)
        ax.scatter(x, y)
        ax.add_collection(line_segments)
        ax.grid()
        plt.show()
        #print(self.points)
