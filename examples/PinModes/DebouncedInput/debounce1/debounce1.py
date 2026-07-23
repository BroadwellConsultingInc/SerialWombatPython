# Converted from PinModes/DebouncedInput/debounce1/debounce1.ino
import SerialWombat
from ArduinoFunctions import delay, delayMicroseconds, millis

import SerialWombat_interface
# >>> IMPORTANT: Set this to the configured I2C address of your Serial Wombat chip.
SERIAL_WOMBAT_ADDRESS = 0x60
sw = SerialWombat_interface.SerialWombatChipInstance(SERIAL_WOMBAT_ADDRESS)


# Interface independent code starts here:
import SerialWombatDebouncedInput

# ===== Arduino tab: debounce1.ino =====
# sw is provided by the selected Python interface block above
# Declare a Serial Wombat
redButton = SerialWombatDebouncedInput.SerialWombatDebouncedInput(sw)
greenButton = SerialWombatDebouncedInput.SerialWombatDebouncedInput(sw)
RED_BUTTON_PIN = 0
GREEN_BUTTON_PIN = 1
# This example is explained in a video tutorial at: https://youtu.be/R1KM0J2Ug-M
def setup():
  # put your setup code here, to run once:
  # Wire.begin() is handled by the selected Python interface block
  # Initialize the I2C Bus on default pins
  # Serial.begin() is not used in this Python example
  delay(3000)
  print("Two Button Debounce Example")
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
  # initialize with default settings, including internal pull up
  greenButton.begin(GREEN_BUTTON_PIN)
def clearTerminal():
  print(chr(27), end="")
  # ESC command
  print("[2J", end="")
  # clear screen command
  print(chr(27), end="")
  print("[H", end="")
  # cursor to home command
greenTransitions = 0
redTransitions = 0
def loop():
  global greenTransitions, redTransitions
  clearTerminal()
  redButton.readTransitionsState()
  redTransitions += redButton.transitions
  greenButton.readTransitionsState()
  greenTransitions += greenButton.transitions
  print(greenTransitions, end="")
  print(" ", end="")
  print(greenButton.readDurationInTrueState_mS())
  print(redTransitions, end="")
  print(" ", end="")
  print(redButton.readDurationInTrueState_mS())
  delay(50)

setup()
while True:
  loop()
