# Converted from PinModes/ScaledOutput/SO_Ex04_Timeout/SO_Ex04_Timeout.ino
import SerialWombat
from ArduinoFunctions import delay, delayMicroseconds, millis

import SerialWombat_interface
# >>> IMPORTANT: Set this to the configured I2C address of your Serial Wombat chip.
SERIAL_WOMBAT_ADDRESS = 0x60
sw = SerialWombat_interface.SerialWombatChipInstance(SERIAL_WOMBAT_ADDRESS)


# Interface independent code starts here:
import SerialWombatPWM

# ===== Arduino tab: SO_Ex04_Timeout.ino =====
#
# This example shows how to use the Scaled Output function to make an output
# default to a value if the host does not periodically check in either by
# explicitly resetting a timer.
#
# This functionality is useful to set an output to a default value if the host ceases communicating.  This function comes after any feedback control such as PID, so it will override the controller's output
#
# In this example the PWM output will be varied between about 50 percent (32000) and
# nearly 100 percent (64000) by the host.  Then the host will stop communicating, and the Serial Wombat 18AB Scaled output will set the output to a predefined value of 10 percent (6554) about 250 mS after the last timer reset call.
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
  print("Output scaling timeout example")
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
  # timeout if this amount of time elapses without calling this function again
  sw18ABPWM.writeTimeout(250 , 6554)
  # 10 percent duty cycle on timeout
def loop():
  nextPWMOutput = 0
  for nextPWMOutput in range(32768, 64000, 1000):
    sw18ABPWM.writePublicData(nextPWMOutput)
    sw18ABPWM.writeTimeout(250,6554)
    delay(100)
    # 10 updates per second, leading to about a 3 second ramp.
  delay(5000)
  # The scaled output timer will timeout and set the output to 10 percent

setup()
while True:
  loop()
