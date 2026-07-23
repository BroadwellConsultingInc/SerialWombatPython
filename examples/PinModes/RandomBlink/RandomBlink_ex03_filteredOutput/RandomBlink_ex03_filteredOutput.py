# Converted from PinModes/RandomBlink/RandomBlink_ex03_filteredOutput/RandomBlink_ex03_filteredOutput.ino
import SerialWombat
from ArduinoFunctions import delay, delayMicroseconds, millis

import SerialWombat_interface
# >>> IMPORTANT: Set this to the configured I2C address of your Serial Wombat chip.
SERIAL_WOMBAT_ADDRESS = 0x60
sw = SerialWombat_interface.SerialWombatChipInstance(SERIAL_WOMBAT_ADDRESS)


# Interface independent code starts here:
import SerialWombatAbstractScaledOutput
import SerialWombatRandomBlink

# ===== Arduino tab: RandomBlink_ex03_filteredOutput.ino =====
#   This example shows how to use the Serial Wombat Random Blink pin mode.
#
#     This example builds on ex01 to add filtering to the output so that LED
#     turns on and off smoothly instead of blinking from off to on instantly.
#
#
#      This example is compatible with the Serial Wombat 18AB and 8B chips,
#      when the RandomBlink pin mode is present in the firmware build.
#
#      In this example pin 1 is configured as a Random Blink output.  The pin
#      randomly alternates between on and off.  Each on time and off time is
#      randomly selected between 0 and 2000 ms.
#
#      The outputscaling module first order filter is used for smoothing.
#
#      This example assumes an LED and current limiting resistor with anode connected
#      to Pin 1, and cathode attached to ground (high side drive)
#
#      The on PWM value is fixed at 65535, fully on.  The off PWM value is fixed
#      at 0, fully off.
#
#      SerialWombatRandomBlink pin mode documentation:
#
#      TODO coming soon
#
#      SerialWombatRandomBlink tutorial video:
#
#      TODO coming soon
# sw is provided by the selected Python interface block above
randomBlink = SerialWombatRandomBlink.SerialWombatRandomBlink(sw)
RANDOM_BLINK_PIN = 1
def setup():
  # put your setup code here, to run once:
  # Wire.begin() is handled by the selected Python interface block
  # Initialize the I2C Bus on default pins
  # Serial.begin() is not used in this Python example
  delay(3000)
  print("Random Blink Example")
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
  randomBlink.begin(RANDOM_BLINK_PIN, 2000, 2000)
  # Pin 1, on time up to 2 seconds, off time up to 2 seconds
  randomBlink.begin(RANDOM_BLINK_PIN, 2000, 2000)
  # Pin 1, on time up to 2 seconds, off time up to 2 seconds
  # Add first order filtering using the Serial Wombat scaled output capability.
  # The Random Blink pin mode writes a target PWM value.  The scaled output block
  # filters that target before writing it to the physical output.
  # Higher filter constants produce slower transitions.
  randomBlink.write1stOrderFiltering(SerialWombatAbstractScaledOutput.SerialWombatAbstractScaledOutput.PERIOD_16mS, 0xF000)
  # Enable scaled output processing.  Use the same pin as the input source so
  # the Random Blink pin mode's generated target value is filtered.
  randomBlink.writeScalingEnabled(True, RANDOM_BLINK_PIN)
  print("Pin 1 is now blinking randomly with on and off times each up to 2 seconds.")
def loop():
  pass
  # The Serial Wombat chip controls the random blinking without any additional host activity.

setup()
while True:
  loop()
