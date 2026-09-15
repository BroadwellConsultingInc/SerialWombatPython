import SW18B_UnitTest_globals
import SerialWombatHBridge

try:
    from ArduinoFunctions import delay
except ImportError:
    import time

    def delay(milliseconds):
        time.sleep(milliseconds / 1000.0)


HBRIDGE_TEST_INCREMENTS = 100
HBRIDGE_OFF_BOTH_LOW = getattr(SerialWombatHBridge, "HBRIDGE_OFF_BOTH_LOW", 0)


def _buildHBridges():
    HBridge18 = SerialWombatHBridge.SerialWombatHBridge_18AB(SW18B_UnitTest_globals.SW18AB_6B)
    HBridge8 = SerialWombatHBridge.SerialWombatHBridge_18AB(SW18B_UnitTest_globals.SW8B_68)
    return HBridge18, HBridge8


def _writeHBridgePublicData(hBridge, value):
    value &= 0xFFFF
    if hasattr(hBridge, "writePublicData"):
        hBridge.writePublicData(value)
    elif hasattr(hBridge, "writeDutyCycle"):
        hBridge.writeDutyCycle(value)
    else:
        hBridge._sw.writePublicData(hBridge._pin, value)


def _testValue(designator, value, expected, counts=0, sixtyFourths=0):
    if hasattr(SW18B_UnitTest_globals, "test_value"):
        SW18B_UnitTest_globals.test_value(designator, value, expected, counts, sixtyFourths)
    else:
        SW18B_UnitTest_globals.test(designator, value, expected, counts, sixtyFourths)


def _pulseCounts(sw, pin):
    if hasattr(SW18B_UnitTest_globals, "pulseCounts"):
        return SW18B_UnitTest_globals.pulseCounts(sw, pin)
    SW18B_UnitTest_globals.test("TEST ERROR: pulseCounts is not exported from SW18B_UnitTest_globals", 0)
    return 0


def _dutyCycleRead(sw, pin):
    if hasattr(SW18B_UnitTest_globals, "dutyCycleRead"):
        return SW18B_UnitTest_globals.dutyCycleRead(sw, pin)
    SW18B_UnitTest_globals.test("TEST ERROR: dutyCycleRead is not exported from SW18B_UnitTest_globals", 0)
    return 0


