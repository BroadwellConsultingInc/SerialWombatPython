import SW18B_UnitTest_globals
import SerialWombatHSClock

try:
    from ArduinoFunctions import delay
except ImportError:
    import time

    def delay(milliseconds):
        time.sleep(milliseconds / 1000.0)


HSClock = SerialWombatHSClock.SerialWombatHSClock(SW18B_UnitTest_globals.SW18AB_6B)


def hsClockTest():
    SW18B_UnitTest_globals.resetAll()
    HSClock.begin(15, 2000)
    SW18B_UnitTest_globals.initializePulseReaduS(SW18B_UnitTest_globals.SW18AB_6B, 15)
    delay(100)
    highTime = SW18B_UnitTest_globals.pulseRead(SW18B_UnitTest_globals.SW18AB_6B, 15)
    SW18B_UnitTest_globals.test_value("HSCLOCK_00", highTime, 250, 10, 0)  # Should be a 250 uS high time (500us period)

    SW18B_UnitTest_globals.resetAll()
