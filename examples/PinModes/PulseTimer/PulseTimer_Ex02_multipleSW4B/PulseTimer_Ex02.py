# Converted from PinModes/PulseTimer/PulseTimer_Ex02_multipleSW4B/PulseTimer_Ex02.ino
import SerialWombat
from ArduinoFunctions import delay, delayMicroseconds, millis

import SerialWombat_interface
# >>> IMPORTANT: Set this to the configured I2C address of your Serial Wombat chip.
SERIAL_WOMBAT_ADDRESS = 0x60
sw = SerialWombat_interface.SerialWombatChipInstance(SERIAL_WOMBAT_ADDRESS)


# Interface independent code starts here:
import SerialWombatPulseTimer

# ===== Arduino tab: PulseTimer_Ex02.ino =====
sw6C = SerialWombat_interface.SerialWombatChipInstance(SERIAL_WOMBAT_ADDRESS)  # Set this chip's address as needed
# Declare a Serial Wombat chip
steering = SerialWombatPulseTimer.SerialWombatPulseTimer(sw6C)
throttle = SerialWombatPulseTimer.SerialWombatPulseTimer(sw6C)
button = SerialWombatPulseTimer.SerialWombatPulseTimer(sw6C)
thumbSwitch = SerialWombatPulseTimer.SerialWombatPulseTimer(sw6C)
sw6D = SerialWombat()
# Declare a second Serial Wombat
leftKnob = SerialWombatPulseTimer.SerialWombatPulseTimer(sw6D)
rightKnob = SerialWombatPulseTimer.SerialWombatPulseTimer(sw6D)
# This example is explained in a video tutorial at: https://youtu.be/YtQWUub9gYw
def setup():
  # put your setup code here, to run once:
  # Wire.begin() is handled by the selected Python interface block
  sw6C.begin()  # Python interface was configured above
  # Initialize the Serial Wombat library to use the primary I2C port, SerialWombat is address 6C.
  sw6D.begin()  # Python interface was configured above
  # Initialize the second Serial Wombat on address 6D
  # Optional Error handling code begin:
  if not sw6C.isLatestFirmware() or not sw6D.isLatestFirmware():
    print("Firmware version mismatch. Download latest Serial Wombat Arduino Library and update Serial Wombat Firmware to latest version")
  # sw6C.registerErrorHandler(...) is Arduino-specific; Python methods return error codes
  # Register an error handler that will print communication errors to Serial
  # sw6D.registerErrorHandler(...) is Arduino-specific; Python methods return error codes
  # Register an error handler that will print communication errors to Serial
  # Optional Error handling code end
  steering.begin(0)
  # On sw6C
  throttle.begin(1)
  button.begin(2)
  thumbSwitch.begin(3)
  leftKnob.begin(0)
  # On sw6D
  rightKnob.begin(1)
  # Serial.begin() is not used in this Python example
def clearTerminal():
  print(chr(27), end="")
  # ESC command
  print("[2J", end="")
  # clear screen command
  print(chr(27), end="")
  print("[H")
  # cursor to home command
def loop():
  clearTerminal()
  print(steering.readHighCounts())
  print(throttle.readHighCounts())
  print(button.readHighCounts())
  print(thumbSwitch.readHighCounts())
  print(leftKnob.readHighCounts())
  print(rightKnob.readHighCounts())
  delay(50)

setup()
while True:
  loop()
