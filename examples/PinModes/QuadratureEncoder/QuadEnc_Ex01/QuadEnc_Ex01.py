# Converted from PinModes/QuadratureEncoder/QuadEnc_Ex01/QuadEnc_Ex01.ino
import SerialWombat
from ArduinoFunctions import delay, delayMicroseconds, millis

import SerialWombat_interface
# >>> IMPORTANT: Set this to the configured I2C address of your Serial Wombat chip.
SERIAL_WOMBAT_ADDRESS = 0x6B
sw = SerialWombat_interface.SerialWombatChipInstance(SERIAL_WOMBAT_ADDRESS)


# Interface independent code starts here:
import SerialWombatQuadEnc

# ===== Arduino tab: QuadEnc_Ex01.ino =====
# sw is provided by the selected Python interface block above
# Declare a Serial Wombat chip
qeBasic = SerialWombatQuadEnc.SerialWombatQuadEnc(sw)
qeWithPullUps = SerialWombatQuadEnc.SerialWombatQuadEnc(sw)
# This example is explained in a video tutorial at: https://youtu.be/_wO8cOada3w
def setup():
  # put your setup code here, to run once:
  # Wire.begin() is handled by the selected Python interface block
  # Initialize the I2C Bus on default pins
  # Serial.begin() is not used in this Python example
  delay(3000)
  print("1Hz Blink Example")
  sw.begin()  # Python interface was configured above
  # Scan the bus for Serial Wombat chips, and initialize the first one found
  # Optional Error handling code begin:
  if not sw.isLatestFirmware():
    print("Firmware version mismatch. Download latest Serial Wombat Arduino Library and update Serial Wombat Firmware to latest version")
  if sw.isSW08() and not sw.isPinModeSupported(SerialWombat.SerialWombatPinMode_t.PIN_MODE_QUADRATUREENCODER):
    print("The required pin mode does not appear to be supported in this firmware build. Do you need to download a different firmware?")
    while 1:
      delay(100)
  # sw.registerErrorHandler(...) is Arduino-specific; Python errors are returned by library calls
  # Register an error handler that will print communication errors to Serial
  # Optional Error handling code end
  qeBasic.begin(0, 1)
  # Initialize a QE on pins 0 and 1
  qeWithPullUps.begin(2, 3)
  # Initialize a QE on pins 2 and 3  Change these to different pins (say 18 and 19) on the SW18AB, since 3 is SDA
def loop():
  print(qeBasic.read(), end="")
  print(" ", end="")
  print(qeWithPullUps.read(), end="")
  print()
  delay(50)

setup()
while True:
  loop()
