from tkinter import SW

import SerialWombat
from ArduinoFunctions import delay
import time
import serial
import sys


################################################
#CONFIGURE HERE:
################################################
SW_SERIAL_PORT = "COM6"



class SerialWombatChip_cpy_serial_addressed(SerialWombat.SerialWombatChip):
    ser = 0
    def __init__(self,openedSerialPort,address ):
            SerialWombat.SerialWombatChip.__init__(self)
            self.address = address
            self.ser = openedSerialPort

    def sendReceivePacketHardware (self,tx):
        try:
            clear = [0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55]
            self.ser.write(clear)
            while(self.ser.out_waiting > 0):
                pass
            rx = self.ser.read(size=8) 
            while (len(rx) > 0):
                rx = self.ser.read(size = 1)
            
            self.ser.write([self.address])  
            self.ser.write(tx)
            while(self.ser.out_waiting > 0):
                pass
            rx = self.ser.read(size=8) 
            delaycount = 0
            while (len(rx) < 8 and delaycount < 25):
                newBytes = self.ser.read(size = 8 - len(rx))
                if (len(newBytes) > 0):
                    rx += newBytes
                delay(2)
                delaycount +=1
            if (len(rx) < 8):
                return -48,bytes("E00048UU",'utf-8')
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
            
           
            self.ser.write([self.address])  #this is for I2C Bridge when using an arduino or Micropython to do UART to I2C conversion.  
            self.ser.write(tx)
            return (8,bytes("E00048UU",'utf-8'))

        except OSError:
            return -48,bytes("E00048UU",'utf-8')



def SerialWombatChipInstance(address):
    ser = serial.Serial(SW_SERIAL_PORT,115200,timeout=0)
    return SerialWombatChip_cpy_serial_addressed(ser,address)


