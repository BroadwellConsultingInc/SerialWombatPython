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

"""! @file SerialWombatSPI.py
"""

import SerialWombat
from SerialWombatPin import SerialWombatPin
from SerialWombatErrors import SW_ERROR_INVALID_PARAMETER_3

SW_MSBFIRST = 1
SW_SPI_MODE0 = 0x00
SW_SPI_MODE1 = 0x04
SW_SPI_MODE2 = 0x08
SW_SPI_MODE3 = 0x0C

class SerialWombatSPISettings:
    def __init__(self, clock = 0, bitOrder = SW_MSBFIRST, dataMode = SW_SPI_MODE0):
        self.clock = clock
        self.bitOrder = bitOrder
        self.dataMode = dataMode

class SerialWombatSPI(SerialWombatPin):
    def __init__(self, serial_wombat):
        SerialWombatPin.__init__(self, serial_wombat)
        self._pinMode = SerialWombat.SerialWombatPinMode_t.PIN_MODE_SPI

    def begin(self, pin, SPIModeparam = SW_SPI_MODE0, MOSIpin = 255, MISOpin = 255, CSpin = 255):
        self._pin = pin
        self._pinMode = SerialWombat.SerialWombatPinMode_t.PIN_MODE_SPI
        if SPIModeparam == SW_SPI_MODE1:
            SPIModeparam = 1
        elif SPIModeparam == SW_SPI_MODE3:
            SPIModeparam = 3
        elif SPIModeparam == SW_SPI_MODE0:
            SPIModeparam = 0
        elif SPIModeparam not in (0, 1, 3):
            return -SW_ERROR_INVALID_PARAMETER_3
        tx = bytearray([200, self._pin, self._pinMode, SPIModeparam, MOSIpin, MISOpin, CSpin, 0x55])
        result, rx = self._sw.sendPacket(tx)
        return result

    def beginTransaction(self, settings):
        pass

    def endTransaction(self):
        pass

    def transfer(self, data, csSaysStayLow = False):
        if isinstance(data, (bytes, bytearray, list)):
            b = bytearray(data)
            rx = bytearray(len(b))
            self.transferBuffer(b, rx, len(b), csSaysStayLow)
            return rx
        tx = bytearray([202 if csSaysStayLow else 201, self._pin, self._pinMode, 8, data & 0xFF, 0x55, 0x55, 0x55])
        result, rx = self._sw.sendPacket(tx)
        if result < 0:
            return 0
        return rx[4]

    def transfer16(self, data, csSaysStayLow = False):
        tx = bytearray([202 if csSaysStayLow else 201, self._pin, self._pinMode, 16, data & 0xFF, (data >> 8) & 0xFF, 0x55, 0x55])
        result, rx = self._sw.sendPacket(tx)
        if result < 0:
            return 0
        return rx[4] + 256 * rx[5]

    def transferBuffer(self, outBuffer, inBuffer, size, csSaysStayLow = False):
        outBuffer = bytearray(outBuffer)
        bytesSent = 0
        while bytesSent < size:
            bytesThisPacket = min(4, size - bytesSent)
            tx = bytearray([202 if (csSaysStayLow or (bytesSent + bytesThisPacket) < size) else 201, self._pin, self._pinMode, bytesThisPacket * 8])
            tx += outBuffer[bytesSent:bytesSent + bytesThisPacket]
            while len(tx) < 8:
                tx.append(0x55)
            result, rx = self._sw.sendPacket(tx)
            if result < 0:
                return result
            for i in range(bytesThisPacket):
                inBuffer[bytesSent + i] = rx[4 + i]
            bytesSent += bytesThisPacket
        return bytesSent

    def transferPacketUpTo32Bits(self, outBuffer, inBuffer, bitCount, csSaysStayLow = False):
        if bitCount > 32:
            return -1
        byteCount = (bitCount + 7) // 8
        tx = bytearray([202 if csSaysStayLow else 201, self._pin, self._pinMode, bitCount])
        tx += bytearray(outBuffer[:byteCount])
        while len(tx) < 8:
            tx.append(0x55)
        result, rx = self._sw.sendPacket(tx)
        if result < 0:
            return result
        for i in range(byteCount):
            inBuffer[i] = rx[4 + i]
        return result

    def transferPacket40Bits(self, outBuffer, inBuffer, csSaysStayLow = False):
        tx = bytearray([204 if csSaysStayLow else 203, self._pin, self._pinMode]) + bytearray(outBuffer[:5])
        result, rx = self._sw.sendPacket(tx)
        if result < 0:
            return result
        for i in range(5):
            inBuffer[i] = rx[3 + i]
        return result

    def setCSHigh(self):
        tx = bytearray([205, self._pin, self._pinMode, 0x55, 0x55, 0x55, 0x55, 0x55])
        result, rx = self._sw.sendPacket(tx)
        return result

    def usingInterrupt(self, interruptNumber):
        pass

    def notUsingInterrupt(self, interruptNumber):
        pass
