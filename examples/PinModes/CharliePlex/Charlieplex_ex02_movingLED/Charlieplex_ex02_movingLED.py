# Converted from PinModes/CharliePlex/Charlieplex_ex02_movingLED/Charlieplex_ex02_movingLED.ino
import SerialWombat
from ArduinoFunctions import delay, delayMicroseconds, millis

import SerialWombat_interface
# >>> IMPORTANT: Set this to the configured I2C address of your Serial Wombat chip.
SERIAL_WOMBAT_ADDRESS = 0x60
sw = SerialWombat_interface.SerialWombatChipInstance(SERIAL_WOMBAT_ADDRESS)


# Interface independent code starts here:
import SerialWombatCharlieplex

# ===== Arduino tab: Charlieplex_ex02_movingLED.ino =====
#  This example shows how to use the Serial Wombat Charlieplex pin mode
#  set-LED and clear-LED commands.
#
#  This example is compatible with the Serial Wombat 18AB and 8B chips,
#  when the Charlieplex pin mode is present in the firmware build.
#
#  Eight Serial Wombat pins are used to control up to 56 Charlieplexed
#  LEDs.  The pins are assigned sequentially from pin 0 through pin 7.
#
#  One logical LED moves from LED 0 through LED 55.  The previous LED is
#  cleared with CONFIGURE_CHANNEL_MODE_6, command byte 0xCE.  The next LED
#  is set with CONFIGURE_CHANNEL_MODE_5, command byte 0xCD.
#
#  The 0xCD and 0xCE commands can each set or clear as many as five specified
#  logical LEDs without maintaining a bitmap on the Python host.

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
currentLED = 0

def setup():
    delay(3000)
    print("Charlieplex Example 2 - Moving LED")
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
                      56)

    charlieplex.clearLEDs()          # Clear the complete bitmap with 0xCA and 0xCB
    charlieplex.setLEDs(currentLED)  # Set logical LED 0 with command 0xCD
    print("A single LED is moving across logical LEDs 0 through 55.")

def loop():
    global currentLED
    delay(LED_MOVE_DELAY_MS)

    charlieplex.clearLEDs(currentLED) # Clear the previous LED with command 0xCE

    currentLED += 1
    if currentLED >= NUMBER_OF_LEDS:
        currentLED = 0

    charlieplex.setLEDs(currentLED) # Set the next LED with command 0xCD

setup()
while True:
    loop()
