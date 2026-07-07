import SerialWombat
import time
from smbus2 import SMBus, i2c_msg


################################################
#CONFIGURE HERE:
################################################
I2C_BUS = 1


class SerialWombatChip_smbus2_i2c(SerialWombat.SerialWombatChip):
    
    def __init__(self,i2c,address):
        super().__init__()
        self.i2c = i2c
        self.address = address




    def sendReceivePacketHardware (self,tx):
        try:
            if (isinstance(tx,list)):
                tx = bytearray(tx);
            
            msg = i2c_msg.write(self.address,tx)
            self.i2c.i2c_rdwr(msg)
            rx = i2c_msg.read(self.address,8)
            self.i2c.i2c_rdwr(rx)
            
            if (len(rx) < 8 ):
                return (-len(rx))
            return 8,list(rx)  
        except OSError:
            return -48,bytes("E00048UU",'utf-8')

    def sendPacketToHardware (self,tx):
        try:
            if (isinstance(tx,list)):
                tx = bytearray(tx);
            
            msg = i2c_msg.write(self.address,tx)
            self.i2c.i2c_rdwr(msg)
            return 8,bytes("E00048UU",'utf-8')  
        except OSError:
            return -48,bytes("E00048UU",'utf-8')



def SerialWombatChipInstance(address):
    swi2cbus = SMBus(I2C_BUS)
    return SerialWombatChip_smbus2_i2c(swi2cbus,address)


