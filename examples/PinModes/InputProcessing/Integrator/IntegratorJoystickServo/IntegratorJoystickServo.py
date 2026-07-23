# Converted from PinModes/InputProcessing/Integrator/IntegratorJoystickServo/IntegratorJoystickServo.ino
import SerialWombat
from ArduinoFunctions import delay, delayMicroseconds, millis

import SerialWombat_interface
# >>> IMPORTANT: Set this to the configured I2C address of your Serial Wombat chip.
SERIAL_WOMBAT_ADDRESS = 0x60
sw = SerialWombat_interface.SerialWombatChipInstance(SERIAL_WOMBAT_ADDRESS)


# Interface independent code starts here:
import SerialWombatAnalogInput
import SerialWombatServo
import SerialWombatTM1637

# ===== Arduino tab: IntegratorJoystickServo.ino =====
#
#   This example shows how to integrate a joystick or other analog input to control the position
#   of a servo by controlling the servo position based on the net result of the joystick position
#   over time, rather than directly correlating the servo's current position to the joystick's current
#   position.
#
#   This integration function can be applied to any class that inherits from the ProcessedInput class.
#
#   Servo is on pin 7.
#   Joystick / analog is on pin 1.
#
#   This example also outputs the current position on a TM1637 Display attached to pins 5 and 6.
#   A video demonstrating the use of input integration function is avaialble at:
#   TODO
#
#   Documentation for the  class is available at:
#   https://broadwellconsultinginc.github.io/SerialWombatArdLib/class_serial_wombat_abstract_processed_input.html
#
# sw is provided by the selected Python interface block above
joystick = SerialWombatAnalogInput.SerialWombatAnalogInput_18AB(sw)
servo = SerialWombatServo.SerialWombatServo_18AB(sw)
display = SerialWombatTM1637.SerialWombatTM1637(sw)
def setup():
  # put your setup code here, to run once:
  # Wire.begin() is handled by the selected Python interface block
  # Initialize the I2C Bus on default pins
  # Serial.begin() is not used in this Python example
  delay(3000)
  print("Integrator Joystick Servo Example")
  sw.begin()  # Python interface was configured above
  # Scan the bus for Serial Wombat chips, and initialize the first one found
  # Optional Error handling code begin:
  if sw.isSW04():
    print("This Example is not supported on the Serial Wombat 4B chip. An 8B or 18AB chip is required.")
    while 1:
      delay(100)
  if not sw.isLatestFirmware():
    print("Firmware version mismatch. Download latest Serial Wombat Arduino Library and update Serial Wombat Firmware to latest version")
  if sw.isSW08() and not (sw.isPinModeSupported(SerialWombat.SerialWombatPinMode_t.PIN_MODE_ANALOGINPUT) and sw.isPinModeSupported(SerialWombat.SerialWombatPinMode_t.PIN_MODE_SERVO)):
    print("The required pin mode does not appear to be supported in this firmware build. Do you need to download a different firmware?")
    while 1:
      delay(100)
  # sw.registerErrorHandler(...) is Arduino-specific; Python errors are returned by library calls
  # Register an error handler that will print communication errors to Serial
  # Optional Error handling code end
  joystick.begin(1)
  # negativeMaxIndex,
  # negativeMidIndex,
  # negativeDeadZone
  # positiveDeadZone
  # positiveMidIndex,
  # positiveMaxIndex,
  # midIncrement
  # maxIncrement
  # initialValue
  joystick.configureIntegrator (500, 0x4000, 0x7000, 0x9000, 0xC000, 65035, 5, 20, 32768 )
  joystick.writeProcessedInputEnable(True)
  servo.attach(7)
  servo.writeScalingEnabled(True, 1)
  # Position the servo based on Pin 19's output
  # Clk Pin
  # Data pin
  # 6 digits
  # Decimal 16 mode
  # Get data from pin 19
  display.begin(5, 6, 6, SerialWombatTM1637.SWTM1637Mode.tm1637Decimal16, 19, 4)
  # Brightness 4
  display.writeDigitOrder(2, 1, 0, 5, 4, 3)
def loop():
  # No action in loop.  Serial Wombat chip is driving the servo internally.  We can monitor the result:
  print(joystick.readPublicData())

setup()
while True:
  loop()
