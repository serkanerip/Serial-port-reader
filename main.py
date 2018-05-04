'''
*** This project writed by AHURA-MAZDA
'''
from serialController import SerialController
from graphicController import GraphicController
from functions import readAndVisualize, saveData, setSerialPort, checkPortIsAvailable
import threading
import json
import os.path

XDATA = []
YDATA = []
PORT = -1
FILENAME = "sample.json"
stop = False
stdinput = 99
ft = True
connected = False

def Refresh():
    XDATA = []
    YDATA = []
    gc.Refresh(XDATA, YDATA)
    sc.Close()
    sc.serial.open()

PORT = setSerialPort()
sc = SerialController(PORT)
gc = GraphicController(xData=XDATA, yData=YDATA, sc=sc)
connected = True

while(not stop):
    connected = checkPortIsAvailable(PORT)
    if not connected:
        if len(gc.allData) > 0:
            e_h = raw_input("[HATA] Port kapandi son verileri kaydetmek istiyor musunuz ?[e/h]: ")
            if e_h == "e":
                saveData(gc.allData)
        exit(0)
    print "\n\nGSR -----------------KONTROL PROGRAMI------------------------------"
    print "[0]: Olcumu baslatmak icin!"
    print "[1]: Olcum verilerini kaydetmek!"
    print "[2]: Kayitli olcum verilerini grafikte gormek!"
    print "[3]: 2 Saniye arasindaki ortalama degeri goster!"
    print "[99]: Cikis!\n\n"
    stdinput = (raw_input("Secenek: "))
    if stdinput == "99":
        stop = True
    elif stdinput == "0":
        if not ft:
            Refresh()
        else:
            ft = False
        gc.Start()
    elif stdinput == "1":
        saveData(gc.allData)
    elif stdinput == "2":
        _fileN = raw_input("[*] Dosyanin adini giriniz: ")
        if not os.path.exists(_fileN):
            print "[Hata] Dosya bulunamadi!"
        else:
            readAndVisualize(_fileN)
    elif stdinput == "3":
        _fileN = raw_input("[*] Dosyanin adini giriniz: ")
        data = json.load(open(_fileN))
        _stopLoop = False
        while (not _stopLoop):
            _aralik = raw_input(" Araligi giriniz (sayi-sayi cinsinden): \n")
            if _aralik.isdigit():
                if int(_aralik) == 99:
                    _stopLoop = True
                    break
            n1 = float(_aralik[:_aralik.find("-")])
            n2 = float(_aralik[_aralik.find("-")+1:len(_aralik)])
            _sum = 0
            _number = 0
            for row in data:
                if float(row["time"]) >= n1 and n2 >= float(row["time"]):
                    _sum += row["volt"]
                    _number += 1
            print "Ortalama: " + str((_sum/_number))

