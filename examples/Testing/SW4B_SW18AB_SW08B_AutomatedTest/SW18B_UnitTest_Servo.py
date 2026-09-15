# SW18B_UnitTest_Servo.py
#
# Python port of:
#   - Servo.ino : servoTest(SerialWombatChip &sw, uint8_t startPin, uint8_t endPin)
#   - SW4B_SW18AB_SW08B_AutomatedTest.ino : helper functions used by servoTest
#
# Goal: keep structure easy to compare line-by-line with the Arduino code.

from ArduinoFunctions import delay
import SW18B_UnitTest_globals
import SerialWombatServo

from SerialWombat import SerialWombatCommands, SerialWombatPinMode_t


# ---------------------------------------------------------------------------
# Constants (from Servo.ino and SW4B_SW18AB_SW08B_AutomatedTest.ino)
# ---------------------------------------------------------------------------

NUM_TEST_PINS = 20          # #define NUM_TEST_PINS 20
SERVO_TEST_INCREMENTS = 100 # #define SERVO_TEST_INCREMENTS 100

# If you want Arduino-like printing of failures, toggle this:
PRINT_FAILURES = True
# ---------------------------------------------------------------------------
# Servo object array (mirrors Servo.ino’s SW18ABServos[])
# ---------------------------------------------------------------------------

# Create per-pin servo objects for SW18AB.
# Servo.ino uses NULL entries for pins 1-4; we keep None there to match.
SW18ABServos = [None] * NUM_TEST_PINS
SW18ABServos[0]  = SerialWombatServo.SerialWombatServo_18AB(SW18B_UnitTest_globals.SW18AB_6B)
SW18ABServos[5]  = SerialWombatServo.SerialWombatServo_18AB(SW18B_UnitTest_globals.SW18AB_6B)
SW18ABServos[6]  = SerialWombatServo.SerialWombatServo_18AB(SW18B_UnitTest_globals.SW18AB_6B)
SW18ABServos[7]  = SerialWombatServo.SerialWombatServo_18AB(SW18B_UnitTest_globals.SW18AB_6B)
SW18ABServos[8]  = SerialWombatServo.SerialWombatServo_18AB(SW18B_UnitTest_globals.SW18AB_6B)
SW18ABServos[9]  = SerialWombatServo.SerialWombatServo_18AB(SW18B_UnitTest_globals.SW18AB_6B)
SW18ABServos[10] = SerialWombatServo.SerialWombatServo_18AB(SW18B_UnitTest_globals.SW18AB_6B)
SW18ABServos[11] = SerialWombatServo.SerialWombatServo_18AB(SW18B_UnitTest_globals.SW18AB_6B)
SW18ABServos[12] = SerialWombatServo.SerialWombatServo_18AB(SW18B_UnitTest_globals.SW18AB_6B)
SW18ABServos[13] = SerialWombatServo.SerialWombatServo_18AB(SW18B_UnitTest_globals.SW18AB_6B)
SW18ABServos[14] = SerialWombatServo.SerialWombatServo_18AB(SW18B_UnitTest_globals.SW18AB_6B)
SW18ABServos[15] = SerialWombatServo.SerialWombatServo_18AB(SW18B_UnitTest_globals.SW18AB_6B)
SW18ABServos[16] = SerialWombatServo.SerialWombatServo_18AB(SW18B_UnitTest_globals.SW18AB_6B)
SW18ABServos[17] = SerialWombatServo.SerialWombatServo_18AB(SW18B_UnitTest_globals.SW18AB_6B)
SW18ABServos[18] = SerialWombatServo.SerialWombatServo_18AB(SW18B_UnitTest_globals.SW18AB_6B)
SW18ABServos[19] = SerialWombatServo.SerialWombatServo_18AB(SW18B_UnitTest_globals.SW18AB_6B)
# ---------------------------------------------------------------------------
# Public entry point expected by SW18B_UnitTest.py
# ---------------------------------------------------------------------------