def hBridgeTest(sw=None, hBridgeFirstPin=5, hBridgeSecondPin=6):
    if sw is None:
        sw = SW18B_UnitTest_globals.SW18AB_6B

    SW18B_UnitTest_globals.resetAll()

    HBridge18, HBridge8 = _buildHBridges()

    HBridge = None
    if sw is SW18B_UnitTest_globals.SW18AB_6B:
        HBridge = HBridge18

    if sw is SW18B_UnitTest_globals.SW8B_68:
        HBridge = HBridge8

    if HBridge is None:
        print("Invalid chip for HBridge test")
        return

    HBridge.begin(hBridgeFirstPin, hBridgeSecondPin, 4000, HBRIDGE_OFF_BOTH_LOW)  # Should initialize to 32768.  250 cycles per second
    SW18B_UnitTest_globals.initializePulseReaduS(sw, hBridgeFirstPin)
    SW18B_UnitTest_globals.initializePulseReaduS(sw, hBridgeSecondPin)

    firstPinCounts = _pulseCounts(sw, hBridgeFirstPin)
    secondPinCounts = _pulseCounts(sw, hBridgeSecondPin)

    delay(1000)

    _testValue("HBridge_00A", _pulseCounts(sw, hBridgeFirstPin), firstPinCounts)  # There should have been no pulses on either.
    _testValue("HBridge_00B", _pulseCounts(sw, hBridgeSecondPin), secondPinCounts)

    _writeHBridgePublicData(HBridge, 0x0000)  # One high, one low, no PWM
    delay(100)
    firstPinCounts = _pulseCounts(sw, hBridgeFirstPin)
    secondPinCounts = _pulseCounts(sw, hBridgeSecondPin)
    delay(1000)

    _testValue("HBridge_01A", _pulseCounts(sw, hBridgeFirstPin), firstPinCounts)  # There should have been no pulses on either.
    _testValue("HBridge_01B", _pulseCounts(sw, hBridgeSecondPin), secondPinCounts)

    _writeHBridgePublicData(HBridge, 0xFFFF)  # One high, one low, no PWM
    delay(100)
    firstPinCounts = _pulseCounts(sw, hBridgeFirstPin)
    secondPinCounts = _pulseCounts(sw, hBridgeSecondPin)
    delay(1000)

    _testValue("HBridge_02A", _pulseCounts(sw, hBridgeFirstPin), firstPinCounts)  # There should have been no pulses on either.
    _testValue("HBridge_02B", _pulseCounts(sw, hBridgeSecondPin), secondPinCounts)

    _writeHBridgePublicData(HBridge, 0xC000)  # One PWM, one low
    delay(100)
    firstPinCounts = _pulseCounts(sw, hBridgeFirstPin)
    secondPinCounts = _pulseCounts(sw, hBridgeSecondPin)
    delay(1000)

    _testValue("HBridge_03A", _pulseCounts(sw, hBridgeFirstPin), firstPinCounts + 250, 15)
    _testValue("HBridge_03B", _pulseCounts(sw, hBridgeSecondPin), secondPinCounts)
    _testValue("HBridge_03C", _dutyCycleRead(sw, hBridgeFirstPin), 0x8000, 0x100)

    _writeHBridgePublicData(HBridge, 0xE000)  # One PWM, one low
    delay(100)
    firstPinCounts = _pulseCounts(sw, hBridgeFirstPin)
    secondPinCounts = _pulseCounts(sw, hBridgeSecondPin)
    delay(1000)

    _testValue("HBridge_04A", _pulseCounts(sw, hBridgeFirstPin), firstPinCounts + 250, 15)
    _testValue("HBridge_04B", _pulseCounts(sw, hBridgeSecondPin), secondPinCounts)
    _testValue("HBridge_04C", _dutyCycleRead(sw, hBridgeFirstPin), 0xC000, 0x100)

    _writeHBridgePublicData(HBridge, 0xA000)  # One PWM, one low
    delay(100)
    firstPinCounts = _pulseCounts(sw, hBridgeFirstPin)
    secondPinCounts = _pulseCounts(sw, hBridgeSecondPin)
    delay(1000)

    _testValue("HBridge_05A", _pulseCounts(sw, hBridgeFirstPin), firstPinCounts + 250, 15)
    _testValue("HBridge_05B", _pulseCounts(sw, hBridgeSecondPin), secondPinCounts)
    _testValue("HBridge_05C", _dutyCycleRead(sw, hBridgeFirstPin), 0x4000, 0x100)

    _writeHBridgePublicData(HBridge, 0x4000)  # One PWM, one low
    delay(100)
    firstPinCounts = _pulseCounts(sw, hBridgeFirstPin)
    secondPinCounts = _pulseCounts(sw, hBridgeSecondPin)
    delay(1000)

    _testValue("HBridge_06A", _pulseCounts(sw, hBridgeFirstPin), firstPinCounts)
    _testValue("HBridge_06B", _pulseCounts(sw, hBridgeSecondPin), secondPinCounts + 250, 15)
    _testValue("HBridge_06C", _dutyCycleRead(sw, hBridgeSecondPin), 0x8000, 0x100)

    _writeHBridgePublicData(HBridge, 0x2000)  # One PWM, one low
    delay(100)
    firstPinCounts = _pulseCounts(sw, hBridgeFirstPin)
    secondPinCounts = _pulseCounts(sw, hBridgeSecondPin)
    delay(1000)

    _testValue("HBridge_07A", _pulseCounts(sw, hBridgeFirstPin), firstPinCounts)
    _testValue("HBridge_07B", _pulseCounts(sw, hBridgeSecondPin), secondPinCounts + 250, 15)
    _testValue("HBridge_07C", _dutyCycleRead(sw, hBridgeSecondPin), 0xC000, 0x100)

    _writeHBridgePublicData(HBridge, 0x6000)  # One PWM, one low
    delay(100)
    firstPinCounts = _pulseCounts(sw, hBridgeFirstPin)
    secondPinCounts = _pulseCounts(sw, hBridgeSecondPin)
    delay(1000)

    _testValue("HBridge_08A", _pulseCounts(sw, hBridgeFirstPin), firstPinCounts)
    _testValue("HBridge_08B", _pulseCounts(sw, hBridgeSecondPin), secondPinCounts + 250, 15)
    _testValue("HBridge_08C", _dutyCycleRead(sw, hBridgeSecondPin), 0x4000, 0x100)

    if sw is SW18B_UnitTest_globals.SW18AB_6B:
        # Frequency sweep
        for period in range(2500, 60000 + 1, 1000):
            freq = 1000000 // period
            HBridge.begin(hBridgeFirstPin, hBridgeSecondPin, period, HBRIDGE_OFF_BOTH_LOW)
            for i in range(1000, 65535, 5000):
                _writeHBridgePublicData(HBridge, i)
                delay(10)
                SW18B_UnitTest_globals.initializePulseReaduS(sw, hBridgeFirstPin)
                SW18B_UnitTest_globals.initializePulseReaduS(sw, hBridgeSecondPin)
                firstPinCounts = _pulseCounts(sw, hBridgeFirstPin)
                secondPinCounts = _pulseCounts(sw, hBridgeSecondPin)
                delay(1000)

                if i < 0x8000:
                    _testValue("HBridge_09A", _pulseCounts(sw, hBridgeFirstPin), firstPinCounts)
                    _testValue("HBridge_09B", _pulseCounts(sw, hBridgeSecondPin), secondPinCounts + freq, 15, 10)
                    _testValue("HBridge_09C", _dutyCycleRead(sw, hBridgeSecondPin), 2 * (0x8000 - i), 0x100, 10)
                else:
                    _testValue("HBridge_10A", _pulseCounts(sw, hBridgeFirstPin), firstPinCounts + freq, 15, 10)
                    _testValue("HBridge_10B", _pulseCounts(sw, hBridgeSecondPin), secondPinCounts)
                    _testValue("HBridge_10C", _dutyCycleRead(sw, hBridgeFirstPin), 2 * (i - 0x8000), 0x100, 10)

        delay(100)
