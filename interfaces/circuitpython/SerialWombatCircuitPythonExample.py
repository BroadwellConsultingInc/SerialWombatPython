

import SerialWombat
from ArduinoFunctions import delay
from ArduinoFunctions import millis


import board
import busio
import SerialWombat_cp_i2c
swI2Caddress = 0x6B
i2c = busio.I2C(board.SCL,board.SDA)
sw = SerialWombat_cp_i2c.SerialWombatChip_cp_i2c(i2c,swI2Caddress)
sw.address = 0x6B



#Interface independent code starts here:


def setup() :
  # put your setup code here, to run once:
  sw.begin()


def loop():
  # put your main code here, to run repeatedly:
   delay(200);
   print("Frames:")
   print(sw.readPublicData(SerialWombat.SerialWombatDataSource.SW_DATA_SOURCE_FRAMES_RUN_LSW))
   print("Vcc Voltage:")
   print(sw.readPublicData(SerialWombat.SerialWombatDataSource.SW_DATA_SOURCE_VCC_mVOLTS))
   print()

	

setup()
while(True):
    loop()

