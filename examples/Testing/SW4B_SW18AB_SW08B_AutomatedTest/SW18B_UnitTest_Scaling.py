import SW18B_UnitTest_globals
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


SCALING_INPUT_PIN = 5  # 18
SCALING_OUTPUT_PIN = 6  # 19

scalingInput18AB = SerialWombatPWM.SerialWombatPWM_18AB(SW18B_UnitTest_globals.SW18AB_6B)
scalingOutput18AB = SerialWombatPWM.SerialWombatPWM_18AB(SW18B_UnitTest_globals.SW18AB_6B)

scalingInput = scalingInput18AB
scalingOutput = scalingOutput18AB


def _u16(value):
    return int(value) & 0xFFFF


def _withinRange(value, expected, sixtyFourths, counts):
    x32 = int(expected)

    if (value > x32 + counts) and (value > (x32 * (64 + sixtyFourths) // 64)):
        return False
    if (value < x32 - counts) and (value < (x32 * (64 - sixtyFourths) // 64)):
        return False

    return True


def _test_bool(msg, value):
    SW18B_UnitTest_globals.test(msg, 1 if value else 0)


def _test_value(designator, value, expected, counts=0, sixtyFourths=0):
    SW18B_UnitTest_globals.test_value(designator, value, expected, counts, sixtyFourths)


def _pack_u16_table(table):
    data = bytearray()
    for value in table:
        data.append(value & 0xFF)
        data.append((value >> 8) & 0xFF)
    return data


def scalingTest():
    global scalingInput, scalingOutput

    scalingInput = scalingInput18AB
    scalingOutput = scalingOutput18AB

    scalingTimeoutTest()

    scalingInputScalingTest()
    scalingInvertScalingTest()
    scalingOutputScalingTest()

    scalingRateControl16HzTest()
    scaling1stOrderTest()
    scalingHysteresisTest()

    scalingSOLinearInterpolationTest()

    if False:
        # PID test section from the Arduino source is disabled with if (0).
        scalingInput.begin(SCALING_INPUT_PIN)
        scalingOutput.begin(SCALING_OUTPUT_PIN)
        scalingOutput.writeScalingEnabled(False, SCALING_INPUT_PIN)

        kp = 0x100  # 256.00
        ki = 0x0  # 0
        kd = 0
        target = 10000
        processOutput = 8000

        scalingOutput.writePID(kp, ki, kd, target, scalingOutput.PERIOD_128mS)
        scalingInput.writePublicData(processOutput)
        scalingOutput.writeScalingEnabled(True, SCALING_INPUT_PIN)

        _test_value("SCALE_PID_01", scalingOutput.readPublicData(), ((target - processOutput) * kp) >> 8)

        kp = 200
        ki = 300
        scalingOutput.writePID(kp, ki, kd, target, scalingOutput.PERIOD_128mS)
        result = 0
        while result < 65535:
            result = scalingOutput.readPublicData()
            process = result - 16000
            if process < 0:
                process = 0

            scalingInput.writePublicData(process)
            print(result, process)


def scalingTimeoutTest():
    # Timeout Test
    SW18B_UnitTest_globals.resetAll()

    scalingInput.begin(SCALING_INPUT_PIN)
    scalingOutput.begin(SCALING_OUTPUT_PIN)
    scalingOutput.writeScalingEnabled(False, SCALING_INPUT_PIN)
    scalingOutput.writeScalingEnabled(False, SCALING_OUTPUT_PIN)
    scalingOutput.writeScalingEnabled(True, SCALING_OUTPUT_PIN)
    SW18B_UnitTest_globals.SW18AB_6B.writePublicData(SCALING_OUTPUT_PIN, 0x0000)
    scalingOutput.writeTimeout(1000, 0x8000)
    startTime = millis()
    while millis() < startTime + 900:
        if scalingOutput.readLastOutputValue() == 0:
            SW18B_UnitTest_globals.pass_(0)
        else:
            SW18B_UnitTest_globals.fail(1)
            print("F0")
        delay(100)
    delay(200)
    v = scalingOutput.readLastOutputValue()
    x = 0x8000
    if v == x:
        SW18B_UnitTest_globals.pass_(0)
    else:
        SW18B_UnitTest_globals.fail(2)
        print(f"F0.  V: {v} X:{x}")


def scalingInputScalingTest():
    # Input Scaling Test
    SW18B_UnitTest_globals.resetAll()

    scalingInput.begin(SCALING_INPUT_PIN)
    scalingOutput.begin(SCALING_OUTPUT_PIN)
    lowLimit = 3000
    highLimit = 50000

    scalingOutput.writeScalingEnabled(False, SCALING_INPUT_PIN)
    scalingOutput.writeScalingEnabled(True, SCALING_INPUT_PIN)

    for i in range(0, 65536, 10):
        SW18B_UnitTest_globals.SW18AB_6B.writePublicData(SCALING_INPUT_PIN, i)
        scalingOutput.writeInputScaling(lowLimit, highLimit)
        delay(10)
        expected = 0
        if i > lowLimit:
            if i > highLimit:
                expected = 65535
            else:
                expected = int(((i - lowLimit) / float(highLimit - lowLimit)) * 65535)

        value = scalingOutput.readPublicData()

        if _withinRange(value, expected, 0, 1):
            SW18B_UnitTest_globals.pass_(1)
        else:
            SW18B_UnitTest_globals.fail(1)
            print(f"F1. i: {i} V: {value} X:{expected}")


def scalingInvertScalingTest():
    # Invert Scaling Test
    scalingInput.begin(SCALING_INPUT_PIN)
    scalingOutput.begin(SCALING_OUTPUT_PIN)
    lowLimit = 3000
    highLimit = 50000
    scalingOutput.writeScalingEnabled(False, SCALING_INPUT_PIN)
    scalingOutput.writeScalingEnabled(True, SCALING_INPUT_PIN)
    scalingOutput.writeScalingInvertedInput(True)

    for i in range(0, 65536, 10):
        SW18B_UnitTest_globals.SW18AB_6B.writePublicData(SCALING_INPUT_PIN, i)
        scalingOutput.writeOutputScaling(lowLimit, highLimit)
        delay(10)

        expected = int((highLimit - lowLimit) * float(65535 - i) / 65535 + lowLimit)
        value = scalingOutput.readPublicData()

        if _withinRange(value, expected, 0, 1):
            SW18B_UnitTest_globals.pass_(1)
        else:
            SW18B_UnitTest_globals.fail(1)
            print(f"F2. i: {i} V: {value} X:{expected}")


def scalingOutputScalingTest():
    # Output Scaling Test
    scalingInput.begin(SCALING_INPUT_PIN)
    scalingOutput.begin(SCALING_OUTPUT_PIN)
    lowLimit = 3000
    highLimit = 50000
    scalingOutput.writeScalingEnabled(False, SCALING_INPUT_PIN)
    scalingOutput.writeScalingEnabled(True, SCALING_INPUT_PIN)

    for i in range(0, 65536, 10):
        SW18B_UnitTest_globals.SW18AB_6B.writePublicData(SCALING_INPUT_PIN, i)
        scalingOutput.writeOutputScaling(lowLimit, highLimit)
        delay(10)

        expected = int((highLimit - lowLimit) * float(i) / 65535 + lowLimit)
        value = scalingOutput.readPublicData()

        if _withinRange(value, expected, 0, 1):
            SW18B_UnitTest_globals.pass_(1)
        else:
            SW18B_UnitTest_globals.fail(1)
            print(f"F3. i: {i} V: {value} X:{expected}")


def scalingRateControl16HzTest():
    # Rate Control Test 16 Hz, dual pin
    scalingInput.begin(SCALING_INPUT_PIN)
    scalingOutput.begin(SCALING_OUTPUT_PIN)
    SW18B_UnitTest_globals.SW18AB_6B.writePublicData(SCALING_OUTPUT_PIN, 0)

    scalingOutput.writeScalingEnabled(False, SCALING_INPUT_PIN)

    scalingOutput.writeRateControl(scalingOutput.PERIOD_64mS, 100)
    scalingOutput.writeScalingEnabled(True, SCALING_INPUT_PIN)
    SW18B_UnitTest_globals.SW18AB_6B.writePublicData(SCALING_INPUT_PIN, 1000)
    while scalingOutput.readPublicData() == 0:
        pass

    for i in range(1, 10):
        value = scalingOutput.readPublicData()

        if _withinRange(value, i * 100, 0, 0):
            SW18B_UnitTest_globals.pass_(1)
        else:
            SW18B_UnitTest_globals.fail(1)
            print(f"F8. i: {i} V: {value} X:{i * 100}")
        delay(64)

    for i in range(1, 10):
        value = scalingOutput.readPublicData()

        if _withinRange(value, 1000, 0, 0):
            SW18B_UnitTest_globals.pass_(1)
        else:
            SW18B_UnitTest_globals.fail(1)
            print(f"F9. i: {i} V: {value} X:{1000}")
        delay(64)

    SW18B_UnitTest_globals.SW18AB_6B.writePublicData(SCALING_INPUT_PIN, 500)
    expected = 1000
    for i in range(0, 5):
        value = scalingOutput.readPublicData()

        if _withinRange(value, expected, 0, 0):
            SW18B_UnitTest_globals.pass_(1)
        else:
            SW18B_UnitTest_globals.fail(1)
            print(f"F10. i: {i} V: {value} X:{expected}")

        expected -= 100
        delay(64)

    for i in range(1, 10):
        value = scalingOutput.readPublicData()

        if _withinRange(value, 500, 0, 0):
            SW18B_UnitTest_globals.pass_(1)
        else:
            SW18B_UnitTest_globals.fail(1)
            print(f"F11. i: {i} V: {value} X:{500}")
        delay(64)


def scaling1stOrderTest():
    # 1stOrderFiltering, different pins
    scalingInput.begin(SCALING_INPUT_PIN)
    scalingOutput.begin(SCALING_OUTPUT_PIN)
    SW18B_UnitTest_globals.SW18AB_6B.writePublicData(SCALING_OUTPUT_PIN, 0)

    scalingOutput.writeScalingEnabled(False, SCALING_INPUT_PIN)
    scalingOutput.write1stOrderFiltering(scalingOutput.PERIOD_8mS, 65000)
    scalingOutput.writeScalingEnabled(True, SCALING_INPUT_PIN)
    SW18B_UnitTest_globals.SW18AB_6B.writePublicData(SCALING_INPUT_PIN, 10000)

    value = scalingOutput.readPublicData()
    startTime = millis()
    while value < 9700:
        value = scalingOutput.readPublicData()
        delay(0)
    endTime = millis()
    elapsed = endTime - startTime  # Should take about 3400mS

    if _withinRange(elapsed, 3400, 0, 200):
        SW18B_UnitTest_globals.pass_(1)
    else:
        SW18B_UnitTest_globals.fail(1)
        print(f"F12.  Critical!  V: {elapsed} X:{3400}")


def scalingHysteresisTest():
    # Hysteresis
    SW18B_UnitTest_globals.resetAll()
    scalingInput.begin(SCALING_INPUT_PIN)
    scalingOutput.begin(SCALING_OUTPUT_PIN)
    scalingOutput.writeScalingEnabled(False, SCALING_INPUT_PIN)

    lowLimit = 0x5000
    highLimit = 0xA000
    lowValue = 500
    highValue = 1000
    startValue = 750
    midValue = lowLimit + (highLimit - lowLimit) // 2

    scalingInput.writePublicData(midValue)
    scalingOutput.writeScalingEnabled(True, SCALING_INPUT_PIN)
    scalingOutput.writeHysteresis(lowLimit, lowValue, highLimit, highValue, startValue)

    _test_value("SCALE_HYS_01", scalingOutput.readPublicData(), startValue)

    scalingInput.writePublicData(highLimit)
    _test_value("SCALE_HYS_02", scalingOutput.readPublicData(), highValue)

    scalingInput.writePublicData(lowLimit)
    _test_value("SCALE_HYS_03", scalingOutput.readPublicData(), lowValue)

    scalingInput.writePublicData(65535)
    _test_value("SCALE_HYS_04", scalingOutput.readPublicData(), highValue)

    scalingInput.writePublicData(midValue)
    _test_value("SCALE_HYS_05", scalingOutput.readPublicData(), highValue)

    scalingInput.writePublicData(0)
    _test_value("SCALE_HYS_06", scalingOutput.readPublicData(), lowValue)

    scalingInput.writePublicData(midValue)
    _test_value("SCALE_HYS_07", scalingOutput.readPublicData(), lowValue)


def scalingSOLinearInterpolationTest():
    SW18B_UnitTest_globals.resetAll()

    # Linear scaling test. Table is input/output 16-bit point pairs.
    table = [
        0, 0x1000,
        10000, 0x0000,
        20000, 0x8000,
        30000, 0xC000,
        40000, 0xC000,
        0xFFFF, 0,
    ]

    bufferAddr = 0x20  # Was 220 on 6B test
    tableBytes = _pack_u16_table(table)
    SW18B_UnitTest_globals.SW18AB_6B.writeUserBuffer(bufferAddr, tableBytes, len(tableBytes))

    scalingInput.begin(SCALING_INPUT_PIN)
    scalingOutput.begin(SCALING_OUTPUT_PIN)
    scalingOutput.writeScalingEnabled(False, SCALING_INPUT_PIN)
    scalingOutput.Enable2DLookupOutputScaling(bufferAddr)
    scalingOutput.writeScalingEnabled(True, SCALING_INPUT_PIN)

    for i in range(0, 65536):
        scalingInput.writePublicData(i)
        if i == 0:
            _test_value("SCALE_LI_00", scalingOutput.readPublicData(), 0x1000)
        elif i <= 10000:
            _test_value("SCALE_LI_01", scalingOutput.readPublicData(), (10000 - i) * 0x1000 // 10000, 2, 3)
        elif i <= 20000:
            _test_value("SCALE_LI_02", scalingOutput.readPublicData(), (i - 10000) * 0x8000 // 10000, 2, 3)
        elif i <= 30000:
            _test_value("SCALE_LI_03", scalingOutput.readPublicData(), (i - 20000) * 0x4000 // 10000 + 0x8000, 2, 3)
        elif i <= 40000:
            _test_value("SCALE_LI_04", scalingOutput.readPublicData(), 0xC000)
        else:
            _test_value("SCALE_LI_05", scalingOutput.readPublicData(), 0xC000 - (i - 40000) * 0xC000 // (0xFFFF - 40000), 2, 3)
        delay(0)
