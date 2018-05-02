import json
import matplotlib.pyplot as plt

def readAndVisualize(filename):
    data = json.load(open(filename))
    x = []
    y = []
    for row in data:
        x.append(row['time'])
        y.append(row['volt'])
    plt.figure(1)
    plt.subplot(311)
    plt.plot(x, y, "r--")
    plt.grid(True)
    plt.subplot(312)
    plt.grid(True)
    plt.plot(x, y, "bo")
    plt.subplot(313)
    plt.plot(x, y)
    plt.grid(True)
    plt.show()

