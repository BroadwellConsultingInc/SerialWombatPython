# Converted from PinModes/PS2Keyboard/PS2Keyboard_ex_01_queueing/PS2Keyboard_ex_01_queueing.ino
import SerialWombat
from ArduinoFunctions import delay, delayMicroseconds, millis

import SerialWombat_interface
# >>> IMPORTANT: Set this to the configured I2C address of your Serial Wombat chip.
SERIAL_WOMBAT_ADDRESS = 0x60
sw = SerialWombat_interface.SerialWombatChipInstance(SERIAL_WOMBAT_ADDRESS)


# Interface independent code starts here:
import SerialWombatPS2Keyboard

# ===== Arduino tab: PS2Keyboard_ex_01_queueing.ino =====
#
# This example shows how to configure two pins to work together to connect to an IBM PS2 Keyboard.
#
# This example assumes a Serial Wombat 18AB chip is attached to the Arduino board via I2C.
#
# The goal of this example is to read keystrokes in ASCII from the Keyboard / Serial Wombat 18AB chip and output it
# to serial.
#
# Keyboard data and clock lines should be pulled up to +5v using a 2k resistor.  5V tollerant pins (9-12, 14, 15) should
# be used.
#
# A video demonstrating the use of the PS2 Keyboard pin mode on the Serial Wombat 18AB chip is available at:
# https://www.youtube.com/watch?v=YV00GfyxFJU
#
# Documentation for the SerialWombatTM1637 Arduino class is available at:
# https://broadwellconsultinginc.github.io/SerialWombatArdLib/class_serial_wombat_p_s2_keyboard.html
# sw is provided by the selected Python interface block above
myKeyboard = SerialWombatPS2Keyboard.SerialWombatPS2Keyboard(sw)
PS2_CLK_PIN = 10  # <<<<<<<<<   Set this to the Serial Wombat pin connected to your Keyboard Clock Pin
PS2_DATA_PIN = 11  # <<<<<<<<<   Set this to the Serial Wombat pin connected to your Keyboard Data Pin
def setup():
  # put your setup code here, to run once:
  # Wire.begin() is handled by the selected Python interface block
  # Initialize the I2C Bus on default pins
  # Serial.begin() is not used in this Python example
  delay(3000)
  print("PS2 Keyboard Queueing Example")
  sw.begin()  # Python interface was configured above
  # Scan the bus for Serial Wombat chips, and initialize the first one found
  # Optional Error handling code begin:
  if sw.isSW04():
    print("This Example is not supported on the Serial Wombat 4B chip. An 8B or 18AB chip is required.")
    while 1:
      delay(100)
  if not sw.isLatestFirmware():
    print("Firmware version mismatch. Download latest Serial Wombat Arduino Library and update Serial Wombat Firmware to latest version")
  if sw.isSW08() and not sw.isPinModeSupported(SerialWombat.SerialWombatPinMode_t.PIN_MODE_PS2KEYBOARD):
    print("The required pin mode does not appear to be supported in this firmware build. Do you need to download a different firmware?")
    while 1:
      delay(100)
  # sw.registerErrorHandler(...) is Arduino-specific; Python errors are returned by library calls
  # Register an error handler that will print communication errors to Serial
  # Optional Error handling code end
  print("Connect Clock line to pin ", end="")
  print(PS2_CLK_PIN)
  print(" and data pin to pin ", end="")
  print(PS2_DATA_PIN)
  # Clk Pin
  myKeyboard.begin(PS2_CLK_PIN, PS2_DATA_PIN)
  # Data Pin
def loop():
  x = 0
  x = myKeyboard.read()
  # Read the keyboard queue.  Returns -1 if no characters available
  while x > 0:
    c = x
    # Convert the value to a character
    print(c, end="")
    # Send the character to the serial interface
    x = myKeyboard.read()
    # Read the keyboard queue.  Returns -1 if no characters available

setup()
while True:
  loop()
