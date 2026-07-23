# Converted from PinModes/UniqueID_SW4B/UniqueID_SW4B.ino
import SerialWombat
from ArduinoFunctions import delay, delayMicroseconds, millis

import SerialWombat_interface
# >>> IMPORTANT: Set this to the configured I2C address of your Serial Wombat chip.
SERIAL_WOMBAT_ADDRESS = 0x60
sw = SerialWombat_interface.SerialWombatChipInstance(SERIAL_WOMBAT_ADDRESS)


# Interface independent code starts here:

# ===== Arduino tab: UniqueID_SW4B.ino =====
# See https://youtu.be/IHTcKyXT_2Q for a tutorial on how to use Unique ID
# sw is provided by the selected Python interface block above
def setup():
  # Serial.begin() is not used in this Python example
  # Wire.begin() is handled by the selected Python interface block
  delay(500)
  i2cAddress = sw.find()
  sw.begin()  # Python interface was configured above
  # Initialize the Serial Wombat library to use the primary I2C port
  # sw.registerErrorHandler(...) is Arduino-specific; Python errors are returned by library calls
  # Register an error handler that will print communication errors to Serial
def loop():
  # put your main code here, to run repeatedly:
  print("Version: ", end="")
  print(sw.readVersion())
  # readVersion() must be called prior to using the data below
  print("UniqueIDLength: ", end="")
  print(sw.uniqueIdentifierLength)
  print("0x6C UniqueID: ", end="")
  for i in range(0, sw.uniqueIdentifierLength):
    print("%X " % (sw.uniqueIdentifier[i],), end="")
  print()
  print("0x6C DeviceId: ", end="")
  print(sw.deviceIdentifier)
  print("0x6C DeviceRevision: ", end="")
  print(sw.deviceRevision)
  delay(2000)

setup()
while True:
  loop()
