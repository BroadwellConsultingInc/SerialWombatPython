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

"""! @file PCB0031_Grip.py

Transport-neutral helper for PCB0031 Grip boards.
"""

from ArduinoFunctions import delay
from SerialWombatAnalogInput import SerialWombatAnalogInput_18AB
from SerialWombatServo import SerialWombatServo_18AB
from SerialWombatErrors import SW_ERROR_PIN_NOT_CAPABLE

class GripACS712(SerialWombatAnalogInput_18AB):
    def __init__(self, serial_wombat):
        SerialWombatAnalogInput_18AB.__init__(self, serial_wombat)
        self.zeroCurrentCalibration = 32768

    def begin(self, pin):
        if pin < 4 or pin > 7:
            return -SW_ERROR_PIN_NOT_CAPABLE
        return SerialWombatAnalogInput_18AB.begin(self, pin)

    def calibrateIdleCurrent(self):
        self.zeroCurrentCalibration = self.readAveragedCounts()
        return self.zeroCurrentCalibration

    def readCurrent_mA(self):
        reading = self.readAveragedCounts() - self.zeroCurrentCalibration
        return int(reading * 1000 / 2425)

class GripServo(SerialWombatServo_18AB):
    def __init__(self, serial_wombat):
        SerialWombatServo_18AB.__init__(self, serial_wombat)
        self.sensor = GripACS712(serial_wombat)
        self.calibratedMinPosition = 0
        self.calibratedMaxPosition = 65535
        self.calibratedMinCurrent = 0
        self.calibratedMaxCurrent = 65535

    def begin(self, pin, reverse = False):
        self.attach(pin, reverse = reverse)
        return self.sensor.begin(pin + 4)

    def calibrateServoRange(self, expectedCurrentRise = 400, calibrationStartPosition = 0x8000):
        self.write(calibrationStartPosition // 256)
        delay(500)
        self.sensor.calibrateIdleCurrent()
        position = calibrationStartPosition
        self.calibratedMinCurrent = self.sensor.readAveragedCounts()
        while position > 0:
            position -= 2000
            self.write(position // 256)
            delay(80)
            current = self.sensor.readCurrent_mA()
            if current > expectedCurrentRise:
                break
        self.calibratedMinPosition = max(position, 0)
        position = calibrationStartPosition
        while position < 65535:
            position += 2000
            self.write(min(position, 65535) // 256)
            delay(80)
            current = self.sensor.readCurrent_mA()
            if current > expectedCurrentRise:
                break
        self.calibratedMaxPosition = min(position, 65535)
        self.calibratedMaxCurrent = self.sensor.readAveragedCounts()

    def grip(self, gripStrength = 0, slowIncrement = 100, fastSlowThreshold = 350, fastIncrement = 3500):
        if gripStrength == 0:
            gripStrength = 49152
        gripCurrent = (self.calibratedMaxCurrent - self.calibratedMinCurrent)
        gripCurrent = int(gripCurrent * gripStrength / 65535) + self.sensor.zeroCurrentCalibration
        self.writeScalingTargetValue(gripCurrent)
        self.writeRamp(slowIncrement, fastIncrement, fastSlowThreshold)
        self.writeOutputScaling(self.calibratedMinPosition, self.calibratedMaxPosition)
        self.writeScalingEnabled(True, self.sensor.pin())

    def release(self):
        self.writeOutputScaling(self.calibratedMinPosition, self.calibratedMaxPosition)
        self.writeScalingEnabled(True, self._pin)
        self.writePublicData(0)

    def objectPresent(self, divisor = 50):
        threshold = self.calibratedMinPosition + int((self.calibratedMaxPosition - self.calibratedMinPosition) / divisor)
        return self.readPublicData() > threshold

    def calibrateGripper(self, reverse = False, rangeConstant = 49152):
        self.begin(self._pin, reverse)
        minCurrent = 65535
        maxCurrent = 0
        minCurrentPosition = 0
        position = 0
        while position <= 65535:
            self.writePublicData(position)
            delay(50)
            current = self.sensor.readAveragedCounts()
            if current < minCurrent:
                minCurrent = current
                minCurrentPosition = position
            if current > maxCurrent:
                maxCurrent = current
            position += 2048
        self.calibratedMinCurrent = minCurrent
        self.calibratedMaxCurrent = maxCurrent
        self.sensor.zeroCurrentCalibration = minCurrent
        self.calibrateServoRange(int((maxCurrent - minCurrent) * rangeConstant / 65535), minCurrentPosition)

class PCB0031_Grip:
    def __init__(self, serial_wombat):
        self.sw = serial_wombat
        self.gs0 = GripServo(serial_wombat)
        self.gs1 = GripServo(serial_wombat)
        self.gs2 = GripServo(serial_wombat)
        self.gs3 = GripServo(serial_wombat)
        self.gsArray = [self.gs0,self.gs1,self.gs2,self.gs3]
        self.powerVoltage = SerialWombatAnalogInput_18AB(serial_wombat)
        self.pin3VoltageEnable = False

    def begin(self, pin3IsVoltage = False):
        self.pin3VoltageEnable = pin3IsVoltage
        for i in range(3):
            result = self.gsArray[i].begin(i)
            if result < 0:
                return result
        if not pin3IsVoltage:
            return self.gs3.begin(3)
        return self.powerVoltage.begin(3)

    def readPowerVoltage_mv(self):
        if self.pin3VoltageEnable:
            v = self.powerVoltage.readAveraged_mV()
            v = v * (8200 + 2000) / 2000
            return int(v)
        return 0
