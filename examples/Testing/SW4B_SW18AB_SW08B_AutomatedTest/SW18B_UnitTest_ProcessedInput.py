import SW18B_UnitTest_globals
import SerialWombat
import SerialWombatPWM
import SerialWombatProcessedInputPin

try:
    from ArduinoFunctions import delay
except ImportError:
    import time

    def delay(milliseconds):
        time.sleep(milliseconds / 1000.0)


ipInput18 = SerialWombatPWM.SerialWombatPWM_18AB(SW18B_UnitTest_globals.SW18AB_6B)
ipInput8 = SerialWombatPWM.SerialWombatPWM_18AB(SW18B_UnitTest_globals.SW8B_68)
processedInput18 = SerialWombatProcessedInputPin.SerialWombatProcessedInputPin(SW18B_UnitTest_globals.SW18AB_6B)
processedInput8 = SerialWombatProcessedInputPin.SerialWombatProcessedInputPin(SW18B_UnitTest_globals.SW8B_68)

ipInputPtr = ipInput18
ipProcessedInputPtr = processedInput18


def _test_value(designator, value, expected, counts=0, sixtyFourths=0):
    SW18B_UnitTest_globals.test_value(designator, value, expected, counts, sixtyFourths)


def inputProcessorTest(sw, pin):
    global ipInputPtr, ipProcessedInputPtr

    if sw is SW18B_UnitTest_globals.SW18AB_6B:
        ipInputPtr = ipInput18
        ipProcessedInputPtr = processedInput18
    elif sw is SW18B_UnitTest_globals.SW8B_68:
        ipInputPtr = ipInput8
        ipProcessedInputPtr = processedInput8

    ipDisabledTest(pin)
    ipExclusionTest(pin)
    ipAverageTest(pin)
    ipMxbTest(pin)


def ipDisabledTest(pin):
    SW18B_UnitTest_globals.resetAll()
    ipInputPtr.begin(pin + 1)
    ipProcessedInputPtr.begin(pin, pin + 1)

    for i in range(0, 65536, 13):
        ipInputPtr.writePublicData(i)
        result = ipProcessedInputPtr.readPublicData()
        _test_value("IP_DIS_01", result, i)
        delay(0)

    ipProcessedInputPtr.writeInverted(True)
    for i in range(0, 65536, 13):
        ipInputPtr.writePublicData(i)
        result = ipProcessedInputPtr.readPublicData()
        _test_value("IP_DIS_02", result, i)
        delay(0)

    ipProcessedInputPtr.writeProcessedInputEnable(True)
    for i in range(0, 65536, 13):
        ipInputPtr.writePublicData(i)
        result = ipProcessedInputPtr.readPublicData()
        _test_value("IP_INV_01", result, 65535 - i)
        delay(0)

    ipProcessedInputPtr.writeInverted(False)
    for i in range(0, 65536, 13):
        ipInputPtr.writePublicData(i)
        result = ipProcessedInputPtr.readPublicData()
        _test_value("IP_INV_02", result, i)
        delay(0)


def ipExclusionTest(pin):
    SW18B_UnitTest_globals.resetAll()
    ipInputPtr.begin(pin + 1)
    ipProcessedInputPtr.begin(pin, pin + 1)
    ipProcessedInputPtr.writeProcessedInputEnable(True)
    ipInputPtr.writePublicData(12500)
    ipProcessedInputPtr.writeExcludeBelowAbove(20000, 40000)

    for i in range(0, 19999, 13):
        ipInputPtr.writePublicData(i)
        result = ipProcessedInputPtr.readPublicData()
        _test_value("IP_EX_01", result, 12500)
        delay(0)

    lastVal = 0
    for i in range(20000, 40001, 13):
        ipInputPtr.writePublicData(i)
        lastVal = ipProcessedInputPtr.readPublicData()
        _test_value("IP_EX_02", lastVal, i)
        delay(0)

    for i in range(40001, 65536, 13):
        ipInputPtr.writePublicData(i)
        result = ipProcessedInputPtr.readPublicData()
        _test_value("IP_EX_03", result, lastVal)
        delay(0)


def ipAverageTest(pin):
    SW18B_UnitTest_globals.resetAll()

    ipProcessedInputPtr.begin(pin, SerialWombat.SerialWombatDataSource.SW_DATA_SOURCE_LFSR)
    ipProcessedInputPtr.writeAveragingNumberOfSamples(4000)
    ipProcessedInputPtr.writeProcessedInputEnable(True)

    delay(5000)

    result = ipProcessedInputPtr.readAverage()
    _test_value("IP_AVG_01", result, 32768, 500, 0)  # Random should average out to 32768, will allow +/- 500

    ipProcessedInputPtr.writeExcludeBelowAbove(40000, 60000)

    delay(30000)

    result = ipProcessedInputPtr.readAverage()
    _test_value("IP_AVG_01", result, 50000, 500, 0)  # Random should average out to 50000, will allow +/- 500


def ipMxbTest(pin):
    SW18B_UnitTest_globals.resetAll()
    ipInputPtr.begin(pin + 1)
    ipProcessedInputPtr.begin(pin, pin + 1)
    ipProcessedInputPtr.writeProcessedInputEnable(True)

    ipProcessedInputPtr.writeTransformLinearMXB(5 * 256, 32)

    for i in range(0, 65535, 13):
        ipInputPtr.writePublicData(i)
        result = ipProcessedInputPtr.readPublicData()
        expected = int(i) * 5 + 32
        if expected > 65535:
            expected = 65535
        _test_value("IP_MXB_01", result, expected)
        delay(0)

    ipProcessedInputPtr.writeTransformLinearMXB(5 * 256, -20000)

    for i in range(0, 65535, 13):
        ipInputPtr.writePublicData(i)
        result = ipProcessedInputPtr.readPublicData()
        expected = int(i) * 5 - 20000
        if expected > 65535:
            expected = 65535
        if expected < 0:
            expected = 0
        _test_value("IP_MXB_02", result, expected)
        delay(0)

    ipProcessedInputPtr.writeTransformLinearMXB(-5 * 256, 100000)

    for i in range(0, 65535, 13):
        ipInputPtr.writePublicData(i)
        result = ipProcessedInputPtr.readPublicData()
        expected = int(i) * -5 + 100000
        if expected > 65535:
            expected = 65535
        if expected < 0:
            expected = 0
        _test_value("IP_MXB_03", result, expected)
        delay(0)
