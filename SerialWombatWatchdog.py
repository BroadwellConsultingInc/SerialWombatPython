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

"""! @file SerialWombatWatchdog.py
"""

import SerialWombat
from SerialWombat import SW_LE16
from SerialWombatPin import SerialWombatPin

class SerialWombatWatchdog(SerialWombatPin):
    def __init__(self, serial_wombat):
        SerialWombatPin.__init__(self, serial_wombat)
        self._pinMode = SerialWombat.SerialWombatPinMode_t.PIN_MODE_WATCHDOG
        self._resetStateTime = 10

    def begin(self, pin, normalState, resetState, timeout_mS, resetWombatAfterTimeout):
        self._pin = pin
        self._pinMode = SerialWombat.SerialWombatPinMode_t.PIN_MODE_WATCHDOG
        tx = bytearray([200, pin, self._pinMode, int(normalState), int(resetState)]) + SW_LE16(timeout_mS) + bytearray([1 if resetWombatAfterTimeout else 0])
        result, rx = self._sw.sendPacket(tx)
        if result < 0:
            return result
        tx1 = bytearray([201, pin, self._pinMode, 0, 0, 0, 0, 0x55])
        if not resetWombatAfterTimeout:
            tx1[5] = 0xFF
            tx1[6] = 0xFF
        result, rx = self._sw.sendPacket(tx1)
        return result

    def updateResetCountdown(self, time_mS):
        return self._sw.writePublicData(self._pin, time_mS)
