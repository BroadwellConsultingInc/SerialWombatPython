import SW18B_UnitTest_globals
import SerialWombatPin
import SerialWombatPWM
import SerialWombatQuadEnc
import SerialWombatSimulatedQuadEnc

try:
    from ArduinoFunctions import delay
except ImportError:
    import time

    def delay(milliseconds):
        time.sleep(milliseconds / 1000.0)


USEQEA = True
QE_ONBOTH_INT = 2
OUTPUT = 1


sw18qeA = SerialWombatQuadEnc.SerialWombatQuadEnc_18AB(SW18B_UnitTest_globals.SW18AB_6B)
sw18qeSimA = SerialWombatSimulatedQuadEnc.SerialWombatSimulatedQuadEnc(
    SW18B_UnitTest_globals.SW4B_6D,
    SW18B_UnitTest_globals.SW4B_6D,
    1,
    2,
    True,
    False,
)
sw18qeSimB = SerialWombatSimulatedQuadEnc.SerialWombatSimulatedQuadEnc(
    SW18B_UnitTest_globals.SW4B_6E,
    SW18B_UnitTest_globals.SW4B_6E,
    1,
    2,
    True,
    False,
)
sw18qeB = SerialWombatQuadEnc.SerialWombatQuadEnc_18AB(SW18B_UnitTest_globals.SW18AB_6B)

sw8qeA = SerialWombatQuadEnc.SerialWombatQuadEnc_18AB(SW18B_UnitTest_globals.SW8B_68)
sw8qeSimA = SerialWombatSimulatedQuadEnc.SerialWombatSimulatedQuadEnc(
    SW18B_UnitTest_globals.SW4B_6F,
    SW18B_UnitTest_globals.SW4B_6E,
    1,
    3,
    True,
    False,
)
sw8qeSimB = SerialWombatSimulatedQuadEnc.SerialWombatSimulatedQuadEnc(
    SW18B_UnitTest_globals.SW4B_6E,
    SW18B_UnitTest_globals.SW4B_6E,
    1,
    2,
    True,
    False,
)
sw8qeB = SerialWombatQuadEnc.SerialWombatQuadEnc_18AB(SW18B_UnitTest_globals.SW8B_68)


def _u16(value):
    return int(value) & 0xFFFF


def _select_quadenc_objects(sw):
    qeA = None
    qeB = None
    qeSimA = None
    qeSimB = None

    if sw is SW18B_UnitTest_globals.SW18AB_6B:
        if USEQEA:
            qeA = sw18qeA
            qeSimA = sw18qeSimA
        qeB = sw18qeB
        qeSimB = sw18qeSimB
    elif sw is SW18B_UnitTest_globals.SW8B_68:
        if USEQEA:
            qeA = sw8qeA
            qeSimA = sw8qeSimA
        qeB = sw8qeB
        qeSimB = sw8qeSimB
    else:
        SW18B_UnitTest_globals.test("Quad Enc invalid Serial Wombat Chip", 0)

    return qeA, qeB, qeSimA, qeSimB


def _begin_quadenc_for_chip(sw, qeA, qeB, qeSimA, qeSimB, pollType=6, debounce_mS=10):
    if sw is SW18B_UnitTest_globals.SW18AB_6B:
        if USEQEA:
            qeSimA.initialize()
            qeA.begin(5, 6, debounce_mS, True, pollType)

        qeSimB.initialize()
        qeB.begin(18, 19, debounce_mS, True, pollType)
    elif sw is SW18B_UnitTest_globals.SW8B_68:
        if USEQEA:
            qeSimA.initialize()
            qeA.begin(3, 2, debounce_mS, True, pollType)

        qeSimB.initialize()
        qeB.begin(6, 7, debounce_mS, True, pollType)
    else:
        SW18B_UnitTest_globals.test("Quad Enc invalid Serial Wombat Chip", 0)


def _service_until_targets_reached(qeSimA, qeSimB):
    while (
        qeSimB.targetPosition != _u16(qeSimB.currentPosition)
        or (USEQEA and qeSimA.targetPosition != _u16(qeSimA.currentPosition))
    ):
        if USEQEA:
            qeSimA.service()
        qeSimB.service()


