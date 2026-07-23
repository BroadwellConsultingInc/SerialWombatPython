# Converted from PinModes/TM1637/TM1637_Ex01_012345/TM1637_Ex01_012345.ino
import SerialWombat
from ArduinoFunctions import delay, delayMicroseconds, millis

import SerialWombat_interface
# >>> IMPORTANT: Set this to the configured I2C address of your Serial Wombat chip.
SERIAL_WOMBAT_ADDRESS = 0x60
sw = SerialWombat_interface.SerialWombatChipInstance(SERIAL_WOMBAT_ADDRESS)


# Interface independent code starts here:
import SerialWombatTM1637

# ===== Arduino tab: TM1637_Ex01_012345.ino =====
#
#   This example shows how to configure two pins to work together to drive a TM1637 seven-segment
#   LED display with a Serial Wombat 8B or 18AB chip.
#
#   The goal of this example is to display "012345" on the display.  Ideally, "012345" will be displayed
#   on a 6-segment display, and "0123" will be displayed on a 4 digit display.
#
#   However, some displays may have the digits connected to the display in a different order than expected.
#   For instance, the 6 segment diymore display I bought on Amazon in September of 2021 displayed "210543"
#   indicating that each of the 3-segment LED displays used to make up the 6 digits was wired backwards.
#
#   In the example below, note the call to writeDigitOrder().  This function is used to correct digit order.
#   Simply enter the number displayed on the display by default as parameters and the display will show
#   correctly.  For example for the diymore display:
#   writeDigitalOrder(2,1,0,5,4,3);
#
#   A video demonstrating the use of the TM1637 pin mode on the Serial Wombat 18AB chip is available at:
#   https://youtu.be/AwW12n6o_T0
#
#   Documentation for the SerialWombatTM1637 Arduino class is available at:
#   https://broadwellconsultinginc.github.io/SerialWombatArdLib/class_serial_wombat_t_m1637.html#details
#
# sw is provided by the selected Python interface block above
myDisplay = SerialWombatTM1637.SerialWombatTM1637(sw)
DISPLAY_CLK_PIN = 19  # <<<<<<<<<   Set this to the Serial Wombat pin connected to your Display Clock Pin
DISPLAY_DIN_PIN = 18  # <<<<<<<<<   Set this to the Serial Wombat pin connected to your Display Data Pin
def setup():
  # put your setup code here, to run once:
  # Wire.begin() is handled by the selected Python interface block
  # Initialize the I2C Bus on default pins
  # Serial.begin() is not used in this Python example
  delay(3000)
  print("TM1637 123456 Example")
  sw.begin()  # Python interface was configured above
  # Scan the bus for Serial Wombat chips, and initialize the first one found
  # Optional Error handling code begin:
  if sw.isSW04():
    print("This Example is not supported on the Serial Wombat 4B chip. An 8B or 18AB chip is required.")
    while 1:
      delay(100)
  if not sw.isLatestFirmware():
    print("Firmware version mismatch. Download latest Serial Wombat Arduino Library and update Serial Wombat Firmware to latest version")
  if sw.isSW08() and not sw.isPinModeSupported(SerialWombat.SerialWombatPinMode_t.PIN_MODE_TM1637):
    print("The required pin mode does not appear to be supported in this firmware build. Do you need to download a different firmware?")
    while 1:
      delay(100)
  # sw.registerErrorHandler(...) is Arduino-specific; Python errors are returned by library calls
  # Register an error handler that will print communication errors to Serial
  # Optional Error handling code end
  # Clk Pin
  # Data Pin
  # Number of digits
  # Mode enumeration
  # Source pin Not used in SerialWombatTM1637.SWTM1637Mode.tm1637CharArray mode
  myDisplay.begin(DISPLAY_CLK_PIN, DISPLAY_DIN_PIN, 6, SerialWombatTM1637.SWTM1637Mode.tm1637CharArray, 0x55, 4)
  # Brightness
  # myDisplay.writeDigitOrder(2,3,4,5,0,1);
  test = "012345"
  myDisplay.writeArray(test)
def loop():
  pass

setup()
while True:
  loop()
