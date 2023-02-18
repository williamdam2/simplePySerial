import serial
import sys
import threading

class SerialPort:
    def __init__(self):
        self.comportName:str = ""
        self.baud:int = 0
        self.timeout:int = None
        self.isopen:bool = False
        self.receivedMessage:bytes = None
        self.serialport = serial.Serial()
        self.ReceiveLineCallbackFunction = None
        self.ReceiveCallBackThread:threading.Thread = None
    def __del__(self):
        try:
            if self.IsOpen():
                self.serialport.close()
            else:
                pass
        except:
            print("Destructor error closing COM port: ", sys.exc_info()[0] )

    def RegisterReceiveLineCallback(self,receiveCallBackFuncPointer):
        try:
            self.ReceiveLineCallbackFunction = receiveCallBackFuncPointer
            self.ReceiveCallBackThread = threading.Thread(target=self.SerialReadlineThread)
        except:
            print("Fail to register a thread for receive message")
            print("Error:",sys.exc_info()[0])

    def SerialReadlineThread(self):
        print("callback thread start")
        while True:
            try:
                if self.IsOpen():
                    self.receivedMessage = self.serialport.readline()                           
                    if self.receivedMessage != "":
                        try:
                            message = self.receivedMessage.decode("utf-8",errors="ignore")
                            self.ReceiveLineCallbackFunction(message)
                        except:
                            print("decode fail")
                            pass
                else:
                    break
            except:
                print("Error reading COM port: ", sys.exc_info()[0])

    def IsOpen(self):
        return self.isopen

    def Open(self,portname,baudrate):
        if not self.isopen:
            # serialPort = 'portname', baudrate, bytesize = 8, parity = 'N', stopbits = 1, timeout = None, xonxoff = 0, rtscts = 0)
            self.serialport.port = portname
            self.serialport.baudrate = baudrate
            try:
                self.serialport.open()
                self.isopen = True
                self.ReceiveCallBackThread.start()
                
            except:
                print("Error opening COM port: ", sys.exc_info()[0])

    def Close(self):
        if self.isopen:
            self.isopen = False
            try:
                self.serialport.close()
            except:
                print("Close error closing COM port: ", sys.exc_info()[0])

    def Send(self,message):
        if self.isopen:
            try:
                # Ensure that the end of the message has both \r and \n, not just one or the other
                newmessage = message.strip()
                newmessage += '\r\n'
                self.serialport.write(newmessage.encode('utf-8'))
            except:
                print("Error sending message: ", sys.exc_info()[0] )
            else:
                return True
        else:
            return False




