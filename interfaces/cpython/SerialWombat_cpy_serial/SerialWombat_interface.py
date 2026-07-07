import SerialWombat
from ArduinoFunctions import delay
import time
import serial

################################################
#CONFIGURE HERE:
################################################

sw_com_port = setYourComPortHere # example "COM6"
ser = serial.Serial(sw_com_port,115200,timeout=0)


class SerialWombatChip_cpy_serial(SerialWombat.SerialWombatChip):
    ser = 0
    def __init__(self,serialPortName,address = 0):
            SerialWombat.SerialWombatChip.__init__(self)
            self.address = address
            self.ser = serial.Serial(serialPortName,115200,timeout=0)


    def sendReceivePacketHardware (self,tx):
        try:
            clear = [0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55]
            self.ser.write(clear)
            while(self.ser.out_waiting > 0):
                pass
            rx = self.ser.read(size=8) 
            while (len(rx) > 0):
                rx = self.ser.read(size = 1)
            
            self.ser.write(tx)
            rx = self.ser.read(size=8) 
            delaycount = 0
            while (len(rx) < 8 and delaycount < 25):
                newBytes = self.ser.read(size = 8 - len(rx))
                if (len(newBytes) > 0):
                    rx += newBytes
                delay(2)
                delaycount +=1
            return 8,rx  #TODO add error check, size check

        except OSError:
            return -48,bytes("E00048UU",'utf-8')

    def sendPacketToHardware(self,tx):
        try:
            clear = [0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55]
            self.ser.write(clear)
            while(self.ser.out_waiting > 0):
                pass
            rx = self.ser.read(size=8) 
            while (len(rx) > 0):
                rx = self.ser.read(size = 1)
            
            self.ser.write(tx)
            return (8,bytes("E00048UU",'utf-8'))

        except OSError:
            return -48,bytes("E00048UU",'utf-8')

def SerialWombatChipInstance(address):
    return SerialWombatChip_cpy_serial(ser,address)