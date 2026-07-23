# Converted from PinModes/IRRx/IRRx_ex03_addressFiltering/IRRx_ex03_addressFiltering.ino
import SerialWombat
from ArduinoFunctions import delay, delayMicroseconds, millis

import SerialWombat_interface
# >>> IMPORTANT: Set this to the configured I2C address of your Serial Wombat chip.
SERIAL_WOMBAT_ADDRESS = 0x60
sw = SerialWombat_interface.SerialWombatChipInstance(SERIAL_WOMBAT_ADDRESS)


# Interface independent code starts here:
import SerialWombatIRRx

# ===== Arduino tab: IRRx_ex03_addressFiltering.ino =====
#   This example shows how to use the Serial Wombat IR Receive (IRRx) pin mode.  It assumes an NEC compatible IR Transmitter
#   (most inexpensive Arduino kit remotes are compatible) and a 38kHz receiver module that goes low when a modulated IR signal is
#   present.
#
#   This example is compatible with the Serial Wombat 18AB and 8B chips.
#
#   In this example commands are received from the pin mode and printed to Serial.  Address filtering is turned on
#   so that only a single transmitter address is processed (other addresses are ignored).  The address is set
#   with the #define TRANSMITTER_ADDRESS .  Example 2 can help find the address of a given transmitter.
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
#   https://broadwellconsultinginc.github.io/SerialWombatArdLib/class_serial_wombat_i_r_rx.html
#
# sw is provided by the selected Python interface block above
irrx = SerialWombatIRRx.SerialWombatIRRx(sw)
IRRX_PIN = 3
TRANSMITTER_ADDRESS = 0xEF00
def setup():
  # put your setup code here, to run once:
  # Wire.begin() is handled by the selected Python interface block
  # Initialize the I2C Bus on default pins
  # Serial.begin() is not used in this Python example
  delay(3000)
  print("IR Address Filtering Example")
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
  irrx.begin(IRRX_PIN, SerialWombatIRRx.publicDataOutput.DATACOUNT, 0, True, SerialWombat.SerialWombatPinState_t.SW_LOW, 1000, 0xFFFF, True, TRANSMITTER_ADDRESS)
  # Filter to address TRANSMITTER_ADDRESS  (This value was determined for a given remote using example 2
  # irrx.enablePullup(true);   //Comment in this line if your receiver is open drain type without pullup
  print("Press a key on the remote to see it's 8 bit.")
  print("If you get no result, ensure the remote is NEC compatible, and that a pull up resistor is in place or enabled if required.")
def loop():
  receivedData = irrx.read()
  if receivedData >=0:
    print(receivedData)

setup()
while True:
  loop()
