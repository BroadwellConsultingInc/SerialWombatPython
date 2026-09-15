from ArduinoFunctions import millis
import SW18B_UnitTest_globals
import SerialWombat18ABDataLogger
import SerialWombatPWM
import SerialWombatQueue

try:
    from ArduinoFunctions import delay
except ImportError:
    import time

    def delay(milliseconds):
        time.sleep(milliseconds / 1000.0)


DLQUEUELENGTH = 512
DLQUEUEADDR = 300


def _test(designator, value, expected, counts=0, sixtyFourths=0):
    SW18B_UnitTest_globals.test_value(designator, value, expected, counts, sixtyFourths)


def _readQueueByte(dlQueue):
    return dlQueue.read()


def _readQueueUInt16(dlQueue):
    lowByte = dlQueue.read()
    highByte = dlQueue.read()
    if lowByte < 0:
        lowByte = 0
    if highByte < 0:
        highByte = 0
    return (lowByte & 0xFF) | ((highByte & 0xFF) << 8)


def _readAllWordFrame(dlQueue):
    return [
        _readQueueUInt16(dlQueue),
        _readQueueUInt16(dlQueue),
        _readQueueUInt16(dlQueue),
        _readQueueUInt16(dlQueue),
        _readQueueUInt16(dlQueue),
    ]


def _readMixedFrame(dlQueue):
    return [
        _readQueueUInt16(dlQueue),
        _readQueueUInt16(dlQueue),
        _readQueueUInt16(dlQueue),
        _readQueueByte(dlQueue),
        _readQueueByte(dlQueue),
    ]


def _allDataFieldsMatch(d0, d1):
    return d0[1] == d1[1] and d0[2] == d1[2] and d0[3] == d1[3] and d0[4] == d1[4]


def _testPeriodFrameDelta(designator, d0, d1):
    _test(designator, d1[0] - d0[0], 128)


def _testChangeFrameDelta(designator, d0, d1, expected):
    if d1[0] < d0[0]:
        d1[0] += 65536
    _test(designator, d1[0] - d0[0], expected, 10)


def _beginPWMOutputs():
    p0 = SerialWombatPWM.SerialWombatPWM_18AB(SW18B_UnitTest_globals.SW18AB_6B)
    p8 = SerialWombatPWM.SerialWombatPWM_18AB(SW18B_UnitTest_globals.SW18AB_6B)
    p10 = SerialWombatPWM.SerialWombatPWM_18AB(SW18B_UnitTest_globals.SW18AB_6B)
    p17 = SerialWombatPWM.SerialWombatPWM_18AB(SW18B_UnitTest_globals.SW18AB_6B)

    p0.begin(0)
    p8.begin(8)
    p10.begin(10)
    p17.begin(17)

    return p0, p8, p10, p17


def _clearPublicData(p0, p8, p10, p17):
    p0.writePublicData(0)
    p8.writePublicData(0)
    p10.writePublicData(0)
    p17.writePublicData(0)


def _writeStepPattern(p0, p8, p10, p17, delays):
    delay(delays[0])
    p0.writePublicData(1000)
    delay(delays[1])
    p8.writePublicData(2000)
    delay(delays[2])
    p10.writePublicData(3000)
    delay(delays[3])
    p17.writePublicData(4000)
    delay(delays[4])


def _skipRepeatedAllWordFrame(dlQueue, d0, d1):
    if _allDataFieldsMatch(d0, d1):
        return _readAllWordFrame(dlQueue), False
    return d1, True


def _skipRepeatedMixedFrame(dlQueue, d0, d1):
    if _allDataFieldsMatch(d0, d1):
        return _readMixedFrame(dlQueue), False
    return d1, True


