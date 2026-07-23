# Converted from PinModes/TM1637/TM1637_Ex04_FlashUI/TM1637_Ex04_FlashUI.ino
import SerialWombat
from ArduinoFunctions import delay, delayMicroseconds, millis

import SerialWombat_interface
# >>> IMPORTANT: Set this to the configured I2C address of your Serial Wombat chip.
SERIAL_WOMBAT_ADDRESS = 0x60
sw = SerialWombat_interface.SerialWombatChipInstance(SERIAL_WOMBAT_ADDRESS)


# Interface independent code starts here:
import SerialWombat18CapTouch
import SerialWombatDebouncedInput
import SerialWombatTM1637

# ===== Arduino tab: TM1637_Ex04_FlashUI.ino =====
PENNY_PIN = 16  # Must be an Analog capable pin:  0,1,2,3,4,16,17,18,19
QUARTER_PIN = 17  # Must be an Analog capable pin:  0,1,2,3,4,16,17,18,19
#
#   This example shows how to configure two Serial Wombat 18AB pins to Touch input and use the
#   SerialWombat18CapTouchCounter class to implement a two touch sensor interface to increment
#   a counter at various speeds by two different increments.
#
#   The example was created using a Serial Wombat 18AB chip in I2C mode with a Node MCU clone Arduino
#   and a penny and quarter both covered with electrial tape wired to pins WP16 and WP17.
#
#   When the penny is touched briefly the total will increment by 1 cent.  When the quarter is touched
#   the total will increment by 25 cents.  If a finger is held on them then they will increment slowly, then
#   more quickly, then very quickly.  This type of interface could be easily integrated into a complete solution
#   for user configuration of parameters.
#
# A video demonstrating the use of the TM1637 pin mode on the Serial Wombat 18AB chip is available at:
# https://youtu.be/AwW12n6o_T0
#
# Documentation for the SerialWombatTM1637 Arduino class is available at:
# https://broadwellconsultinginc.github.io/SerialWombatArdLib/class_serial_wombat_t_m1637.html#details
penny = SerialWombat18CapTouch.SerialWombat18CapTouch(sw)
quarter = SerialWombat18CapTouch.SerialWombat18CapTouch(sw)
myDisplay = SerialWombatTM1637.SerialWombatTM1637(sw)
quarterCounter = SerialWombatDebouncedInput.SerialWombatButtonCounter(quarter)
digitChange = 0
displayString = bytearray(b"000000")
currentDigit = 6
# 6 means none, 0-5 are the displayed digits
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
  # Initialize the Penny sensor
  # 9000 based on previous calibration of this penny on this pin with this wire using the Calibration example
  penny.begin(PENNY_PIN, 9000, 0)
  # Initialize the Penny sensor
  # 9250 based on previous calibration of this quarter on this pin with this wire using the Calibration example
  quarter.begin(QUARTER_PIN, 9250, 0)
  delay(500)
  penny.makeDigital(53985, 57620, 1, 0, 0, 0)
  # Low and High limits based on previous calibration of this penny on this pin with this wire
  quarter.makeDigital(54349, 57792, 1, 0, 0, 0)
  # Low and High limits based on previous calibration of this quarter on this pin with this wire
  delay(250)
  # Increment by 1
  # Every 500 ms
  # for 2000ms, then...
  # by 1
  # every 250ms
  # for 5000 ms, then
  # by 1
  quarterCounter.begin(1, 500, 2000, 1, 250, 5000, 1, 100)
  # every 100ms
  # Clk Pin
  # Data Pin
  # Number of digits
  # Mode enumeration
  # Source pin Not used in SerialWombatTM1637.SWTM1637Mode.tm1637CharArray mode
  myDisplay.begin(19, 18, 6, SerialWombatTM1637.SWTM1637Mode.tm1637CharArray, 0x55, 4)
  # Brightness
  myDisplay.writeDigitOrder(2, 1, 0, 5, 4, 3)
  myDisplay.writeArray(displayString)
def loop():
  global digitChange
  if penny.readTransitionsState() and penny.transitions > 0:
    # The penny was touched. Move to the next digit.
    nextDigit()
  _, digitChange = quarterCounter.update(digitChange)
  if currentDigit < 6 and digitChange != 0:
    displayString[currentDigit] += digitChange
    if displayString[currentDigit] > ord('z'):
      displayString[currentDigit] = ord(' ')
    if displayString[currentDigit] < ord(' '):
      displayString[currentDigit] = ord('z')
    digitChange = 0
    myDisplay.writeArray(displayString)

def nextDigit():
  global digitChange, currentDigit
  digitChange = 0
  currentDigit += 1
  if currentDigit > 6:
    currentDigit = 0
  if currentDigit < 6:
    myDisplay.writeBlinkBitmap(0x01 << currentDigit)
  else:
    myDisplay.writeBlinkBitmap(0)
  return 0

setup()
while True:
  loop()
