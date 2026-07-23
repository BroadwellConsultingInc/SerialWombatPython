# Converted from PinModes/PulseTimer/PulseTimer_Ex01/PulseTimer_Ex01.ino
import SerialWombat
from ArduinoFunctions import delay, delayMicroseconds, millis

import SerialWombat_interface
# >>> IMPORTANT: Set this to the configured I2C address of your Serial Wombat chip.
SERIAL_WOMBAT_ADDRESS = 0x60
sw = SerialWombat_interface.SerialWombatChipInstance(SERIAL_WOMBAT_ADDRESS)


# Interface independent code starts here:
import SerialWombatPulseTimer

# ===== Arduino tab: PulseTimer_Ex01.ino =====
# sw is provided by the selected Python interface block above
# Declare a Serial Wombat chip
steering = SerialWombatPulseTimer.SerialWombatPulseTimer(sw)
throttle = SerialWombatPulseTimer.SerialWombatPulseTimer(sw)
button = SerialWombatPulseTimer.SerialWombatPulseTimer(sw)
thumbSwitch = SerialWombatPulseTimer.SerialWombatPulseTimer(sw)
STEERING_PIN = 0
THROTTLE_PIN = 1
BUTTON_PIN = 2
THUMBSWITCH_PIN = 3
# This example is explained in a video tutorial at: https://youtu.be/YtQWUub9gYw
def setup():
  # put your setup code here, to run once:
  # Wire.begin() is handled by the selected Python interface block
  # Initialize the I2C Bus on default pins
  # Serial.begin() is not used in this Python example
  delay(3000)
  print("Pulse Timer Example")
  sw.begin()  # Python interface was configured above
  # Scan the bus for Serial Wombat chips, and initialize the first one found
  # Optional Error handling code begin:
  if not sw.isLatestFirmware():
    print("Firmware version mismatch. Download latest Serial Wombat Arduino Library and update Serial Wombat Firmware to latest version")
  if sw.isSW08() and not sw.isPinModeSupported(SerialWombat.SerialWombatPinMode_t.PIN_MODE_PULSETIMER):
    print("The required pin mode does not appear to be supported in this firmware build. Do you need to download a different firmware?")
    while 1:
      delay(100)
  # sw.registerErrorHandler(...) is Arduino-specific; Python errors are returned by library calls
  # Register an error handler that will print communication errors to Serial
  # Optional Error handling code end
  steering.begin(STEERING_PIN)
  throttle.begin(THROTTLE_PIN)
  button.begin(BUTTON_PIN)
  thumbSwitch.begin(THUMBSWITCH_PIN)
  # Change this to a different pin on 18AB, since 3 is SDA
def clearTerminal():
  print(chr(27), end="")
  # ESC command
  print("[2J", end="")
  # clear screen command
  print(chr(27), end="")
  print("[H", end="")
  # cursor to home command
i = 0
def loop():
  clearTerminal()
  print(steering.readHighCounts())
  print(throttle.readHighCounts())
  print(button.readHighCounts())
  print(thumbSwitch.readHighCounts())
  delay(50)

setup()
while True:
  loop()
