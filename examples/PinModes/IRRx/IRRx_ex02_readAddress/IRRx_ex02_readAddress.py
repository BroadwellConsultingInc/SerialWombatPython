# Converted from PinModes/IRRx/IRRx_ex02_readAddress/IRRx_ex02_readAddress.ino
import SerialWombat
from ArduinoFunctions import delay, delayMicroseconds, millis

import SerialWombat_interface
# >>> IMPORTANT: Set this to the configured I2C address of your Serial Wombat chip.
SERIAL_WOMBAT_ADDRESS = 0x60
sw = SerialWombat_interface.SerialWombatChipInstance(SERIAL_WOMBAT_ADDRESS)


# Interface independent code starts here:
import SerialWombatIRRx

# ===== Arduino tab: IRRx_ex02_readAddress.ino =====
#   This example shows how to use the Serial Wombat IR Receive (IRRx) pin mode.  It assumes an NEC compatible IR Transmitter
#   (most inexpensive Arduino kit remotes are compatible) and a 38kHz receiver module that goes low when a modulated IR signal is
#   present.
#
#   This example is compatible with the Serial Wombat 18AB and 8B chips.
#
#   In this example a 16 bit address is received from the transmitter and printed to Serial in hex format.
#
#   This example is useful to determine the address used by a generic NEC transmitter.  This can then be used in
#   the address filtering example (Example 3) to allow only a specific address to be received.
#
#   NEC compatible transmitters may either use and 8 bit address and then send the complement of the
#   address in the alternative byte, or may use all 16 bits for one address.
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
def setup():
  # put your setup code here, to run once:
  # Wire.begin() is handled by the selected Python interface block
  # Initialize the I2C Bus on default pins
  # Serial.begin() is not used in this Python example
  delay(3000)
  print("IR Address Read Example")
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
  irrx.begin(IRRX_PIN)
  # Default parameters:  NEC Mode, queue repeats, active low, 1000ms public data timeout, 0xFFFF public data default, no address filtering
  # irrx.enablePullup(true);   //Comment in this line if your receiver is open drain type without pullup
  print("Press a key on the remote to see it's 16 bit address. If you get no result, ensure the remote is NEC compatible, and that a pull up resistor is in place or enabled if required.")
def loop():
  receivedData = irrx.read()
  if receivedData >=0:
    s = bytearray(10)
    s = "0x%X" % (irrx.readAddress(),)
    # Read the 16 bit address of the transmitter, and convert it to a hex string
    print(s)

setup()
while True:
  loop()
