import SW18B_UnitTest_globals
import SerialWombatDebouncedInput
import SerialWombatPWM

try:
    from ArduinoFunctions import delay
except ImportError:
    import time

    def delay(milliseconds):
        time.sleep(milliseconds / 1000.0)


def _pass(i):
    if hasattr(SW18B_UnitTest_globals, "pass_"):
        SW18B_UnitTest_globals.pass_(i)
    else:
        SW18B_UnitTest_globals.test("Pass helper missing", 1)


def _fail(i):
    SW18B_UnitTest_globals.fail(i)


def _test(message, value):
    SW18B_UnitTest_globals.test(message, value)


def _get_pwm_frequency(pwm, name):
    if hasattr(pwm, name):
        return getattr(pwm, name)

    frequency_values = getattr(SerialWombatPWM, "Wombat4A_B_PWMFrequencyValues_t", None)
    if frequency_values is not None and hasattr(frequency_values, name):
        return getattr(frequency_values, name)

    if hasattr(SerialWombatPWM, name):
        return getattr(SerialWombatPWM, name)

    raise AttributeError(f"Unable to find Serial Wombat 4A/B PWM frequency constant {name}")


def _buildDebounceTestObjects():
    debouncedInput18 = SerialWombatDebouncedInput.SerialWombatDebouncedInput(
        SW18B_UnitTest_globals.SW18AB_6B
    )
    DBPWM5 = SerialWombatPWM.SerialWombatPWM_4AB(
        SW18B_UnitTest_globals.SW4B_6D
    )

    return debouncedInput18, DBPWM5


def debounceTest(sw=None):
    if sw is None:
        sw = SW18B_UnitTest_globals.SW18AB_6B

    debouncedInput = None

    if sw is SW18B_UnitTest_globals.SW18AB_6B:
        SW18ABpin = 5
        debouncedInput18, DBPWM5 = _buildDebounceTestObjects()
        debouncedInput = debouncedInput18

        DBPWM5.begin(SW18B_UnitTest_globals.SW18ABPinTo4BPin(SW18ABpin))
        DBPWM5.setFrequency_SW4AB(_get_pwm_frequency(DBPWM5, "SW4AB_PWMFrequency_125_Hz"))
        DBPWM5.writeDutyCycle(0x8000)  # 4 ms
        debouncedInput.begin(SW18ABpin, 6, False, False)  # 6ms time.
        delay(500)
        debouncedInput.readTransitionsState()

        if debouncedInput.transitions < 2:
            _pass(1)
        else:
            _fail(1)

        DBPWM5.setFrequency_SW4AB(_get_pwm_frequency(DBPWM5, "SW4AB_PWMFrequency_63_Hz"))
        DBPWM5.writeDutyCycle(0x8000)  # 8 ms
        delay(500)
        debouncedInput.readTransitionsState()
        if debouncedInput.transitions < 15:
            _fail(1)
        else:
            _pass(1)

        DBPWM5.begin(SW18B_UnitTest_globals.SW18ABPinTo4BPin(SW18ABpin))
        DBPWM5.setFrequency_SW4AB(_get_pwm_frequency(DBPWM5, "SW4AB_PWMFrequency_125_Hz"))
        DBPWM5.writeDutyCycle(0xF000)
        delay(100)
        if debouncedInput.readTransitionsState():
            _pass(1)
        else:
            _fail(1)

        DBPWM5.writeDutyCycle(0x1000)
        delay(100)
        if debouncedInput.readTransitionsState():
            _fail(1)
        else:
            _pass(1)

    elif sw is SW18B_UnitTest_globals.SW8B_68:
        _test("Debounce for SW8B Not Implemented. ", 0)
    elif sw is SW18B_UnitTest_globals.SW4B_6C:
        _test("Debounce for SW4B Not Implemented. ", 0)