def servoTest(sw, startPin: int, endPin: int):
   
    _servoTest_chip(sw, startPin, endPin)


# ---------------------------------------------------------------------------
# Port of Servo.ino: servoTest(SerialWombatChip &sw, uint8_t startPin, uint8_t endPin)
# ---------------------------------------------------------------------------

def _servoTest_chip(sw, startPin: int, endPin: int):
    # resetAll();
    if hasattr(SW18B_UnitTest_globals, "resetAll"):
        SW18B_UnitTest_globals.resetAll()

    # for (int pin = startPin; pin <= endPin; ++ pin) { ... initializePulseReaduS(sw,pin); }
    for pin in range(startPin, endPin + 1):
        if not SW18B_UnitTest_globals.test_pinCanBeOutput(sw, pin):
            continue
        SW18B_UnitTest_globals.initializePulseReaduS(sw, pin)

    # Select ServoArray based on chip (Arduino does pointer comparisons)
    ServoArray = None
    if sw is SW18B_UnitTest_globals.SW18AB_6B:
        ServoArray = SW18ABServos
    else:
        print("Invalid chip for servo test")
        return

    # for (uint16_t variable = 800; variable <= 2000; variable += 100)
    for variable in range(800, 2000 + 1, 100):
        print(f" iteration {(variable - 800) // 100} of 13")

        # for (uint16_t base = 500; base <= 1200; base += 100)
        for base in range(500, 1200 + 1, 100):

            # for (int reverse = 0; reverse < 2; ++ reverse)
            for reverse in range(0, 2):

                # for (int i = 0; i < SERVO_TEST_INCREMENTS; ++i)
                for i in range(0, SERVO_TEST_INCREMENTS):

                    # for (int pin = startPin; pin <= endPin; ++ pin) { ... attach + write16bit }
                    for pin in range(startPin, endPin + 1):
                        if not SW18B_UnitTest_globals.test_pinCanBeOutput(sw, pin):
                            continue

                        # ServoArray[pin]-> attach(pin, base, base + variable, reverse);
                        # ServoArray[pin]->write16bit((i * 65535 ) / SERVO_TEST_INCREMENTS + (pin * 65535 / NUM_TEST_PINS));
                        servo = ServoArray[pin]
                        if servo is None:
                            # Matches Arduino behavior: those entries are NULL and pins are skipped by test_pinCanBeOutput.
                            continue

                        servo.attach(pin, base, base + variable, reverse)
                        setting = (i * 65535) // SERVO_TEST_INCREMENTS + (pin * 65535 // NUM_TEST_PINS)
                        servo.write16bit(setting)

                    # delay(100);
                    delay(100)

                    # for (int pin = startPin; pin <= endPin; ++ pin) { ... pulseRead + compare }
                    for pin in range(startPin, endPin + 1):
                        if not SW18B_UnitTest_globals.test_pinCanBeOutput(sw, pin):
                            continue

                        result = SW18B_UnitTest_globals.pulseRead(sw, pin)

                        setting = (i * 65535) // SERVO_TEST_INCREMENTS + (pin * 65535 // NUM_TEST_PINS)
                        setting = setting & 0xFFFF # Clip to 16 bits
                        if reverse:
                            setting = (65535 - setting)

                        # expected = (variable) * (uint32_t)setting / 65536 + base;
                        expected = (variable * setting) // 65536 + base

                        # if ((result < (expected + (expected / 20)) + 20) && (result > (expected - (expected / 20) - 20)))
                        #   pass(i); else fail(i);
                        upper = (expected + (expected // 20)) + 20
                        lower = (expected - (expected // 20)) - 20

                        if (result < upper) and (result > lower):
                            SW18B_UnitTest_globals.pass_(i)
                        else:
                            if PRINT_FAILURES:
                                print(f"{pin} {result} {expected} Fail")
                            SW18B_UnitTest_globals.fail(i)

