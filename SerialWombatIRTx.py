"""
Copyright 2020-2026 Broadwell Consulting Inc.

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

"""! @file SerialWombatIRTx.py
"""

import SerialWombat
from SerialWombat import SW_LE16
from SerialWombatPin import SerialWombatPin

class SerialWombatIRTx(SerialWombatPin):
    def __init__(self, serial_wombat):
        SerialWombatPin.__init__(self, serial_wombat)
        self._address = 0
        self._pinMode = SerialWombat.SerialWombatPinMode_t.PIN_MODE_IRTX

    def begin(self, pin, address, irMode = 0):
        self._pin = pin
        self._pinMode = SerialWombat.SerialWombatPinMode_t.PIN_MODE_IRTX
        self._address = address
        tx = bytearray([200, self._pin, self._pinMode, irMode, 0x55, 0x55, 0x55, 0x55])
        result, rx = self._sw.sendPacket(tx)
        return result

    def enableSW8b38KHzWP6(self):
        tx = bytearray([220, self._pin, self._pinMode, 0x55, 0x55, 0x55, 0x55, 0x55])
        result, rx = self._sw.sendPacket(tx)
        return result

    def sendMessage(self, command, address = -1, repeat = 0):
        if address >= 0:
            self._address = address
        peektx = bytearray([203, self._pin, self._pinMode, 0x55, 0x55, 0x55, 0x55, 0x55])
        result, peekrx = self._sw.sendPacket(peektx)
        if result < 0:
            return result
        if peekrx[3] >= 4:
            tx = bytearray([201, self._pin, self._pinMode, 4]) + SW_LE16(self._address) + bytearray([command & 0xFF, repeat & 0xFF])
            result, rx = self._sw.sendPacket(tx)
            if result < 0:
                return result
            return 1
        return -1

    def available(self):
        return 0

    def read(self):
        return -1

    def flush(self):
        pass

    def peek(self):
        return -1

    def write(self, data):
        return self.sendMessage(data)

    def availableForWrite(self):
        peektx = bytearray([203, self._pin, self._pinMode, 0x55, 0x55, 0x55, 0x55, 0x55])
        result, peekrx = self._sw.sendPacket(peektx)
        if result < 0:
            return 0
        return peekrx[3]

    def readBytes(self, length):
        return bytearray()

    def setTimeout(self, timeout_mS):
        pass
