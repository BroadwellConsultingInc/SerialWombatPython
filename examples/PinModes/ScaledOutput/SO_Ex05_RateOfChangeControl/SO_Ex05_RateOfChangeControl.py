# Converted from PinModes/ScaledOutput/SO_Ex05_RateOfChangeControl/SO_Ex05_RateOfChangeControl.ino
import SerialWombat
from ArduinoFunctions import delay, delayMicroseconds, millis

import SerialWombat_interface
# >>> IMPORTANT: Set this to the configured I2C address of your Serial Wombat chip.
SERIAL_WOMBAT_ADDRESS = 0x60
sw = SerialWombat_interface.SerialWombatChipInstance(SERIAL_WOMBAT_ADDRESS)


# Interface independent code starts here:
import SerialWombatAbstractScaledOutput
import SerialWombatPWM

# ===== Arduino tab: SO_Ex05_RateOfChangeControl.ino =====
#
# This example shows how to use the Scaled Output function to smooth the output of a Scaled Output pin.
#
# In this case the host will make occasional relatively large updates to the duty cycle of a PWM output.
#
# The Serial Wombat 18AB Chip's Scaled Output unit will limit how many counts the output can change within a given period
# (in this case 33 in 1ms, effectivly allowing a full scale transition of 0-65535 in two seconds).
#
# This functionality is useful to limit how fast an output can change.  This could poentially be used to limit the speed of a servo, smooth out
# jerky motor power transitions, automatically dim LEDs, etc.
#
# In this example the host will alternate between full off and full on every 5 seconds, but the Serial Wombat chip will smooth that output over 2 seconds.
#
# Note that the actual output may have a different update rate (50 Hz for servos, a PWM frequency, etc) than the period selected, and this will also affect how
# the output physically behaves.
#
# A video demonstrating the use of the Scaled Output is available at:
# TODO
#
# https://broadwellconsultinginc.github.io/SerialWombatArdLib/class_serial_wombat_abstract_scaled_output.html
# sw is provided by the selected Python interface block above
sw18ABPWM = SerialWombatPWM.SerialWombatPWM_18AB(sw)
PWM_PIN = 1
def setup():
  # put your setup code here, to run once:
  # Wire.begin() is handled by the selected Python interface block
  # Initialize the I2C Bus on default pins
  # Serial.begin() is not used in this Python example
  delay(3000)
  print("Output scaling rate of change control example")
  sw.begin()  # Python interface was configured above
  # Scan the bus for Serial Wombat chips, and initialize the first one found
  # Optional Error handling code begin:
  if sw.isSW04():
    print("This Example is not supported on the Serial Wombat 4B chip. An 8B or 18AB chip is required.")
    while 1:
      delay(100)
  if not sw.isLatestFirmware():
    print("Firmware version mismatch. Download latest Serial Wombat Arduino Library and update Serial Wombat Firmware to latest version")
  if sw.isSW08() and not (sw.isPinModeSupported(SerialWombat.SerialWombatPinMode_t.PIN_MODE_PWM) and sw.isPinModeSupported(SerialWombat.SerialWombatPinMode_t.PIN_MODE_ANALOGINPUT)):
    print("The required pin mode does not appear to be supported in this firmware build. Do you need to download a different firmware?")
    while 1:
      delay(100)
  # sw.registerErrorHandler(...) is Arduino-specific; Python errors are returned by library calls
  # Register an error handler that will print communication errors to Serial
  # Optional Error handling code end
  sw18ABPWM.begin(PWM_PIN)
  sw18ABPWM.writeScalingEnabled(True,PWM_PIN)
  sw18ABPWM.writeTimeout(SerialWombatAbstractScaledOutput.SerialWombatAbstractScaledOutput.Period.PERIOD_1mS, 33)
  # Allow 33 counts of change per ms.
def loop():
  sw18ABPWM.writePublicData(0)
  delay(5000)
  sw18ABPWM.writePublicData(65535)
  delay(5000)

setup()
while True:
  loop()
