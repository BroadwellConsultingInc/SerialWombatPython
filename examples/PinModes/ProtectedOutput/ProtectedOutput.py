# Converted from PinModes/ProtectedOutput/ProtectedOutput.ino
import SerialWombat
from ArduinoFunctions import delay, delayMicroseconds, millis

import SerialWombat_interface
# >>> IMPORTANT: Set this to the configured I2C address of your Serial Wombat chip.
SERIAL_WOMBAT_ADDRESS = 0x60
sw = SerialWombat_interface.SerialWombatChipInstance(SERIAL_WOMBAT_ADDRESS)


# Interface independent code starts here:
import SerialWombatAnalogInput
import SerialWombatProtectedOutput

# ===== Arduino tab: ProtectedOutput.ino =====
# sw is provided by the selected Python interface block above
# Declare a Serial Wombat chip
swpo = SerialWombatProtectedOutput.SerialWombatProtectedOutput(sw)
Feedback = SerialWombatAnalogInput.SerialWombatAnalogInput(sw)
# This example is explained in a video tutorial at: https://youtu.be/p8CO04C1q_Y
def setup():
  # put your setup code here, to run once:
  # Wire.begin() is handled by the selected Python interface block
  # Initialize the I2C Bus on default pins
  # Serial.begin() is not used in this Python example
  delay(3000)
  print("Protected Output Example")
  sw.begin()  # Python interface was configured above
  # Scan the bus for Serial Wombat chips, and initialize the first one found
  # Optional Error handling code begin:
  if not sw.isLatestFirmware():
    print("Firmware version mismatch. Download latest Serial Wombat Arduino Library and update Serial Wombat Firmware to latest version")
  if sw.isSW08() and not (sw.isPinModeSupported(SerialWombat.SerialWombatPinMode_t.PIN_MODE_ANALOGINPUT) and sw.isPinModeSupported(SerialWombat.SerialWombatPinMode_t.PIN_MODE_PROTECTED_OUTPUT)):
    print("The required pin mode does not appear to be supported in this firmware build. Do you need to download a different firmware?")
    while 1:
      delay(100)
  # sw.registerErrorHandler(...) is Arduino-specific; Python errors are returned by library calls
  # Register an error handler that will print communication errors to Serial
  # Optional Error handling code end
  swpo.begin(3,1)
  # Controlling pin 3.   Feedback from pin 1.
  Feedback.begin(1)
  # Begin analog reading on pin 1
i = 0
def loop():
  global i
  if swpo.isInSafeState():
    print("Protected Output Fault Detected, Output set to Safe State!")
  if i & 0x01:
    swpo.configure(SerialWombatProtectedOutput.PO_FAULT_IF_FEEDBACK_GREATER_THAN_EXPECTED,8000,10,SerialWombat.SerialWombatPinState_t.SW_HIGH,SerialWombat.SerialWombatPinState_t.SW_LOW)
    print("On")
  else:
    swpo.digitalWrite(0)
    print("Off")
  delay(100)
  print("counts at drain: ", end="")
  print(Feedback.readCounts())
  print(Feedback.readVoltage_mV(), end="")
  print(" mV")
  print()
  delay(3000)
  i += 1
setup()
while True:
  loop()
