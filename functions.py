import json
import matplotlib.pyplot as plt
import serial.tools.list_ports

def readAndVisualize(filename):
    data = json.load(open(filename))
    x = []
    y = []
    for row in data:
        x.append(row['time'])
        y.append(row['resistance'])
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

def saveData(data):
    _fileN = raw_input("[*] Kaydedilecek dosyanin adini giriniz: ")
    with open(_fileN, "w") as outFile:
        json.dump(data, outFile)
    print "[+] Dosya Kaydedildi!"

def checkPortIsAvailable(port):
    ports = list(serial.tools.list_ports.comports())
    if len(ports) == 0:
        return False
    else:
        for i in ports:
            strPort = str(i)
            if port in strPort:
                return True
    return False

def setSerialPort():
    ports = list(serial.tools.list_ports.comports())
    print "Serial Portu Secin:"
    if len(ports) == 0:
        print "Herhangi bir acik port bulunamadi!"
        exit(0)
    else:
        _in = -1
        _index = 0
        for i in ports:
            print "[" + str(_index) + "]: " + str(i)
        _in = (raw_input("Secim: "))
        if not _in.isdigit():
            print "Boyle bir port bulunmamaktadir!"
            exit(0)
        _in = int(_in)
        if (_in >= 0 and _in < len(ports)):
            _secim = str(ports[_in])
            PORT = _secim.split(" ")[0]
            return PORT
        else:
            print "Boyle bir port bulunmamaktadir!"
            exit(0)
