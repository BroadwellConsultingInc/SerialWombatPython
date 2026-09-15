import SW18B_UnitTest_globals
import SerialWombatAnalogInput

try:
    from ArduinoFunctions import delay
except ImportError:
    import time

    def delay(milliseconds):
        time.sleep(milliseconds / 1000.0)

from SerialWombat import SW_LE16

from SW18B_UnitTest_globals import setAnalogRatio, analogShutdown

MCP4728_ADDR = 0x60

analog16 = SerialWombatAnalogInput.SerialWombatAnalogInput(SW18B_UnitTest_globals.SW18AB_6B)
analog17 = SerialWombatAnalogInput.SerialWombatAnalogInput(SW18B_UnitTest_globals.SW18AB_6B)
analog18 = SerialWombatAnalogInput.SerialWombatAnalogInput(SW18B_UnitTest_globals.SW18AB_6B)
analog19 = SerialWombatAnalogInput.SerialWombatAnalogInput(SW18B_UnitTest_globals.SW18AB_6B)

analog16SW4B = SerialWombatAnalogInput.SerialWombatAnalogInput(SW18B_UnitTest_globals.SW4B_6F)
analog17SW4B = SerialWombatAnalogInput.SerialWombatAnalogInput(SW18B_UnitTest_globals.SW4B_6E)
analog18SW4B = SerialWombatAnalogInput.SerialWombatAnalogInput(SW18B_UnitTest_globals.SW4B_6E)
analog19SW4B = SerialWombatAnalogInput.SerialWombatAnalogInput(SW18B_UnitTest_globals.SW4B_6E)

analog0SW8B = SerialWombatAnalogInput.SerialWombatAnalogInput(SW18B_UnitTest_globals.SW8B_68)
analog1SW8B = SerialWombatAnalogInput.SerialWombatAnalogInput(SW18B_UnitTest_globals.SW8B_68)
analog2SW8B = SerialWombatAnalogInput.SerialWombatAnalogInput(SW18B_UnitTest_globals.SW8B_68)
analog3SW8B = SerialWombatAnalogInput.SerialWombatAnalogInput(SW18B_UnitTest_globals.SW8B_68)
analog4SW8B = SerialWombatAnalogInput.SerialWombatAnalogInput(SW18B_UnitTest_globals.SW8B_68)
analog5SW8B = SerialWombatAnalogInput.SerialWombatAnalogInput(SW18B_UnitTest_globals.SW8B_68)
analog6SW8B = SerialWombatAnalogInput.SerialWombatAnalogInput(SW18B_UnitTest_globals.SW8B_68)
analog7SW8B = SerialWombatAnalogInput.SerialWombatAnalogInput(SW18B_UnitTest_globals.SW8B_68)

SW8BAnalogs = [
    analog0SW8B,
    analog1SW8B,
    analog2SW8B,
    analog3SW8B,
    analog4SW8B,
    analog5SW8B,
    analog6SW8B,
    analog7SW8B,
]

SW18ABAnalogs = [
    analog16,
    analog16,
    analog16,
    analog16,
    analog16,
    analog16,
    analog16,
    analog16,
    analog16,
    analog16,
    analog16,
    analog16,
    analog16,
    analog16,
    analog16,
    analog16,
    analog16,
    analog17,
    analog18,
    analog19,
]

analogSeed = 1


def _uint16(value):
    return int(value) & 0xFFFF








