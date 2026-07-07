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

"""! @file SerialWombatIRRx.py
"""

import SerialWombat
from SerialWombat import SW_LE16
from SerialWombatPin import SerialWombatPin
from ArduinoFunctions import millis

COMMAND = 0
ADDRESS = 1
DATACOUNT = 2

class SerialWombatIRRx(SerialWombatPin):
    def __init__(self, serial_wombat):
        SerialWombatPin.__init__(self, serial_wombat)
        self._pinMode = SerialWombat.SerialWombatPinMode_t.PIN_MODE_IRRX
        self.timeout = 5000

    def begin(self, pin, dataOutput = DATACOUNT, irMode = 0, useRepeat = True, activeState = SerialWombat.SerialWombatPinState_t.SW_LOW, publicDataTimeoutPeriod_mS = 1000, publicDataTimeoutValue = 0xFFFF, useAddressFilter = False, addressFilterValue = 0x1234):
        self._pin = pin
        self._pinMode = SerialWombat.SerialWombatPinMode_t.PIN_MODE_IRRX
        tx = bytearray([200, self._pin, self._pinMode, irMode, 1 if useRepeat else 0, activeState]) + SW_LE16(addressFilterValue)
        result, rx = self._sw.sendPacket(tx)
        if result < 0:
            return result
        tx = bytearray([201, self._pin, self._pinMode]) + SW_LE16(publicDataTimeoutPeriod_mS) + SW_LE16(publicDataTimeoutValue) + bytearray([1 if useAddressFilter else 0])
        result, rx = self._sw.sendPacket(tx)
        if result < 0:
            return result
        tx = bytearray([205, self._pin, self._pinMode, dataOutput, 0x55, 0x55, 0x55, 0x55])
        result, rx = self._sw.sendPacket(tx)
        return result

    def available(self):
        tx = bytearray([201, self._pin, self._pinMode, 0, 0x55, 0x55, 0x55, 0x55])
        result, rx = self._sw.sendPacket(tx)
        return rx[4]

    def read(self):
        tx = bytearray([202, self._pin, self._pinMode, 1, 0x55, 0x55, 0x55, 0x55])
        result, rx = self._sw.sendPacket(tx)
        if result < 0:
            return -1
        if rx[3] != 0:
            return rx[4]
        return -1

    def flush(self):
        pass

    def peek(self):
        tx = bytearray([203, self._pin, self._pinMode, 0x55, 0x55, 0x55, 0x55, 0x55])
        result, rx = self._sw.sendPacket(tx)
        if result < 0:
            return -1
        if rx[4] > 0:
            return rx[5]
        return -1

    def write(self, data):
        return 1

    def availableForWrite(self):
        return 0

    def readBytes(self, length):
        buf = bytearray()
        timeoutMillis = millis() + self.timeout
        while length > 0 and timeoutMillis > millis():
            bytecount = 4
            if length < 4:
                bytecount = length
            tx = bytearray([202, self._pin, self._pinMode, bytecount, 0x55, 0x55, 0x55, 0x55])
            result, rx = self._sw.sendPacket(tx)
            if result < 0:
                return buf
            bytesAvailable = rx[3]
            if bytesAvailable == 0:
                continue
            timeoutMillis = millis() + self.timeout
            bytesReturned = bytecount
            if rx[3] < bytecount:
                bytesReturned = rx[3]
            for i in range(bytesReturned):
                buf.append(rx[i + 4])
                length -= 1
        return buf

    def setTimeout(self, timeout_mS):
        if timeout_mS == 0:
            self.timeout = 0x80000000
        else:
            self.timeout = timeout_mS

    def readAddress(self):
        tx = bytearray([204, self._pin, self._pinMode, 0x55, 0x55, 0x55, 0x55, 0x55])
        result, rx = self._sw.sendPacket(tx)
        return rx[3] + 256 * rx[4]

    def readDataCount(self):
        tx = bytearray([204, self._pin, self._pinMode, 0x55, 0x55, 0x55, 0x55, 0x55])
        result, rx = self._sw.sendPacket(tx)
        return rx[5] + 256 * rx[6]
