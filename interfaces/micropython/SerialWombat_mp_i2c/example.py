import SerialWombat
from ArduinoFunctions import delay, delayMicroseconds, millis


SW_ADDRESS = 0x6B  #Change the address to match your configuration

import SerialWombat_interface
sw = SerialWombat_interface.SerialWombatChipInstance(SW_ADDRESS)  

#note that the above initializes the I2C bus.  If you want to use mulitple Serial
#wombat chips or other i2c devices, initalize the bus yourself, and call
# sw = SerialWombatChip_cp_i2c(yourI2CAddress, yourI2Cbus)

def setup():
    # put your setup code here, to run once:
    # Wire.begin() is handled by the selected Python interface block

    # Serial.begin() is not used in this Python example
    delay(3000)


    sw.begin()  # Python interface was configured above
  
    print("Querying Serial Wombat Chip...\n")

    # Read chip information
    sw.queryVersion()

    print(f"Model:            {sw.model.decode('ascii')}")
    print(f"Firmware Version: {sw.fwVersion.decode('ascii')}")
    print(f"Unique ID:        {sw.uniqueIdentifier}")
    print(f"Device Revision:  {sw.deviceRevision}")
    print(f"Supply Voltage:   {sw.readSupplyVoltage_mV()} mV")




def loop():

  # put your main code here, to run repeatedly:
  counter = sw.readPublicData(
        SerialWombat.SerialWombatDataSource.SW_DATA_SOURCE_INCREMENTING_NUMBER
    )
  print(counter)
  delay(2000)


setup()
while True:
    loop()
