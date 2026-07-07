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

"""! @file PCB0042_LSD.py

Transport-neutral helper for PCB0042 LSD PWM boards.
"""

from SerialWombatPWM import SerialWombatPWM_18AB
from SerialWombatAnalogInput import SerialWombatAnalogInput_18AB

class PCB0042_LSD_PWM:
    def __init__(self, serial_wombat):
        self.sw = serial_wombat
        self.vinMeas = SerialWombatAnalogInput_18AB(serial_wombat)
        self.output0 = SerialWombatPWM_18AB(serial_wombat)
        self.output1 = SerialWombatPWM_18AB(serial_wombat)
        self.output2 = SerialWombatPWM_18AB(serial_wombat)
        self.output3 = SerialWombatPWM_18AB(serial_wombat)
        self.output4 = SerialWombatPWM_18AB(serial_wombat)
        self.output5 = SerialWombatPWM_18AB(serial_wombat)
        self.output6 = SerialWombatPWM_18AB(serial_wombat)
        self.output7 = SerialWombatPWM_18AB(serial_wombat)
        self.outputArray = [self.output0,self.output1,self.output2,self.output3,self.output4,self.output5,self.output6,self.output7]

    def begin(self, measureVin = False):
        for i,o in enumerate(self.outputArray):
            result = o.begin(i)
            if result is not None and result < 0:
                return result
        if measureVin:
            return self.vinMeas.begin(1)
        return 0

    def readVin_mV(self):
        return int(self.vinMeas.readAveraged_mV() * 11)
