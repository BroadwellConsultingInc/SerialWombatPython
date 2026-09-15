import SW18B_UnitTest_globals
import SerialWombatPWM
import SerialWombatServo
import SerialWombatUltrasonicDistanceSensor
import SerialWombatWatchdog

try:
    from ArduinoFunctions import delay
    from ArduinoFunctions import millis
except ImportError:
    import time

    _start_time = time.monotonic()

    def delay(milliseconds):
        time.sleep(milliseconds / 1000.0)

    def millis():
        return int((time.monotonic() - _start_time) * 1000)


SW_LOW = 0
SW_HIGH = 1
HC_SR04 = 0


def _testValue(designator, value, expected, counts=0, sixtyFourths=0):
    SW18B_UnitTest_globals.test_value(designator, value, expected, counts, sixtyFourths)


def _buildUsdObjects():
    USDSensor = SerialWombatUltrasonicDistanceSensor.SerialWombatUltrasonicDistanceSensor(
        SW18B_UnitTest_globals.SW18AB_6B
    )
    usdWD = SerialWombatWatchdog.SerialWombatWatchdog(
        SW18B_UnitTest_globals.SW4B_6C
    )
    usdsServo = SerialWombatServo.SerialWombatServo(
        SW18B_UnitTest_globals.SW18AB_6B
    )
    SWPWM10 = SerialWombatPWM.SerialWombatPWM_4AB(
        SW18B_UnitTest_globals.SW4B_6C
    )

    return USDSensor, usdWD, usdsServo, SWPWM10


def usdSensorTest(pin):
    SW18B_UnitTest_globals.resetAll()

    USDSensor, usdWD, usdsServo, SWPWM10 = _buildUsdObjects()

    USDSensor.begin(
        pin,  # Echo Pin, goes to SW6C pin 2
        HC_SR04,
        pin + 1,  # Trigger Pin, goes to SW6C Pin 3
        True,
        False,
    )
    usdWD.begin(
        SW18B_UnitTest_globals.SW18ABPinTo4BPin(pin),
        SW_HIGH,
        SW_LOW,
        20,
        False,
    )

    delay(30)
    _testValue("USDSensor_00", USDSensor.readPublicData(), 3400, 500)

    USDServoSweep(pin)


def USDServoSweep(pin):
    servoPin = pin + 2
    SW18B_UnitTest_globals.resetAll()

    USDSensor, usdWD, usdsServo, SWPWM10 = _buildUsdObjects()

    USDSensor.begin(
        pin,  # Echo Pin, goes to SW6C pin 2
        HC_SR04,
        pin + 1,  # Trigger Pin, goes to SW6C Pin 3
        True,
        False,
    )

    SW18B_UnitTest_globals.initializePulseReaduS(
        SW18B_UnitTest_globals.SW18AB_6B,
        servoPin,
    )

    SWPWM10.begin(SW18B_UnitTest_globals.SW18ABPinTo4BPin(pin))
    SWPWM10.setFrequency_SW4AB(SWPWM10.SW4AB_PWMFrequency_488_Hz)
    SWPWM10.writePublicData(0x8000)  # Setup PWM with frequency 1KHz to trick the echo to move the servof

    usdsServo.attach(
        servoPin,
        1000,  # Min
        2600,  # Max  # Chosen so that each each increment of the servo should increase it by 100uS (1/16 of range)
    )
    USDSensor.configureServoSweep(
        servoPin,
        0x0000,  # memoryIndex
        8,  # Servo Positions
        0x1000,  # servoIncrement,
        False,  # Reverse
        1000,  # servoMoveDelay
        1000,  # uint16_t servoReturnDelay
    )
    USDSensor.enableServoSweep(True)
    # Wait for servo reading to be between 1000 and 1100

    for trycount in range(17):
        pulseTime = SW18B_UnitTest_globals.pulseRead(
            SW18B_UnitTest_globals.SW18AB_6B,
            servoPin,
        )
        if pulseTime > 930 and pulseTime < 1070:
            break
        delay(515)
    else:
        SW18B_UnitTest_globals.test("USDSensor_SS_00", 0)
        return

    testtime = millis()
    for i in range(8):
        while millis() < testtime:
            delay(0)
        pulseTime = SW18B_UnitTest_globals.pulseRead(
            SW18B_UnitTest_globals.SW18AB_6B,
            servoPin,
        )
        _testValue("USDSensor_SS_01", pulseTime, 1000 + i * 100, 50)

        testtime += 1000
