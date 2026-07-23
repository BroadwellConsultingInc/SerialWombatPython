# Converted from PinModes/InputProcessing/Integrator/IntegratorRotaryEncoderServo/IntegratorRotaryEncoderServo.ino
import SerialWombat
from ArduinoFunctions import delay, delayMicroseconds, millis

import SerialWombat_interface
# >>> IMPORTANT: Set this to the configured I2C address of your Serial Wombat chip.
SERIAL_WOMBAT_ADDRESS = 0x60
sw = SerialWombat_interface.SerialWombatChipInstance(SERIAL_WOMBAT_ADDRESS)


# Interface independent code starts here:
import SerialWombatQuadEnc
import SerialWombatServo
import SerialWombatTM1637

# ===== Arduino tab: IntegratorRotaryEncoderServo.ino =====
#
# This example shows how to integrate a rotary encoder to control the position
# of a servo by controlling the servo position based on the net result of the rotary encoder position
# over time, rather than directly correlating the servo's current position to the encoders's current
# position.
#
# The encoder will have 5 positions, fast left, slow left, stop, slow right, and fast right
#
# This integration function can be applied to any class that inherits from the ProcessedInput class.
#
# Servo is on pin 1.
# The rotary encoder is on pins 5 and 6.
#
# This example also outputs the current position on a TM1637 Display attached to pins 16 and 17.
# A video demonstrating the use of input integration function is avaialble at:
# TODO
#
# Documentation for the  class is available at:
# https://broadwellconsultinginc.github.io/SerialWombatArdLib/class_serial_wombat_abstract_processed_input.html
#
# sw is provided by the selected Python interface block above
rotary = SerialWombatQuadEnc.SerialWombatQuadEnc_18AB(sw)
servo = SerialWombatServo.SerialWombatServo_18AB(sw)
display = SerialWombatTM1637.SerialWombatTM1637(sw)
def setup():
  # put your setup code here, to run once:
  # Wire.begin() is handled by the selected Python interface block
  # Initialize the I2C Bus on default pins
  # Serial.begin() is not used in this Python example
  delay(3000)
  print("Integrator Quadrature Encoder Servo Example")
  sw.begin()  # Python interface was configured above
  # Scan the bus for Serial Wombat chips, and initialize the first one found
  # Optional Error handling code begin:
  if sw.isSW04():
    print("This Example is not supported on the Serial Wombat 4B chip. An 8B or 18AB chip is required.")
    while 1:
      delay(100)
  if not sw.isLatestFirmware():
    print("Firmware version mismatch. Download latest Serial Wombat Arduino Library and update Serial Wombat Firmware to latest version")
  if sw.isSW08() and not (sw.isPinModeSupported(SerialWombat.SerialWombatPinMode_t.PIN_MODE_QUADRATUREENCODER) and sw.isPinModeSupported(SerialWombat.SerialWombatPinMode_t.PIN_MODE_SERVO)):
    print("The required pin mode does not appear to be supported in this firmware build. Do you need to download a different firmware?")
    while 1:
      delay(100)
  # sw.registerErrorHandler(...) is Arduino-specific; Python errors are returned by library calls
  # Register an error handler that will print communication errors to Serial
  # Optional Error handling code end
  rotary.begin(5,6)
  rotary.writeMinMaxIncrementTargetPin(0,6)
  # negativeMaxIndex,
  # negativeMidIndex,
  # negativeDeadZone
  # positiveDeadZone
  # positiveMidIndex,
  # positiveMaxIndex,
  # midIncrement 5 counts per ms, 5000 counts per second
  # maxIncrement 20 counts per ms, 20000 counts per second
  # initialValue
  rotary.configureIntegrator (0, 2, 3, 3, 4, 6, 5, 40, 32768 )
  rotary.writeProcessedInputEnable(True)
  servo.attach(1)
  servo.writeScalingEnabled(True,5)
  # Position the servo based on Pin 5's output
  # Clk Pin
  # Data pin
  # 6 digits
  # Decimal 16 mode
  # Get data from pin 5
  display.begin(16, 17, 6, SerialWombatTM1637.SWTM1637Mode.tm1637Decimal16, 5, 4)
  # Brightness 4
  display.writeDigitOrder(2,1,0,5,4,3)
def loop():
  # No action in loop.  Serial Wombat chip is driving the servo internally.  We can monitor the result:
  print(rotary.readPublicData())

setup()
while True:
  loop()
