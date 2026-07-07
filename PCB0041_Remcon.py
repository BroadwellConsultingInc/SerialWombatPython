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

"""! @file PCB0041_Remcon.py

Transport-neutral helper for PCB0041 REMCON boards.
"""

from SerialWombatIRRx import SerialWombatIRRx
from SerialWombatIRTx import SerialWombatIRTx
from SerialWombatBlink import SerialWombatBlink

class PCB0041_Remcon:
    def __init__(self, serial_wombat):
        self.sw = serial_wombat
        self.irrx = SerialWombatIRRx(serial_wombat)
        self.irtx = SerialWombatIRTx(serial_wombat)
        self.blink = SerialWombatBlink(serial_wombat)

    def begin(self, irTxAddress = 0x1234, enableBlink = True):
        result = self.irrx.begin(3)
        if result < 0: return result
        result = self.irtx.begin(7, irTxAddress)
        if result < 0: return result
        result = self.irtx.enableSW8b38KHzWP6()
        if result < 0: return result
        if enableBlink:
            result = self.blink.begin(1, 3)
            if result < 0: return result
        return 0
