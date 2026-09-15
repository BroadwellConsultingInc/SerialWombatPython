import SW18B_UnitTest_globals
import SerialWombatPin
import SerialWombatPulseOnChange

try:
    from ArduinoFunctions import delay
except ImportError:
    import time

    def delay(milliseconds):
        time.sleep(milliseconds / 1000.0)


POC_IN_PIN2 = 7
POC_IN_PIN1 = 6
POC_OUT_PIN = 0

OUTPUT = 1
SW_LOW = 0
SW_HIGH = 1

pocInput1 = None
pocInput2 = None
pocPointer = None


def _testValue(designator, value, expected, counts=0, sixtyFourths=0):
    SW18B_UnitTest_globals.test_value(designator, value, expected, counts, sixtyFourths)


def _pin(sw, pin):
    p = SerialWombatPin.SerialWombatPin(sw)
    p._pin = pin
    return p


def pulseOnChangeTest(sw):
    global pocInput1, pocInput2, pocPointer

    SW18B_UnitTest_globals.resetAll()

    pocInput1 = _pin(sw, POC_IN_PIN1)
    pocInput2 = _pin(sw, POC_IN_PIN2)
    pocPointer = SerialWombatPulseOnChange.SerialWombatPulseOnChange(sw)

    pocPulseOnChange(sw)
    pocPulseOnIncrease(sw)
    pocPulseOnDecrease(sw)
    pocPulseOnEqualValue(sw)
    pocPulseOnLessThanValue(sw)
    pocPulseOnGreaterThanValue(sw)
    pocPulseOnNotEqualValue(sw)
    pocPulseOnPinsEqual(sw)
    pocPulseOnPinsNotEqual(sw)

    pocInput1.readPublicData()
    pocInput2.readPublicData()
    pocPointer.readPublicData()


def pulseOnChangeTest18AB():
    pulseOnChangeTest(SW18B_UnitTest_globals.SW18AB_6B)


def pocPulseOnChange(sw):
    SW18B_UnitTest_globals.resetAll()
    # pocInput1.begin(POC_IN_PIN1)
    pocInput1.pinMode(OUTPUT)
    pocInput1.writePublicData(0x8000)
    pocPointer.begin(POC_OUT_PIN)
    SW18B_UnitTest_globals.initializePulseReaduS(sw, POC_OUT_PIN)
    delay(1000)
    _testValue(
        "POC_POC_01",
        SW18B_UnitTest_globals.pulseCounts(sw, POC_OUT_PIN),
        0,
    )  # No Pulses So far
    pocPointer.setEntryOnChange(0, POC_IN_PIN1)
    pocInput1.writePublicData(0x8001)
    delay(1000)
    _testValue(
        "POC_POC_02A",
        SW18B_UnitTest_globals.pulseCounts(sw, POC_OUT_PIN),
        1,
    )  # 1 change
    _testValue(
        "POC_POC_02B",
        SW18B_UnitTest_globals.pulseRead(sw, POC_OUT_PIN),
        50000,
        10000,
    )  # Should be a 50 mS pulse


def pocPulseOnIncrease(sw):
    pocPointer.begin(POC_OUT_PIN)
    # pocInput1.begin(POC_IN_PIN1)
    pocInput1.writePublicData(0x8000)
    pocInput1.pinMode(OUTPUT)
    SW18B_UnitTest_globals.initializePulseReaduS(sw, POC_OUT_PIN)
    delay(1000)
    _testValue(
        "POC_INC_01",
        SW18B_UnitTest_globals.pulseCounts(sw, POC_OUT_PIN),
        0,
    )  # No Pulses So far
    pocPointer.setEntryOnIncrease(1, POC_IN_PIN1)
    pocInput1.writePublicData(0x7FFF)
    delay(1000)
    _testValue(
        "POC_INC_02",
        SW18B_UnitTest_globals.pulseCounts(sw, POC_OUT_PIN),
        0,
    )  # No Pulses So far
    pocInput1.writePublicData(0x8000)
    delay(1000)
    _testValue(
        "POC_INC_03",
        SW18B_UnitTest_globals.pulseCounts(sw, POC_OUT_PIN),
        1,
    )  # 1 change
    _testValue(
        "POC_INC_04",
        SW18B_UnitTest_globals.pulseRead(sw, POC_OUT_PIN),
        50000,
        10000,
    )  # Should be a 50 mS pulse
    pocInput1.writePublicData(0xC000)
    delay(1000)
    _testValue(
        "POC_INC_05",
        SW18B_UnitTest_globals.pulseCounts(sw, POC_OUT_PIN),
        2,
    )  # 2 changes
    _testValue(
        "POC_INC_06",
        SW18B_UnitTest_globals.pulseRead(sw, POC_OUT_PIN),
        50000,
        10000,
    )  # Should be a 50 mS pulse


