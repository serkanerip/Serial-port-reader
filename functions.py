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

def findAvarage(_fileN):
    data = json.load(open(_fileN))
    _stopLoop = False
    while (not _stopLoop):
        _aralik = raw_input("[+] Araligi giriniz (sayi-sayi cinsinden): ")
        if _aralik.isdigit():
            if int(_aralik) == 99:
                _stopLoop = True
                break
        indexOfDash = _aralik.find("-")
        if _aralik.count('-') != 1 or len(_aralik) == 0 or len(_aralik[:indexOfDash]) == 0 or indexOfDash+1 == len(_aralik):
            continue
        n1 = (_aralik[:_aralik.find("-")])
        n2 = (_aralik[_aralik.find("-")+1:len(_aralik)])
        if not n1.replace('.', '', 1).isdigit() or not n2.replace('.', '', 1).isdigit():
            continue
        n1 = float(n1)
        n2 = float(n2)
        _sum = 0
        _number = 0
        for row in data:
            if float(row["time"]) >= n1 and n2 >= float(row["time"]):
                _sum += row["resistance"]
                _number += 1
        if _number == 0:
            print "[*] Bu aralikta deger bulunamadi!"
        else:
            print "[+] Ortalama= " + str((_sum/_number))


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