def analogInputTest(sw=None):
    if sw is None:
        sw = SW18B_UnitTest_globals.SW18AB_6B

    SW18B_UnitTest_globals.resetAll()
    analogShutdown()

    if sw is SW18B_UnitTest_globals.SW18AB_6B:
        analogInputTest_SW18AB()
        return

    if sw is SW18B_UnitTest_globals.SW8B_68:
        analogInputTest_SW8B()
        return

    if sw is SW18B_UnitTest_globals.SW4B_6C:
        analog16SW4B.begin(1)
        analog17SW4B.begin(3)
        analog18SW4B.begin(2)
        analog19SW4B.begin(1)

    for i in range(0, 65535, 1024):
        ratio = _uint16(i)
        setAnalogRatio(16, ratio)
        setAnalogRatio(17, ratio + 15000)
        setAnalogRatio(18, ratio + 30000)
        setAnalogRatio(19, ratio + 45000)

        delay(100)

        for x in range(100):
            if sw is SW18B_UnitTest_globals.SW18AB_6B:
                SW18B_UnitTest_globals.SW18AB_6B.readTemperature_100thsDegC()
                readResult = analog16.readCounts()
                SW18B_UnitTest_globals.test_value("ANALOGIN_COUNTS_16", readResult, ratio, 256, 3)

                readResult = analog16.readAveragedCounts()
                SW18B_UnitTest_globals.test_value("ANALOGIN_AVERAGE_16", readResult, ratio, 256, 3)

            if sw is SW18B_UnitTest_globals.SW4B_6C:
                readResult = analog16SW4B.readCounts()
                SW18B_UnitTest_globals.test_value("ANALOGIN_COUNTS_16_4B", readResult, ratio, 256, 3)

                readResult = analog16SW4B.readAveragedCounts()
                SW18B_UnitTest_globals.test_value("ANALOGIN_AVERAGE_16_4B", readResult, ratio, 256, 3)

            if sw is SW18B_UnitTest_globals.SW8B_68:
                readResult = analog16SW4B.readCounts()
                SW18B_UnitTest_globals.test_value("ANALOGIN_COUNTS_16_4B", readResult, ratio, 256, 3)

                readResult = analog16SW4B.readAveragedCounts()
                SW18B_UnitTest_globals.test_value("ANALOGIN_AVERAGE_16_4B", readResult, ratio, 256, 3)

            delay(0)

        ratio = _uint16(ratio + 15000)

        for x in range(100):
            if sw is SW18B_UnitTest_globals.SW18AB_6B:
                SW18B_UnitTest_globals.SW18AB_6B.readTemperature_100thsDegC()
                readResult = analog17.readCounts()
                SW18B_UnitTest_globals.test_value("ANALOGIN_COUNTS_17", readResult, ratio, 256, 3)

            if sw is SW18B_UnitTest_globals.SW4B_6C:
                readResult = analog17SW4B.readCounts()
                SW18B_UnitTest_globals.test_value("ANALOGIN_COUNTS_17_4B", readResult, ratio, 256, 3)

            delay(0)

        ratio = _uint16(ratio + 15000)
        for x in range(100):
            if sw is SW18B_UnitTest_globals.SW18AB_6B:
                SW18B_UnitTest_globals.SW18AB_6B.readTemperature_100thsDegC()
                readResult = analog18.readCounts()
                SW18B_UnitTest_globals.test_value("ANALOGIN_COUNTS_18", readResult, ratio, 256, 3)

            if sw is SW18B_UnitTest_globals.SW4B_6C:
                readResult = analog18SW4B.readCounts()
                SW18B_UnitTest_globals.test_value("ANALOGIN_COUNTS_18_4B", readResult, ratio, 256, 3)

            delay(0)

        ratio = _uint16(ratio + 15000)
        for x in range(100):
            if sw is SW18B_UnitTest_globals.SW18AB_6B:
                SW18B_UnitTest_globals.SW18AB_6B.readTemperature_100thsDegC()
                readResult = analog19.readCounts()
                SW18B_UnitTest_globals.test_value("ANALOGIN_COUNTS_19", readResult, ratio, 256, 3)

            if sw is SW18B_UnitTest_globals.SW4B_6C:
                readResult = analog19SW4B.readCounts()
                SW18B_UnitTest_globals.test_value("ANALOGIN_COUNTS_10_4B", readResult, ratio, 256, 3)

            delay(0)

        delay(100)


