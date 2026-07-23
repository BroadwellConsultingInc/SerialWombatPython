# Converted from PinModes/Watchdog/Watchdog_Ex01_basic/Watchdog_Ex01_basic.ino
import SerialWombat
from ArduinoFunctions import delay, delayMicroseconds, millis

import SerialWombat_interface
# >>> IMPORTANT: Set this to the configured I2C address of your Serial Wombat chip.
SERIAL_WOMBAT_ADDRESS = 0x60
sw = SerialWombat_interface.SerialWombatChipInstance(SERIAL_WOMBAT_ADDRESS)


# Interface independent code starts here:
import SerialWombatWatchdog

# ===== Arduino tab: Watchdog_Ex01_basic.ino =====
# sw is provided by the selected Python interface block above
# Declare a Serial Wombat chip
Watchdog = SerialWombatWatchdog.SerialWombatWatchdog(sw)
# Declare a Watchdog pin
# A video tutorial for this example is available at: https://youtu.be/fIObjmHmprY
def setup():
  # put your setup code here, to run once:
  # Wire.begin() is handled by the selected Python interface block
  # Initialize the I2C Bus on default pins
  # Serial.begin() is not used in this Python example
  delay(3000)
  print("Watchdog Basic Example")
  sw.begin()  # Python interface was configured above
  # Scan the bus for Serial Wombat chips, and initialize the first one found
  # Optional Error handling code begin:
  if not sw.isLatestFirmware():
    print("Firmware version mismatch. Download latest Serial Wombat Arduino Library and update Serial Wombat Firmware to latest version")
  if sw.isSW08() and not sw.isPinModeSupported(SerialWombat.SerialWombatPinMode_t.PIN_MODE_WATCHDOG):
    print("The required pin mode does not appear to be supported in this firmware build. Do you need to download a different firmware?")
    while 1:
      delay(100)
  # sw.registerErrorHandler(...) is Arduino-specific; Python errors are returned by library calls
  # Register an error handler that will print communication errors to Serial
  # Optional Error handling code end
  # Start the watchdog on pin 2.
  # Make the pin Input for normal operation
  # Make the pin go low on timeout
  # Timeout is 10 seconds
  Watchdog.begin(2, SerialWombat.SerialWombatPinState_t.SW_INPUT, SerialWombat.SerialWombatPinState_t.SW_LOW, 10000, False)
  # The Serial Wombat won't self-reset on timeout
  print()
  print("Setup Complete.")
# This flawed routine works well if A is a multiple of B, but
# acts badly otherwise because quotient is unsigned and rolls
# back to a big number if the subtraction goes negative.
# Some values, such as 60 / 7 eventually end up returning a
# (wrong) result as the rollover(s) end up eventually
# giving a number that is a multiple of B.
# others such as 60 / 8 stay trapped in the loop forever.
def DivideAByB(A, B):
  C = 0
  while A > 0:
    A = A - B
    C += 1
  return C
x = 1
def loop():
  global x
  # put your main code here, to run repeatedly:
  print()
  print("60 / ", end="")
  print(x, end="")
  print(" = ", end="")
  print(DivideAByB(60, x))
  x += 1
  Watchdog.updateResetCountdown(10000)
  # Reset the watchdog clock to 10 seconds
  delay(1000)

setup()
while True:
  loop()
