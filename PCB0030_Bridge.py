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

"""! @file PCB0030_Bridge.py

Transport-neutral helper for PCB0030 Bridge boards.
"""

from SerialWombatHBridge import SerialWombatHBridge, SerialWombatHBridgeDriverMode
from SerialWombatAnalogInput import SerialWombatAnalogInput_18AB

class PCB0030_Bridge:
    def __init__(self, serial_wombat):
        self.sw = serial_wombat
        self.hBridge45 = SerialWombatHBridge(serial_wombat)
        self.hBridge67 = SerialWombatHBridge(serial_wombat)
        self.powerVoltage = SerialWombatAnalogInput_18AB(serial_wombat)
        self.pin3VoltageEnable = False

    def begin(self, pin3IsVoltage = False, pwmFrequency = 1000):
        self.pin3VoltageEnable = pin3IsVoltage
        self.hBridge45.begin(4, 5, pwmFrequency, SerialWombatHBridgeDriverMode.HBRIDGE_OFF_BOTH_HIGH)
        self.hBridge67.begin(6, 7, pwmFrequency, SerialWombatHBridgeDriverMode.HBRIDGE_OFF_BOTH_HIGH)
        if pin3IsVoltage:
            return self.powerVoltage.begin(3)
        return 0

    def readPowerVoltage_mv(self):
        if self.pin3VoltageEnable:
            v = self.powerVoltage.readAveraged_mV()
            v = v * (8200 + 2000) / 2000
            return int(v)
        return 0
