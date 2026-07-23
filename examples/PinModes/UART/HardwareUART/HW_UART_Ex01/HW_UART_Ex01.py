# Converted from PinModes/UART/HardwareUART/HW_UART_Ex01/HW_UART_Ex01.ino
import SerialWombat
from ArduinoFunctions import delay, delayMicroseconds, millis

import SerialWombat_interface
# >>> IMPORTANT: Set this to the configured I2C address of your Serial Wombat chip.
SERIAL_WOMBAT_ADDRESS = 0x6B
sw = SerialWombat_interface.SerialWombatChipInstance(SERIAL_WOMBAT_ADDRESS)


# Interface independent code starts here:
import SerialWombatUART

# ===== Arduino tab: HW_UART_Ex01.ino =====
# sw is provided by the selected Python interface block above
# Declare a Serial Wombat chip
SerWomUart = SerialWombatUART.SerialWombatUART(sw)
# Declare a Serial Wombat UART  Only one UART can be assigned on the SerialWombat 4B.  This pin mode does not work on Serial Wombat 4A.  Pins 5 and 4 must be used as Rx and TX on the SW8B.  Enhanced digital performance pins must be used on the SW18AB
# There is a video tutorial to go with this example at:  https://youtu.be/C1FjcaiBYZs
def setup():
  # put your setup code here, to run once:
  # Wire.begin() is handled by the selected Python interface block
  # Initialize the I2C Bus on default pins
  # Serial.begin() is not used in this Python example
  delay(3000)
  print("Serial Wombat HW UART Example")
  sw.begin()  # Python interface was configured above
  # Scan the bus for Serial Wombat chips, and initialize the first one found
  # Optional Error handling code begin:
  if not sw.isLatestFirmware():
    print("Firmware version mismatch. Download latest Serial Wombat Arduino Library and update Serial Wombat Firmware to latest version")
  if sw.isSW08() and not sw.isPinModeSupported(SerialWombat.SerialWombatPinMode_t.PIN_MODE_UART_RX_TX):
    print("The required pin mode does not appear to be supported in this firmware build. Do you need to download a different firmware?")
    while 1:
      delay(100)
  # sw.registerErrorHandler(...) is Arduino-specific; Python errors are returned by library calls
  # Register an error handler that will print communication errors to Serial
  # Optional Error handling code end
  SerWomUart.begin(57600, 1, 0, 1)
  # Start the UART at 57600, assigned to pin 1, receive on Pin 0, Transmit on Pin 1.
  SerWomUart.println()
  SerWomUart.println("Setup complete")
  # Notify that we finished startup.
def loop():
  # put your main code here, to run repeatedly:
  c = SerWomUart.read()
  if c == ord('A'):
    SerWomUart.println("A is for AARDVARK!")
  elif c == ord('B'):
    SerWomUart.println("B is for BUTTERFLY!")
  elif c == ord('C'):
    SerWomUart.println("C is for CAT!")
  elif c == ord('X'):
    # Print out all printable ASCII characters.
    array = bytearray(range(0x21, 0x80))
    SerWomUart.write(array, len(array))

setup()
while True:
  loop()
