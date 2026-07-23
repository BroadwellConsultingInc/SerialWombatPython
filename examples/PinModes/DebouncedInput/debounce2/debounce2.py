# Converted from PinModes/DebouncedInput/debounce2/debounce2.ino
import SerialWombat
from ArduinoFunctions import delay, delayMicroseconds, millis

import SerialWombat_interface
# >>> IMPORTANT: Set this to the configured I2C address of your Serial Wombat chip.
SERIAL_WOMBAT_ADDRESS = 0x6B
sw = SerialWombat_interface.SerialWombatChipInstance(SERIAL_WOMBAT_ADDRESS)


# Interface independent code starts here:
import SerialWombatDebouncedInput
import SerialWombatServo

# ===== Arduino tab: debounce2.ino =====
# sw is provided by the selected Python interface block above
# Declare a Serial Wombat
blueButton = SerialWombatDebouncedInput.SerialWombatDebouncedInput(sw)
redButton = SerialWombatDebouncedInput.SerialWombatDebouncedInput(sw)
redCounter = SerialWombatDebouncedInput.SerialWombatButtonCounter(redButton)
greenButton = SerialWombatDebouncedInput.SerialWombatDebouncedInput(sw)
greenCounter = SerialWombatDebouncedInput.SerialWombatButtonCounter(greenButton)
servo = SerialWombatServo.SerialWombatServo(sw)
SERVO_PIN = 2
RED_BUTTON_PIN = 0
GREEN_BUTTON_PIN = 1
BLUE_BUTTON_PIN = 3  # Set this to some other value on SW18AB, as 3 is an I2C pin
# This example is explained in a video tutorial at: https://youtu.be/R1KM0J2Ug-M
servoPosition = 90
def setup():
  # put your setup code here, to run once:
  # Wire.begin() is handled by the selected Python interface block
  # Initialize the I2C Bus on default pins
  # Serial.begin() is not used in this Python example
  delay(3000)
  print("Three Button Debounced Counter Example")
  sw.begin()  # Python interface was configured above
  # Scan the bus for Serial Wombat chips, and initialize the first one found
  # Optional Error handling code begin:
  if not sw.isLatestFirmware():
    print("Firmware version mismatch. Download latest Serial Wombat Arduino Library and update Serial Wombat Firmware to latest version")
  if sw.isSW08() and not sw.isPinModeSupported(SerialWombat.SerialWombatPinMode_t.PIN_MODE_DEBOUNCE):
    print("The required pin mode does not appear to be supported in this firmware build. Do you need to download a different firmware?")
    while 1:
      delay(100)
  # sw.registerErrorHandler(...) is Arduino-specific; Python errors are returned by library calls
  # Register an error handler that will print communication errors to Serial
  # Optional Error handling code end
  redButton.begin(RED_BUTTON_PIN)
  greenButton.begin(GREEN_BUTTON_PIN)
  blueButton.begin(BLUE_BUTTON_PIN)
  redCounter.begin(1, 500, 2000, 5, 250, 5000, 10, 100)
  redCounter.lowLimit = 0
  redCounter.highLimit = 180
  greenCounter.begin(-1, 500, 2000, -5, 250, 5000, -10, 100)
  greenCounter.lowLimit = 0
  greenCounter.highLimit = 180
  servo.attach(SERVO_PIN,True)
  # Servo on serial wombat pin 2, reverse direction
def loop():
  global servoPosition
  _, servoPosition = redCounter.update(servoPosition)
  _, servoPosition = greenCounter.update(servoPosition)
  if blueButton.digitalRead():
    servoPosition = 90
  servo.write(servoPosition)
  print(servoPosition)
  delay(50)

setup()
while True:
  loop()
