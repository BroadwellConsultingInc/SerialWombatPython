import SerialWombat
import board
import busio
import time

################################################
#CONFIGURE HERE:
################################################
SW_SCL_PIN = board.SCL
SW_SDA_PIN = board.SDA



class SerialWombatChip_cp_i2c(SerialWombat.SerialWombatChip):
    i2c  = 0
    def __init__(self,address,i2cPort):
        super().__init__()
        self.i2c = i2cPort
        self.address = address



    def sendReceivePacketHardware (self,tx):
        try:
            while not self.i2c.try_lock():
                pass
            if (isinstance(tx,list)):
                tx = bytearray(tx);
            
            self.i2c.writeto(self.address,tx)
            rx = bytearray(8);
            self.i2c.readfrom_into(self.address,rx)
            if (len(rx) < 8 ):
                self.i2c.unlock()
                return (-len(rx))
            self.i2c.unlock()
            return 8,rx  
        except OSError:
            self.i2c.unlock()
            return -48,bytes("E00048UU",'utf-8')

    def sendPacketToHardware (self,tx):
        try:
            while not self.i2c.try_lock():
                pass
            if (isinstance(tx,list)):
                tx = bytearray(tx);
            
            self.i2c.writeto(self.address,tx)
            self.i2c.unlock()
            return 8,bytes("E00048UU",'utf-8')  
        except OSError:
            self.i2c.unlock()
            return -48,bytes("E00048UU",'utf-8')

def SerialWombatChipInstance(address):
    sw_i2c = busio.I2C(SW_SCL_PIN, SW_SDA_PIN)
    return SerialWombatChip_cp_i2c(address,sw_i2c)