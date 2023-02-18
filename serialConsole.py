import serial_rx_tx
import time
import json

# Check the log file


serialPort = serial_rx_tx.SerialPort()
# config
serialPort.comportName = 'COM3'
serialPort.baud = 115200



# Callback when received a line 
def calback_onReceivedLine(message:str):
    print(message)

# define the callback
serialPort.RegisterReceiveLineCallback(calback_onReceivedLine)

print("Start open")
try:
    serialPort.Open(serialPort.comportName,serialPort.baud)
    print("COM Port Opened")
    while(True):
        a = input()
        if(a=="stop"):
            break
except Exception as e:
    print("unhandle exception")
    print(e)
print("closing")
serialPort.Close()
if(serialPort.Close):
    print("closed")