# Converted from PinModes/WS2812/WS2812_Ex02_SetColors/WS2812_Ex02_SetColors.ino
import SerialWombat
from ArduinoFunctions import delay, delayMicroseconds, millis

import SerialWombat_interface
# >>> IMPORTANT: Set this to the configured I2C address of your Serial Wombat chip.
SERIAL_WOMBAT_ADDRESS = 0x60
sw = SerialWombat_interface.SerialWombatChipInstance(SERIAL_WOMBAT_ADDRESS)


# Interface independent code starts here:
import SerialWombatWS2812

# ===== Arduino tab: WS2812_Ex02_SetColors.ino =====
#
#   This example shows how to initialize an animation on a strip/board of WS2812b or equivalent LEDs and use the write
#   command to write colors to the LEDs using the SerialWombat18AB's SerialWombatWS2812 class to configure a pin to drive the LEDs.  The
#   selected pin must be an enhanced performance pin.
#
#   When executed this sketch will set 16 LEDs to
#   Red
#   White
#   Green
#   Blue
#   Yellow
#   Off,
#   Purple
#   Blue,
#   Blue,
#   Blue,
#   Red,
#   Green
#   White
#   White
#   Yellow
#   Green
#
#
#   Change the WS2812_PIN below to fit your circuit.
#
#   A video demonstrating the use of the WS2812b pin mode on the Serial Wombat 18AB chip is available at:
# https://youtu.be/WoXvLBJFpXk
#   Documentation for the SerialWombatTM1637 Arduino class is available at:
#   https://broadwellconsultinginc.github.io/SerialWombatArdLib/class_serial_wombat_w_s2812.html#details
#
ws2812 = SerialWombatWS2812.SerialWombatWS2812(sw)
WS2812_PIN = 15  # Must be an enhanced performance pin: 0,1,2,3,4,7,9,10-19
NUMBER_OF_LEDS = 16
WS2812_USER_BUFFER_INDEX = 0x0000  # Set this to an index into the on-chip user buffer.  Can't overlap with area used by other pins.
# Define colors.  prefix them with SW_ so we don't conflict with any other libraries, such as a graphic display library.
SW_RED = 0x000F0000  # Red, changed from 0x00FF0000 to reduce power
SW_GREEN = 0x0000F00
SW_WHITE = 0x000F0F0F
SW_YELLOW = 0x000F0F00
SW_BLUE = 0x0000000F
SW_OFF = 0x00000000
SW_PURPLE = 0x000F000F
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
  # The Pin connected to WS2812 array
  # The number of LEDs being used
  ws2812.begin(WS2812_PIN, NUMBER_OF_LEDS, WS2812_USER_BUFFER_INDEX)
  # A location in the Serial Wombat chip's user RAM area where LED output signals will be buffered
  ws2812.write(0, SW_RED)
  ws2812.write(1, SW_WHITE)
  ws2812.write(2, SW_GREEN)
  ws2812.write(3, SW_BLUE)
  ws2812.write(4, SW_YELLOW)
  ws2812.write(5, SW_OFF)
  ws2812.write(6, SW_PURPLE)
  ws2812.write(7, SW_BLUE)
  ws2812.write(8, SW_BLUE)
  ws2812.write(9, SW_BLUE)
  ws2812.write(10, SW_RED)
  ws2812.write(11, SW_GREEN)
  ws2812.write(12, SW_WHITE)
  ws2812.write(13, SW_WHITE)
  ws2812.write(14, SW_YELLOW)
  ws2812.write(15, SW_GREEN)
def loop():
  pass

setup()
while True:
  loop()
