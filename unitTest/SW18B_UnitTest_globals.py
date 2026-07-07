import sys

def is_micropython():
    return sys.implementation.name == 'micropython'

if (is_micropython()):
    import machine
    import SerialWombat_mp_i2c
else:
    import SerialWombat_smbus2_i2c

import SerialWombatPulseTimer
import time


def ticks_ms():
    if (is_micropython()):
        return time.ticks_ms()
    else:
        return time.monotonic_ns() / 1000000
    

global i2c
i2c = None


def init():
    global i2c
#    i2c = machine.I2C(0,
#                  scl=machine.Pin(1),
#                  sda=machine.Pin(0),
#                  freq=100000,timeout = 50000)
    from smbus2 import SMBus
    i2c = SMBus(1)

    global NUM_TEST_PINS
    NUM_TEST_PINS = 20

    global FAILUREPIN
    FAILUREPIN = 8

    global SW8B_68
    SW8B_68 = SerialWombat_smbus2_i2c.SerialWombatChip_smbus2_i2c(i2c,0x68)
    SW8B_68.address = 0x68

    global SW18AB_6B 
    SW18AB_6B = SerialWombat_smbus2_i2c.SerialWombatChip_smbus2_i2c(i2c,0x6B)
    SW18AB_6B.address = 0x6B

    global SW4B_6C
    SW4B_6C = SerialWombat_smbus2_i2c.SerialWombatChip_smbus2_i2c(i2c,0x6C)
    SW4B_6C.address = 0x6C

    global SW4B_6D
    SW4B_6D = SerialWombat_smbus2_i2c.SerialWombatChip_smbus2_i2c(i2c,0x6D)
    SW4B_6D.address = 0x6D
    
    global SW4B_6E
    SW4B_6E = SerialWombat_smbus2_i2c.SerialWombatChip_smbus2_i2c(i2c,0x6E)
    SW4B_6E.address = 0x6E

    global SW4B_6F
    S4B_6F = SerialWombat_smbus2_i2c.SerialWombatChip_smbus2_i2c(i2c,0x6F)
    S4B_6F.address = 0x6F

    global SW_NULL
    SW_NULL = None

    global SW18ABPinTo8BPin
    def SW18ABPinTo8BPin(pin: int) -> int:
        mapping = {
            0: 1,
            6: 0,
            7: 5,
            9: 4,
            16: 2,
            17: 3,
            18: 6,
            19: 7,
        }

        if pin not in mapping:
            test("Invalid SW18AB pin to 4B pin", 0)
            return 255

        return mapping[pin]

    global SW18ABPinTo4BPin
    def SW18ABPinTo4BPin(pin: int) -> int:
        mapping = {
            0: 3,
            5: 2,
            6: 1,
            7: 0,
            8: 0,
            9: 1,
            10: 2,
            11: 3,
            12: 0,
            13: 0,
            14: 3,
            15: 2,
            16: 1,
            17: 3,
            18: 2,
            19: 1,
        }

        if pin not in mapping:
            test(f"Invalid SW18B pin {pin} to 4B pin", 0)
            return 255

        return mapping[pin]
    
    global SW8BPinTo18ABPin
    def SW8BPinTo18ABPin(pin: int) -> int:
        mapping = {
            0: 6,
            1: 0,
            2: 16,
            3: 17,
            4: 9,
            5: 7,
            6: 18,
            7: 19,
        }

        if pin not in mapping:
            test("Invalid 8B pin to 18AB pin", 0)
            return 255  # Should never happen

        return mapping[pin]

    global SW8BPinTo4BPin
    def SW8BPinTo4BPin(pin: int) -> int:
        return SW18ABPinTo4BPin(SW8BPinTo18ABPin(pin))
    
    global SW18ABPinTo4BChip
    def SW8BPinTo4BChip(pin: int):
        return SW18ABPinTo4BChip(SW8BPinTo18ABPin(pin))
    
    global SWChipAndPinTo4BChip
    def SWChipAndPinTo4BChip(sw, pin: int):
        if sw is SW18AB_6B:
            return SW18ABPinTo4BChip(pin)
        elif sw is SW8B_68:
            return SW8BPinTo4BChip(pin)
        else:
            return SW_NULL
        
    global SWChipAndPinTo4BPin
    def SWChipAndPinTo4BPin(sw, pin: int) -> int:
        if sw is SW18AB_6B:
            return SW18ABPinTo4BPin(pin)
        elif sw is SW8B_68:
            return SW8BPinTo4BPin(pin)
        else:
            return 0

    global SW18ABPinTo4BChip   
    def SW18ABPinTo4BChip(pin: int):
        mapping = {
            0: SW4B_6D,
            5: SW4B_6D,
            6: SW4B_6D,
            7: SW4B_6C,
            8: SW4B_6D,
            9: SW4B_6C,
            10: SW4B_6C,
            11: SW4B_6C,
            12: SW4B_6E,
            13: SW4B_6F,
            14: SW4B_6F,
            15: SW4B_6F,
            16: SW4B_6F,
            17: SW4B_6E,
            18: SW4B_6E,
            19: SW4B_6E,
        }

        return mapping.get(pin, SW_NULL)  # Pin has no associated SW4B

    global test_pinCanBeOutput  
    def test_pinCanBeOutput(sw, pin: int) -> bool:
        if sw is SW18AB_6B:
            if 1 <= pin <= 4:
                return False
            if pin > 19:
                return False

        elif sw is SW8B_68:
            if pin > 7:
                return False

        elif sw is SW4B_6C or sw is SW4B_6D or sw is SW4B_6E or sw is SW4B_6F:
            if pin == 0 or pin > 3:
                return False

        else:
            test("TEST ERROR:  Invalid SW Chip in test_pinCanBeOutput", 0)
            return False

        return True

    global lastPassedTest
    lastPassedTest = -1

    global passCount
    passCount = 0
    global failCount
    failCount = 0   

    def pass_(i: int) -> None:
        global passCount, lastPassedTest, lastDisplayUpdate

        passCount += 1
        lastPassedTest = i


    lastFailedTest = -1

    def fail(i: int) -> None:
        global failCount, lastFailedTest, lastDisplayUpdate

        lastFailedTest = i
        # print(f"Fail at iteration {i}")

        failCount += 1

        # Optional "FAILUREPIN" behavior, if you define it (and the helpers) in your Python environment.
        if 'FAILUREPIN' in globals():
            digitalWrite(FAILUREPIN, True)   # HIGH
            delay_ms(1)
            digitalWrite(FAILUREPIN, False)  # LOW

        # Yield periodically in case in tight loop
        if lastDisplayUpdate + 250 < millis():
            lastDisplayUpdate = millis()
            yield_()
    
    # --- Helpers (replace/wire these to your environment) ---

    INPUT = 0  # placeholder for Arduino INPUT constant

    def sw_le16(x: int) -> bytes:
        """Little-endian 16-bit packing (replacement for SW_LE16)."""
        return int(x & 0xFFFF).to_bytes(2, byteorder="little", signed=False)

    # Assume you already have: pass_(), fail(), test(msg, code) (the 2-arg version)
    # And global objects: SW8B_68, SW18AB_6B, SW4B_6C, SW4B_6D, SW4B_6E, SW4B_6F
    # And: Wire, Serial, analogShutdown()


    # --- disablePPS ---

    def disablePPS(sw) -> None:
        b = bytearray([219, 1, 16, 0x55, 0x55, 0x55, 0x55, 0x55])
        sw.sendPacket(b)

        b[1] = 2
        sw.sendPacket(b)

        b[1] = 3
        sw.sendPacket(b)

        sw.pinMode(1, INPUT)
        sw.pinMode(2, INPUT)
        sw.pinMode(3, INPUT)


    # --- resetAll ---

    _versionChecked = False

    def resetAll() -> None:
        global _versionChecked

        analogShutdown()

        SW8B_68.registerErrorHandler(None)
        SW8B_68.begin()
        while not SW8B_68.queryVersion():
            print("Serial Wombat chip at 0x68 did not respond to version query")
            SW8B_68.begin()

        if (not _versionChecked) and (not SW8B_68.isLatestFirmware()):
            print("Serial Wombat chip at 0x68 is not latest firmware")

        SW18AB_6B.registerErrorHandler(None)
        SW18AB_6B.begin()
        while not SW18AB_6B.queryVersion():
            print("Serial Wombat chip at 0x6B did not respond to version query")
            SW18AB_6B.begin()

        if (not _versionChecked) and (not SW18AB_6B.isLatestFirmware()):
            print("Serial Wombat chip at 0x6B is not latest firmware")  
        SW4B_6C.begin()
        while not SW4B_6C.queryVersion():
            print("Serial Wombat chip at 0x6C did not respond to version query")
            SW4B_6C.begin()
        disablePPS(SW4B_6C)

        SW4B_6D.begin()
        while not SW4B_6D.queryVersion():
            print("Serial Wombat chip at 0x6D did not respond to version query")
            SW4B_6D.begin()
        disablePPS(SW4B_6D)

        SW4B_6E.begin()
        while not SW4B_6E.queryVersion():
            print("Serial Wombat chip at 0x6E did not respond to version query")
            SW4B_6E.begin()
        disablePPS(SW4B_6E)

        SW4B_6F.begin()
        while not SW4B_6F.queryVersion():
            print("Serial Wombat chip at 0x6F did not respond to version query")
            SW4B_6F.begin()
        disablePPS(SW4B_6F)

        # C++: #ifdef TEST_SW18AB
        if 'TEST_SW18AB' in globals() and TEST_SW18AB:
            SW18AB_6B.registerErrorHandler(SerialWombatSerialErrorHandlerBrief)

        _versionChecked = True


    # --- PulseTimer instances ---

    SW18AB_PT00 = SerialWombatPulseTimer(SW4B_6D)
    SW18AB_PT05 = SerialWombatPulseTimer(SW4B_6D)
    SW18AB_PT06 = SerialWombatPulseTimer(SW4B_6D)
    SW18AB_PT07 = SerialWombatPulseTimer(SW4B_6C)
    SW18AB_PT08 = SerialWombatPulseTimer(SW4B_6D)
    SW18AB_PT09 = SerialWombatPulseTimer(SW4B_6C)
    SW18AB_PT10 = SerialWombatPulseTimer(SW4B_6C)
    SW18AB_PT11 = SerialWombatPulseTimer(SW4B_6C)
    SW18AB_PT12 = SerialWombatPulseTimer(SW4B_6E)
    SW18AB_PT13 = SerialWombatPulseTimer(SW4B_6F)
    SW18AB_PT14 = SerialWombatPulseTimer(SW4B_6F)
    SW18AB_PT15 = SerialWombatPulseTimer(SW4B_6F)
    SW18AB_PT16 = SerialWombatPulseTimer(SW4B_6F)
    SW18AB_PT17 = SerialWombatPulseTimer(SW4B_6E)
    SW18AB_PT18 = SerialWombatPulseTimer(SW4B_6E)
    SW18AB_PT19 = SerialWombatPulseTimer(SW4B_6E)

    # C++ assigns objects by value; in Python this makes aliases (references).
    SW8B_PT00 = SW18AB_PT06
    SW8B_PT01 = SW18AB_PT00
    SW8B_PT02 = SW18AB_PT16
    SW8B_PT03 = SW18AB_PT17
    SW8B_PT04 = SW18AB_PT09
    SW8B_PT05 = SW18AB_PT07
    SW8B_PT06 = SW18AB_PT18
    SW8B_PT07 = SW18AB_PT19


    # Arrays (NUM_TEST_PINS should exist)
    PulseTimerArray18AB = [
        SW18AB_PT00,  # 0
        None,         # 1
        None,         # 2
        None,         # 3
        None,         # 4
        SW18AB_PT05,  # 5
        SW18AB_PT06,  # 6
        SW18AB_PT07,  # 7
        SW18AB_PT08,  # 8
        SW18AB_PT09,  # 9
        SW18AB_PT10,  # 10
        SW18AB_PT11,  # 11
        SW18AB_PT12,  # 12
        SW18AB_PT13,  # 13
        SW18AB_PT14,  # 14
        SW18AB_PT15,  # 15
        SW18AB_PT16,  # 16
        SW18AB_PT17,  # 17
        SW18AB_PT18,  # 18
        SW18AB_PT19,  # 19
    ]

    PulseTimerArray08B = [
        SW8B_PT00,  # 0
        SW8B_PT01,  # 1
        SW8B_PT02,  # 2
        SW8B_PT03,  # 3
        SW8B_PT04,  # 4
        SW8B_PT05,  # 5
        SW8B_PT06,  # 6
        SW8B_PT07,  # 7
        None,       # 8
        None,       # 9
        None,       # 10
        None,       # 11
        None,       # 12
        None,       # 13
        None,       # 14
        None,       # 15
        None,       # 16
        None,       # 17
        None,       # 18
        None,       # 19
    ]


    global test
    def test(msg: str, val: int) -> None:
        if (val == 1):
            pass_(1)
        else:
            fail(1)
            print(msg)
            

    # --- initializePulseReaduS ---

    def initializePulseReaduS(sw, pin: int) -> None:
        if sw is SW18AB_6B:
            if pin < NUM_TEST_PINS:
                pt = PulseTimerArray18AB[pin]
                if pt is not None:
                    pt.begin(SW18ABPinTo4BPin(pin))
                else:
                    test("TEST ERROR:  NULL PIN in initializePulseReaduS", 0)
            else:
                test("TEST ERROR:  INVALID PIN in initializePulseReaduS", 0)

        elif sw is SW8B_68:
            if pin < NUM_TEST_PINS:
                pt = PulseTimerArray08B[pin]
                if pt is not None:
                    pt.begin(SW8BPinTo4BPin(pin))
                else:
                    test("TEST ERROR:  NULL PIN in initializePulseReaduS", 0)
            else:
                test("TEST ERROR:  INVALID PIN in initializePulseReaduS", 0)

        else:
            test("TEST ERROR:  INVALID CHIP in initializePulseReaduS", 0)


    # --- dutyCycleRead ---

    def dutyCycleRead(sw, pin: int) -> int:
        if sw is SW18AB_6B:
            if pin < NUM_TEST_PINS:
                pt = PulseTimerArray18AB[pin]
                if pt is not None:
                    pt.refreshHighCountsLowCounts()
                    denom = pt.HighCounts + pt.LowCounts
                    if denom == 0:
                        return 0
                    result = 65536 * pt.HighCounts
                    result //= denom
                    return int(result)
                test("TEST ERROR:  NULL PIN in pulseRead", 0)
                return 0
            test("TEST ERROR:  INVALID PIN in pulseRead", 0)
            return 0

        elif sw is SW8B_68:
            if pin < NUM_TEST_PINS:
                pt = PulseTimerArray08B[pin]
                if pt is not None:
                    pt.refreshHighCountsLowCounts()
                    denom = pt.HighCounts + pt.LowCounts
                    if denom == 0:
                        return 0
                    result = 65536 * pt.HighCounts
                    result //= denom
                    return int(result)
                test("TEST ERROR:  NULL PIN in pulseRead", 0)
                return 0
            test("TEST ERROR:  INVALID PIN in pulseRead", 0)
            return 0

        test("TEST ERROR:  INVALID CHIP in pulseRead", 0)
        return 0


    # --- pulseRead ---

    def pulseRead(sw, pin: int) -> int:
        if sw is SW18AB_6B:
            if pin < NUM_TEST_PINS:
                pt = PulseTimerArray18AB[pin]
                if pt is not None:
                    return int(pt.readHighCounts())
                test("TEST ERROR:  NULL PIN in pulseRead", 0)
                return 0
            test("TEST ERROR:  INVALID PIN in pulseRead", 0)
            return 0

        elif sw is SW8B_68:
            if pin < NUM_TEST_PINS:
                pt = PulseTimerArray08B[pin]
                if pt is not None:
                    return int(pt.readHighCounts())
                test("TEST ERROR:  NULL PIN in pulseRead", 0)
                return 0
            test("TEST ERROR:  INVALID PIN in pulseRead", 0)
            return 0

        test("TEST ERROR:  INVALID CHIP in pulseRead", 0)
        return 0


    # --- pulseCounts ---

    def pulseCounts(sw, pin: int) -> int:
        if sw is SW18AB_6B:
            if pin < NUM_TEST_PINS:
                pt = PulseTimerArray18AB[pin]
                if pt is not None:
                    return int(pt.readPulses())
                test("TEST ERROR:  NULL PIN in pulseCounts", 0)
                return 0
            test("TEST ERROR:  INVALID PIN in pulseCounts", 0)
            return 0

        elif sw is SW8B_68:
            if pin < NUM_TEST_PINS:
                pt = PulseTimerArray08B[pin]
                if pt is not None:
                    return int(pt.readPulses())
                test("TEST ERROR:  NULL PIN in pulseCounts", 0)
                return 0
            test("TEST ERROR:  INVALID PIN in pulseCounts", 0)
            return 0

        test("TEST ERROR:  INVALID CHIP in pulseCounts", 0)
        return 0


    # --- withinRange ---

    def withinRange(value: int, expected: int, sixtyFourths: int, counts: int) -> bool:
        x32 = int(expected)

        if (value > x32 + counts) and (value > (x32 * (64 + sixtyFourths) // 64)):
            return False
        if (value < x32 - counts) and (value < (x32 * (64 - sixtyFourths) // 64)):
            return False

        return True


    # --- test(designator, value, expected, counts, sixtyFourths) ---
    # NOTE: This overload name collides with your earlier test(msg, 0).
    # If you need both in Python, rename one of them (e.g., test_value()).

    def test_value(designator: str, value: int, expected: int, counts: int, sixtyFourths: int) -> None:
        if withinRange(value, expected, sixtyFourths, counts):
            pass_(1)
        else:
            fail(1)
            failPacket = (
                bytes([0x40, 0x00])
                + sw_le16(expected)
                + sw_le16(value)
                + bytes([0x55, 0x55])
            )
            SW18AB_6B.sendPacket(failPacket)
            Serial.print(designator)
            Serial.print(" V: ")
            Serial.print(value)
            Serial.print(" X:")
            Serial.println(expected)

