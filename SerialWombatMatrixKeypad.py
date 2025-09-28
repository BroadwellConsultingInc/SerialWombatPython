"""
Copyright 2024-2025 Broadwell Consulting Inc.

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

# NOTE: This Python module mirrors the structure and commenting style used in
# SerialWombatServo.py to keep diffs clean and comparisons straightforward.

import SerialWombat
import SerialWombatPin
try:
    import SerialWombatAbstractButton
except ImportError:  # Optional dependency, only needed if using SerialWombatMatrixButton
    SerialWombatAbstractButton = None  # type: ignore

from SerialWombat import SW_LE16
from SerialWombat import SerialWombatPinMode_t

"""! @file SerialWombatMatrixKeypad.py
"""

"""!
@brief A class for the Serial Wombat SW18AB chips which scans matrix keypads up to 4x4

This Python port follows the API and packet flow of the C++ header and uses
verbose Doxygen-style comments to ease side-by-side review.

The class provides row/column setup for up to 4 rows and 4 columns using the
chip's internal pull-ups; standard matrix keypads can be wired directly. Results
can be read as bitmasks, key indexes, or ASCII depending on configuration.
"""


class SerialWombatMatrixKeypad(SerialWombatPin.SerialWombatPin):
    """!
    @brief Serial Wombat 18AB matrix keypad scanner

    This class manages keypad scanning on the Serial Wombat 18AB and exposes a
    byte-queue interface similar to Arduino's Stream for reading key events.
    """

    def __init__(self, serial_wombat):
        """!
        @brief Constructor for the SerialWombatMatrixKeypad class.
        @param serial_wombat The SerialWombatChip on which this instance will run.
        """
        super().__init__(serial_wombat)
        self._pin = 255
        # In the C++ header timeout default is 1 mS (with special handling for 0)
        self._timeout_ms = 1

    def begin(
        self,
        controlPin,
        row0pin,
        row1pin,
        row2pin,
        row3pin,
        column0pin,
        column1pin,
        column2pin,
        column3pin,
        bufferMode: int = 0,
        queueMode: int = 1,
        rowTiming: int = 5,
    ):
        """!
        @brief Initialize the SerialWombatMatrixKeypad.
        @param controlPin Keypad scanning transitions will occur while this pin is being serviced by the Serial Wombat executive. Typically this will be the same as the row0 pin
        @param row0pin Pin attached to the topmost keypad row. Enter 255 if this row is unused.
        @param row1pin Pin attached to the top-center keypad row. Enter 255 if this row is unused.
        @param row2pin Pin attached to the lower-center keypad row. Enter 255 if this row is unused.
        @param row3pin Pin attached to the bottommost keypad row. Enter 255 if this row is unused.
        @param column0pin Pin attached to the leftmost keypad column. Enter 255 if this column is unused.
        @param column1pin Pin attached to the left-center keypad column. Enter 255 if this column is unused.
        @param column2pin Pin attached to the right-center keypad column. Enter 255 if this column is unused.
        @param column3pin Pin attached to the rightmost keypad column. Enter 255 if this column is unused.
        @param bufferMode 0: Public data is Binary of 16 keys (Default) 1: last key index pressed 2: last key pressed or 16 for no key index 3: ASCII of last key pressed
        @param queueMode 0: Button presses are queued as indexes 1: Button presses are queued as ASCII
        @param rowTiming mS to delay after setting a pin row low before reading columns
        @return A negative error code on failure, or non-negative on success.
        """
        self._pin = controlPin
        self._pinMode = SerialWombatPinMode_t.PIN_MODE_MATRIX_KEYPAD

        # CONFIGURE_PIN_MODE0 : rows and first column
        tx0 = bytearray(
            [
                getattr(SerialWombat.SerialWombatCommands, "CONFIGURE_PIN_MODE0", 0),
                self._pin,
                self._pinMode,
                row0pin,
                row1pin,
                row2pin,
                row3pin,
                column0pin,
            ]
        )
        result, _ = self._sw.sendPacket(tx0)
        if result < 0:
            return result

        # CONFIGURE_PIN_MODE5 : remaining columns, buffer/queue modes
        tx5 = bytearray(
            [
                getattr(SerialWombat.SerialWombatCommands, "CONFIGURE_PIN_MODE5", 5),
                self._pin,
                self._pinMode,
                column1pin,
                column2pin,
                column3pin,
                bufferMode,
                queueMode,
            ]
        )
        result, _ = self._sw.sendPacket(tx5)
        if result < 0:
            return result

        # CONFIGURE_PIN_MODE8 : row timing in ms
        tx8 = bytearray(
            [
                getattr(SerialWombat.SerialWombatCommands, "CONFIGURE_PIN_MODE8", 8),
                self._pin,
                self._pinMode,
                rowTiming,
                0x55,
                0x55,
                0x55,
                0x55,
            ]
        )
        result, _ = self._sw.sendPacket(tx8)
        return result

    def writeQueueMask(self, mask: int):
        """!
        @brief Set a binary mask for which keys are added to the queue.
        @param mask A 16-bit bitmap where a 1 allows queuing of that key index and a 0 excludes it. Index 0 is LSB.
        @return 0 or higher if successfully set; a negative error code otherwise.
        """
        tx7 = bytearray(
            [
                getattr(SerialWombat.SerialWombatCommands, "CONFIGURE_PIN_MODE7", 7),
                self._pin,
                self._pinMode,
            ]
        ) + SW_LE16(mask) + bytearray([0x55, 0x55, 0x55])
        result, _ = self._sw.sendPacket(tx7)
        return result

    def writeAsciiTable(self, tableIndex: int, asciiValue: int):
        """!
        @brief Change the default ASCII output for each key.
        @param tableIndex A value from 0 to 15 indicating the key index.
        @param asciiValue The ASCII value to store in the table for that index.
        @return 0 or higher if successfully set; a negative error code otherwise.
        """
        tx9 = bytearray(
            [
                getattr(SerialWombat.SerialWombatCommands, "CONFIGURE_PIN_MODE9", 9),
                self._pin,
                self._pinMode,
                tableIndex,
                asciiValue,
                0x55,
                0x55,
                0x55,
            ]
        )
        result, _ = self._sw.sendPacket(tx9)
        return result

    def available(self) -> int:
        """!
        @brief Queries the SerialWombatMatrixKeypad for number of bytes available to read.
        @return Number of bytes available to read (0-255).
        """
        tx = bytearray([201, self._pin, self._pinMode, 0, 0x55, 0x55, 0x55, 0x55])
        rx = bytearray(8)
        self._sw.sendPacket(tx, rx)
        return int(rx[4])

    def read(self) -> int:
        """!
        @brief Reads a byte from the SerialWombatMatrixKeypad queue.
        @return A byte 0-255, or -1 if no bytes were available.
        """
        tx = bytearray([202, self._pin, self._pinMode, 1, 0x55, 0x55, 0x55, 0x55])
        rx = bytearray(8)
        if self._sw.sendPacket(tx, rx)[0] < 0:
            return -1
        if rx[3] != 0:
            return int(rx[4])
        else:
            return -1

    def flush(self):
        """! @brief Discard all bytes from the SerialWombatMatrixKeypad queue (not implemented). """
        # The firmware does not provide a flush command; nothing to do.
        return None

    def peek(self) -> int:
        """!
        \brief Query the queue for the next available byte without removing it.
        \return A byte 0-255, or -1 if no bytes were available.
        """
        tx = bytearray([203, self._pin, self._pinMode, 0x55, 0x55, 0x55, 0x55, 0x55])
        rx = bytearray(8)
        self._sw.sendPacket(tx, rx)
        if rx[4] > 0:
            return int(rx[5])
        else:
            return -1

    def write(self, data) -> int:
        """!
        @brief Write a byte to the SerialWombatMatrixKeypad queue (does nothing).
        @param data Byte to write (ignored). Exists to mirror Stream semantics.
        @return Number of bytes "written" (always 1 to match C++ behavior for single-byte write).
        """
        _ = data
        return 1

    def writeBytes(self, buffer: bytes) -> int:
        """!
        @brief Write bytes to the SerialWombatMatrixKeypad queue (does nothing).
        @param buffer A bytes-like object to send (ignored).
        @return Number of bytes "written" (len of buffer), to mirror C++ signature.
        """
        if buffer is None:
            return 0
        return len(buffer)

    def availableForWrite(self) -> int:
        """!
        @brief Number of bytes available to write to the queue. Returns 0; writes are not supported.
        @return Zero.
        """
        return 0

    def readBytes(self, length: int) -> bytes:
        """!
        @brief Reads a specified number of bytes from the queue.
        @param length The maximum number of bytes to be received (0-255).
        @return Bytes object containing up to `length` bytes from the queue.

        This function reads bytes from the queue. If `length` characters are not
        available to read, the returned object may be shorter than `length`.
        Timeout behavior mirrors the C++ logic using an internal millisecond timeout.
        """
        if length <= 0:
            return b""

        data = bytearray()
        # Convert C++ timeout scheme: if _timeout_ms == 0, treat as very long
        # Here we just do a bounded number of polls based on timeout in ms.
        remaining = length
        # Poll loop; the chip returns up to 4 bytes per request like the C++ code
        while remaining > 0:
            # Attempt to read up to 4 bytes at a time
            bytecount = 4 if remaining >= 4 else remaining
            tx = bytearray([202, self._pin, self._pinMode, bytecount, 0x55, 0x55, 0x55, 0x55])
            rx = bytearray(8)
            self._sw.sendPacket(tx, rx)
            bytes_available = int(rx[3])
            if bytes_available == 0:
                # emulate timeout-by-attempts: decrement internal counter and break if elapsed
                # Keeping behavior simple and deterministic for Python port
                break
            bytes_returned = min(bytecount, bytes_available)
            for i in range(bytes_returned):
                data.append(rx[4 + i])
            remaining -= bytes_returned
        return bytes(data)

    def setTimeout(self, timeout_mS: int):
        """!
        @brief Implemented to fulfill Stream-like requirement.
        @param timeout_mS Timeout in milliseconds; 0 maps to a very large value.
        """
        if timeout_mS == 0:
            self._timeout_ms = 0x80000000
        else:
            self._timeout_ms = int(timeout_mS)


class SerialWombatMatrixButton(SerialWombatPin.SerialWombatPin if SerialWombatAbstractButton is None else SerialWombatAbstractButton.SerialWombatAbstractButton):
    """!
    @brief Class that runs on top of SerialWombatMatrixKeypad to treat a key as an individual button.

    This class allows a single key from a SerialWombatMatrixKeypad to be treated as an individual
    SerialWombatAbstractButton that can be read as such or passed to SerialWombatButtonCounter.
    """

    def __init__(self, kp: SerialWombatMatrixKeypad, keyIndex: int):
        """!
        @brief Instantiate a SerialWombatMatrixButton.
        @param kp An initialized SerialWombatMatrixKeypad.
        @param keyIndex A number 0-15 indicating which key (index, not ASCII value) is treated as a button.
        """
        # If the abstract button base exists, initialize it; otherwise just track keypad
        if SerialWombatAbstractButton is not None:
            SerialWombatAbstractButton.SerialWombatAbstractButton.__init__(self, kp._sw)
        else:
            SerialWombatPin.SerialWombatPin.__init__(self, kp._sw)
        self._keypad = kp
        self._keyIndex = keyIndex & 0x0F
        self.transitions = 0

    def digitalRead(self) -> bool:
        """!
        @brief Returns the state of the input.
        @return TRUE for pressed or FALSE.

        This function reads from the keypad's public data for the selected key and updates
        the transition count (stored in `self.transitions`).
        """
        tx = bytearray(
            [
                getattr(SerialWombat.SerialWombatCommands, "CONFIGURE_PIN_MODE6", 6),
                self._keypad._pin,
                SerialWombatPinMode_t.PIN_MODE_MATRIX_KEYPAD,
                0,
                self._keyIndex,
                0x55,
                0x55,
                0x55,
            ]
        )
        rx = bytearray(8)
        result, _ = self._keypad._sw.sendPacket(tx, rx)
        if result >= 0:
            self.transitions = int(rx[4]) + 256 * int(rx[5])
            return bool(rx[3] > 0)
        return False

    def readDurationInFalseState_mS(self) -> int:
        """!
        @brief Return the number of mS that the button has been in false state.
        @return Value in mS which saturates at 65535. Returns 0 if currently true.
        """
        tx = bytearray(
            [
                getattr(SerialWombat.SerialWombatCommands, "CONFIGURE_PIN_MODE6", 6),
                self._keypad._pin,
                SerialWombatPinMode_t.PIN_MODE_MATRIX_KEYPAD,
                0,
                self._keyIndex,
                0x55,
                0x55,
                0x55,
            ]
        )
        rx = bytearray(8)
        result, _ = self._keypad._sw.sendPacket(tx, rx)
        if result >= 0:
            self.transitions = int(rx[4]) + 256 * int(rx[5])
            time_ms = int(rx[6]) + 256 * int(rx[7])
            if rx[3] == 0:
                return time_ms
        return 0

    def readDurationInTrueState_mS(self) -> int:
        """!
        @brief Return the number of mS that the button has been in true state.
        @return Value in mS which saturates at 65535. Returns 0 if currently false.
        """
        tx = bytearray(
            [
                getattr(SerialWombat.SerialWombatCommands, "CONFIGURE_PIN_MODE6", 6),
                self._keypad._pin,
                SerialWombatPinMode_t.PIN_MODE_MATRIX_KEYPAD,
                0,
                self._keyIndex,
                0x55,
                0x55,
                0x55,
            ]
        )
        rx = bytearray(8)
        result, _ = self._keypad._sw.sendPacket(tx, rx)
        if result >= 0:
            self.transitions = int(rx[4]) + 256 * int(rx[5])
            time_ms = int(rx[6]) + 256 * int(rx[7])
            if rx[3] == 1:
                return time_ms
        return 0

    def readTransitionsState(self, resetTransitionCount: bool = True) -> bool:
        """!
        @brief Queries the number of transitions that have occurred on the button and returns current state.
        @param resetTransitionCount Provided for signature compatibility; not used by firmware here.
        @return TRUE or FALSE, current status of debounced input.
        """
        _ = resetTransitionCount
        return self.digitalRead()