def pocPulseOnDecrease(sw):
    pocPointer.begin(POC_OUT_PIN, SW_HIGH, SW_LOW, 20)
    # pocInput1.begin(POC_IN_PIN1)
    pocInput1.pinMode(OUTPUT)
    pocInput1.writePublicData(0x8000)
    SW18B_UnitTest_globals.initializePulseReaduS(sw, POC_OUT_PIN)
    delay(1000)
    _testValue(
        "POC_DEC_01",
        SW18B_UnitTest_globals.pulseCounts(sw, POC_OUT_PIN),
        0,
    )  # No Pulses So far
    pocPointer.setEntryOnDecrease(1, POC_IN_PIN1)
    pocInput1.writePublicData(0xC000)
    delay(1000)
    _testValue(
        "POC_DEC_02",
        SW18B_UnitTest_globals.pulseCounts(sw, POC_OUT_PIN),
        0,
    )  # No Pulses So far
    pocInput1.writePublicData(0x8000)
    delay(1000)
    _testValue(
        "POC_DEC_03",
        SW18B_UnitTest_globals.pulseCounts(sw, POC_OUT_PIN),
        1,
    )  # 1 change
    _testValue(
        "POC_DEC_04",
        SW18B_UnitTest_globals.pulseRead(sw, POC_OUT_PIN),
        20000,
        5000,
    )  # Should be a 20 mS pulse
    pocInput1.writePublicData(0x0000)
    delay(1000)
    _testValue(
        "POC_DEC_05",
        SW18B_UnitTest_globals.pulseCounts(sw, POC_OUT_PIN),
        2,
    )  # 2 changes
    _testValue(
        "POC_DEC_06",
        SW18B_UnitTest_globals.pulseRead(sw, POC_OUT_PIN),
        20000,
        5000,
    )  # Should be a 50 mS pulse


def pocPulseOnEqualValue(sw):
    pocPointer.begin(POC_OUT_PIN)
    # pocInput1.begin(POC_IN_PIN1)
    pocInput1.pinMode(OUTPUT)
    pocInput1.writePublicData(0x8000)
    SW18B_UnitTest_globals.initializePulseReaduS(sw, POC_OUT_PIN)
    delay(1000)
    _testValue(
        "POC_EQV_01",
        SW18B_UnitTest_globals.pulseCounts(sw, POC_OUT_PIN),
        0,
    )  # No Pulses So far
    pocPointer.setEntryOnEqualValue(1, POC_IN_PIN1, 0x1234)
    pocInput1.writePublicData(0xC000)
    delay(1000)
    _testValue(
        "POC_EQV_02",
        SW18B_UnitTest_globals.pulseCounts(sw, POC_OUT_PIN),
        0,
    )  # No Pulses So far
    pocInput1.writePublicData(0x1234)
    delay(1000)
    _testValue(
        "POC_EQV_03",
        SW18B_UnitTest_globals.pulseCounts(sw, POC_OUT_PIN),
        10,
        3,
    )  # 1 change
    _testValue(
        "POC_EQV_04",
        SW18B_UnitTest_globals.pulseRead(sw, POC_OUT_PIN),
        50000,
        5000,
    )  # Should be a 50 mS pulse
    pocInput1.writePublicData(0x0000)
    delay(1000)
    _testValue(
        "POC_EQV_05",
        SW18B_UnitTest_globals.pulseCounts(sw, POC_OUT_PIN),
        10,
        3,
    )  # 1 change
    pocInput1.writePublicData(0x1234)
    delay(1000)
    _testValue(
        "POC_EQV_06",
        SW18B_UnitTest_globals.pulseCounts(sw, POC_OUT_PIN),
        20,
        6,
    )  # 2 changes
    _testValue(
        "POC_EQV_07",
        SW18B_UnitTest_globals.pulseRead(sw, POC_OUT_PIN),
        50000,
        5000,
    )  # Should be a 50 mS pulse


