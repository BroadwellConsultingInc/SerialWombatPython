"""
Copyright 2026 Broadwell Consulting Inc.

"Serial Wombat" is a registered trademark of Broadwell Consulting Inc. in
the United States.  See SerialWombat.com for usage guidance.

Permission is hereby granted, free of charge, to any person obtaining a
 * copy of this software and associated documentation files (the "Software"),
 * to deal in the Software without restriction, including without limitation
 * the rights to use, copy, modify, merge, publish, distribute, sublicense,
 * and/or sell copies of the Software, and to permit persons to whom the
 * Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
 * THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
 * OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
 * ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
 * OTHER DEALINGS IN THE SOFTWARE.
"""

"""! @file SerialWombatCharlieplex.py
"""

import SerialWombat
from SerialWombatAbstractScaledOutput import SerialWombatAbstractScaledOutput


class SerialWombatCharlieplex(SerialWombatAbstractScaledOutput):
    """!
    @brief A class representing a Serial Wombat Charlieplexed LED display.

    The Charlieplex pin mode uses between 2 and 8 Serial Wombat pins to control
    up to N * (N - 1) LEDs, for a maximum of 56 LEDs with 8 pins.  One LED is
    driven during each approximately 1 ms Serial Wombat execution frame.

    The first pin in the pins array is the controlling pin.  Its public data is
    used by display modes that consume public data.  The second pin is also used
    by the firmware to store the customizable 56-byte logical LED lookup table.

    Each lookup-table byte contains two logical pin indexes:
     - Bits 7:4: logical pin index driven high
     - Bits 3:0: logical pin index driven low

    The class inherits SerialWombatAbstractScaledOutput.  Scaled-output functions
    are useful with DISPLAY_MODE_SCALED_SINGLE_LED and
    DISPLAY_MODE_SCALED_BARGRAPH.
    """

    DISPLAY_MODE_BITMAP = 0
    """!< Seven-byte protocol bitmap controls up to 56 LEDs. """
    DISPLAY_MODE_PUBLIC_DATA_BITMAP = 1
    """!< Controlling pin public data controls LEDs 0 through 15 as a bitfield. """
    DISPLAY_MODE_SCALED_SINGLE_LED = 2
    """!< Scaled-output value selects one logical LED index. """
    DISPLAY_MODE_SCALED_BARGRAPH = 3
    """!< Scaled-output value lights LEDs 0 through the selected index. """

    MAX_PINS = 8
    MAX_LEDS = 56
    BITMAP_BYTES = 7
    UNUSED_PIN = 0xFF
    UNUSED_LED = 0xFF

    def __init__(self, serial_wombat):
        """!
        @brief Constructor for the SerialWombatCharlieplex class.
        @param serial_wombat Serial Wombat chip on which the pin mode will run.
        """
        super().__init__(serial_wombat)

    def begin(self, pin0, pin1, pin2, pin3, pin4,
              pin5=UNUSED_PIN, pin6=UNUSED_PIN, pin7=UNUSED_PIN,
              displayMode=DISPLAY_MODE_BITMAP, scanPeriod_mS=0):
        """!
        @brief Initialize a Charlieplexed LED display.

        @param pin0 First physical Serial Wombat pin.  This is the controlling pin.
        @param pin1 Second physical Serial Wombat pin.  The firmware uses this pin's
        pin memory to store the customizable logical LED lookup table.
        @param pin2 Third physical Serial Wombat pin, or UNUSED_PIN.
        @param pin3 Fourth physical Serial Wombat pin, or UNUSED_PIN.
        @param pin4 Fifth physical Serial Wombat pin, or UNUSED_PIN.
        @param pin5 Sixth physical Serial Wombat pin, or UNUSED_PIN. Defaults to UNUSED_PIN.
        @param pin6 Seventh physical Serial Wombat pin, or UNUSED_PIN. Defaults to UNUSED_PIN.
        @param pin7 Eighth physical Serial Wombat pin, or UNUSED_PIN. Defaults to UNUSED_PIN.
        @param displayMode Selects bitmap, public-data bitmap, single-LED, or bargraph operation.
        @param scanPeriod_mS Minimum number of approximately 1 ms execution frames between
        the starts of consecutive scans. Zero adds no blank padding. The documented useful
        range is 0 through 56.
        @return 0 or a positive value if successful, otherwise a negative error code.

        The number of Charlieplex pins is calculated by counting pin parameters from pin0
        through the first UNUSED_PIN value. Pin parameters after the first UNUSED_PIN are
        ignored by the firmware.
        """
        pins = [pin0, pin1, pin2, pin3, pin4, pin5, pin6, pin7]

        numberOfPins = self.MAX_PINS
        for i in range(self.MAX_PINS):
            if pins[i] == self.UNUSED_PIN:
                numberOfPins = i
                break

        self._pin = pin0
        self._pinMode = SerialWombat.SerialWombatPinMode_t.PIN_MODE_CHARLIEPLEX

        tx0 = bytearray([
            SerialWombat.SerialWombatCommands.CONFIGURE_PIN_MODE0,
            self._pin,
            self._pinMode,
            numberOfPins,
            int(displayMode),
            scanPeriod_mS,
            pin1,
            pin2
        ])

        result, rx = self._sw.sendPacket(tx0)
        if result < 0:
            return result

        tx1 = bytearray([
            SerialWombat.SerialWombatCommands.CONFIGURE_PIN_MODE1,
            self._pin,
            self._pinMode,
            pin3,
            pin4,
            pin5,
            pin6,
            pin7
        ])

        result, rx = self._sw.sendPacket(tx1)
        return result

    def writeLEDArray(self, ledArray):
        """!
        @brief Write the complete LED bitmap from an array of bytes.

        @param ledArray Array of seven bytes in little-endian bit order. Bit 0 of
        byte 0 controls logical LED 0; bit 7 of byte 6 controls logical LED 55.
        @return 0 or a positive value if successful, otherwise a negative error code.
        """
        tx2 = bytearray([
            SerialWombat.SerialWombatCommands.CONFIGURE_PIN_MODE2,
            self._pin,
            self._pinMode,
            ledArray[0],
            ledArray[1],
            ledArray[2],
            ledArray[3],
            ledArray[4]
        ])

        result, rx = self._sw.sendPacket(tx2)
        if result < 0:
            return result

        tx3 = bytearray([
            SerialWombat.SerialWombatCommands.CONFIGURE_PIN_MODE3,
            self._pin,
            self._pinMode,
            ledArray[5],
            ledArray[6],
            0x55,
            0x55,
            0x55
        ])

        result, rx = self._sw.sendPacket(tx3)
        return result

    def setLEDs(self, led0, led1=UNUSED_LED, led2=UNUSED_LED,
                led3=UNUSED_LED, led4=UNUSED_LED):
        """!
        @brief Set up to five logical LEDs in bitmap display mode.

        Each scalar argument is a logical LED index from 0 through 55. Use UNUSED_LED
        for an unused argument. The first argument may alternatively be a list, tuple,
        bytes, or bytearray. In that form, the second argument may specify the count;
        if omitted, the full array length is used, up to five entries.

        The firmware modifies its LED bitmap directly; no host-side bitmap copy is maintained.

        @param led0 First logical LED index to set, or an array of LED indexes.
        @param led1 Second logical LED index, UNUSED_LED, or count when led0 is an array.
        @param led2 Third logical LED index, or UNUSED_LED.
        @param led3 Fourth logical LED index, or UNUSED_LED.
        @param led4 Fifth logical LED index, or UNUSED_LED.
        @return 0 or a positive value if successful, otherwise a negative error code.
        """
        if isinstance(led0, (list, tuple, bytes, bytearray)):
            count = len(led0) if led1 == self.UNUSED_LED else int(led1)
            return self._writeLEDCommandArray(
                SerialWombat.SerialWombatCommands.CONFIGURE_PIN_MODE5,
                led0,
                count)

        return self._writeLEDCommand(
            SerialWombat.SerialWombatCommands.CONFIGURE_PIN_MODE5,
            led0, led1, led2, led3, led4)

    def clearLEDs(self, led0=None, led1=UNUSED_LED, led2=UNUSED_LED,
                  led3=UNUSED_LED, led4=UNUSED_LED):
        """!
        @brief Clear logical LEDs in bitmap display mode, or clear all LEDs.

        With no arguments, the complete seven-byte bitmap is cleared. With scalar
        arguments, up to five logical LED indexes from 0 through 55 are cleared. The
        first argument may alternatively be a list, tuple, bytes, or bytearray. In that
        form, the second argument may specify the count; if omitted, the full array
        length is used, up to five entries.

        @param led0 First logical LED index to clear, an array of LED indexes, or None
        to clear all LEDs.
        @param led1 Second logical LED index, UNUSED_LED, or count when led0 is an array.
        @param led2 Third logical LED index, or UNUSED_LED.
        @param led3 Fourth logical LED index, or UNUSED_LED.
        @param led4 Fifth logical LED index, or UNUSED_LED.
        @return 0 or a positive value if successful, otherwise a negative error code.
        """
        if led0 is None:
            ledArray = [0, 0, 0, 0, 0, 0, 0]
            return self.writeLEDArray(ledArray)

        if isinstance(led0, (list, tuple, bytes, bytearray)):
            count = len(led0) if led1 == self.UNUSED_LED else int(led1)
            return self._writeLEDCommandArray(
                SerialWombat.SerialWombatCommands.CONFIGURE_PIN_MODE6,
                led0,
                count)

        return self._writeLEDCommand(
            SerialWombat.SerialWombatCommands.CONFIGURE_PIN_MODE6,
            led0, led1, led2, led3, led4)

    def writeLookupEntries(self, firstLEDIndex, entry0, entry1, entry2, entry3):
        """!
        @brief Write four consecutive logical LED lookup entries.

        Each entry is encoded as high logical pin index in bits 7:4 and low logical
        pin index in bits 3:0. The firmware writes four entries per command.

        @param firstLEDIndex Logical LED index for entry0.
        @param entry0 Encoded mapping for firstLEDIndex.
        @param entry1 Encoded mapping for firstLEDIndex + 1.
        @param entry2 Encoded mapping for firstLEDIndex + 2.
        @param entry3 Encoded mapping for firstLEDIndex + 3.
        @return 0 or a positive value if successful, otherwise a negative error code.
        """
        tx = bytearray([
            SerialWombat.SerialWombatCommands.CONFIGURE_PIN_MODE4,
            self._pin,
            self._pinMode,
            firstLEDIndex,
            entry0,
            entry1,
            entry2,
            entry3
        ])
        result, rx = self._sw.sendPacket(tx)
        return result

    def writeLookupTable(self, lookupTable):
        """!
        @brief Write all 56 logical LED lookup entries.

        @param lookupTable Array of 56 encoded high/low logical pin pairs.
        @return 0 or a positive value if successful, otherwise a negative error code.
        """
        for firstLEDIndex in range(0, self.MAX_LEDS, 4):
            result = self.writeLookupEntries(
                firstLEDIndex,
                lookupTable[firstLEDIndex],
                lookupTable[firstLEDIndex + 1],
                lookupTable[firstLEDIndex + 2],
                lookupTable[firstLEDIndex + 3])

            if result < 0:
                return result
        return 0

    @staticmethod
    def encodePinPair(highPinIndex, lowPinIndex):
        """!
        @brief Encode a logical high pin and logical low pin into one lookup byte.
        @param highPinIndex Logical Charlieplex pin index driven high.
        @param lowPinIndex Logical Charlieplex pin index driven low.
        @return Encoded lookup-table byte.
        """
        return ((highPinIndex << 4) | (lowPinIndex & 0x0F)) & 0xFF

    def pin(self):
        """!
        @brief Fulfills a virtual function requirement of SerialWombatAbstractScaledOutput.
        @return Current controlling pin number.
        """
        return self._pin

    def swPinModeNumber(self):
        """!
        @brief Fulfills a virtual function requirement of SerialWombatAbstractScaledOutput.
        @return Current pin mode number.
        """
        return self._pinMode

    def _writeLEDCommand(self, command, led0, led1, led2, led3, led4):
        ledIndexes = [led0, led1, led2, led3, led4]

        for ledIndex in ledIndexes:
            if ledIndex != self.UNUSED_LED and ledIndex >= self.MAX_LEDS:
                return -1

        tx = bytearray([
            command,
            self._pin,
            self._pinMode,
            led0,
            led1,
            led2,
            led3,
            led4
        ])

        result, rx = self._sw.sendPacket(tx)
        return result

    def _writeLEDCommandArray(self, command, ledIndexes, count):
        if count > 5:
            return -1

        leds = [
            self.UNUSED_LED,
            self.UNUSED_LED,
            self.UNUSED_LED,
            self.UNUSED_LED,
            self.UNUSED_LED
        ]

        for i in range(count):
            if ledIndexes[i] >= self.MAX_LEDS:
                return -1
            leds[i] = ledIndexes[i]

        return self._writeLEDCommand(
            command,
            leds[0],
            leds[1],
            leds[2],
            leds[3],
            leds[4])
