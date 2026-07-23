# Converted from PinModes/IRTx/IRTx_Ex01_SimpleCommand/IRTx_Ex01_SimpleCommand.ino
import SerialWombat
from ArduinoFunctions import delay, delayMicroseconds, millis

import SerialWombat_interface
# >>> IMPORTANT: Set this to the configured I2C address of your Serial Wombat chip.
SERIAL_WOMBAT_ADDRESS = 0x60
sw = SerialWombat_interface.SerialWombatChipInstance(SERIAL_WOMBAT_ADDRESS)


# Interface independent code starts here:
import SerialWombatFrequencyOutput
import SerialWombatIRTx

# ===== Arduino tab: IRTx_Ex01_SimpleCommand.ino =====
# sw is provided by the selected Python interface block above
irTx = SerialWombatIRTx.SerialWombatIRTx(sw)
def setup():
  # Serial.begin() is not used in this Python example
  # Wire.begin() is handled by the selected Python interface block
  delay(3000)
  sw.begin()  # Python interface was configured above
  # sw.registerErrorHandler(...) is Arduino-specific; Python errors are returned by library calls
  # Register an error handler that will print communication errors to Serial
  if not sw.isLatestFirmware():
    print("Firmware version mismatch. Download latest Serial Wombat Arduino Library and update Serial Wombat Firmware to latest version")
  irTx.begin(7,0xC7EA)
  # Set up pin 7 as IRTx
  if sw.isSW08():
    irTx.enableSW8b38KHzWP6()
    # Set up Pin 6 on SW08 as carrier
  elif sw.isSW18():
    # Set up pin 9 on SW18AB as carrier
    fo = SerialWombatFrequencyOutput.SerialWombatFrequencyOutput_18AB(sw)
    fo.begin(9)
    fo.writePublicData(38000)
def loop():
  delay(5000)
  irTx.sendMessage(0x10,0xC7EA)
  # Every 5000 ms send 0x10 to device 0xC7EA.  This is volume down on Jon's TCL TV

setup()
while True:
  loop()