def pocPulseOnLessThanValue(sw):
    pocPointer.begin(POC_OUT_PIN)
    # pocInput1.begin(POC_IN_PIN1)
    pocInput1.pinMode(OUTPUT)
    pocInput1.writePublicData(0x8000)
    SW18B_UnitTest_globals.initializePulseReaduS(sw, POC_OUT_PIN)
    delay(1000)
    _testValue(
        "POC_LTV_01",
        SW18B_UnitTest_globals.pulseCounts(sw, POC_OUT_PIN),
        0,
    )  # No Pulses So far
    pocPointer.setEntryOnLessThanValue(1, POC_IN_PIN1, 0x1234)
    pocInput1.writePublicData(0xC000)
    delay(1000)
    _testValue(
        "POC_LTV_02",
        SW18B_UnitTest_globals.pulseCounts(sw, POC_OUT_PIN),
        0,
    )  # No Pulses So far
    pocInput1.writePublicData(0x1233)
    delay(1000)
    _testValue(
        "POC_LTV_03",
        SW18B_UnitTest_globals.pulseCounts(sw, POC_OUT_PIN),
        10,
        3,
    )  # 1 change
    _testValue(
        "POC_LTV_04",
        SW18B_UnitTest_globals.pulseRead(sw, POC_OUT_PIN),
        50000,
        5000,
    )  # Should be a 50 mS pulse
    pocInput1.writePublicData(0x6000)
    delay(1000)
    _testValue(
        "POC_LTV_05",
        SW18B_UnitTest_globals.pulseCounts(sw, POC_OUT_PIN),
        10,
        3,
    )  # 1 change
    pocInput1.writePublicData(0x1234)
    delay(1000)
    pocInput1.writePublicData(0x6000)
    delay(1000)
    _testValue(
        "POC_LTV_06",
        SW18B_UnitTest_globals.pulseCounts(sw, POC_OUT_PIN),
        10,
        3,
    )  # 1 change
    pocInput1.writePublicData(0x1000)
    delay(1000)
    _testValue(
        "POC_LTV_07",
        SW18B_UnitTest_globals.pulseCounts(sw, POC_OUT_PIN),
        20,
        6,
    )  # 2 changes
    _testValue(
        "POC_LTV_08",
        SW18B_UnitTest_globals.pulseRead(sw, POC_OUT_PIN),
        50000,
        5000,
    )  # Should be a 50 mS pulse


def pocPulseOnGreaterThanValue(sw):
    pocPointer.begin(POC_OUT_PIN)
    # pocInput1.begin(POC_IN_PIN1)
    pocInput1.pinMode(OUTPUT)
    pocInput1.writePublicData(0x0000)
    SW18B_UnitTest_globals.initializePulseReaduS(sw, POC_OUT_PIN)
    delay(1000)
    _testValue(
        "POC_GTV_01",
        SW18B_UnitTest_globals.pulseCounts(sw, POC_OUT_PIN),
        0,
    )  # No Pulses So far
    pocPointer.setEntryOnGreaterThanValue(1, POC_IN_PIN1, 0x1234)
    pocInput1.writePublicData(0x0000)
    delay(1000)
    _testValue(
        "POC_GTV_02",
        SW18B_UnitTest_globals.pulseCounts(sw, POC_OUT_PIN),
        0,
    )  # No Pulses So far
    pocInput1.writePublicData(0x1235)
    delay(1000)
    _testValue(
        "POC_GTV_03",
        SW18B_UnitTest_globals.pulseCounts(sw, POC_OUT_PIN),
        10,
        3,
    )  # 1 change
    _testValue(
        "POC_GTV_04",
        SW18B_UnitTest_globals.pulseRead(sw, POC_OUT_PIN),
        50000,
        5000,
    )  # Should be a 50 mS pulse
    pocInput1.writePublicData(0x0500)
    delay(1000)
    _testValue(
        "POC_GTV_05",
        SW18B_UnitTest_globals.pulseCounts(sw, POC_OUT_PIN),
        10,
        3,
    )  # 1 change
    pocInput1.writePublicData(0x0500)
    delay(1000)
    _testValue(
        "POC_GTV_06",
        SW18B_UnitTest_globals.pulseCounts(sw, POC_OUT_PIN),
        10,
        3,
    )  # 1 change
    pocInput1.writePublicData(0x6000)
    delay(1000)
    _testValue(
        "POC_GTV_07",
        SW18B_UnitTest_globals.pulseCounts(sw, POC_OUT_PIN),
        20,
        6,
    )  # 2 changes
    _testValue(
        "POC_GTV_08",
        SW18B_UnitTest_globals.pulseRead(sw, POC_OUT_PIN),
        50000,
        5000,
    )  # Should be a 50 mS pulse


def pocPulseOnNotEqualValue(sw):
    pocPointer.begin(POC_OUT_PIN)
    pocInput1.pinMode(OUTPUT)
    # pocInput1.begin(POC_IN_PIN1)
    pocInput1.writePublicData(0x1234)
    SW18B_UnitTest_globals.initializePulseReaduS(sw, POC_OUT_PIN)
    delay(1000)
    _testValue(
        "POC_NEV_01",
        SW18B_UnitTest_globals.pulseCounts(sw, POC_OUT_PIN),
        0,
    )  # No Pulses So far
    pocPointer.setEntryOnNotEqualValue(1, POC_IN_PIN1, 0x1234)

    pocInput1.writePublicData(0x1233)
    delay(1000)
    _testValue(
        "POC_NEV_03",
        SW18B_UnitTest_globals.pulseCounts(sw, POC_OUT_PIN),
        10,
        3,
    )  # 1 change
    _testValue(
        "POC_NEV_04",
        SW18B_UnitTest_globals.pulseRead(sw, POC_OUT_PIN),
        50000,
        5000,
    )  # Should be a 50 mS pulse
    pocInput1.writePublicData(0x1234)
    delay(1000)
    _testValue(
        "POC_NEV_05",
        SW18B_UnitTest_globals.pulseCounts(sw, POC_OUT_PIN),
        10,
        3,
    )  # 1 change
    pocInput1.writePublicData(0x1235)
    delay(1000)
    _testValue(
        "POC_NEV_06",
        SW18B_UnitTest_globals.pulseCounts(sw, POC_OUT_PIN),
        20,
        6,
    )  # 2 changes
    _testValue(
        "POC_NEV_07",
        SW18B_UnitTest_globals.pulseRead(sw, POC_OUT_PIN),
        50000,
        5000,
    )  # Should be a 50 mS pulse


