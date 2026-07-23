# Converted from PinModes/RandomBlink/RandomBlink_ex06_inversePwmOnPin2/RandomBlink_ex06_inversePwmOnPin2.ino
import SerialWombat
from ArduinoFunctions import delay, delayMicroseconds, millis

import SerialWombat_interface
# >>> IMPORTANT: Set this to the configured I2C address of your Serial Wombat chip.
SERIAL_WOMBAT_ADDRESS = 0x60
sw = SerialWombat_interface.SerialWombatChipInstance(SERIAL_WOMBAT_ADDRESS)


# Interface independent code starts here:
import SerialWombatPWM
import SerialWombatRandomBlink

# ===== Arduino tab: RandomBlink_ex06_inversePwmOnPin2.ino =====
#   This example shows how to use the Serial Wombat Random Blink pin mode
#   together with a PWM output whose duty cycle is the inverse of the Random
#   Blink output.
#
#   This example is compatible with the Serial Wombat 18AB and 8B chips,
#   when the RandomBlink and PWM pin modes are present in the firmware build.
#
#   In this example pin 1 is configured as a Random Blink output.  The pin
#   randomly alternates between on and off.  Each on time and off time is
#   randomly selected between 0 and 2000 ms.
#
#   Pin 2 is configured as a PWM output.  The scaled output block on pin 2
#   uses pin 1 as its input source and inverts it.  As a result, pin 2 is
#   bright when pin 1 is off, and pin 2 is off when pin 1 is bright.
#
#   SerialWombatRandomBlink pin mode documentation:
#
#   TODO coming soon
#
# sw is provided by the selected Python interface block above
randomBlink = SerialWombatRandomBlink.SerialWombatRandomBlink(sw)
inversePWM = SerialWombatPWM.SerialWombatPWM_18AB(sw)
RANDOM_BLINK_PIN = 1
INVERSE_PWM_PIN = 2
def setup():
  # put your setup code here, to run once:
  # Wire.begin() is handled by the selected Python interface block
  # Initialize the I2C Bus on default pins
  # Serial.begin() is not used in this Python example
  delay(3000)
  print("Random Blink Inverse PWM Example")
  sw.begin()  # Python interface was configured above
  # Scan the bus for Serial Wombat chips, and initialize the first one found
  # Optional Error handling code begin:
  if sw.isSW04():
    print("This Example is not supported on the Serial Wombat 4B chip. An 8B or 18AB chip is required.")
    while 1:
      delay(100)
  if not sw.isLatestFirmware():
    print("Firmware version mismatch. Download latest Serial Wombat Arduino Library and update Serial Wombat Firmware to latest version")
  if sw.isSW08() and (not (sw.isPinModeSupported(SerialWombat.SerialWombatPinMode_t.PIN_MODE_RANDOMBLINK)) or not (sw.isPinModeSupported(SerialWombat.SerialWombatPinMode_t.PIN_MODE_PWM))):
    print("The required pin modes do not appear to be supported in this firmware build. Do you need to download a different firmware?")
    while 1:
      delay(100)
  # sw.registerErrorHandler(...) is Arduino-specific; Python errors are returned by library calls
  # Register an error handler that will print communication errors to Serial
  # Optional Error handling code end
  randomBlink.begin(RANDOM_BLINK_PIN, 2000, 2000)
  # Pin 1, on time up to 2 seconds, off time up to 2 seconds
  inversePWM.begin(INVERSE_PWM_PIN, 0)
  # Pin 2 starts as PWM with 0 duty cycle
  # Configure the scaled output block on pin 2 to use pin 1 as its source,
  # and invert the source value before writing it to the PWM output.
  inversePWM.writeScalingInvertedInput(True)
  inversePWM.writeScalingEnabled(True, RANDOM_BLINK_PIN)
  print("Pin 1 is blinking randomly. Pin 2 is a PWM output that is the inverse of pin 1.")
def loop():
  pass
  # The Serial Wombat chip controls the random blinking and inverse PWM output
  # without any additional host activity.

setup()
while True:
  loop()
