# Converted from PinModes/PulseOnChange/PulseOnChange_Ex02_BeepOnButtons/PulseOnChange_Ex02_BeepOnButtons.ino
import SerialWombat
from ArduinoFunctions import delay, delayMicroseconds, millis

import SerialWombat_interface
# >>> IMPORTANT: Set this to the configured I2C address of your Serial Wombat chip.
SERIAL_WOMBAT_ADDRESS = 0x60
sw = SerialWombat_interface.SerialWombatChipInstance(SERIAL_WOMBAT_ADDRESS)


# Interface independent code starts here:
import SerialWombatDebouncedInput
import SerialWombatPulseOnChange

# ===== Arduino tab: PulseOnChange_Ex02_BeepOnButtons.ino =====
#
#
# THIS EXAMPLE REQUIRES SW18AB Firmware Version 2.1.0 or Higher!
#
# This example shows how to create a PulseOnChange pin configured to pulse when any of a set of
# configured pins or data sources changes.
#
# This example assumes a piezo is attached to Pin 8 (The kind of piezo without a built in driver)
# through a resistor.  Pin 8 is chosen because this example requires minimal hardware
# support (Analog, enhanced digital capability, etc.) and pin 8 has none of these things.
#
# The pulse on change pin mode looks at pins 19,18, and 17 which are configured as debounced inputs.
# When the value of any of those pins increases (the button is pressed) then a tone is generated.
#
# Documentation for the SerialWombatPulseOnChange Arduino class is available at:
# https://broadwellconsultinginc.github.io/SerialWombatArdLib/class_serial_wombat_pulse_on_change.html#details
#
# sw is provided by the selected Python interface block above
poc = SerialWombatPulseOnChange.SerialWombatPulseOnChange(sw)
dbi19 = SerialWombatDebouncedInput.SerialWombatDebouncedInput(sw)
dbi18 = SerialWombatDebouncedInput.SerialWombatDebouncedInput(sw)
dbi17 = SerialWombatDebouncedInput.SerialWombatDebouncedInput(sw)
def setup():
  # put your setup code here, to run once:
  # Wire.begin() is handled by the selected Python interface block
  # Initialize the I2C Bus on default pins
  # Serial.begin() is not used in this Python example
  delay(3000)
  print("Pulse on Change multiple input Example")
  sw.begin()  # Python interface was configured above
  # Scan the bus for Serial Wombat chips, and initialize the first one found
  # Optional Error handling code begin:
  if sw.isSW04():
    print("This Example is not supported on the Serial Wombat 4B chip. An 8B or 18AB chip is required.")
    while 1:
      delay(100)
  if not sw.isLatestFirmware():
    print("Firmware version mismatch. Download latest Serial Wombat Arduino Library and update Serial Wombat Firmware to latest version")
  if sw.isSW08() and not (sw.isPinModeSupported(SerialWombat.SerialWombatPinMode_t.PIN_MODE_PULSE_ON_CHANGE) and sw.isPinModeSupported(SerialWombat.SerialWombatPinMode_t.PIN_MODE_DEBOUNCE)):
    print("The required pin mode does not appear to be supported in this firmware build. Do you need to download a different firmware?")
    while 1:
      delay(100)
  # sw.registerErrorHandler(...) is Arduino-specific; Python errors are returned by library calls
  # Register an error handler that will print communication errors to Serial
  # Optional Error handling code end
  dbi19.begin(19)
  dbi18.begin(18)
  dbi17.begin(17)
  poc.begin(8)
  # Implied values active high, inactive low, 50mS pulse time, 50mS pulse off, OR entries, No PWM
  # first entry (valid values are 0-7)
  poc.setEntryOnIncrease(0, 19)
  # The data source we're monitoring for change
  # first entry (valid values are 0-7)
  poc.setEntryOnIncrease(1, 18)
  # The data source we're monitoring for change
  # first entry (valid values are 0-7)
  poc.setEntryOnIncrease(2, 17)
  # The data source we're monitoring for change
def loop():
  # Nothing to do...  The Serial Wombat chip is handling this internally.
  delay(1000)

setup()
while True:
  loop()
