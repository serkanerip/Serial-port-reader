import serial

class SerialController:
    def __init__(self, _port):
        self.port = _port
        self.anyError = False
        try:
            self.serial = serial.Serial(port=self.port, baudrate=9600, bytesize=serial.EIGHTBITS)
            self.Close()
            self.serial.open()
        except IOError, e:
            self.anyError = True
            self.error = str(e)

    def ReadData(self):
        unPackedData = ""
        try:
            unPackedData = self.serial.readline()
            if unPackedData.find(',') == -1:
                self.anyError = True
                self.error = "[Hata]: Bozuk veri!"
                return {}
            resistance, time = unPackedData.split(',')
            if not resistance.replace('.', '', 1).isdigit() or not time.replace('.', '', 1):
                self.anyError = True
                self.error = "[Hata]: Bozuk veri!"
                return {}
            resistance = float(resistance)
            time = float(time)
            self.anyError = False
            self.error = ""
            return { 'resistance': resistance, 'time': time }
        except serial.SerialException, e:
            self.anyError = True
            self.error = "[Hata]: Baglanti hatasi!"
            print self.error
            return {}
    def CheckPort(self):
        return self.serial.isOpen()
    def Close(self):
        self.serial.close()




