# Converted from PinModes/Servo/Servo_Ex01/Servo_Ex01.ino
import SerialWombat
from ArduinoFunctions import delay, delayMicroseconds, millis

import SerialWombat_interface
# >>> IMPORTANT: Set this to the configured I2C address of your Serial Wombat chip.
SERIAL_WOMBAT_ADDRESS = 0x6B
sw = SerialWombat_interface.SerialWombatChipInstance(SERIAL_WOMBAT_ADDRESS)


# Interface independent code starts here:
import SerialWombatServo

# ===== Arduino tab: Servo_Ex01.ino =====
# sw is provided by the selected Python interface block above
# Declare a Serial Wombat chip
ContinuousServo = SerialWombatServo.SerialWombatServo(sw)
# Declare a Servo on pin 2 of Serial Wombat sw
StandardServo = SerialWombatServo.SerialWombatServo(sw)
# Declare a Servo on pin 3 of Serial Wombat sw
# A video tutorial is available which explains this example in detail at: https://youtu.be/WiciAtS1ng0
def setup():
  # put your setup code here, to run once:
  # Wire.begin() is handled by the selected Python interface block
  # Initialize the I2C Bus on default pins
  # Serial.begin() is not used in this Python example
  delay(3000)
  print("Basic Servo Example")
  sw.begin()  # Python interface was configured above
  # Scan the bus for Serial Wombat chips, and initialize the first one found
  # Optional Error handling code begin:
  if not sw.isLatestFirmware():
    print("Firmware version mismatch. Download latest Serial Wombat Arduino Library and update Serial Wombat Firmware to latest version")
  if sw.isSW08() and not sw.isPinModeSupported(SerialWombat.SerialWombatPinMode_t.PIN_MODE_SERVO):
    print("The required pin mode does not appear to be supported in this firmware build. Do you need to download a different firmware?")
    while 1:
      delay(100)
  # sw.registerErrorHandler(...) is Arduino-specific; Python errors are returned by library calls
  # Register an error handler that will print communication errors to Serial
  # Optional Error handling code end
  ContinuousServo.attach(2, 500, 2500, True)
  # Initialize a servo on pin 2, 500uS minimum pulse, 2500 us Maximum pulse, reversed
  StandardServo.attach(3)
  # Initialize a servo on pin 3 using Arduino equivalent default values.  Use a different pin on SW18AB, since 3 is SDA
def loop():
  # put your main code here, to run repeatedly:
  ContinuousServo.write(30)
  # Takes a number from 0 to 180
  StandardServo.write16bit(5500)
  # Takes a number from 0 to 65535:  Higher resolution
  delay(5000)
  ContinuousServo.write(140)
  StandardServo.write16bit(50000)
  delay(5000)

setup()
while True:
  loop()