def _runPeriodicAllWordDataLoggerTest(swdl, dlQueue, p0, p8, p10, p17):
    dlQueue.begin(DLQUEUEADDR, DLQUEUELENGTH)
    i = dlQueue.available() #debug
    swdl.begin(
        DLQUEUEADDR,
        DLQUEUELENGTH,
        True,  # Queue Frame Index
        False,  # QueueOnChange
        SerialWombat18ABDataLogger.DataLoggerPeriod.PERIOD_128mS,
    )

    swdl.configurePin(0, True, True)
    swdl.configurePin(8, True, True)
    swdl.configurePin(10, True, True)
    swdl.configurePin(17, True, True)
    beginningTime = millis()    
    swdl.enable(True)
    _writeStepPattern(p0, p8, p10, p17, [130, 130, 130, 130, 130])
    swdl.enable(False)
    endTime = millis()
    totalTime = endTime - beginningTime
    expectedBytes = totalTime // 128 * 10 # 10 bytes per entry, including frame number
    # Should be at least 5 * 2 * 5 = 50 data bytes available, no more than 60
    i = dlQueue.available()
    if i >= expectedBytes   and i <= expectedBytes *3 // 2 : 
        i = expectedBytes
    _test("DataLogger_00", i, expectedBytes)

    d0 = _readAllWordFrame(dlQueue)
    d1 = _readAllWordFrame(dlQueue)

    # Test that first entry is all 0's
    for i in range(1, 5):
        _test(f"Datalogger_01_{i}", d0[i], 0)

    d1, testDelta = _skipRepeatedAllWordFrame(dlQueue, d0, d1)
    if testDelta:
        _testPeriodFrameDelta("Datalogger_02", d0, d1)
    _test("Datalogger_03", d1[1], 1000)
    _test("Datalogger_04", d1[2], 0)
    _test("Datalogger_05", d1[3], 0)
    _test("Datalogger_06", d1[4], 0)

    d0 = d1[:]
    d1 = _readAllWordFrame(dlQueue)
    d1, testDelta = _skipRepeatedAllWordFrame(dlQueue, d0, d1)
    if testDelta:
        _testPeriodFrameDelta("Datalogger_07", d0, d1)
    _test("Datalogger_08", d1[1], 1000)
    _test("Datalogger_09", d1[2], 2000)
    _test("Datalogger_10", d1[3], 0)
    _test("Datalogger_11", d1[4], 0)

    d0 = d1[:]
    d1 = _readAllWordFrame(dlQueue)
    d1, testDelta = _skipRepeatedAllWordFrame(dlQueue, d0, d1)
    if testDelta:
        _testPeriodFrameDelta("Datalogger_12", d0, d1)
    _test("Datalogger_13", d1[1], 1000)
    _test("Datalogger_14", d1[2], 2000)
    _test("Datalogger_15", d1[3], 3000)
    _test("Datalogger_16", d1[4], 0)

    d0 = d1[:]
    d1 = _readAllWordFrame(dlQueue)
    d1, testDelta = _skipRepeatedAllWordFrame(dlQueue, d0, d1)
    if testDelta:
        _testPeriodFrameDelta("Datalogger_17", d0, d1)
    _test("Datalogger_18", d1[1], 1000)
    _test("Datalogger_19", d1[2], 2000)
    _test("Datalogger_20", d1[3], 3000)
    _test("Datalogger_21", d1[4], 4000)


def _runPeriodicMixedDataLoggerTest(swdl, dlQueue, p0, p8, p10, p17):
    swdl.enable(False)
    _clearPublicData(p0, p8, p10, p17)

    dlQueue.begin(DLQUEUEADDR, DLQUEUELENGTH)
    swdl.begin(
        DLQUEUEADDR,
        DLQUEUELENGTH,
        True,  # Queue Frame Index
        False,  # QueueOnChange
        SerialWombat18ABDataLogger.DataLoggerPeriod.PERIOD_128mS,
    )

    swdl.configurePin(0, True, True)
    swdl.configurePin(8, True, True)
    swdl.configurePin(10, True, False)
    swdl.configurePin(17, False, True)
    swdl.enable(True)
    _writeStepPattern(p0, p8, p10, p17, [130, 130, 130, 130, 130])
    swdl.enable(False)

    # Should be at least 40 data bytes available, no more than 48
    i = dlQueue.available()
    if i >= 40 and i <= 48:
        i = 40
    _test("DataLogger_22", i, 40)

    d0 = _readMixedFrame(dlQueue)
    d1 = _readMixedFrame(dlQueue)

    # Test that first entry is all 0's
    for i in range(1, 5):
        _test(f"Datalogger_21_{i}", d0[i], 0)

    d1, testDelta = _skipRepeatedMixedFrame(dlQueue, d0, d1)
    if testDelta:
        _testPeriodFrameDelta("Datalogger_22", d0, d1)
    _test("Datalogger_23", d1[1], 1000)
    _test("Datalogger_24", d1[2], 0)
    _test("Datalogger_25", d1[3], 0)
    _test("Datalogger_26", d1[4], 0)

    d0 = d1[:]
    d1 = _readMixedFrame(dlQueue)
    d1, testDelta = _skipRepeatedMixedFrame(dlQueue, d0, d1)
    if testDelta:
        _testPeriodFrameDelta("Datalogger_27", d0, d1)
    _test("Datalogger_28", d1[1], 1000)
    _test("Datalogger_29", d1[2], 2000)
    _test("Datalogger_30", d1[3], 0)
    _test("Datalogger_31", d1[4], 0)

    d0 = d1[:]
    d1 = _readMixedFrame(dlQueue)
    d1, testDelta = _skipRepeatedMixedFrame(dlQueue, d0, d1)
    if testDelta:
        _testPeriodFrameDelta("Datalogger_32", d0, d1)
    _test("Datalogger_33", d1[1], 1000)
    _test("Datalogger_34", d1[2], 2000)
    _test("Datalogger_35", d1[3], 3000 & 0xFF)
    _test("Datalogger_36", d1[4], 0)

    d0 = d1[:]
    d1 = _readMixedFrame(dlQueue)
    d1, testDelta = _skipRepeatedMixedFrame(dlQueue, d0, d1)
    if testDelta:
        _testPeriodFrameDelta("Datalogger_37", d0, d1)
    _test("Datalogger_38", d1[1], 1000)
    _test("Datalogger_39", d1[2], 2000)
    _test("Datalogger_40", d1[3], 3000 & 0xFF)
    _test("Datalogger_41", d1[4], 4000 >> 8)


