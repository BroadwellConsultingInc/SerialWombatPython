# Converted from PinModes/WS2812/WS2812_Ex01_FirstTest/WS2812_Ex01_FirstTest.ino
import SerialWombat
from ArduinoFunctions import delay, delayMicroseconds, millis

import SerialWombat_interface
# >>> IMPORTANT: Set this to the configured I2C address of your Serial Wombat chip.
SERIAL_WOMBAT_ADDRESS = 0x60
sw = SerialWombat_interface.SerialWombatChipInstance(SERIAL_WOMBAT_ADDRESS)


# Interface independent code starts here:
import SerialWombatWS2812

# ===== Arduino tab: WS2812_Ex01_FirstTest.ino =====
#
# This example shows how to initialize and test a strip/board of WS2812b or equivalent LEDs.  This sketch uses
# the SerialWombat18AB's SerialWombatWS2812 class to configure a pin to drive the LEDs.  The
# selected pin must be an enhanced performance pin.
#
# When executed this sketch will configure the Serial Wombat chip to cycle through the indicated number of LEDs
# on the strip in order in various colors.
#
# Change the WS2812_PIN and NUMBER_OF_LEDSs below to fit your circuit.
#
# A video demonstrating the use of the WS2812b pin mode on the Serial Wombat 18AB chip is available at:
# https://youtu.be/WoXvLBJFpXk
#
# Documentation for the SerialWombatTM1637 Arduino class is available at:
# https://broadwellconsultinginc.github.io/SerialWombatArdLib/class_serial_wombat_w_s2812.html#details
#
ws2812 = SerialWombatWS2812.SerialWombatWS2812(sw)
WS2812_PIN = 15  # Must be an enhanced performance pin: 0,1,2,3,4,7,9,10-19
NUMBER_OF_LEDS = 16
WS2812_USER_BUFFER_INDEX = 0x0000  # Set this to an index into the on-chip user buffer.  Can't overlap with area used by other pins.
def setup():
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
  ws2812.begin(WS2812_PIN, NUMBER_OF_LEDS, WS2812_USER_BUFFER_INDEX)
  ws2812.writeMode( SerialWombatWS2812.SWWS2812Mode.ws2812ModeChase)
def loop():
  pass
  # No code in here.  The Serial Wombat chip handles generating the LED sequence with no additional
  # help from the Arduino.  In fact, you could unplug the I2C lines and it would continue working until
  # powered down.

setup()
while True:
  loop()