def analogInputTest_SW8B():
    for i in range(8):
        SW8BAnalogs[i].begin(i)

    for i in range(0, 65535, 100):
        adc = _uint16(i)

        for pin in range(8):
            setAnalogRatio(SW18B_UnitTest_globals.SW8BPinTo18ABPin(pin), adc + 0x1800 * pin)

        delay(100)

        for pin in range(8):
            expected = _uint16(adc + 0x1800 * pin)
            readResult = SW8BAnalogs[pin].readPublicData()
            SW18B_UnitTest_globals.test_value("ANALOGIN_COUNTS_8B", readResult, expected, 256, 3)

            readResult = SW8BAnalogs[pin].readAveragedCounts()
            SW18B_UnitTest_globals.test_value("ANALOGIN_COUNTS_8B_AVG", readResult, expected, 256, 3)

    setAnalogRatio(SW18B_UnitTest_globals.SW8BPinTo18ABPin(4), 0x8000)
    SW8BAnalogs[4].readMaximumCounts(True)

    setAnalogRatio(SW18B_UnitTest_globals.SW8BPinTo18ABPin(4), 0x4000)
    delay(100)
    setAnalogRatio(SW18B_UnitTest_globals.SW8BPinTo18ABPin(4), 0xC000)
    delay(100)

    minimum = SW8BAnalogs[4].readMinimumCounts()
    SW18B_UnitTest_globals.test_value("ANALOGIN_MIN_8", minimum, 0x4000, 256, 3)

    maximum = SW8BAnalogs[4].readMaximumCounts()
    SW18B_UnitTest_globals.test_value("ANALOGIN_MAX_8", maximum, 0xC000, 256, 3)

    setAnalogRatio(SW18B_UnitTest_globals.SW8BPinTo18ABPin(4), 0x0000)
    SW8BAnalogs[4].begin(SW18B_UnitTest_globals.SW8BPinTo18ABPin(4), 10000)
    for i in range(60):
        setAnalogRatio(SW18B_UnitTest_globals.SW8BPinTo18ABPin(4), 0x4000)
        delay(100)
        setAnalogRatio(SW18B_UnitTest_globals.SW8BPinTo18ABPin(4), 0xC000)
        delay(100)

    average = SW8BAnalogs[4].readAveragedCounts()
    SW18B_UnitTest_globals.test_value("ANALOGIN_AVG_8", average, 0x4000, 256, 3)

    setAnalogRatio(SW18B_UnitTest_globals.SW8BPinTo18ABPin(4), 0xFFFF)
    delay(100)
    SW8BAnalogs[4].begin(SW18B_UnitTest_globals.SW8BPinTo18ABPin(4), 10000, 65445)
    setAnalogRatio(SW18B_UnitTest_globals.SW8BPinTo18ABPin(4), 0)
    delay(500)

    result = SW8BAnalogs[4].readFilteredCounts()
    SW18B_UnitTest_globals.test_value("ANALOGIN_Filter_8", result, 0x8000, 256, 3)
    delay(500)
    result = SW8BAnalogs[4].readFilteredCounts()
    SW18B_UnitTest_globals.test_value("ANALOGIN_Filter_8_2", result, 0x4000, 256, 3)


def analogInputTest_SW18AB():
    for i in range(16, 19 + 1):
        SW18ABAnalogs[i].begin(i)

    for i in range(0, 65535, 100):
        adc = _uint16(i)

        for pin in range(16, 19 + 1):
            setAnalogRatio(pin, adc + 0x1800 * pin)

        delay(200)

        for pin in range(16, 19 + 1):
            expected = _uint16(adc + 0x1800 * pin)
            readResult = SW18ABAnalogs[pin].readPublicData()
            SW18B_UnitTest_globals.test_value("ANALOGIN_COUNTS_18AB", readResult, expected, 256, 3)

            readResult = SW18ABAnalogs[pin].readAveragedCounts()
            SW18B_UnitTest_globals.test_value("ANALOGIN_COUNTS_18AB_AVG", readResult, expected, 256, 3)

    setAnalogRatio(16, 0x8000)
    analog16.readMaximumCounts(True)

    setAnalogRatio(16, 0x4000)
    delay(100)
    setAnalogRatio(16, 0xC000)
    delay(100)

    minimum = analog16.readMinimumCounts()
    SW18B_UnitTest_globals.test_value("ANALOGIN_MIN_16", minimum, 0x4000, 256, 3)

    maximum = analog16.readMaximumCounts()
    SW18B_UnitTest_globals.test_value("ANALOGIN_MAX_16", maximum, 0xC000, 256, 3)

    setAnalogRatio(16, 0x0000)
    analog16.begin(16, 10000)
    for i in range(60):
        setAnalogRatio(16, 0x4000)
        delay(100)
        setAnalogRatio(16, 0xC000)
        delay(100)

    average = analog16.readAveragedCounts()
    SW18B_UnitTest_globals.test_value("ANALOGIN_AVG_16", average, 0x4000, 256, 3)

    setAnalogRatio(16, 0xFFFF)
    delay(100)
    analog16.begin(16, 10000, 65445)
    setAnalogRatio(16, 0)
    delay(500)

    result = analog16.readFilteredCounts()
    SW18B_UnitTest_globals.test_value("ANALOGIN_Filter_16", result, 0x8000, 256, 3)
    delay(500)
    result = analog16.readFilteredCounts()
    SW18B_UnitTest_globals.test_value("ANALOGIN_Filter_16_2", result, 0x4000, 256, 3)
