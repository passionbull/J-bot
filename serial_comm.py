#!/usr/bin/env python3
import serial
import threading
import time
class SerialComm:
    def __init__(self):
        self.comm = serial.Serial('/dev/serial/by-id/usb-Arduino_LLC_Arduino_Leonardo-if00',9600)
        self.isWorking = True
        self.distance = 0
        self.angle = 0
    
    def action(self):
        self.motorControl(60)
        time.sleep(1)
        self.motorControl(140)

    def read(self):
        try:
            output = self.comm.readline()
            output = str(output)
            output = output.replace("b'","")
            output = output.replace("\\r\\n'","")
            data = output.split('*')
            # print(data)
            self.distance = int(data[0])
            self.angle = int(data[1])
        except:
            self.distance = 10000

    def motorControl(self, angle):
        if self.comm is None:
            return 0
        msg_motor = str(angle)+'*'
        self.comm.write(msg_motor.encode())        

def main():
    sc1 = SerialComm()


if __name__ == '__main__':
    main()
        

    