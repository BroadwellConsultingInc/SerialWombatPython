import SW18B_UnitTest_globals
import SerialWombatPWM

try:
    from ArduinoFunctions import delay
except ImportError:
    import time

    def delay(milliseconds):
        time.sleep(milliseconds / 1000.0)


PWM_TEST_INCREMENTS = 100


def _uint16(value):
    return value & 0xFFFF


def _buildPWMArrays():
    SW18AB_PWM0 = SerialWombatPWM.SerialWombatPWM_18AB(SW18B_UnitTest_globals.SW18AB_6B)
    # SW18AB_PWM1 = SerialWombatPWM.SerialWombatPWM_18AB(SW18B_UnitTest_globals.SW18AB_6B)
    # SW18AB_PWM2 = SerialWombatPWM.SerialWombatPWM_18AB(SW18B_UnitTest_globals.SW18AB_6B)
    # SW18AB_PWM3 = SerialWombatPWM.SerialWombatPWM_18AB(SW18B_UnitTest_globals.SW18AB_6B)
    # SW18AB_PWM4 = SerialWombatPWM.SerialWombatPWM_18AB(SW18B_UnitTest_globals.SW18AB_6B)
    SW18AB_PWM5 = SerialWombatPWM.SerialWombatPWM_18AB(SW18B_UnitTest_globals.SW18AB_6B)
    SW18AB_PWM6 = SerialWombatPWM.SerialWombatPWM_18AB(SW18B_UnitTest_globals.SW18AB_6B)
    SW18AB_PWM7 = SerialWombatPWM.SerialWombatPWM_18AB(SW18B_UnitTest_globals.SW18AB_6B)
    SW18AB_PWM8 = SerialWombatPWM.SerialWombatPWM_18AB(SW18B_UnitTest_globals.SW18AB_6B)
    SW18AB_PWM9 = SerialWombatPWM.SerialWombatPWM_18AB(SW18B_UnitTest_globals.SW18AB_6B)
    SW18AB_PWM10 = SerialWombatPWM.SerialWombatPWM_18AB(SW18B_UnitTest_globals.SW18AB_6B)
    SW18AB_PWM11 = SerialWombatPWM.SerialWombatPWM_18AB(SW18B_UnitTest_globals.SW18AB_6B)
    SW18AB_PWM12 = SerialWombatPWM.SerialWombatPWM_18AB(SW18B_UnitTest_globals.SW18AB_6B)
    SW18AB_PWM13 = SerialWombatPWM.SerialWombatPWM_18AB(SW18B_UnitTest_globals.SW18AB_6B)
    SW18AB_PWM14 = SerialWombatPWM.SerialWombatPWM_18AB(SW18B_UnitTest_globals.SW18AB_6B)
    SW18AB_PWM15 = SerialWombatPWM.SerialWombatPWM_18AB(SW18B_UnitTest_globals.SW18AB_6B)
    SW18AB_PWM16 = SerialWombatPWM.SerialWombatPWM_18AB(SW18B_UnitTest_globals.SW18AB_6B)
    SW18AB_PWM17 = SerialWombatPWM.SerialWombatPWM_18AB(SW18B_UnitTest_globals.SW18AB_6B)
    SW18AB_PWM18 = SerialWombatPWM.SerialWombatPWM_18AB(SW18B_UnitTest_globals.SW18AB_6B)
    SW18AB_PWM19 = SerialWombatPWM.SerialWombatPWM_18AB(SW18B_UnitTest_globals.SW18AB_6B)

    SW18ABPWMs = [
        SW18AB_PWM0,
        None,
        None,
        None,
        None,
        SW18AB_PWM5,
        SW18AB_PWM6,
        SW18AB_PWM7,
        SW18AB_PWM8,
        SW18AB_PWM9,
        SW18AB_PWM10,
        SW18AB_PWM11,
        SW18AB_PWM12,
        SW18AB_PWM13,
        SW18AB_PWM14,
        SW18AB_PWM15,
        SW18AB_PWM16,
        SW18AB_PWM17,
        SW18AB_PWM18,
        SW18AB_PWM19,
    ]

    SW8B_PWM0 = SerialWombatPWM.SerialWombatPWM_18AB(SW18B_UnitTest_globals.SW8B_68)
    SW8B_PWM1 = SerialWombatPWM.SerialWombatPWM_18AB(SW18B_UnitTest_globals.SW8B_68)
    SW8B_PWM2 = SerialWombatPWM.SerialWombatPWM_18AB(SW18B_UnitTest_globals.SW8B_68)
    SW8B_PWM3 = SerialWombatPWM.SerialWombatPWM_18AB(SW18B_UnitTest_globals.SW8B_68)
    SW8B_PWM4 = SerialWombatPWM.SerialWombatPWM_18AB(SW18B_UnitTest_globals.SW8B_68)
    SW8B_PWM5 = SerialWombatPWM.SerialWombatPWM_18AB(SW18B_UnitTest_globals.SW8B_68)
    SW8B_PWM6 = SerialWombatPWM.SerialWombatPWM_18AB(SW18B_UnitTest_globals.SW8B_68)
    SW8B_PWM7 = SerialWombatPWM.SerialWombatPWM_18AB(SW18B_UnitTest_globals.SW8B_68)

    SW8BPWMs = [
        SW8B_PWM0,
        SW8B_PWM1,
        SW8B_PWM2,
        SW8B_PWM3,
        SW8B_PWM4,
        SW8B_PWM5,
        SW8B_PWM6,
        SW8B_PWM7,
    ]

    return SW18ABPWMs, SW8BPWMs





