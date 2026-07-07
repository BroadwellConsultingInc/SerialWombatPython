import SerialWombat
import time
import machine

################################################
#CONFIGURE HERE:
################################################
SW_I2C_BUS = 1		
SW_SCL_PIN = machine.pin(7) # D5
SW_SDA_PIN = machine.pin(6) # D4
SW_I2C_FREQ = 100000

class SerialWombatChip_mp_i2c(SerialWombat.SerialWombatChip):
    i2c  = 0
    def __init__(self,address,i2c_port):
        super().__init__()
        self.i2c = i2c_port
        self.address = address



    def sendReceivePacketHardware (self,tx):
        try:
            if (isinstance(tx,list)):
                tx = bytearray(tx);
            
            self.i2c.writeto(self.address,tx)
            rx = self.i2c.readfrom(self.address,8)
            if (len(rx) < 8 ):
                return (-len(rx))
            return 8,rx  
        except OSError:
            return -48,bytes("E00048UU",'utf-8')

    def sendPacketToHardware (self,tx):
        try:
            if (isinstance(tx,list)):
                tx = bytearray(tx);
            
            self.i2c.writeto(self.address,tx)
            return 8,bytes("E00048UU",'utf-8')  
        except OSError:
            return -48,bytes("E00048UU",'utf-8')

def SerialWombatChipInstance(address):
    i2c_port = machine.I2C(SW_I2C_BUS, scl=machine.Pin(SW_SCL_PIN), sda=machine.Pin(SW_SDA_PIN), freq=SW_I2C_FREQ)
    return SerialWombatChip_mp_i2c(address,i2c_port)