# Converted from PinModes/TM1637/TM1637_Ex02_PublicData/TM1637_Ex02_PublicData.ino
import SerialWombat
from ArduinoFunctions import delay, delayMicroseconds, millis

import SerialWombat_interface
# >>> IMPORTANT: Set this to the configured I2C address of your Serial Wombat chip.
SERIAL_WOMBAT_ADDRESS = 0x60
sw = SerialWombat_interface.SerialWombatChipInstance(SERIAL_WOMBAT_ADDRESS)


# Interface independent code starts here:
import SerialWombatAnalogInput
import SerialWombatTM1637

# ===== Arduino tab: TM1637_Ex02_PublicData.ino =====
#
# This example shows how to display a number on a TM1637 display based on the public data of a Serial Wombat pin or other
# data source within the Serial Wombat chip.
#
# If you haven't already, run the SW_Ard_TM1637_012345 example to ensure your display displays digits in
# the correct order.  If necessary, correct the call to writeDigitOrder below as described in that example.
# For four digit displays, you'll likely want to use writeDigitOrder(2,3,4,5,0,1) in order to show the least
# significant digits.
#
# This sketch assumes a potentiometer output dividing ground and 3.3v  is connected to pin 0 as an analog input.
#
# This sketch is designed to be experimented with.  Comment in #define's in the  CONFIG sections below to try out different options and how they affect the display
#
# A video demonstrating the use of the TM1637 pin mode on the Serial Wombat 18AB chip is available at:
# https://youtu.be/AwW12n6o_T0
#
# Documentation for the SerialWombatTM1637 Arduino class is available at:
# https://broadwellconsultinginc.github.io/SerialWombatArdLib/class_serial_wombat_t_m1637.html#details
#
# Serial Wombat is a registered trademark in the United States of Broadwell Consulting Inc.
#
myDisplay = SerialWombatTM1637.SerialWombatTM1637(sw)
DISPLAY_CLK_PIN = 19  # <<<<<<<<<   Set this to the Serial Wombat pin connected to your Display Clock Pin
DISPLAY_DIN_PIN = 18  # <<<<<<<<<   Set this to the Serial Wombat pin connected to your Display Data Pin
potentiometer = SerialWombatAnalogInput.SerialWombatAnalogInput(sw)
# CONFIG:  Which mode... Hex or decimal?  Comment in one...
TM1637_MODE = SerialWombatTM1637.SWTM1637Mode.tm1637Decimal16
# #define TM1637_MODE tm1637Hex16
# Config:  What data source?  Comment in one
# #define DATA_SOURCE SW_DATA_SOURCE_PIN_0
DATA_SOURCE = SerialWombat.SerialWombatDataSource.SW_DATA_SOURCE_INCREMENTING_NUMBER
# #define DATA_SOURCE SW_DATA_SOURCE_TEMPERATURE
# Config:  blank leading zeros?   Make True or false
SURPRESS_LEADING_ZEROS = True
def setup():
  # put your setup code here, to run once:
  # Wire.begin() is handled by the selected Python interface block
  # Initialize the I2C Bus on default pins
  # Serial.begin() is not used in this Python example
  delay(3000)
  print("TM1637 Public Data Display Example")
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
  myDisplay.begin(19, 18, 6, TM1637_MODE, DATA_SOURCE, 4)
  # Brightness
  myDisplay.writeDigitOrder(0,1,2,3,4,5)
  myDisplay.suppressLeadingZeros(SURPRESS_LEADING_ZEROS)
  potentiometer.begin(0,64,0)
def loop():
  pass

setup()
while True:
  loop()
