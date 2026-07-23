# Converted from PinModes/ScaledOutput/SO_Ex01_OutputScaling/SO_Ex01_OutputScaling.ino
import SerialWombat
from ArduinoFunctions import delay, delayMicroseconds, millis

import SerialWombat_interface
# >>> IMPORTANT: Set this to the configured I2C address of your Serial Wombat chip.
SERIAL_WOMBAT_ADDRESS = 0x60
sw = SerialWombat_interface.SerialWombatChipInstance(SERIAL_WOMBAT_ADDRESS)


# Interface independent code starts here:
import SerialWombatPWM

# ===== Arduino tab: SO_Ex01_OutputScaling.ino =====
#
# This example shows how to use the Scaled Output function to scale the output of a PWM pin
# so that an input range drives a different output range.  In this example an input  value of 0 to 65535
# will cause a duty cycle output of  0 to 27306 (0 to 41 percent).  This would be useful if a 5V motor was
# being driven from 12V through a FET.  In this case 0 to 65535 input would still represent "full scale"
# but full scale would now be an output between 0 and 5V.
#
# This sketch is applicable to the SW8B and SW18AB chips (even though the class is called SerialWombatPWM_18AB).
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
  print("Output scaling output range example")
  sw.begin()  # Python interface was configured above
  # Scan the bus for Serial Wombat chips, and initialize the first one found
  # Optional Error handling code begin:
  if sw.isSW04():
    print("This Example is not supported on the Serial Wombat 4B chip. An 8B or 18AB chip is required.")
    while 1:
      delay(100)
  if not sw.isLatestFirmware():
    print("Firmware version mismatch. Download latest Serial Wombat Arduino Library and update Serial Wombat Firmware to latest version")
  if sw.isSW08() and not sw.isPinModeSupported(SerialWombat.SerialWombatPinMode_t.PIN_MODE_PWM):
    print("The required pin mode does not appear to be supported in this firmware build. Do you need to download a different firmware?")
    while 1:
      delay(100)
  # sw.registerErrorHandler(...) is Arduino-specific; Python errors are returned by library calls
  # Register an error handler that will print communication errors to Serial
  # Optional Error handling code end
  sw18ABPWM.begin(PWM_PIN)
  sw18ABPWM.writeScalingEnabled(True,PWM_PIN)
  # Minimum output
  sw18ABPWM.writeOutputScaling(0, 27306)
  # Maximum output 27306 = 65535 * 12 / 5
# This loop will cause a 3 second ramp of the PWM from 0 to 5V equivalent
nextPWMOutput = 0
def loop():
  global nextPWMOutput
  nextPWMOutput += 1000
  # Will roll over after 65535, leading to ramping output
  sw18ABPWM.writePublicData(nextPWMOutput)
  delay(50)
  # 20 updates per second, leading to about a 3 second ramp.

setup()
while True:
  loop()
