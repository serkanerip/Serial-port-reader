'''
*** This project writed by AHURA-MAZDA
'''
from serialController import SerialController
from graphicController import GraphicController
from functions import readAndVisualize, saveData, setSerialPort, checkPortIsAvailable, findAvarage
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
    gc.Init(XDATA, YDATA)

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
        Refresh()
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
        if not os.path.exists(_fileN):
            print "[Hata] Dosya bulunamadi!"
        else:
            data = json.load(open(_fileN))
            findAvarage(_fileN)