def pocPulseOnPinsEqual(sw):
    pocPointer.begin(POC_OUT_PIN)
    # pocInput1.begin(POC_IN_PIN1)
    pocInput1.pinMode(OUTPUT)
    # pocInput2.begin(POC_IN_PIN2)
    pocInput2.pinMode(OUTPUT)

    pocInput1.writePublicData(0x1234)
    pocInput2.writePublicData(0x1235)
    SW18B_UnitTest_globals.initializePulseReaduS(sw, POC_OUT_PIN)
    delay(1000)
    _testValue(
        "POC_EQP_01",
        SW18B_UnitTest_globals.pulseCounts(sw, POC_OUT_PIN),
        0,
    )  # No Pulses So far
    pocPointer.setEntryOnPinsEqual(1, POC_IN_PIN1, POC_IN_PIN2)

    pocInput1.writePublicData(0x1235)
    delay(1000)
    _testValue(
        "POC_EQP_03",
        SW18B_UnitTest_globals.pulseCounts(sw, POC_OUT_PIN),
        10,
        3,
    )  # 1 change
    _testValue(
        "POC_EQP_04",
        SW18B_UnitTest_globals.pulseRead(sw, POC_OUT_PIN),
        50000,
        5000,
    )  # Should be a 50 mS pulse
    pocInput1.writePublicData(0x1234)
    delay(1000)
    _testValue(
        "POC_EQP_05",
        SW18B_UnitTest_globals.pulseCounts(sw, POC_OUT_PIN),
        10,
        3,
    )  # 1 change
    pocInput2.writePublicData(0x1234)
    delay(1000)
    _testValue(
        "POC_EQP_06",
        SW18B_UnitTest_globals.pulseCounts(sw, POC_OUT_PIN),
        20,
        6,
    )  # 2 changes
    _testValue(
        "POC_EQP_07",
        SW18B_UnitTest_globals.pulseRead(sw, POC_OUT_PIN),
        50000,
        5000,
    )  # Should be a 50 mS pulse


def pocPulseOnPinsNotEqual(sw):
    pocPointer.begin(POC_OUT_PIN)
    pocInput1.pinMode(OUTPUT)
    pocInput2.pinMode(OUTPUT)
    # pocInput1.begin(POC_IN_PIN1)
    # pocInput2.begin(POC_IN_PIN2)

    pocInput1.writePublicData(0x1234)
    pocInput2.writePublicData(0x1234)
    SW18B_UnitTest_globals.initializePulseReaduS(sw, POC_OUT_PIN)
    delay(1000)
    _testValue(
        "POC_EQP_01",
        SW18B_UnitTest_globals.pulseCounts(sw, POC_OUT_PIN),
        0,
    )  # No Pulses So far
    pocPointer.setEntryOnPinsNotEqual(1, POC_IN_PIN1, POC_IN_PIN2)

    pocInput1.writePublicData(0x1235)
    delay(1000)
    _testValue(
        "POC_EQP_03",
        SW18B_UnitTest_globals.pulseCounts(sw, POC_OUT_PIN),
        10,
        3,
    )  # 1 change
    _testValue(
        "POC_EQP_04",
        SW18B_UnitTest_globals.pulseRead(sw, POC_OUT_PIN),
        50000,
        5000,
    )  # Should be a 50 mS pulse
    pocInput1.writePublicData(0x1234)
    delay(1000)
    _testValue(
        "POC_EQP_05",
        SW18B_UnitTest_globals.pulseCounts(sw, POC_OUT_PIN),
        10,
        3,
    )  # 1 change
    pocInput2.writePublicData(0x1200)
    delay(1000)
    _testValue(
        "POC_EQP_06",
        SW18B_UnitTest_globals.pulseCounts(sw, POC_OUT_PIN),
        20,
        6,
    )  # 2 changes
    _testValue(
        "POC_EQP_07",
        SW18B_UnitTest_globals.pulseRead(sw, POC_OUT_PIN),
        50000,
        5000,
    )  # Should be a 50 mS pulse
