import SW18B_UnitTest_globals
import SerialWombatFrequencyOutput

try:
    from ArduinoFunctions import delay
except ImportError:
    import time

    def delay(milliseconds):
        time.sleep(milliseconds / 1000.0)


SWFrequencyOutput18 = SerialWombatFrequencyOutput.SerialWombatFrequencyOutput_18AB(SW18B_UnitTest_globals.SW18AB_6B)
SWFrequencyOutput8 = SerialWombatFrequencyOutput.SerialWombatFrequencyOutput_18AB(SW18B_UnitTest_globals.SW8B_68)


def frequencyOutputTest(sw, pin):
    fo = None
    if sw is SW18B_UnitTest_globals.SW18AB_6B:
        fo = SWFrequencyOutput18
    elif sw is SW18B_UnitTest_globals.SW8B_68:
        fo = SWFrequencyOutput8

    SW18B_UnitTest_globals.resetAll()
    fo.begin(pin, maxFrequency_Hz=2000, lowFrequency=False, dutyCycle=0x8000)
    SW18B_UnitTest_globals.initializePulseReaduS(sw, pin)
    delay(100)
    highTime = SW18B_UnitTest_globals.pulseRead(sw, pin)
    SW18B_UnitTest_globals.test_value("FreqOutput_00", highTime, 250, 10, 2)  # Should be a 250 uS high time (500us period)

    fo.writePublicData(1000)  # 1000 Hz
    delay(100)
    highTime = SW18B_UnitTest_globals.pulseRead(sw, pin)
    SW18B_UnitTest_globals.test_value("FreqOutput_01", highTime, 500, 10, 2)  # Should be a 500 uS high time (1000us period)

    SW18B_UnitTest_globals.resetAll()
    fo.begin(pin, maxFrequency_Hz=14400, lowFrequency=False, dutyCycle=0x8000)
    fo.writePublicData(14400)  # 25000 Hz
    SW18B_UnitTest_globals.initializePulseReaduS(sw, pin)
    delay(100)
    highTime = SW18B_UnitTest_globals.pulseRead(sw, pin)
    SW18B_UnitTest_globals.test_value("FreqOutput_02", highTime, 34, 5, 2)  # Should be a 20 uS high time (68us period)

    SW18B_UnitTest_globals.resetAll()
    fo.begin(pin, maxFrequency_Hz=14400, lowFrequency=False, dutyCycle=0xC000)  # 75% duty cycle
    fo.writePublicData(14400)  # 25000 Hz
    SW18B_UnitTest_globals.initializePulseReaduS(sw, pin)
    delay(100)
    highTime = SW18B_UnitTest_globals.pulseRead(sw, pin)
    SW18B_UnitTest_globals.test_value("FreqOutput_03", highTime, 51, 5, 2)  # Should be a 30 uS high time (68uS period)
