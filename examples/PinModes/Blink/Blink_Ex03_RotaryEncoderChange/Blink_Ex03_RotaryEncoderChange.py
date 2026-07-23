# Converted from PinModes/Blink/Blink_Ex03_RotaryEncoderChange/Blink_Ex03_RotaryEncoderChange.ino
import SerialWombat
from ArduinoFunctions import delay, delayMicroseconds, millis

import SerialWombat_interface
# >>> IMPORTANT: Set this to the configured I2C address of your Serial Wombat chip.
SERIAL_WOMBAT_ADDRESS = 0x60
sw = SerialWombat_interface.SerialWombatChipInstance(SERIAL_WOMBAT_ADDRESS)


# Interface independent code starts here:
import SerialWombatBlink
import SerialWombatQuadEnc

# ===== Arduino tab: Blink_Ex03_RotaryEncoderChange.ino =====
#
# This example shows how to configure a Serial Wombat 8B or 18AB chip to blink an LED any
# time the count on a rotary encoder changes
#
# This sketch was last tested with version 2.2.2 of the firmware.
#
#
# A video demonstrating the Blink pin mode is available here:
# TODO
#
# Documentation for the SerialWombatBlink class is available at:
# https://broadwellconsultinginc.github.io/SerialWombatArdLib/class_serial_wombat_blink.html
#
# For reference, the source code to the firmware (looking at this isn't required, but is interesting) is available here:
# https://github.com/BroadwellConsultingInc/SerialWombat/blob/main/SerialWombatPinModes/blink.c
#
# sw is provided by the selected Python interface block above
blinkPin = SerialWombatBlink.SerialWombatBlink(sw)
rotaryEncoder = SerialWombatQuadEnc.SerialWombatQuadEnc_18AB(sw)
BLINK_PIN = 1  # SW8B PCB0029 On Board LED is on pin 1 (must close solder jumper)
ROTARY_ENC_PIN_A = 5
ROTARY_ENC_PIN_B = 7
def setup():
  # put your setup code here, to run once:
  # Wire.begin() is handled by the selected Python interface block
  # Initialize the I2C Bus on default pins
  # Serial.begin() is not used in this Python example
  delay(3000)
  print("Rotary Encoder example. Connect encoder to pins 5 and 6")
  sw.begin()  # Python interface was configured above
  # Scan the bus for Serial Wombat chips, and initialize the first one found
  # Optional Error handling code begin:
  if sw.isSW04():
    print("This Example is not supported on the Serial Wombat 4B chip. An 8B or 18AB chip is required.")
    while 1:
      delay(100)
  if not sw.isLatestFirmware():
    print("Firmware version mismatch. Download latest Serial Wombat Arduino Library and update Serial Wombat Firmware to latest version")
  if not sw.isPinModeSupported(SerialWombat.SerialWombatPinMode_t.PIN_MODE_BLINK):
    print("The required pin mode does not appear to be supported in this firmware build. Do you need to download a different firmware?")
    while 1:
      delay(100)
  # sw.registerErrorHandler(...) is Arduino-specific; Python errors are returned by library calls
  # Register an error handler that will print communication errors to Serial
  # Optional Error handling code end
  rotaryEncoder.begin(ROTARY_ENC_PIN_A, ROTARY_ENC_PIN_B)
  # depending on your rotary encoder, additional settings such as debounce time or read method may be required.  See rotary encoder documentation
  blinkPin.begin(BLINK_PIN, ROTARY_ENC_PIN_A )
  # Blink when the Serial Wombat chip
  # Detects a rotary encoder change
oldRotaryEncoderReading = 0
# Note that in the loop we read the rotary encoder reading, but don't
# blink the LED.  The delay is to illustrate this.  The LED blink
# happens immediately giving user feedback of each change, but the host
# doesn't retreive the new value for some time.
def loop():
  global oldRotaryEncoderReading
  newRotaryEncoderReading = rotaryEncoder.readPublicData()
  if newRotaryEncoderReading != oldRotaryEncoderReading:
    print(newRotaryEncoderReading)
    oldRotaryEncoderReading = newRotaryEncoderReading
  delay(4000)
  # Wait 4 seconds between reads to simulate the host doing other stuff

setup()
while True:
  loop()
