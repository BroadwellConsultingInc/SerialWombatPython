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

"""! @file SerialWombatProtectedOutput.py
"""

import SerialWombat
from SerialWombat import SW_LE16
from SerialWombatPin import SerialWombatPin

PO_FAULT_IF_NOT_EQUAL = 0
PO_FAULT_IF_FEEDBACK_LESS_THAN_EXPECTED = 1
PO_FAULT_IF_FEEDBACK_GREATER_THAN_EXPECTED = 2

SW_LOW = SerialWombat.SerialWombatPinState_t.SW_LOW
SW_HIGH = SerialWombat.SerialWombatPinState_t.SW_HIGH
SW_INPUT = SerialWombat.SerialWombatPinState_t.SW_INPUT
LOW = 0
HIGH = 1

class SerialWombatProtectedOutput(SerialWombatPin):
    def __init__(self, serial_wombat):
        SerialWombatPin.__init__(self, serial_wombat)
        self._monitoredPin = 255
        self._debounceTime = 0
        self._pinMode = SerialWombat.SerialWombatPinMode_t.PIN_MODE_PROTECTED_OUTPUT

    def begin(self, pin, monitoredPin):
        self._pin = pin
        self._monitoredPin = monitoredPin
        self._pinMode = SerialWombat.SerialWombatPinMode_t.PIN_MODE_PROTECTED_OUTPUT

    def configure(self, compareMode, compareValue, debounceTime, activeState, safeState):
        self._debounceTime = debounceTime
        tx = bytearray([200, self._pin, self._pinMode]) + SW_LE16(compareValue) + bytearray([debounceTime, self._monitoredPin, safeState])
        result, rx = self._sw.sendPacket(tx)
        if result < 0:
            return result
        tx = bytearray([201, self._pin, self._pinMode, compareMode, activeState, 0x55, 0x55, 0x55])
        result, rx = self._sw.sendPacket(tx)
        return result

    def isInSafeState(self):
        return self._sw.readPublicData(self._pin) >= self._debounceTime

    def makeInput(self):
        return self.configure(PO_FAULT_IF_FEEDBACK_LESS_THAN_EXPECTED, 0, 100, SW_INPUT, SW_INPUT)

    def digitalWrite(self, state):
        if state == HIGH:
            return self.configure(PO_FAULT_IF_FEEDBACK_LESS_THAN_EXPECTED, 0, 100, SW_HIGH, SW_HIGH)
        else:
            return self.configure(PO_FAULT_IF_FEEDBACK_GREATER_THAN_EXPECTED, 65534, 100, SW_LOW, SW_LOW)
