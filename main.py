from serialController import SerialController
from graphicController import GraphicController
from openSavedData import readAndVisualize
import threading
import json
import os.path
import serial.tools.list_ports

XDATA = []
YDATA = []
PORT = -1
FILENAME = "sample.json"


def saveData(fname):
    with open(fname, "w") as outFile:
        json.dump(gc.allData, outFile)

def Refresh():
    XDATA = []
    YDATA = []
    gc.Refresh(XDATA, YDATA)
    sc.Close()
    sc.serial.open()

stop = False
stdinput = 99
ft = True

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
    else:
        print "Boyle bir port bulunmamaktadir!"
        exit(0)

sc = SerialController(PORT)
gc = GraphicController(xData=XDATA, yData=YDATA, sc=sc)

while(not stop):
    if sc.anyError:
        if len(XDATA) > 0:
            e_h = raw_input("[Bilgi] Port kapandi son alinan verileri kaydetmek istiyor musunuz?[e/h]: ")
            if e_h == 'e':
                _fileN = raw_input("[*] Kaydedilecek dosyanin adini giriniz: ")
                saveData(_fileN)
                print "[+] Dosya Kaydedildi!"
        exit(0)
    print "\n\nGSR -----------------KONTROL PROGRAMI------------------------------"
    print "[0]: Olcumu baslatmak icin!"
    print "[1]: Olcum verilerini kaydetmek!"
    print "[2]: Kayitli olcum verilerini grafikte gormek!"
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
        _fileN = raw_input("[*] Kaydedilecek dosyanin adini giriniz: ")
        saveData(_fileN)
        print "[+] Dosya Kaydedildi!"
    elif stdinput == "2":
        _fileN = raw_input("[*] Dosyanin adini giriniz: ")
        if not os.path.exists(_fileN):
            print "[Hata] Dosya bulunamadi!"
        else:
            readAndVisualize(_fileN)