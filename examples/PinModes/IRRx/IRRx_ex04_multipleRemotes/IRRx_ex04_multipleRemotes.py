# Converted from PinModes/IRRx/IRRx_ex04_multipleRemotes/IRRx_ex04_multipleRemotes.ino
import SerialWombat
from ArduinoFunctions import delay, delayMicroseconds, millis

import SerialWombat_interface
# >>> IMPORTANT: Set this to the configured I2C address of your Serial Wombat chip.
SERIAL_WOMBAT_ADDRESS = 0x60
sw = SerialWombat_interface.SerialWombatChipInstance(SERIAL_WOMBAT_ADDRESS)


# Interface independent code starts here:
import SerialWombatIRRx

# ===== Arduino tab: IRRx_ex04_multipleRemotes.ino =====
#   This example shows how to use the Serial Wombat IR Receive (IRRx) pin mode.  It assumes two  NEC compatible IR Transmitters with different addresses
#   (most inexpensive Arduino kit remotes are compatible) and a 38kHz receiver module that goes low when a modulated IR signal is
#   present.
#
#   This example is compatible with the Serial Wombat 18AB and 8B chips.
#
#   This example shows how to simultaneously monitor for two different IR Transmitters (with different addresses)
#
#   In order to achieve this, a single IR receiver module is routed to multiple Serial Wombat pins, each of which
#   is configured to SerialWombatIRRx pin mode.  Each pin mode is configured to filter to a different address.
#
#   In this example commands are received from the pin mode and printed to Serial, along with either A or B depending on
#   which remote sent the command.
#   Note that if both transmitters transmit at the same time their signals may interfere with each other.
#
#   Example 2 can help find the address of a given transmitter.
#
#
#   NEC compatible transmitters may either use and 8 bit address and then send the complement of the
#   address in the alternative byte, or may use all 16 bits for one address.  The Serial Wombat IRRx pin mode
#   treats both of these cases as a single 16 bit address.
#
#   Video on IRRx pin mode:
#
#   TODO coming soon
#
#   SerialWombatIRRx pin mode documentation:
#
#   TODO
#
# sw is provided by the selected Python interface block above
irrx1 = SerialWombatIRRx.SerialWombatIRRx(sw)
irrx2 = SerialWombatIRRx.SerialWombatIRRx(sw)
IRRX_FIRST_REMOTE_PIN = 7
IRRX_SECOND_REMOTE_PIN = 8
def setup():
  # put your setup code here, to run once:
  # Wire.begin() is handled by the selected Python interface block
  # Initialize the I2C Bus on default pins
  # Serial.begin() is not used in this Python example
  delay(3000)
  print("IR Multiple Remote Example")
  sw.begin()  # Python interface was configured above
  # Scan the bus for Serial Wombat chips, and initialize the first one found
  # Optional Error handling code begin:
  if sw.isSW04():
    print("This Example is not supported on the Serial Wombat 4B chip. An 8B or 18AB chip is required.")
    while 1:
      delay(100)
  if not sw.isLatestFirmware():
    print("Firmware version mismatch. Download latest Serial Wombat Arduino Library and update Serial Wombat Firmware to latest version")
  if sw.isSW08() and not (sw.isPinModeSupported(SerialWombat.SerialWombatPinMode_t.PIN_MODE_IRRX) ):
    print("The required pin mode does not appear to be supported in this firmware build. Do you need to download a different firmware?")
    while 1:
      delay(100)
  # sw.registerErrorHandler(...) is Arduino-specific; Python errors are returned by library calls
  # Register an error handler that will print communication errors to Serial
  # Optional Error handling code end
  # Make data count the output
  # Mode 0 : NEC
  # Use repeat
  # Active Low
  # 1000 ms Public Data Timeout
  # Default public data
  # Use Address Filtering
  irrx1.begin(IRRX_FIRST_REMOTE_PIN, SerialWombatIRRx.publicDataOutput.DATACOUNT, 0, True, SerialWombat.SerialWombatPinState_t.SW_LOW, 1000, 0xFFFF, True, 0xEF00)
  # Filter to address 0xEF00  (This value was determined for a given remote using example 2
  # irrx1.enablePullup(true);   //Comment in this line if your receiver is open drain type without pullup .  Only one pin needs its pull up enabled
  # Make data count the output
  # Mode 0 : NEC
  # Use repeat
  # Active Low
  # 1000 ms Public Data Timeout
  # Default public data
  # Use Address Filtering
  irrx2.begin(IRRX_SECOND_REMOTE_PIN, SerialWombatIRRx.publicDataOutput.DATACOUNT, 0, True, SerialWombat.SerialWombatPinState_t.SW_LOW, 1000, 0xFFFF, True, 0xFF00)
  # Filter to address 0xFF00  (This value was determined for a given remote using example 2
def loop():
  receivedData = irrx1.read()
  if receivedData >=0:
    s = bytearray(10)
    print("A: ", end="")
    print(receivedData)
  receivedData = irrx2.read()
  if receivedData >=0:
    s = bytearray(10)
    print("B: ", end="")
    print(receivedData)

setup()
while True:
  loop()
