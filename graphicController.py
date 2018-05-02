import matplotlib.pyplot as plt
import matplotlib.animation as anim
import threading

class GraphicController:
    def __init__(self, xData, yData, sc, xLabel="Time", yLabel="Conductivity"):
        self.fig, self.ax = plt.subplots()
        self.xLabel = xLabel
        self.yLabel = yLabel
        plt.xlabel(xLabel)
        plt.ylabel(yLabel)
        self.x = xData
        self.y = yData
        self.sc = sc
        self.allData = []
        self.pause = False
        self.read = True
        self.closeReadThread = False
        self.readThread = threading.Thread(target=self.ReadData)
        

    def Start(self):
        self.animation = anim.FuncAnimation(self.fig, self.Update, interval=50,blit=False)
        self.readThread.start()
        plt.show()
        self.pause = True
        self.closeReadThread = True
        self.readThread.join()

    def Update(self, i):
        if not self.pause:
            self.ax.clear()
            self.ax.grid(b=True, which="major", color="black", linestyle="-")
            self.ax.plot(self.x, self.y)

    def Refresh(self, x, y):
        self.fig, self.ax = plt.subplots()
        plt.xlabel(self.xLabel)
        plt.ylabel(self.yLabel)
        self.read = True
        self.pause = False
        self.closeReadThread = False
        self.allData = []
        self.readThread = threading.Thread(target=self.ReadData)
        self.x = x
        self.y = y

    def ReadData(self):
        while(not self.closeReadThread):
            if self.read:
                obj = self.sc.ReadData()
                if not self.sc.anyError:
                    self.allData.append(obj)
                    self.x.append(obj['time'])
                    self.y.append(obj['volt'])
                else:
                    self.closeReadThread = True


