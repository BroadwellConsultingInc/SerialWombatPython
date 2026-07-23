# Converted from PinModes/TM1637/TM1637_Ex03_Decimals/TM1637_Ex03_Decimals.ino
import SerialWombat
from ArduinoFunctions import delay, delayMicroseconds, millis

import SerialWombat_interface
# >>> IMPORTANT: Set this to the configured I2C address of your Serial Wombat chip.
SERIAL_WOMBAT_ADDRESS = 0x60
sw = SerialWombat_interface.SerialWombatChipInstance(SERIAL_WOMBAT_ADDRESS)


# Interface independent code starts here:
import SerialWombatTM1637

# ===== Arduino tab: TM1637_Ex03_Decimals.ino =====
#
# This example shows how to use the writeDecimalBitmap command to write decimal points on a TM1637 display.
# When properly configured with a properly wired display it will light up the decimal points in a binary-counting
# fashion, with the left-most digit changing state most frequenly.
#
# If you haven't already, run the SW_Ard_TM1637_012345 example to ensure your display displays digits in
# the correct order.  If necessary, correct the call to writeDigitOrder below as described in that example.
#
# There is a good chance that this example will not work as expected.  The manufacturers of hobbiest TM1637
# displays often do not connect the decimal point line as expected.  In some cases it may be connected to
# one or both of the dots in a colon ':' for time display.  In other conditions it may be connected incorrectly
# or not at all.
#
# This sketch and the writeDecimalBitmap has been verified to work properly on  properly wired TM1637 6-digit and
# 4-digit display.  If it behaves oddly on your display, it's probably your display.  The most popular 4 digit TM1637
# display on Amazon from diymore as of October 2021 connects a colon rather than decimals.  The most popular 6 digit display from
# diymore has a couple of decimal points connected and the remainder cause the display to malfunction when set.
#
# A video demonstrating the use of the TM1637 pin mode on the Serial Wombat 18AB chip is available at:
# https://youtu.be/AwW12n6o_T0
#
# Documentation for the SerialWombatTM1637 Arduino class is available at:
# https://broadwellconsultinginc.github.io/SerialWombatArdLib/class_serial_wombat_t_m1637.html#details
#
# Serial Wombat is a registered trademark in the United States of Broadwell Consulting Inc.
# sw is provided by the selected Python interface block above
myDisplay = SerialWombatTM1637.SerialWombatTM1637(sw)
DISPLAY_CLK_PIN = 19  # <<<<<<<<<   Set this to the Serial Wombat pin connected to your Display Clock Pin
DISPLAY_DIN_PIN = 18  # <<<<<<<<<   Set this to the Serial Wombat pin connected to your Display Data Pin
def setup():
  # put your setup code here, to run once:
  # Wire.begin() is handled by the selected Python interface block
  # Initialize the I2C Bus on default pins
  # Serial.begin() is not used in this Python example
  delay(3000)
  print("TM1637 Decimal Point Example")
  sw.begin()  # Python interface was configured above
  # Scan the bus for Serial Wombat chips, and initialize the first one found
  # Optional Error handling code begin:
  if sw.isSW04():
    print("This Example is not supported on the Serial Wombat 4B chip. An 8B or 18AB chip is required.")
    while 1:
      delay(100)
  if not sw.isLatestFirmware():
    print("Firmware version mismatch. Download latest Serial Wombat Arduino Library and update Serial Wombat Firmware to latest version")
  if sw.isSW08() and not sw.isPinModeSupported(SerialWombat.SerialWombatPinMode_t.PIN_MODE_TM1637):
    print("The required pin mode does not appear to be supported in this firmware build. Do you need to download a different firmware?")
    while 1:
      delay(100)
  # sw.registerErrorHandler(...) is Arduino-specific; Python errors are returned by library calls
  # Register an error handler that will print communication errors to Serial
  # Optional Error handling code end
  # Clk Pin
  # Data Pin
  # Number of digits
  # Mode enumeration
  # Not used in SerialWombatTM1637.SWTM1637Mode.tm1637CharArray mode
  myDisplay.begin(DISPLAY_CLK_PIN, DISPLAY_DIN_PIN, 6, SerialWombatTM1637.SWTM1637Mode.tm1637CharArray, 0x55, 4)
  # Brightness
  myDisplay.writeDigitOrder(0,1,2,3,4,5)
  test = " "
  myDisplay.writeArray(test)
count = 0
def loop():
  global count
  myDisplay.writeDecimalBitmap(count)
  count += 1
  if count >= 0x40:
    count = 0
  delay(250)

setup()
while True:
  loop()
