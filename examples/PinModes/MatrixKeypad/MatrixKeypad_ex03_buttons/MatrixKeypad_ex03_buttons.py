# Converted from PinModes/MatrixKeypad/MatrixKeypad_ex03_buttons/MatrixKeypad_ex03_buttons.ino
import SerialWombat
from ArduinoFunctions import delay, delayMicroseconds, millis

import SerialWombat_interface
# >>> IMPORTANT: Set this to the configured I2C address of your Serial Wombat chip.
SERIAL_WOMBAT_ADDRESS = 0x60
sw = SerialWombat_interface.SerialWombatChipInstance(SERIAL_WOMBAT_ADDRESS)


# Interface independent code starts here:
import SerialWombatMatrixKeypad

# ===== Arduino tab: MatrixKeypad_ex03_buttons.ino =====
#
# This example shows how to initialize a 16 key, 8 pin 4x4 matrix keypad using the
# Serial Wombat 18AB or 8B chip's SerialWombatMatrixKeypad class.
#
# Note that firmware versions prior to 2.0.7 have a bug that may cause slow recognition of
# button presses.
#
# This example shows how to treat the matrix keypad as if it were 16 separate digital
# inputs by creating 16 instances of SerialWombatMatrixButton from a single instance of
# SerialWombatMatrixKeypad.  The SerialWombatMatrixKeypad instance scans the keys and
# the SerialWombatMatrixButton class abstracts each one into a single digital input.
#
# After initialization the SerialWombatMatrixButton class has the same interfaces and
# is conceptually interchangable with instances of SerialWombatDebouncedInput and
# digitally configured SerialWombat18CapTouch instances.
#
# This example assumes a 4x4 keypad attached with rows connected to pins 10,11,12,13
# and columns attached to pins 16,17,18,19 .  This can be changed in the keypad.begin
# statement to fit your circuit.
#
# A video demonstrating the use of the SerialWombatMatrixKeypad class on the Serial Wombat 18AB chip is available at:
# https://youtu.be/hxLda6lBWNg
#
# Documentation for the SerialWombatTM1637 Arduino class is available at:
# https://broadwellconsultinginc.github.io/SerialWombatArdLib/class_serial_wombat_w_s2812.html#details
#
# sw is provided by the selected Python interface block above
keypad = SerialWombatMatrixKeypad.SerialWombatMatrixKeypad(sw)
button0 = SerialWombatMatrixKeypad.SerialWombatMatrixButton(keypad,0)
button1 = SerialWombatMatrixKeypad.SerialWombatMatrixButton(keypad,1)
button2 = SerialWombatMatrixKeypad.SerialWombatMatrixButton(keypad,2)
button3 = SerialWombatMatrixKeypad.SerialWombatMatrixButton(keypad,3)
button4 = SerialWombatMatrixKeypad.SerialWombatMatrixButton(keypad,4)
button5 = SerialWombatMatrixKeypad.SerialWombatMatrixButton(keypad,5)
button6 = SerialWombatMatrixKeypad.SerialWombatMatrixButton(keypad,6)
button7 = SerialWombatMatrixKeypad.SerialWombatMatrixButton(keypad,7)
button8 = SerialWombatMatrixKeypad.SerialWombatMatrixButton(keypad,8)
button9 = SerialWombatMatrixKeypad.SerialWombatMatrixButton(keypad,9)
button10 = SerialWombatMatrixKeypad.SerialWombatMatrixButton(keypad,10)
button11 = SerialWombatMatrixKeypad.SerialWombatMatrixButton(keypad,11)
button12 = SerialWombatMatrixKeypad.SerialWombatMatrixButton(keypad,12)
button13 = SerialWombatMatrixKeypad.SerialWombatMatrixButton(keypad,13)
button14 = SerialWombatMatrixKeypad.SerialWombatMatrixButton(keypad,14)
button15 = SerialWombatMatrixKeypad.SerialWombatMatrixButton(keypad,15)
def setup():
  # put your setup code here, to run once:
  # Wire.begin() is handled by the selected Python interface block
  # Initialize the I2C Bus on default pins
  # Serial.begin() is not used in this Python example
  delay(3000)
  print("Matrix Keypad as Individual Buttons Example")
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
  keypad.begin(10,10,11,12,13,16,17,18,19)
def loop():
  # put your main code here, to run repeatedly:
  # If any of the 16 keys is pressed, print its index number.
  if button0.digitalRead():
    print("0 ", end="")
  if button1.digitalRead():
    print("1 ", end="")
  if button2.digitalRead():
    print("2 ", end="")
  if button3.digitalRead():
    print("3 ", end="")
  if button4.digitalRead():
    print("4 ", end="")
  if button5.digitalRead():
    print("5 ", end="")
  if button6.digitalRead():
    print("6 ", end="")
  if button7.digitalRead():
    print("7 ", end="")
  if button8.digitalRead():
    print("8 ", end="")
  if button9.digitalRead():
    print("9 ", end="")
  if button10.digitalRead():
    print("10 ", end="")
  if button11.digitalRead():
    print("11 ", end="")
  if button12.digitalRead():
    print("12 ", end="")
  if button13.digitalRead():
    print("13 ", end="")
  if button14.digitalRead():
    print("14 ", end="")
  if button15.digitalRead():
    print("15 ", end="")
  # Print how many times the lower right key has been pressed or released
  print(button15.transitions, end="")
  print(" ", end="")
  # Print how long the lower right key has been held down (0 if not pressed)
  print(button15.readDurationInTrueState_mS(), end="")
  print(" ", end="")
  print()

setup()
while True:
  loop()
