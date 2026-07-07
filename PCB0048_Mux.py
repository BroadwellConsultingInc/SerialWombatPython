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

"""! @file PCB0048_Mux.py

Transport-neutral helper for PCB0048 Mux boards.  Pass an already-initialized
SerialWombatChip instance to the constructor.
"""

from SerialWombatDigitalOutput import SerialWombatDigitalOutput_18AB, LOW, HIGH

class PCB0048_Mux:
    def __init__(self, serial_wombat):
        self.sw = serial_wombat
        self.bus1 = SerialWombatDigitalOutput_18AB(serial_wombat)
        self.bus2 = SerialWombatDigitalOutput_18AB(serial_wombat)
        self.bus3 = SerialWombatDigitalOutput_18AB(serial_wombat)
        self.bus7 = SerialWombatDigitalOutput_18AB(serial_wombat)

    def begin(self):
        result = self.bus1.begin(1, LOW)
        if result < 0: return result
        result = self.bus2.begin(2, LOW)
        if result < 0: return result
        result = self.bus3.begin(3, LOW)
        if result < 0: return result
        return self.bus7.begin(7, LOW)

    def enableBus1Only(self):
        self.sw.writePublicData(2, 0, 3, 0)
        self.sw.writePublicData(7, 0)
        return self.sw.writePublicData(1, 0xFFFF)

    def enableBus2Only(self):
        self.sw.writePublicData(1, 0, 3, 0)
        self.sw.writePublicData(7, 0)
        return self.sw.writePublicData(2, 0xFFFF)

    def enableBus3Only(self):
        self.sw.writePublicData(1, 0, 2, 0)
        self.sw.writePublicData(7, 0)
        return self.sw.writePublicData(3, 0xFFFF)

    def enableBus7Only(self):
        self.sw.writePublicData(1, 0, 2, 0)
        self.sw.writePublicData(3, 0)
        return self.sw.writePublicData(7, 0xFFFF)
