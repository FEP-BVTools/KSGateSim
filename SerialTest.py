import sys
import glob
import serial
 
#取得目前可使用的COM Port


class SerialCtrl:
    # 取得目前可使用的COM Port
    def serial_ports(self):
        """ Lists serial port names

            :raises EnvironmentError:
                On unsupported or unknown platforms
            :returns:
                A list of the serial ports available on the system
        """
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result

    def ConnectSerial(self,COMNumber,BaudRate):
        try:
            print('連接',COMNumber)
            self.ser=serial.Serial(COMNumber,eval(BaudRate),timeout=0.01)
        except:
            print('連接失敗')

    def GetAvailableCOMPorts(self):
        for x in ser.serial_ports():
            print(x)

    def GetDebugHexInfo(self):
        #data = self.ser.readline().decode("big5")
        data=[]
        for x in self.ser.readlines():
            data.append(x)
            for y in x:
                print(hex(y)[2::].upper(), end=' ')

        return data

    def GetDebugTextInfo(self):
        data=[]
        for x in self.ser.readlines():
            data.append(x)
            print(x,end=' ')
        return data

    def GetDebugInfo(self):
        data=self.ser.readlines()
        # print(data)
        HexCMD = bytearray()
        if len(data)>1:
            for x in data:
                for y in x:
                    HexCMD.append(y)
        elif len(data)==1:
            for x in data[0]:
                HexCMD.append(x)

        return HexCMD

    def SerialClose(self):
        self.ser.close()
        print()
        print("已關閉COM port")

    def SerialWrite(self,words):
        self.ser.write(words)
        self.ser.flush()


 
if __name__ == '__main__':
    # print('Version:V1.0')

    ser=SerialCtrl()
    print(ser.serial_ports())

    # # ser.GetCOMPorts()
    # # COMPortNumber=input('輸入連接埠:')
    # # BuadRate = eval(input('輸入速率:'))
    # ser.ConnectSerial(serial_ports()[0],'57600')
    #
    # CommandWords='EA 01 00 00 01 00 90 00'
    # a=CommandWords.split(' ')
    # HexCMD = bytearray()
    # for x in a:
    #     base16INT = int(x, 16)
    #     HexCMD.append(base16INT)
    #
    # ser.SerialWrite(HexCMD)
    # ser.GetDebugInfo()
    #
    # ser.SerialClose()



