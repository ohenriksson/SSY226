import matplotlib
import matplotlib.pyplot as plt


class TaskPlotter:
    tasks = []

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
        row = string_line.rsplit("\t")
        self.read_task(row)

    def read_task(self, taskRow):
        task = [taskRow[1], taskRow[2]]
        self.tasks.append(task)

    def plot(self):
        fig, ax = plt.subplots()
        x = [x[0] for x in self.points]
        y = [x[1] for x in self.points]
        ax.scatter(x, y)
        ax.grid()
        plt.show()
        print(self.points)


pp = TaskPlotter("/home/oskar/Desktop/tasks.txt")
print(pp.tasks[1][1])
print( [x[1] for x in pp.tasks.tasks[1]]);
#pp.plot()
