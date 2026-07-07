import SerialWombat
import time
import machine

################################################
#CONFIGURE HERE:
################################################
SW_UART_BUS = 1
SW_UART_TX_PIN = 4
SW_UART_RX_PIN = 5


class SerialWombatChipUART(SerialWombat.SerialWombatChip):
    sw_ser  = 0
    def __init__(self,port):
        self.ser = port
        SerialWombat.SerialWombatChip.__init__(self)


    def sendReceivePacketHardware (self,tx):
        if (isinstance(tx,list)):
            tx = bytearray(tx);
        clear = bytearray([0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55])
        self.ser.write(clear)
        self.ser.flush()

        rx = self.ser.read(8) 
        while (rx != None):
            rx = self.ser.read(1)
        self.ser.write(tx)
        #self.ser.write([self.address])  #TODO this is for I2C Bridge.  Remove
        rx = self.ser.read(8)
        if (rx== None):
            rx = bytearray()
        delaycount = 0
        while (len(rx) < 8 and delaycount < 25):
            newBytes = self.ser.read(8 - len(rx))
            if (newBytes != None and len(newBytes) > 0):
                rx += newBytes
            time.sleep(.002)
            delaycount +=1
        return 8,rx  #TODO add error check, size check
		
    def sendPacketToHardware (self,tx):
        if (isinstance(tx,list)):
            tx = bytearray(tx);
        clear = bytearray([0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55])
        self.ser.write(clear)
        self.ser.flush()

        rx = self.ser.read(8) 
        while (rx != None):
            rx = self.ser.read(1)
        self.ser.write(tx)
        return 8,bytes("E00048UU",'utf-8')  

	
def SerialWombatChipInstance(address): #address not used...
    uart_port = machine.UART(SW_UART_BUS, tx=machine.Pin(SW_UART_TX_PIN), rx=machine.Pin(SW_UART_RX_PIN))
    return SerialWombatChipUART(uart_port)
