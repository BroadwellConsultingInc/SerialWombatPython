# Converted from PinModes/CharliePlex/Charlieplex_ex01_bitmapPatterns/Charlieplex_ex01_bitmapPatterns.ino
import SerialWombat
from ArduinoFunctions import delay, delayMicroseconds, millis

import SerialWombat_interface
# >>> IMPORTANT: Set this to the configured I2C address of your Serial Wombat chip.
SERIAL_WOMBAT_ADDRESS = 0x60
sw = SerialWombat_interface.SerialWombatChipInstance(SERIAL_WOMBAT_ADDRESS)


# Interface independent code starts here:
import SerialWombatCharlieplex

# ===== Arduino tab: Charlieplex_ex01_bitmapPatterns.ino =====
#  This example shows how to use the Serial Wombat Charlieplex pin mode
#  to display bitmap patterns on 56 LEDs.
#
#  This example is compatible with the Serial Wombat 18AB and 8B chips,
#  when the Charlieplex pin mode is present in the firmware build.
#
#  Eight Serial Wombat pins are used to control up to 56 Charlieplexed
#  LEDs.  The pins are assigned sequentially from pin 0 through pin 7.
#
#  The LED bitmap is stored in a seven-byte array.  Bit 0 of byte 0 controls
#  logical LED 0, and bit 7 of byte 6 controls logical LED 55.
#
#  SerialWombatCharlieplex.writeLEDArray() sends the bitmap using the
#  CONFIGURE_CHANNEL_MODE_2 and CONFIGURE_CHANNEL_MODE_3 commands.  These
#  commands have command bytes 0xCA and 0xCB.
#
#  A new pattern is written every 200 ms.
#
#  Each LED must have an appropriate current-limiting resistor.  The LED
#  wiring direction determines which logical LED index controls it.
#
#  SerialWombatCharlieplex pin mode documentation:
#
#  TODO coming soon
#
#  SerialWombatCharlieplex tutorial video:
#
#  TODO coming soon

charlieplex = SerialWombatCharlieplex.SerialWombatCharlieplex(sw)

CHARLIEPLEX_PIN_0 = 0
CHARLIEPLEX_PIN_1 = CHARLIEPLEX_PIN_0 + 1
CHARLIEPLEX_PIN_2 = CHARLIEPLEX_PIN_1 + 1
CHARLIEPLEX_PIN_3 = CHARLIEPLEX_PIN_2 + 1
CHARLIEPLEX_PIN_4 = CHARLIEPLEX_PIN_3 + 1
CHARLIEPLEX_PIN_5 = CHARLIEPLEX_PIN_4 + 1
CHARLIEPLEX_PIN_6 = CHARLIEPLEX_PIN_5 + 1
CHARLIEPLEX_PIN_7 = CHARLIEPLEX_PIN_6 + 1

PATTERN_DELAY_MS = 200

ledPatterns = [
    [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00], # All LEDs off
    [0x55, 0x55, 0x55, 0x55, 0x55, 0x55, 0x55], # Even-numbered LEDs
    [0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA], # Odd-numbered LEDs
    [0x33, 0x33, 0x33, 0x33, 0x33, 0x33, 0x33], # Two LEDs on, two LEDs off
    [0xCC, 0xCC, 0xCC, 0xCC, 0xCC, 0xCC, 0xCC], # Inverse two-on, two-off pattern
    [0xFF, 0xFF, 0xFF, 0x0F, 0x00, 0x00, 0x00], # LEDs 0 through 27
    [0x00, 0x00, 0x00, 0xF0, 0xFF, 0xFF, 0xFF], # LEDs 28 through 55
    [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]  # All 56 LEDs on
]

NUMBER_OF_PATTERNS = len(ledPatterns)
currentPattern = 0

def setup():
    global currentPattern
    delay(3000)
    print("Charlieplex Example 1 - Bitmap Patterns")
    sw.begin()

    if sw.isSW04():
        print("This Example is not supported on the Serial Wombat 4B chip. An 8B or 18AB chip is required.")
        while 1:
            delay(100)
    if not sw.isLatestFirmware():
        print("Firmware version mismatch. Download latest Serial Wombat Arduino Library and update Serial Wombat Firmware to latest version")
    if sw.isSW08() and not sw.isPinModeSupported(SerialWombat.SerialWombatPinMode_t.PIN_MODE_CHARLIEPLEX):
        print("The required pin mode does not appear to be supported in this firmware build. Do you need to download a different firmware?")
        while 1:
            delay(100)

    # A 56 ms minimum scan period provides consistent per-LED duty cycle as the
    # number of illuminated LEDs changes from one pattern to another.
    charlieplex.begin(CHARLIEPLEX_PIN_0,
                      CHARLIEPLEX_PIN_1,
                      CHARLIEPLEX_PIN_2,
                      CHARLIEPLEX_PIN_3,
                      CHARLIEPLEX_PIN_4,
                      CHARLIEPLEX_PIN_5,
                      CHARLIEPLEX_PIN_6,
                      CHARLIEPLEX_PIN_7,
                      SerialWombatCharlieplex.SerialWombatCharlieplex.DISPLAY_MODE_BITMAP,
                      56)

    charlieplex.writeLEDArray(ledPatterns[currentPattern]) # Sends 0xCA and 0xCB commands
    print("Displaying a new 56-LED bitmap pattern every 200 ms.")

def loop():
    global currentPattern
    delay(PATTERN_DELAY_MS)

    currentPattern += 1
    if currentPattern >= NUMBER_OF_PATTERNS:
        currentPattern = 0

    charlieplex.writeLEDArray(ledPatterns[currentPattern]) # Sends 0xCA and 0xCB commands

setup()
while True:
    loop()
