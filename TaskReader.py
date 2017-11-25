class TaskReader:
    tasks = [] #each task has a start and a end node

    def __init__(self, filename = "/home/oskar/Desktop/tasks.txt"):
        self.filename = filename
        self.main()

    def main(self):
        f = open(self.filename, "r")

        while f.readable():
            line = f.readline()
            if  not self.read_row(line): break
        f.close()
        return

    def read_row(self, string_line):
        string_line = string_line.rstrip("\n")
        row = string_line.rsplit("\t")
        if row.__len__() < 3: return False
        self.read_task(row)
        return True

    def read_task(self, task_row):
        task = [int(task_row[1]), int(task_row[2])]
        self.tasks.append(task)