def _testValue(designator, value, expected, counts, sixtyFourths):
    if hasattr(SW18B_UnitTest_globals, "test_value"):
        SW18B_UnitTest_globals.test_value(designator, value, expected, counts, sixtyFourths)
    else:
        SW18B_UnitTest_globals.test(designator, value, expected, counts, sixtyFourths)


def pwmTest(sw=None, startPin=18, endPin=19):
    if sw is None:
        sw = SW18B_UnitTest_globals.SW18AB_6B

    SW18B_UnitTest_globals.resetAll()
    for pin in range(startPin, endPin + 1):
        if not SW18B_UnitTest_globals.test_pinCanBeOutput(sw, pin):
            continue

        SW18B_UnitTest_globals.initializePulseReaduS(sw, pin)

    SW18ABPWMs, SW8BPWMs = _buildPWMArrays()

    PWMArray = None
    if sw is SW18B_UnitTest_globals.SW18AB_6B:
        PWMArray = SW18ABPWMs
    elif sw is SW18B_UnitTest_globals.SW8B_68:
        PWMArray = SW8BPWMs
    # elif sw is SW18B_UnitTest_globals.SW4B_6C:
    #     PWMArray = SW4BPWMs
    else:
        print("Invalid chip for pwm test")
        return

    pwmPeriod_uS = 122
    while pwmPeriod_uS <= 50000:
        for pin in range(startPin, endPin + 1):
            if not SW18B_UnitTest_globals.test_pinCanBeOutput(sw, pin):
                continue

            PWMArray[pin].begin(pin, 0)
            PWMArray[pin].writePeriod_uS(pwmPeriod_uS)

        for duty in range(0x0100, 0xE000 + 1, 0x1000):
            for pin in range(startPin, endPin + 1):
                if not SW18B_UnitTest_globals.test_pinCanBeOutput(sw, pin):
                    continue

                pinDuty = _uint16(duty + 0x1000 * pin)
                if pinDuty == 0:
                    pinDuty = 0x1000
                PWMArray[pin].writePublicData(pinDuty)

            delay((10 * pwmPeriod_uS) // 1000)
            for pin in range(startPin, endPin + 1):
                if not SW18B_UnitTest_globals.test_pinCanBeOutput(sw, pin):
                    continue

                pinDuty = _uint16(duty + 0x1000 * pin)
                result = SW18B_UnitTest_globals.pulseRead(sw, pin)
                setting = (pwmPeriod_uS * pinDuty) >> 16
                if setting < 50:
                    continue

                s = f"PWM 01 Pin: {pin} Period: {pwmPeriod_uS} Duty cycle: {pinDuty} "
                _testValue(s, result, setting, 30, 5)

        pwmPeriod_uS *= 2