def QuadEncTest(sw=None):
    if sw is None:
        sw = SW18B_UnitTest_globals.SW18AB_6B

    SW18B_UnitTest_globals.resetAll()

    qeA, qeB, qeSimA, qeSimB = _select_quadenc_objects(sw)

    if sw is SW18B_UnitTest_globals.SW18AB_6B:
        # Test different port error
        print("EXPECTED ERROR HERE - PART OF TEST: ", end="")
        priorErrorCount = sw.errorCount
        qeA.begin(7, 8, 10, True, QE_ONBOTH_INT)
        SW18B_UnitTest_globals.test_value(
            "Quad Enc Port Mismatch: ",
            sw.errorCount,
            priorErrorCount + 1,
            0,
            0,
        )

    for pollType in range(2, 7, 4):
        _begin_quadenc_for_chip(sw, qeA, qeB, qeSimA, qeSimB, pollType)

        target = 30000

        if USEQEA:
            qeA.writePublicData(target)
            qeSimA.targetPosition = target
            qeSimA.currentPosition = target

        qeB.writePublicData(target)
        qeSimB.targetPosition = target
        qeSimB.currentPosition = target

        for testIteration in range(20):
            if USEQEA:
                qeSimA.targetPosition += testIteration

            qeSimB.targetPosition += testIteration

            _service_until_targets_reached(qeSimA, qeSimB)
            delay(10)

            if USEQEA:
                SW18B_UnitTest_globals.test_value(
                    f"QuadEnc_00A_I{testIteration}",
                    qeA.readPublicData(),
                    _u16(qeSimA.currentPosition),
                    0,
                    0,
                )
                qeSimA.targetPosition -= 2 * testIteration

            SW18B_UnitTest_globals.test_value(
                f"QuadEnc_00B_I{testIteration}",
                qeB.readPublicData(),
                _u16(qeSimB.currentPosition),
                0,
                0,
            )

            qeSimB.targetPosition -= 2 * testIteration

            while (
                qeSimB.targetPosition != _u16(qeSimB.currentPosition)
                or (USEQEA and qeSimA.targetPosition != _u16(qeSimA.currentPosition))
            ):
                if USEQEA:
                    qeSimA.service()
                qeSimB.service()
                delay(1)

            delay(10)

            if USEQEA:
                SW18B_UnitTest_globals.test_value(
                    f"QuadEnc_01A_I{testIteration}",
                    qeA.read(),
                    _u16(qeSimA.currentPosition),
                    0,
                    0,
                )

            SW18B_UnitTest_globals.test_value(
                f"QuadEnc_01B_I{testIteration}",
                qeB.read(),
                _u16(qeSimB.currentPosition),
                0,
                0,
            )

    # Increment Increment testing
    increment = 10
    qeSimB.initialize()
    if sw is SW18B_UnitTest_globals.SW18AB_6B:
        qeB.begin(18, 19, 10, True)
        qeB.writeMinMaxIncrementTargetPin(0, 65535, increment,18)
    elif sw is SW18B_UnitTest_globals.SW8B_68:
        qeB.begin(6, 7, 10, True)
        qeB.writeMinMaxIncrementTargetPin(0, 65535, increment,6)

    target = 30000
    qeB.writePublicData(target)
    qeSimB.targetPosition = target
    qeSimB.currentPosition = target

    expectedOutput = 30000
    for testIteration in range(20):
        qeSimB.targetPosition += testIteration
        expectedOutput += testIteration * increment
        while qeSimB.targetPosition != qeSimB.currentPosition:
            qeSimB.service()
            delay(1)
        delay(10)

        SW18B_UnitTest_globals.test_value(
            "QUADENC_INC_A",
            qeB.readPublicData(),
            expectedOutput,
            0,
            0,
        )

        qeSimB.targetPosition -= 2 * testIteration
        expectedOutput -= 2 * testIteration * increment

        while qeSimB.targetPosition != _u16(qeSimB.currentPosition):
            qeSimB.service()
            delay(1)
        delay(10)

        SW18B_UnitTest_globals.test_value(
            "QUADENC_INC_B",
            qeB.readPublicData(),
            expectedOutput,
            0,
            0,
        )

    # Minimum testing
    increment = 10
    qeSimB.initialize()
    if sw is SW18B_UnitTest_globals.SW18AB_6B:
        qeB.begin(18, 19, 10, True)
        qeB.writeMinMaxIncrementTargetPin(0, 65535, increment,18)
    elif sw is SW18B_UnitTest_globals.SW8B_68:
        qeB.begin(6, 7, 10, True)
        qeB.writeMinMaxIncrementTargetPin(29999, 65535, increment,6)

    target = 30000
    qeB.writePublicData(target)
    qeSimB.targetPosition = target
    qeSimB.currentPosition = target

    qeSimB.targetPosition = 29500
    while qeSimB.targetPosition != _u16(qeSimB.currentPosition):
        qeSimB.service()
        delay(1)
    delay(10)

    SW18B_UnitTest_globals.test_value(
        "QUADENC_MIN_A",
        qeB.readPublicData(),
        29999,
        0,
        0,
    )

    # Maximum testing
    increment = 10
    qeSimB.initialize()
    if sw is SW18B_UnitTest_globals.SW18AB_6B:
        qeB.begin(18, 19, 10, True)
        qeB.writeMinMaxIncrementTargetPin(0, 30500, increment,18)
    elif sw is SW18B_UnitTest_globals.SW8B_68:
        qeB.begin(6, 7, 10, True)
        qeB.writeMinMaxIncrementTargetPin(0, 30500, increment,6)

    target = 30000
    qeB.writePublicData(target)
    qeSimB.targetPosition = target
    qeSimB.currentPosition = target

    qeSimB.targetPosition = 36000
    while qeSimB.targetPosition != _u16(qeSimB.currentPosition):
        qeSimB.service()
        delay(1)
    delay(10)

    SW18B_UnitTest_globals.test_value(
        "QUADENC_MAX_A",
        qeB.readPublicData(),
        30500,
        0,
        0,
    )

    # Target Pin testing
    servo = SerialWombatPin.SerialWombatPin(sw)
    servo._pin = 0
    servo.pinMode(OUTPUT)
    servo.writePublicData(30000)

    increment = 10
    qeSimB.initialize()
    if sw is SW18B_UnitTest_globals.SW18AB_6B:
        qeB.begin(18, 19, 10, True)
    elif sw is SW18B_UnitTest_globals.SW8B_68:
        qeB.begin(6, 7, 10, True)
    qeB.writeMinMaxIncrementTargetPin(0, 65535, increment, 0)

    target = 30000
    qeB.writePublicData(target)
    qeSimB.targetPosition = target
    qeSimB.currentPosition = target

    expectedOutput = 30000
    for testIteration in range(20):
        qeSimB.targetPosition += testIteration
        expectedOutput += testIteration * increment
        while qeSimB.targetPosition != qeSimB.currentPosition:
            qeSimB.service()
            delay(1)
        delay(10)

        SW18B_UnitTest_globals.test_value(
            "QUADENC_TARGET_PIN_A",
            servo.readPublicData(),
            expectedOutput,
            0,
            0,
        )

        qeSimB.targetPosition -= 2 * testIteration
        expectedOutput -= 2 * testIteration * increment

        while qeSimB.targetPosition != _u16(qeSimB.currentPosition):
            qeSimB.service()
            delay(1)
        delay(10)

        SW18B_UnitTest_globals.test_value(
            "QUADENC_TARGET_PIN_B",
            servo.readPublicData(),
            expectedOutput,
            0,
            0,
        )

    # Frequency testing
    SW18B_UnitTest_globals.resetAll()
    if sw is SW18B_UnitTest_globals.SW18AB_6B:
        qeB.begin(18, 19, 1, True)  # 1mS debounce
    elif sw is SW18B_UnitTest_globals.SW8B_68:
        qeB.begin(6, 7, 1, True)  # 1mS debounce

    sw4b = SW18B_UnitTest_globals.SWChipAndPinTo4BChip(sw, qeB.pin())
    sw4bPin = SW18B_UnitTest_globals.SWChipAndPinTo4BPin(sw, qeB.pin())

    if sw4bPin == 0:
        SW18B_UnitTest_globals.test("QuadEnc Test SW4B 0 pin isn't output", 0)

    pwm4B = SerialWombatPWM.SerialWombatPWM_4AB(sw4b)
    pwm4B.begin(sw4bPin)
    pwm4B.setFrequency_SW4AB(pwm4B.SW4AB_PWMFrequency_125_Hz)
    pwm4B.writePublicData(0x8000)

    delay(3000)

    SW18B_UnitTest_globals.test_value(
        "QUADENC_FREQ_A",
        qeB.readFrequency(),
        125,
        10,
        0,
    )
    SW18B_UnitTest_globals.test_value(
        "QUADENC_FREQ_B",
        sw.readPublicData(qeB.pin() + 1),
        125,
        10,
        0,
    )
