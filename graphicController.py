import matplotlib.pyplot as plt
import matplotlib.animation as anim
import threading

class GraphicController:
    def __init__(self, xData, yData, sc, xLabel="Time", yLabel="Resistance"):
        self.sc = sc
        self.Init(xData, yData)
        self.xLabel = xLabel
        self.yLabel = yLabel
        plt.xlabel(xLabel)
        plt.ylabel(yLabel)

    def Init(self, x, y):
        plt.close("all")
        self.fig, self.ax = plt.subplots()
        self.x = x
        self.y = y
        self.allData = []
        self.pause = False
        self.read = True
        self.closeReadThread = False
        self.readThread = threading.Thread(target=self.ReadData)
        if self.sc.CheckPort:
            self.sc.Close()
            self.sc.Open()


    def Start(self):
        self.animation = anim.FuncAnimation(self.fig, self.Update, interval=50,blit=False)
        self.readThread.start()
        plt.show()
        plt.close("all")
        self.pause = True
        self.closeReadThread = True
        self.readThread.join()

    def Update(self, i):
        if not self.pause:
            self.ax.clear()
            self.ax.grid(b=True, which="major", color="black", linestyle="-")
            if (len(self.x) > len(self.y)):
                print "x daha buyuk"
            elif len(self.y) > len(self.x):
                print "y daha buyuk"
            try:
                self.ax.plot(self.x, self.y)
            except:
                print "error"
            self.pause = True

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
                    self.y.append(obj['resistance'])
                    self.pause = False
                else:
                    self.closeReadThread = True


