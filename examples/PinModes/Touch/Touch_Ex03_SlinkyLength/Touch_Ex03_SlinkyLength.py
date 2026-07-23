# Converted from PinModes/Touch/Touch_Ex03_SlinkyLength/Touch_Ex03_SlinkyLength.ino
import SerialWombat
from ArduinoFunctions import delay, delayMicroseconds, millis

import SerialWombat_interface
# >>> IMPORTANT: Set this to the configured I2C address of your Serial Wombat chip.
SERIAL_WOMBAT_ADDRESS = 0x6B
sw = SerialWombat_interface.SerialWombatChipInstance(SERIAL_WOMBAT_ADDRESS)


# Interface independent code starts here:
import SerialWombat18CapTouch
import SerialWombatAbstractProcessedInput

# ===== Arduino tab: Touch_Ex03_SlinkyLength.ino =====
#
# This example shows how to measure the change in a length of a Slinky by measuring the change in its
# capacitance as it stretches.  The "Magic Values" in the countsToMoney function
# were determined experimentally as shown in the example video.
# SerialWombat18CapTouch class documentation can be found here:
# https://broadwellconsultinginc.github.io/SerialWombatArdLib/class_serial_wombat18_cap_touch.html#details
#
# A demonstration video of this example can be found here:
# https://youtu.be/wHsDJsw18b4
#
#
SLINKY_PIN = 0  # Must be an Analog capable pin:  0,1,2,3,4,16,17,18,19
# sw is provided by the selected Python interface block above
slinky = SerialWombat18CapTouch.SerialWombat18CapTouch(sw)
money = 0
# Place to keep track of total money count
def setup():
  global money
  # put your setup code here, to run once:
  # Wire.begin() is handled by the selected Python interface block
  # Initialize the I2C Bus on default pins
  # Serial.begin() is not used in this Python example
  delay(3000)
  print("High Speed Clock Example")
  sw.begin()  # Python interface was configured above
  # Scan the bus for Serial Wombat chips, and initialize the first one found
  # Optional Error handling code begin:
  if not sw.isSW18():
    print("This Example is not supported on the Serial Wombat 4B or 8B chip. An 18AB chip is required.")
    while 1:
      delay(100)
  if not sw.isLatestFirmware():
    print("Firmware version mismatch. Download latest Serial Wombat Arduino Library and update Serial Wombat Firmware to latest version")
  # sw.registerErrorHandler(...) is Arduino-specific; Python errors are returned by library calls
  # Register an error handler that will print communication errors to Serial
  # Optional Error handling code end
  slinky.begin(SLINKY_PIN,5000,10)
  slinky.writeAveragingNumberOfSamples(500)
  # put this line in setup.  This should be the last of Processed Input Commands for this pin
  slinky.configureOutputValue(SerialWombatAbstractProcessedInput.SerialWombatAbstractProcessedInput.OutputValue.AVERAGE)
  slinky.writeProcessedInputEnable(True)
  delay(500)
  money = countsToMoney(slinky.readPublicData())
  print(money)
def countsToMoney(counts):
  if counts > 26788:
    return 0
  if counts > 26637:
    return 25
  if counts > 26450:
    return 50
  if counts > 26280:
    return 75
  return 100
def loop():
  global money
  newMoney = countsToMoney(slinky.readPublicData())
  if newMoney != money:
    money = newMoney
    print(money)

setup()
while True:
  loop()
