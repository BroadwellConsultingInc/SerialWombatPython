# Converted from PinModes/Touch/Touch_Ex01_Calibration/Touch_Ex01_Calibration.ino
import SerialWombat
from ArduinoFunctions import delay, delayMicroseconds, millis

import SerialWombat_interface
# >>> IMPORTANT: Set this to the configured I2C address of your Serial Wombat chip.
SERIAL_WOMBAT_ADDRESS = 0x6B
sw = SerialWombat_interface.SerialWombatChipInstance(SERIAL_WOMBAT_ADDRESS)


# Interface independent code starts here:
import SerialWombat18CapTouch

# ===== Arduino tab: Touch_Ex01_Calibration.ino =====
#
# This example shows how to configure a Serial Wombat 18AB pin to Touch input and determine working
# calibration constants for the touch sensor.
#
# SerialWombat18CapTouch class documentation can be found here:
# https://broadwellconsultinginc.github.io/SerialWombatArdLib/class_serial_wombat18_cap_touch.html#details
#
#
# A demonstration video of this class can be found here:
# https://youtu.be/c4B0_DRVHs0
#
TOUCH_PIN = 17  # <<<<<< MODIFY THIS BASED ON WHICH PIN YOUR TOUCH SENSOR IS RUNNING ON
# sw is provided by the selected Python interface block above
capTouch = SerialWombat18CapTouch.SerialWombat18CapTouch(sw)
lastDigitalRead = 0
def setup():
  global lastDigitalRead
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
  # Iterate through increasing amounts of charge until we find a value that 90% saturates the sensor.
  print("Determining charge time. Do not touch the sensor.")
  noTouchReading = 0
  chargeTime = 250
  capTouch.begin(TOUCH_PIN,chargeTime,0)
  delay(500)
  noTouchReading = sw.readPublicData(TOUCH_PIN)
  while noTouchReading < 60000:
    if noTouchReading < 30000:
      chargeTime += 250
    else:
      chargeTime += 250
    capTouch.begin(TOUCH_PIN,chargeTime,20)
    delay(500)
    noTouchReading = sw.readPublicData(TOUCH_PIN)
    print(chargeTime, end="")
    print(": ", end="")
    print(noTouchReading)
  recommendedChargeTime = chargeTime
  print("Recommended charge time: ", end="")
  print(recommendedChargeTime)
  print()
  # Now take a bunch of samples at that charge to see how much varation you get.  Find the
  # smallest returned value over 5 seconds.
  print("Calibrating High Limit...")
  HighLimit = 65535
  start = millis()
  while start + 5000 > millis():
    result = sw.readPublicData(TOUCH_PIN)
    if result < HighLimit:
      HighLimit = result
      print(HighLimit)
    delay(0)
  print("Lightly Hold finger on sensor until told to remove...")
  # Wait for the user to touch the sensor
  while sw.readPublicData(TOUCH_PIN) > HighLimit - 1500:
    delay(250)
    print(".", end="")
  print()
  # Now take 5 seconds worth of samples to determine the maximum value you're likely to see
  # while touched.
  LowLimit = 0
  start = millis()
  while start + 5000 > millis():
    result = sw.readPublicData(TOUCH_PIN)
    if result > LowLimit:
      LowLimit = result
      print(LowLimit)
  print("Remove Finger.")
  print("Recommended charge time: ", end="")
  print(recommendedChargeTime)
  print("Recommended High Limit: ", end="")
  print(LowLimit + (HighLimit - LowLimit)*3 / 4)
  print("Recommended Low Limit: ", end="")
  print(LowLimit + (HighLimit - LowLimit) / 4)
  print("Done.")
  print()
  print("Configuring Touch in digital mode using calibrations. Code is:")
  print()
  print(" capTouch.begin(TOUCH_PIN,", end="")
  print(recommendedChargeTime, end="")
  print(",0);")
  print("capTouch.makeDigital(", end="")
  print(LowLimit, end="")
  print(",", end="")
  print(HighLimit, end="")
  print(",1,0,0,0);")
  print()
  capTouch.makeDigital(LowLimit,HighLimit,1,0,0,0)
  delay(250)
  lastDigitalRead = sw.readPublicData(TOUCH_PIN)
# In the loop look for a change in state on the sensor and print a 0 or 1
def loop():
  global lastDigitalRead
  count = 0
  newValue = sw.readPublicData(TOUCH_PIN)
  if newValue != lastDigitalRead:
    print(newValue, end="")
    print(" ", end="")
    lastDigitalRead = newValue
    count += 1
    if count > 20:
      count = 0
      print()

setup()
while True:
  loop()
