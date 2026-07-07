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

"""! @file PCB0046_HSD.py

Transport-neutral helper for PCB0046 HSD PWM boards.  Pass two already-initialized
SerialWombatChip instances: sw0 for channels 0-3 and sw1 for channels 4-7.
"""

from SerialWombatPWM import SerialWombatPWM_18AB
from SerialWombatAnalogInput import SerialWombatAnalogInput_18AB
from SerialWombatDigitalInput import SerialWombatDigitalInput_18AB
from SerialWombatDigitalOutput import SerialWombatDigitalOutput_18AB, LOW, HIGH

class PCB0046_HSD_PWM:
    def __init__(self, sw0, sw1):
        self.sw0 = sw0
        self.sw1 = sw1
        self.vinMeas = SerialWombatAnalogInput_18AB(sw1)
        self.currentSenseSelector1 = SerialWombatAnalogInput_18AB(sw1)
        self.currentSenseSelector2 = SerialWombatAnalogInput_18AB(sw1)
        self.diagEn = SerialWombatDigitalOutput_18AB(sw1)
        self.selL = SerialWombatDigitalOutput_18AB(sw1)
        self.selH = SerialWombatDigitalOutput_18AB(sw1)
        self.fault0to3 = SerialWombatDigitalInput_18AB(sw1)
        self.fault4to7 = SerialWombatDigitalInput_18AB(sw1)
        self.output0 = SerialWombatPWM_18AB(sw0)
        self.output1 = SerialWombatPWM_18AB(sw0)
        self.output2 = SerialWombatPWM_18AB(sw0)
        self.output3 = SerialWombatPWM_18AB(sw0)
        self.output4 = SerialWombatPWM_18AB(sw0)
        self.output5 = SerialWombatPWM_18AB(sw0)
        self.output6 = SerialWombatPWM_18AB(sw0)
        self.output7 = SerialWombatPWM_18AB(sw0)
        self.outputArray = [self.output0,self.output1,self.output2,self.output3,self.output4,self.output5,self.output6,self.output7]
        self.selectedFeedbackChannel = 0

    def begin(self):
        self.vinMeas.begin(1)
        self.currentSenseSelector1.begin(4)
        self.currentSenseSelector2.begin(3)
        self.diagEn.begin(2, HIGH)
        self.selL.begin(0, LOW)
        self.selH.begin(6, LOW)
        self.fault0to3.begin(7, True)
        self.fault4to7.begin(5, True)
        for i,o in enumerate(self.outputArray):
            o.begin(i)
            try:
                o.writeFrequency_Hz(800)
            except Exception:
                pass
        return 0

    def selectCurrentFeedbackChannel(self, ch):
        if ch in (0,4):
            self.selH.high(); self.selL.high()
        elif ch in (1,5):
            self.selH.high(); self.selL.low()
        elif ch in (2,6):
            self.selH.low(); self.selL.high()
        elif ch in (3,7):
            self.selH.low(); self.selL.low()
        else:
            return -1
        self.selectedFeedbackChannel = ch
        return 0

    def readCurrentFeedbackAverage_mA(self):
        if self.selectedFeedbackChannel >= 4:
            mV = self.currentSenseSelector1.readAveraged_mV()
        else:
            mV = self.currentSenseSelector2.readAveraged_mV()
        return int(mV * 3)

    def readCurrentFeedbackInstant_mA(self):
        if self.selectedFeedbackChannel >= 4:
            mV = self.currentSenseSelector1.readVoltage_mV()
        else:
            mV = self.currentSenseSelector2.readVoltage_mV()
        return int(mV * 3)

    def readChip4to7IsFaulted(self):
        return self.fault4to7.readPublicData() == 0

    def readChip0to3IsFaulted(self):
        return self.fault0to3.readPublicData() == 0

    def readVin_mV(self):
        return int(self.vinMeas.readAveraged_mV() * 11)
