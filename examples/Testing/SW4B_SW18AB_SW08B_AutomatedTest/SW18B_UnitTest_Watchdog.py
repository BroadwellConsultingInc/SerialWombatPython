import SW18B_UnitTest_globals
import SerialWombatWatchdog

try:
    from ArduinoFunctions import delay
except ImportError:
    import time

    def delay(milliseconds):
        time.sleep(milliseconds / 1000.0)


SW_LOW = 0
SW_HIGH = 1

swwd = SerialWombatWatchdog.SerialWombatWatchdog(
    SW18B_UnitTest_globals.SW18AB_6B
)


def watchdogTest18AB():
    for pin in range(11, SW18B_UnitTest_globals.NUM_TEST_PINS):
        SW18B_UnitTest_globals.resetAll()
        SW18B_UnitTest_globals.initializePulseReaduS(
            SW18B_UnitTest_globals.SW18AB_6B,
            pin,
        )

        swwd.begin(pin, SW_LOW, SW_LOW, 40, False)
        swwd.begin(pin, SW_HIGH, SW_LOW, 40, False)
        delay(200)

        duration = SW18B_UnitTest_globals.pulseRead(
            SW18B_UnitTest_globals.SW18AB_6B,
            pin,
        )
        if duration > 30000 and duration < 50000:
            SW18B_UnitTest_globals.pass_(pin)
        else:
            SW18B_UnitTest_globals.fail(pin)
            # print(f"pin {pin}: expected {100}, got {duration}")
