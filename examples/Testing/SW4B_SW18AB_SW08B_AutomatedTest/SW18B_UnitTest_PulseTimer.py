import SW18B_UnitTest_globals
import SerialWombatPulseTimer
import SerialWombatPWM

try:
    from ArduinoFunctions import delay
except ImportError:
    import time

    def delay(milliseconds):
        time.sleep(milliseconds / 1000.0)


SW_PULSETIMER_uS = 0
SW_PULSETIMER_mS = 1


def _testValue(designator, value, expected, counts=0, sixtyFourths=0):
    SW18B_UnitTest_globals.test_value(designator, value, expected, counts, sixtyFourths)


def _test(message, value):
    SW18B_UnitTest_globals.test(message, value)


def _getSW4BPin(sw, pin):
    if sw is SW18B_UnitTest_globals.SW18AB_6B:
        return SW18B_UnitTest_globals.SW18ABPinTo4BPin(pin)
    elif sw is SW18B_UnitTest_globals.SW8B_68:
        return SW18B_UnitTest_globals.SW8BPinTo4BPin(pin)
    else:
        _test("Pulse Timer Test invalid Serial Wombat Chip", 0)
        return 0


def pulseTimerTest(sw=None, startPin=0, endPin=19):
    if sw is None:
        sw = SW18B_UnitTest_globals.SW18AB_6B

    SW18B_UnitTest_globals.resetAll()

    # Duty cycle test
    pulseTimers = {}
    for pin in range(startPin, endPin + 1):
        delay(100)
        sw4b = SW18B_UnitTest_globals.SWChipAndPinTo4BChip(sw, pin)
        if sw4b is SW18B_UnitTest_globals.SW_NULL:
            continue

        sw4bPin = _getSW4BPin(sw, pin)
        if sw4bPin == 0:
            continue  # Pin 0 can't output

        pulseTimer = SerialWombatPulseTimer.SerialWombatPulseTimer_18AB(sw)
        pulseTimer.begin(pin)
        pulseTimers[pin] = pulseTimer

        pwm4B = SerialWombatPWM.SerialWombatPWM_4AB(sw4b)
        pwm4B.begin(sw4bPin)
        pwm4B.setFrequency_SW4AB(pwm4B.SW4AB_PWMFrequency_32_Hz)
        pwm4B.writePublicData(0x2000 + 0x800 * pin)

    delay(1000)

    # Read each pin.  High should be 31250 * dutyCycle / 65536.
    # Low should be 31250 - that.
    for pin in range(startPin, endPin + 1):
        delay(100)
        sw4b = SW18B_UnitTest_globals.SWChipAndPinTo4BChip(sw, pin)
        if sw4b is SW18B_UnitTest_globals.SW_NULL:
            continue

        sw4bPin = _getSW4BPin(sw, pin)
        if sw4bPin == 0:
            continue  # Pin 0 can't output

        pulse = sw.readPublicData(pin)
        expected = (0x2000 + 0x800 * pin) * 31250
        expected >>= 16
        _testValue("Pulse Timer High time ", pulse, expected, 50, 5)

        pulseTimer = pulseTimers[pin]
        low = pulseTimer.readLowCounts()
        _testValue("Pulse Timer Low Time ", low, 31250 - expected, 50, 5)

        pulseTimer.configurePublicDataOutput(pulseTimer.PDO_LOW_TIME)
        delay(200)
        _testValue("Pulse Timer Low Time Public Data", pulseTimer.readPublicData(), 31250 - expected, 50, 5)

        pulseTimer.configurePublicDataOutput(pulseTimer.PDO_HIGH_TIME)
        delay(200)
        _testValue("Pulse Timer High  Time Public Data", pulseTimer.readPublicData(), expected, 50, 5)

        pulseTimer.configurePublicDataOutput(pulseTimer.PDO_PERIOD_ON_LTH_TRANSITION)
        delay(200)
        _testValue("Pulse Timer Period LTH Public Data", pulseTimer.readPublicData(), 31250, 2000, 5)

        pulseTimer.configurePublicDataOutput(pulseTimer.PDO_PERIOD_ON_HTL_TRANSITION)
        delay(200)
        _testValue("Pulse Timer Period HTL Public Data", pulseTimer.readPublicData(), 31250, 2000, 5)

    SW18B_UnitTest_globals.resetAll()

    # Check for overflow on period longer than 65535 us.
    for pin in range(startPin, endPin + 1):
        delay(100)
        sw4b = SW18B_UnitTest_globals.SWChipAndPinTo4BChip(sw, pin)
        if sw4b is SW18B_UnitTest_globals.SW_NULL:
            continue

        sw4bPin = _getSW4BPin(sw, pin)
        if sw4bPin == 0:
            continue  # Pin 0 can't output

        pulseTimer = SerialWombatPulseTimer.SerialWombatPulseTimer_18AB(sw)
        pulseTimer.begin(pin)

        pwm4B = SerialWombatPWM.SerialWombatPWM_4AB(sw4b)
        pwm4B.begin(sw4bPin)
        pwm4B.setFrequency_SW4AB(pwm4B.SW4AB_PWMFrequency_8_Hz)
        pwm4B.writePublicData(0x8000)

        delay(1000)

        pulseTimer.configurePublicDataOutput(pulseTimer.PDO_PERIOD_ON_LTH_TRANSITION)
        delay(1000)
        _testValue("Pulse Timer Period LTH Public Data Saturation", pulseTimer.readPublicData(), 65535)

        pulseTimer.configurePublicDataOutput(pulseTimer.PDO_PERIOD_ON_HTL_TRANSITION)
        delay(1000)
        _testValue("Pulse Timer Period HTL Public Data Saturation", pulseTimer.readPublicData(), 65535)

        pulseTimer.begin(pin, SW_PULSETIMER_mS)  # Switch to mS to cut cpu usage on 18AB.

    return  # TODO REMOVE - matches active Arduino test path.
