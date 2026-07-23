# Converted from PinModes/RandomBlink/RandomBlink_ex02_variableOnDimOff/RandomBlink_ex02_variableOnDimOff.ino
import SerialWombat
from ArduinoFunctions import delay, delayMicroseconds, millis

import SerialWombat_interface
# >>> IMPORTANT: Set this to the configured I2C address of your Serial Wombat chip.
SERIAL_WOMBAT_ADDRESS = 0x60
sw = SerialWombat_interface.SerialWombatChipInstance(SERIAL_WOMBAT_ADDRESS)


# Interface independent code starts here:
import SerialWombatRandomBlink

# ===== Arduino tab: RandomBlink_ex02_variableOnDimOff.ino =====
#   This example shows how to use the Serial Wombat Random Blink pin mode.
#  In this example the LED changes brightness instead of just turning on and
#  off.  Separate random brightness ranges are provided for "on" and "off"
#  with the off state being a constant value instead of a range, and the on
#  state varying in brightness on each blink.
#
#   This example is compatible with the Serial Wombat 18AB and 8B chips,
#   when the RandomBlink pin mode is present in the firmware build.
#
#   In this example pin 1 is configured as a Random Blink output.  The pin
#   randomly alternates between on and off.  Each on time and off time is
#   randomly selected between 0 and 2000 ms.
#
#   This example assumes an LED and current limiting resistor with anode connected
#   to Pin 1, and cathode attached to ground (high side drive)
#
#   The on PWM value is randomly selected between 0x0400 and 0x2000.  The off
#   PWM value is fixed at 0x0100, very dim.
#
#   SerialWombatRandomBlink pin mode documentation:
#
#   TODO coming soon
#   SerialWombatRandomBlink tutorial video:
#
#   TODO coming soon
#
# sw is provided by the selected Python interface block above
randomBlink = SerialWombatRandomBlink.SerialWombatRandomBlink(sw)
RANDOM_BLINK_PIN = 1
def setup():
  # put your setup code here, to run once:
  # Wire.begin() is handled by the selected Python interface block
  # Initialize the I2C Bus on default pins
  # Serial.begin() is not used in this Python example
  delay(3000)
  print("Random Blink Example 2")
  sw.begin()  # Python interface was configured above
  # Scan the bus for Serial Wombat chips, and initialize the first one found
  # Optional Error handling code begin:
  if sw.isSW04():
    print("This Example is not supported on the Serial Wombat 4B chip. An 8B or 18AB chip is required.")
    while 1:
      delay(100)
  if not sw.isLatestFirmware():
    print("Firmware version mismatch. Download latest Serial Wombat Arduino Library and update Serial Wombat Firmware to latest version")
  if sw.isSW08() and not (sw.isPinModeSupported(SerialWombat.SerialWombatPinMode_t.PIN_MODE_RANDOMBLINK) ):
    print("The required pin mode does not appear to be supported in this firmware build. Do you need to download a different firmware?")
    while 1:
      delay(100)
  # sw.registerErrorHandler(...) is Arduino-specific; Python errors are returned by library calls
  # Register an error handler that will print communication errors to Serial
  # Optional Error handling code end
  randomBlink.begin(RANDOM_BLINK_PIN, 2000, 2000, 0, 0, 0x1000, 0x4000, 0x0400, 0x0400)
  # Pin 1, on/off time up to 2 seconds, dim off, random on brightness
  print("Pin 1 is now blinking randomly with on and off times each up to 2 seconds.")
  print("Off PWM is fixed at 0x0010. On PWM varies randomly between 0x0200 and 0xFFFF.")
def loop():
  pass
  # The Serial Wombat chip controls the random blinking without any additional host activity.

setup()
while True:
  loop()
