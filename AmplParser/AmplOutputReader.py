
class AmplOutputReader:
    path = ''

    T = 0
    TASKS = 0

    src = 0
    snk = 0
    tsk = 0
    tme = 0

    SRC_LIST = []
    TSK_LIST = []
    X = []
    X_TEMP = []

    def __init__(self,file_path):
        self.path = file_path

    def readAmplOutput(self):
        f = open(self.path, "r")

        while f.readable():
            line = f.readline()
            if line == '': break
            self.getLine(line)


        f.close()
        print('time:', self.T)
        print('tasks:', self.TSK_LIST)
        print('nodes:', self.SRC_LIST)
        print(self.X)
        return

    def getLine(self,line):
        if line.__contains__('['):
            self.getStart(line)
        elif line[0].isdigit():
            self.readXrow(line)

    def getStart(self,x_line):
        array = x_line.rsplit('[')
        array = array[1].rsplit(']')
        array = array[0]
        [src,self.snk,tsk,self.tme] = array.rsplit(',')
        self.src = int(src)
        self.tsk = int(tsk)
        if not self.SRC_LIST.__contains__(self.src): self.SRC_LIST.append(self.src)
        if not self.TSK_LIST.__contains__(self.tsk): self.TSK_LIST.append(self.tsk)
        self.X.append(self.X_TEMP)

    def readXrow(self,line):
        cells = line.rsplit(' ')
        cells = list(filter(None,cells))
        time = cells[0]
        cells = [int(cell.rstrip('\n')) for cell in cells]
        self.storeXrow(cells)

    def storeXrow(self,x_row:[int]):
        self.tme = x_row[0]
        if(self.tme > self.T): self.T = self.tme
        self.X_TEMP.append(x_row[1:])