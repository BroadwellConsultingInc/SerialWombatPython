import SW18B_UnitTest_globals
import SerialWombat
import SerialWombatThroughputConsumer

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


DS = SerialWombat.SerialWombatDataSource

tc18 = SerialWombatThroughputConsumer.SerialWombatThroughputConsumer(
    SW18B_UnitTest_globals.SW18AB_6B
)


def _test(designator, value, expected):
    SW18B_UnitTest_globals.test_value(designator, value, expected, 0, 0)


def _pass_or_fail(passed, test_number=1):
    if passed:
        SW18B_UnitTest_globals.pass_(test_number)
    else:
        SW18B_UnitTest_globals.fail(test_number)


def _frames_from_words(msw, lsw):
    return ((int(msw) & 0xFFFF) << 16) + (int(lsw) & 0xFFFF)


def publicDataTest(sw):
    number = sw.readPublicData(DS.SW_DATA_SOURCE_INCREMENTING_NUMBER)

    for i in range(1, 500):
        result = sw.readPublicData(DS.SW_DATA_SOURCE_INCREMENTING_NUMBER)
        _pass_or_fail(result == number + i)

    print("SW_DATA_SOURCE_1024mvCounts test not implemented")

    framesLSW = sw.readPublicData(DS.SW_DATA_SOURCE_FRAMES_RUN_LSW)
    framesMSW = sw.readPublicData(DS.SW_DATA_SOURCE_FRAMES_RUN_MSW)
    startTime = millis()
    startFrames = _frames_from_words(framesMSW, framesLSW)

    delay(100000)

    framesLSW = sw.readPublicData(DS.SW_DATA_SOURCE_FRAMES_RUN_LSW)
    framesMSW = sw.readPublicData(DS.SW_DATA_SOURCE_FRAMES_RUN_MSW)
    endTime = millis()
    endFrames = _frames_from_words(framesMSW, framesLSW)

    netTime = int(endTime - startTime)
    netFrames = int(endFrames - startFrames)

    _pass_or_fail(
        netTime < ((netFrames * 21) // 20)
        and netTime > ((netFrames * 19) // 20)
    )

    if sw is SW18B_UnitTest_globals.SW18AB_6B:
        tc18.begin(17)
        number = sw.readPublicData(DS.SW_DATA_SOURCE_OVERRUN_FRAMES)
        numDroppedFrames = sw.readPublicData(DS.SW_DATA_SOURCE_DROPPED_FRAMES)
        delay(100)
        finalNumber = sw.readPublicData(DS.SW_DATA_SOURCE_OVERRUN_FRAMES)
        _pass_or_fail(finalNumber == number)

        tc18.write(0, 1200)

        number = sw.readPublicData(DS.SW_DATA_SOURCE_OVERRUN_FRAMES)
        delay(100)
        finalNumber = sw.readPublicData(DS.SW_DATA_SOURCE_OVERRUN_FRAMES)
        _pass_or_fail(finalNumber >= number + 5)

        tc18.begin(17)

        finalNumDroppedFrames = sw.readPublicData(DS.SW_DATA_SOURCE_DROPPED_FRAMES)
        _pass_or_fail(numDroppedFrames == finalNumDroppedFrames)

        numDroppedFrames = finalNumDroppedFrames
        tc18.write(0, 2200)

        delay(100)
        # This preserves the Arduino test source selection exactly.
        finalNumDroppedFrames = sw.readPublicData(DS.SW_DATA_SOURCE_OVERRUN_FRAMES)
        _pass_or_fail(finalNumDroppedFrames >= numDroppedFrames + 5)

        tc18.begin(17)
        delay(1000)
        systemUtilization = sw.readPublicData(DS.SW_DATA_SOURCE_SYSTEM_UTILIZATION)
        tc18.writeAll(200)
        delay(1000)
        systemUtilization2 = sw.readPublicData(DS.SW_DATA_SOURCE_SYSTEM_UTILIZATION)
        tc18.begin(17)

        difference = int(systemUtilization2) - int(systemUtilization)
        if difference > 10000 and difference < 16000:
            SW18B_UnitTest_globals.pass_(1)
        else:
            print("SU: ")
            print(systemUtilization)
            print(" SU2: ")
            print(systemUtilization2)
            SW18B_UnitTest_globals.fail(1)

    print("SW_DATA_SOURCE_TEMPERATURE  test not implemented")

    number = sw.readPublicData(DS.SW_DATA_SOURCE_PACKETS_RECEIVED)

    for _ in range(10):
        sw.readPublicData(DS.SW_DATA_SOURCE_INCREMENTING_NUMBER)

    finalNumber = sw.readPublicData(DS.SW_DATA_SOURCE_PACKETS_RECEIVED)
    _pass_or_fail(finalNumber == number + 11)

    if sw is SW18B_UnitTest_globals.SW18AB_6B or sw is SW18B_UnitTest_globals.SW8B_68:
        sourceErrorsStart = sw.readPublicData(DS.SW_DATA_SOURCE_ERRORS)

        for _ in range(10):
            sw.readPublicData(DS.SW_DATA_SOURCE_INCREMENTING_NUMBER)

        tx = bytearray([200, 50, 0, 0, 0, 0, 0, 0])  # 50 is an invalid pin number
        sw.sendPacket(tx)
        sourceErrorsEnd = sw.readPublicData(DS.SW_DATA_SOURCE_ERRORS)
        _pass_or_fail(sourceErrorsEnd == sourceErrorsStart + 1)

    print("SW_DATA_SOURCE_LFSR  test not implemented")

    if sw is SW18B_UnitTest_globals.SW18AB_6B:
        a = sw.readPublicData(DS.SW_DATA_COM_ADDRESS_LOW)
        _test("SW_DATA_COM_ADDRESS_LOW SW18AB ", a, 0x6B)

    if sw is SW18B_UnitTest_globals.SW8B_68:
        a = sw.readPublicData(DS.SW_DATA_COM_ADDRESS_LOW)
        _test("SW_DATA_COM_ADDRESS_LOW SW18AB ", a, 0x68)

    print("SW_DATA_SOURCE_1024mvCounts test not implemented")
    print("SW_DATA_SOURCE_2HZ_SQUARE and similar  test not implemented")
