# Converted from PinModes/CharliePlex/Charlieplex_ex03_customLookupOrder/Charlieplex_ex03_customLookupOrder.ino
import SerialWombat
from ArduinoFunctions import delay, delayMicroseconds, millis

import SerialWombat_interface
# >>> IMPORTANT: Set this to the configured I2C address of your Serial Wombat chip.
SERIAL_WOMBAT_ADDRESS = 0x60
sw = SerialWombat_interface.SerialWombatChipInstance(SERIAL_WOMBAT_ADDRESS)


# Interface independent code starts here:
import SerialWombatCharlieplex

# ===== Arduino tab: Charlieplex_ex03_customLookupOrder.ino =====
#  This example shows how to customize the Serial Wombat Charlieplex logical
#  LED lookup table. By customizing this table you can change what is the
#  1st, 2nd, 3rd, etc LED in the sequence. This can be highly advantageous
#  in allowing convenient PCB layout, while abstracting the LEDs into a
#  logical order.
#
#  Note that the entries in this table are an index of the pin numbers provided
#  in the begin() call, not explicit Serial Wombat pin numbers.

charlieplex = SerialWombatCharlieplex.SerialWombatCharlieplex(sw)

CHARLIEPLEX_PIN_0 = 0
CHARLIEPLEX_PIN_1 = CHARLIEPLEX_PIN_0 + 1
CHARLIEPLEX_PIN_2 = CHARLIEPLEX_PIN_1 + 1
CHARLIEPLEX_PIN_3 = CHARLIEPLEX_PIN_2 + 1
CHARLIEPLEX_PIN_4 = CHARLIEPLEX_PIN_3 + 1
CHARLIEPLEX_PIN_5 = CHARLIEPLEX_PIN_4 + 1
CHARLIEPLEX_PIN_6 = CHARLIEPLEX_PIN_5 + 1
CHARLIEPLEX_PIN_7 = CHARLIEPLEX_PIN_6 + 1

NUMBER_OF_LEDS = 56
LED_MOVE_DELAY_MS = 200

ledLookupTable = [
    # Forward electrical direction
    0x01,
    0x02, 0x12,
    0x03, 0x13, 0x23,
    0x04, 0x14, 0x24, 0x34,
    0x05, 0x15, 0x25, 0x35, 0x45,
    0x06, 0x16, 0x26, 0x36, 0x46, 0x56,
    0x07, 0x17, 0x27, 0x37, 0x47, 0x57, 0x67,

    # Reverse electrical direction
    0x10,
    0x20, 0x21,
    0x30, 0x31, 0x32,
    0x40, 0x41, 0x42, 0x43,
    0x50, 0x51, 0x52, 0x53, 0x54,
    0x60, 0x61, 0x62, 0x63, 0x64, 0x65,
    0x70, 0x71, 0x72, 0x73, 0x74, 0x75, 0x76
]

currentLED = 0

def setup():
    delay(3000)
    print("Charlieplex Example 3 - Custom Lookup Order")
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

    charlieplex.begin(CHARLIEPLEX_PIN_0,
                      CHARLIEPLEX_PIN_1,
                      CHARLIEPLEX_PIN_2,
                      CHARLIEPLEX_PIN_3,
                      CHARLIEPLEX_PIN_4,
                      CHARLIEPLEX_PIN_5,
                      CHARLIEPLEX_PIN_6,
                      CHARLIEPLEX_PIN_7,
                      SerialWombatCharlieplex.SerialWombatCharlieplex.DISPLAY_MODE_BITMAP,
                      1)

    # Write the initialized RAM lookup array to the Charlieplex pin mode.
    # writeLookupTable() sends fourteen 0xCC packets with four entries each.
    charlieplex.writeLookupTable(ledLookupTable)

    charlieplex.clearLEDs()
    charlieplex.setLEDs(currentLED)

    print("The custom 56-entry lookup table has been written.")
    print("A single LED is moving through the reordered logical LED sequence.")

def loop():
    global currentLED
    delay(LED_MOVE_DELAY_MS)

    charlieplex.clearLEDs(currentLED)

    currentLED += 1
    if currentLED >= NUMBER_OF_LEDS:
        currentLED = 0

    charlieplex.setLEDs(currentLED)

setup()
while True:
    loop()
