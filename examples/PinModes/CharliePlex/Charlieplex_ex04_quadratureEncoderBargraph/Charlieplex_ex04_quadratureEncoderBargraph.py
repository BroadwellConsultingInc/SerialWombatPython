# Converted from PinModes/CharliePlex/Charlieplex_ex04_quadratureEncoderBargraph/Charlieplex_ex04_quadratureEncoderBargraph.ino
import SerialWombat
from ArduinoFunctions import delay, delayMicroseconds, millis

import SerialWombat_interface
# >>> IMPORTANT: Set this to the configured I2C address of your Serial Wombat chip.
SERIAL_WOMBAT_ADDRESS = 0x60
sw = SerialWombat_interface.SerialWombatChipInstance(SERIAL_WOMBAT_ADDRESS)


# Interface independent code starts here:
import SerialWombatCharlieplex
import SerialWombatQuadEnc

# ===== Arduino tab: Charlieplex_ex04_quadratureEncoderBargraph.ino =====
#  This example shows how to use the Serial Wombat Charlieplex pin mode as a
#  12-LED bargraph controlled by a quadrature encoder.
#
#  Four Serial Wombat pins are used to control 12 Charlieplexed LEDs. The
#  Charlieplex pins are assigned sequentially from pin 0 through pin 3.
#
#  The quadrature encoder uses pins 6 and 7. Its 16-bit public data value is
#  read directly by the Charlieplex pin mode's scaled-output block. No host
#  transfer is needed to update the bargraph after configuration.

charlieplex = SerialWombatCharlieplex.SerialWombatCharlieplex(sw)
quadratureEncoder = SerialWombatQuadEnc.SerialWombatQuadEnc(sw)

CHARLIEPLEX_PIN_0 = 0
CHARLIEPLEX_PIN_1 = CHARLIEPLEX_PIN_0 + 1
CHARLIEPLEX_PIN_2 = CHARLIEPLEX_PIN_1 + 1
CHARLIEPLEX_PIN_3 = CHARLIEPLEX_PIN_2 + 1

QUADRATURE_ENCODER_PIN_A = 6
QUADRATURE_ENCODER_PIN_B = 7

NUMBER_OF_LEDS = 12
MAXIMUM_ENCODER_VALUE = NUMBER_OF_LEDS - 1
lastEncoderValue = 0xFFFF

def setup():
    delay(3000)
    print("Charlieplex Example 4 - Quadrature Encoder Bargraph")
    sw.begin()

    if sw.isSW04():
        print("This Example is not supported on the Serial Wombat 4B chip. An 8B or 18AB chip is required.")
        while 1:
            delay(100)
    if not sw.isLatestFirmware():
        print("Firmware version mismatch. Download latest Serial Wombat Arduino Library and update Serial Wombat Firmware to latest version")
    if sw.isSW08() and (not sw.isPinModeSupported(SerialWombat.SerialWombatPinMode_t.PIN_MODE_CHARLIEPLEX) or
                        not sw.isPinModeSupported(SerialWombat.SerialWombatPinMode_t.PIN_MODE_QUADRATUREENCODER)):
        print("The required pin modes do not appear to be supported in this firmware build. Do you need to download a different firmware?")
        while 1:
            delay(100)

    quadratureEncoder.begin(QUADRATURE_ENCODER_PIN_A,
                            QUADRATURE_ENCODER_PIN_B,
                            10,       # 10 ms debounce
                            True,     # Enable weak pull-ups
                            SerialWombatQuadEnc.QE_READ_MODE_t.QE_ONLOW_POLL)
    quadratureEncoder.write(0)

    charlieplex.begin(CHARLIEPLEX_PIN_0,
                      CHARLIEPLEX_PIN_1,
                      CHARLIEPLEX_PIN_2,
                      CHARLIEPLEX_PIN_3,
                      SerialWombatCharlieplex.SerialWombatCharlieplex.UNUSED_PIN,
                      SerialWombatCharlieplex.SerialWombatCharlieplex.UNUSED_PIN,
                      SerialWombatCharlieplex.SerialWombatCharlieplex.UNUSED_PIN,
                      SerialWombatCharlieplex.SerialWombatCharlieplex.UNUSED_PIN,
                      SerialWombatCharlieplex.SerialWombatCharlieplex.DISPLAY_MODE_SCALED_BARGRAPH,
                      NUMBER_OF_LEDS)

    # Scale encoder public data values 0 through 11 to the full internal
    # 0 through 65535 scaled-output range.
    charlieplex.writeInputScaling(0, MAXIMUM_ENCODER_VALUE)

    # Scale the internal 0 through 65535 value back to logical LED indexes 0
    # through 11 for the Charlieplex bargraph display mode.
    charlieplex.writeOutputScaling(0, MAXIMUM_ENCODER_VALUE)

    # Read the quadrature encoder public data directly from encoder pin A.
    charlieplex.writeScalingEnabled(True, QUADRATURE_ENCODER_PIN_A)

    print("Turn the encoder to adjust the 12-LED Charlieplex bargraph.")

def loop():
    global lastEncoderValue
    encoderValue = quadratureEncoder.read()

    # The quadrature encoder position is unsigned. A value in the upper half
    # of the range indicates that the encoder was decremented below zero.
    if encoderValue > 0x7FFF:
        encoderValue = 0
        quadratureEncoder.write(encoderValue)
    elif encoderValue > MAXIMUM_ENCODER_VALUE:
        encoderValue = MAXIMUM_ENCODER_VALUE
        quadratureEncoder.write(encoderValue)

    if encoderValue != lastEncoderValue:
        print("Encoder position: ", end="")
        print(encoderValue, end="")
        print("  LEDs illuminated: ", end="")
        print(encoderValue + 1)
        lastEncoderValue = encoderValue

    delay(10)

setup()
while True:
    loop()
