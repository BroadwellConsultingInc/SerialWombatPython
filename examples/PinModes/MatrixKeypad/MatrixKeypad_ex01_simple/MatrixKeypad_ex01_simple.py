# Converted from PinModes/MatrixKeypad/MatrixKeypad_ex01_simple/MatrixKeypad_ex01_simple.ino
import SerialWombat
from ArduinoFunctions import delay, delayMicroseconds, millis

import SerialWombat_interface
# >>> IMPORTANT: Set this to the configured I2C address of your Serial Wombat chip.
SERIAL_WOMBAT_ADDRESS = 0x60
sw = SerialWombat_interface.SerialWombatChipInstance(SERIAL_WOMBAT_ADDRESS)


# Interface independent code starts here:
import SerialWombatMatrixKeypad

# ===== Arduino tab: MatrixKeypad_ex01_simple.ino =====
#
#   This example shows how to initialize a 16 key, 8 pin 4x4 matrix keypad using the
#   Serial Wombat 18AB or SW8B chip'sSerialWombatMatrixKeypad class.
#
#   This example shows how to treat the matrix keypad as a stream input
#   so that it can be treated as if keypresses are Serial Input
#
#   Note that firmware versions prior to 2.0.7 have a bug that may cause slow recognition of
#   button presses.
#
#   This example assumes a 4x4 keypad attached with rows connected to pins 10,11,12,13
#   and columns attached to pins 16,17,18,19 .  This can be changed in the keypad.begin
#   statement to fit your circuit.  This will need to be changed for the SW8B chip.
#   Note that pin 0 on the Serial Wombat 8B chip has a pull down resistor, so it's best to use
#   that pin as a row rather than column if possible
#
#   This example uses default modes for the SerialWombatMatrixKeypad.  The default values
#   send ASCII to the queue assuming a standard
#
#   123A
#   456B
#   789C
#   0#D
#
#   keypad format.   See the pin mode documentation (link below) for more information on the
#   possible buffer and queue modes
#
#
#   A video demonstrating the use of the SerialWombatMatrixKeypad class on the Serial Wombat 18AB chip is available at:
#   https://youtu.be/hxLda6lBWNg
#
#   Documentation for the SerialWombatMatrixKeypad Arduino class is available at:
#
# sw is provided by the selected Python interface block above
keypad = SerialWombatMatrixKeypad.SerialWombatMatrixKeypad(sw)
def setup():
  # put your setup code here, to run once:
  # Wire.begin() is handled by the selected Python interface block
  # Initialize the I2C Bus on default pins
  # Serial.begin() is not used in this Python example
  delay(3000)
  print("Matrix Keypad Simple Example")
  sw.begin()  # Python interface was configured above
  # Scan the bus for Serial Wombat chips, and initialize the first one found
  # Optional Error handling code begin:
  if sw.isSW04():
    print("This Example is not supported on the Serial Wombat 4B chip. An 8B or 18AB chip is required.")
    while 1:
      delay(100)
  if not sw.isLatestFirmware():
    print("Firmware version mismatch. Download latest Serial Wombat Arduino Library and update Serial Wombat Firmware to latest version")
  if sw.isSW08() and not sw.isPinModeSupported(SerialWombat.SerialWombatPinMode_t.PIN_MODE_MATRIX_KEYPAD):
    print("The required pin mode does not appear to be supported in this firmware build. Do you need to download a different firmware?")
    while 1:
      delay(100)
  # sw.registerErrorHandler(...) is Arduino-specific; Python errors are returned by library calls
  # Register an error handler that will print communication errors to Serial
  # Optional Error handling code end
  # Command pin, typically the same as the row0 pin
  # row 0
  # row 1
  # row 2
  # row 3
  # column 0
  # column 1
  # column 2
  keypad.begin(10, 10, 11, 12, 13, 16, 17, 18, 19)
  # column 3
def loop():
  i = keypad.read()
  # returns a byte, or -1 if no value is avaialble
  if i > 0:
    print(chr(i), end="")
    # We got a keypress.  Dump it to the Serial Terminal

setup()
while True:
  loop()