def _runChangeMixedDataLoggerTest(swdl, dlQueue, p0, p8, p10, p17):
    swdl.enable(False)
    _clearPublicData(p0, p8, p10, p17)

    dlQueue.begin(DLQUEUEADDR, DLQUEUELENGTH)
    swdl.begin(
        DLQUEUEADDR,
        DLQUEUELENGTH,
        True,  # Queue Frame Index
        True,  # QueueOnChange
    )

    swdl.configurePin(0, True, True)
    swdl.configurePin(8, True, True)
    swdl.configurePin(10, True, False)
    swdl.configurePin(17, False, True)
    swdl.enable(True)
    _writeStepPattern(p0, p8, p10, p17, [100, 200, 300, 400, 500])
    swdl.enable(False)

    # Should be at least 40 data bytes available, no more than 48
    i = dlQueue.available()
    if i >= 40 and i <= 48:
        i = 40
    _test("DataLogger_42", i, 40)

    d0 = _readMixedFrame(dlQueue)
    d1 = _readMixedFrame(dlQueue)

    # Test that first entry is all 0's
    for i in range(1, 5):
        _test(f"Datalogger_42_{i}", d0[i], 0)

    d1, testDelta = _skipRepeatedMixedFrame(dlQueue, d0, d1)
    if testDelta:
        _testChangeFrameDelta("Datalogger_43", d0, d1, 100)
    _test("Datalogger_44", d1[1], 1000)
    _test("Datalogger_45", d1[2], 0)
    _test("Datalogger_46", d1[3], 0)
    _test("Datalogger_47", d1[4], 0)

    d0 = d1[:]
    d1 = _readMixedFrame(dlQueue)
    d1, testDelta = _skipRepeatedMixedFrame(dlQueue, d0, d1)
    if testDelta:
        _testChangeFrameDelta("Datalogger_48", d0, d1, 200)
    _test("Datalogger_49", d1[1], 1000)
    _test("Datalogger_50", d1[2], 2000)
    _test("Datalogger_51", d1[3], 0)
    _test("Datalogger_52", d1[4], 0)

    d0 = d1[:]
    d1 = _readMixedFrame(dlQueue)
    d1, testDelta = _skipRepeatedMixedFrame(dlQueue, d0, d1)
    if testDelta:
        _testChangeFrameDelta("Datalogger_53", d0, d1, 300)
    _test("Datalogger_54", d1[1], 1000)
    _test("Datalogger_55", d1[2], 2000)
    _test("Datalogger_56", d1[3], 3000 & 0xFF)
    _test("Datalogger_57", d1[4], 0)

    d0 = d1[:]
    d1 = _readMixedFrame(dlQueue)
    d1, testDelta = _skipRepeatedMixedFrame(dlQueue, d0, d1)
    if testDelta:
        _testChangeFrameDelta("Datalogger_58", d0, d1, 400)
    _test("Datalogger_59", d1[1], 1000)
    _test("Datalogger_60", d1[2], 2000)
    _test("Datalogger_61", d1[3], 3000 & 0xFF)
    _test("Datalogger_62", d1[4], 4000 >> 8)


def dataLoggerTest():
    swdl = SerialWombat18ABDataLogger.SerialWombat18ABDataLogger(SW18B_UnitTest_globals.SW18AB_6B)
    dlQueue = SerialWombatQueue.SerialWombatQueue(SW18B_UnitTest_globals.SW18AB_6B)

    SW18B_UnitTest_globals.resetAll()

    # Set to PWMs to allow config of public data
    p0, p8, p10, p17 = _beginPWMOutputs()

    _runPeriodicAllWordDataLoggerTest(swdl, dlQueue, p0, p8, p10, p17)
    _runPeriodicMixedDataLoggerTest(swdl, dlQueue, p0, p8, p10, p17)
    _runChangeMixedDataLoggerTest(swdl, dlQueue, p0, p8, p10, p17)
