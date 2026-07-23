# Converted from PinModes/ScaledOutput/SO_Ex02_PinToPinControl/SO_Ex02_PinToPinControl.ino
import SerialWombat
from ArduinoFunctions import delay, delayMicroseconds, millis

import SerialWombat_interface
# >>> IMPORTANT: Set this to the configured I2C address of your Serial Wombat chip.
SERIAL_WOMBAT_ADDRESS = 0x60
sw = SerialWombat_interface.SerialWombatChipInstance(SERIAL_WOMBAT_ADDRESS)


# Interface independent code starts here:
import SerialWombatAnalogInput
import SerialWombatPWM

# ===== Arduino tab: SO_Ex02_PinToPinControl.ino =====
#
#   This example shows how to use the Scaled Output function to make the output
#   of one pin (in this case a PWM pin) derive from the public value of another
#   pin (in this case an analog input) on the Serial Wombat 18AB chip.
#
#   In this example a PWM output on pin 19 will vary duty cycle based on the
#   value measured by an Analog Input on pin 0.  As the voltage on that pin
#   approaches the Serial Wombat 18AB chip's source voltage the public data will
#   approach 65535.   This value will be read every mS by the PWM output pin's
#   scaled output module and the PWM will be updated leading to an output that will
#   effectively (when filtered) make the output value match the input value.
#
#
#   A video demonstrating the use of the Scaled Output is available at:
#   TODO
#
#   Documentation for the SerialWombatAbstractScaledOutput class is available at:
#   https://broadwellconsultinginc.github.io/SerialWombatArdLib/class_serial_wombat_abstract_scaled_output.html
# sw is provided by the selected Python interface block above
sw18ABAnalog = SerialWombatAnalogInput.SerialWombatAnalogInput_18AB(sw)
sw18ABPWM = SerialWombatPWM.SerialWombatPWM_18AB(sw)
PWM_PIN = 1
ANALOG_INPUT_PIN = 0
def setup():
  # put your setup code here, to run once:
  # Wire.begin() is handled by the selected Python interface block
  # Initialize the I2C Bus on default pins
  # Serial.begin() is not used in this Python example
  delay(3000)
  print("Output scaling pin to pin example")
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
  sw18ABAnalog.begin(ANALOG_INPUT_PIN)
  sw18ABPWM.begin(PWM_PIN)
  sw18ABPWM.writeScalingEnabled(True, ANALOG_INPUT_PIN)
# Loop code is empty.  All processing is begin done on the Serial Wombat 18AB chip
def loop():
  pass

setup()
while True:
  loop()
