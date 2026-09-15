import SW18B_UnitTest_globals
import SerialWombatHSCounter
import SerialWombatPWM

try:
    from ArduinoFunctions import delay
    from ArduinoFunctions import millis
except ImportError:
    import time

    def delay(milliseconds):
        time.sleep(milliseconds / 1000.0)

    _start_time = time.monotonic()

    def millis():
        return int((time.monotonic() - _start_time) * 1000)


HSCounter = SerialWombatHSCounter.SerialWombatHSCounter(SW18B_UnitTest_globals.SW18AB_6B)


def hsCounterTest():
    SWPWM19 = SerialWombatPWM.SerialWombatPWM_4AB(SW18B_UnitTest_globals.SW4B_6E)
    SW18B_UnitTest_globals.resetAll()

    SW18B_UnitTest_globals.resetAll()
    SWPWM19.begin(1)
    SWPWM19.setFrequency_SW4AB(SWPWM19.SW4AB_PWMFrequency_31250_Hz)
    SWPWM19.writeDutyCycle(0x8000)
    HSCounter.begin(19)
    delay(1000)
    SW18B_UnitTest_globals.pulseRead(SW18B_UnitTest_globals.SW18AB_6B, 15)
    SW18B_UnitTest_globals.test_value("HSCounter_00", HSCounter.readFrequency(), 31250, 500, 0)
    SW18B_UnitTest_globals.test_value("HSCounter_00a", HSCounter.readPublicData(), 31250, 500, 0)

    startTime = millis()
    counts = HSCounter.readCounts(True)
    counts = HSCounter.readCounts(False)
    while millis() - startTime < 500:
        pass

    delay(0)
    counts1 = HSCounter.readCounts(False)

    while millis() - startTime < 1000:
        pass

    delay(0)
    counts2 = HSCounter.readCounts(False)
    SW18B_UnitTest_globals.test_value("HSCounter_01a", counts, 0, 500, 0)
    SW18B_UnitTest_globals.test_value("HSCounter_01", counts1, 15625, 500, 0)
    SW18B_UnitTest_globals.test_value("HSCounter_02", counts2, 31250, 500, 0)

    SW18B_UnitTest_globals.resetAll()
    SWPWM19.begin(1)
    SWPWM19.setFrequency_SW4AB(SWPWM19.SW4AB_PWMFrequency_125_Hz)
    SWPWM19.writeDutyCycle(0x8000)
    HSCounter.begin(19, HSCounter.PULSE_COUNT)
    delay(10000)
    SW18B_UnitTest_globals.test_value("HSCounter_10", HSCounter.readPublicData(), 1250, 50, 0)

    SW18B_UnitTest_globals.resetAll()
    SWPWM19.begin(1)
    SWPWM19.setFrequency_SW4AB(SWPWM19.SW4AB_PWMFrequency_125_Hz)
    SWPWM19.writeDutyCycle(0x8000)
    HSCounter.begin(19, HSCounter.PULSE_COUNT, 8000)
    delay(10000)
    SW18B_UnitTest_globals.test_value("HSCounter_20", HSCounter.readPublicData(), 1000, 50, 0)

    SW18B_UnitTest_globals.resetAll()
    SWPWM19.begin(1)
    SWPWM19.setFrequency_SW4AB(SWPWM19.SW4AB_PWMFrequency_31250_Hz)
    SWPWM19.writeDutyCycle(0x8000)
    HSCounter.begin(19, HSCounter.PULSE_COUNT, 100, 100)
    delay(10000)
    SW18B_UnitTest_globals.test_value("HSCounter_30", HSCounter.readPublicData(), 3125, 10, 0)

    SW18B_UnitTest_globals.resetAll()
