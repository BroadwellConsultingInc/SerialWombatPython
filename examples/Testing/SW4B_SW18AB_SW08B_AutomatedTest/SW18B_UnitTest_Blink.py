import SW18B_UnitTest_globals
import SerialWombatBlink
import SerialWombatPin

try:
    from ArduinoFunctions import delay
except ImportError:
    import time

    def delay(milliseconds):
        time.sleep(milliseconds / 1000.0)


OUTPUT = 1


def blinkTest(sw, blinkPin, sourcePin):
    SW18B_UnitTest_globals.resetAll()

    swBlink = SerialWombatBlink.SerialWombatBlink(sw)
    inputPWM = SerialWombatPin.SerialWombatPin(sw)
    inputPWM._pin = sourcePin

    inputPWM.pinMode(OUTPUT)
    inputPWM.writePublicData(0)

    swBlink.begin(blinkPin, sourcePin)
    SW18B_UnitTest_globals.initializePulseReaduS(sw, blinkPin)

    inputPWM.writePublicData(0x8000)
    delay(50)

    SW18B_UnitTest_globals.test_value(
        "BLINK_01",
        SW18B_UnitTest_globals.pulseCounts(sw, blinkPin),
        1,
        0,
        0,
    )  # 1 change
    SW18B_UnitTest_globals.test_value(
        "Blink_02",
        SW18B_UnitTest_globals.pulseRead(sw, blinkPin),
        30000,
        10000,
        0,
    )  # Should be a 50 mS pulse
