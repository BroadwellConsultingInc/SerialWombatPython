import SW18B_UnitTest_globals
import SerialWombatIRRx
import SerialWombatIRTx

try:
    from ArduinoFunctions import delay
except ImportError:
    import time

    def delay(milliseconds):
        time.sleep(milliseconds / 1000.0)


IR_RX_PUBLIC_DATA_DATACOUNT = SerialWombatIRRx.DATACOUNT
IR_RX_PUBLIC_DATA_ADDRESS = SerialWombatIRRx.ADDRESS
IR_RX_PUBLIC_DATA_COMMAND = SerialWombatIRRx.COMMAND
IR_MODE_NEC = 0
SW_HIGH = True


def _test(designator, value, expected):
    SW18B_UnitTest_globals.test_value(designator, value, expected, 0, 0)


def _buildIrTxRxObjects():
    irRx18 = SerialWombatIRRx.SerialWombatIRRx(SW18B_UnitTest_globals.SW18AB_6B)
    irRx8 = SerialWombatIRRx.SerialWombatIRRx(SW18B_UnitTest_globals.SW8B_68)
    irTx18 = SerialWombatIRTx.SerialWombatIRTx(SW18B_UnitTest_globals.SW18AB_6B)
    irTx8 = SerialWombatIRTx.SerialWombatIRTx(SW18B_UnitTest_globals.SW8B_68)

    return irRx18, irRx8, irTx18, irTx8


def irTxRxTest():
    SW18B_UnitTest_globals.resetAll()
    irRx18, irRx8, irTx18, irTx8 = _buildIrTxRxObjects()

    # Basic test using stream functions
    irRx18.begin(
        19,
        IR_RX_PUBLIC_DATA_DATACOUNT,
        IR_MODE_NEC,  # Mode
        True,  # Use Repeat
        SW_HIGH,  # Active
    )
    irTx8.begin(SW18B_UnitTest_globals.SW18ABPinTo8BPin(19), 0x1234)

    irTx18.begin(
        18,
        0x2345,  # Address
    )
    irRx8.begin(
        SW18B_UnitTest_globals.SW18ABPinTo8BPin(18),
        IR_RX_PUBLIC_DATA_DATACOUNT,
        IR_MODE_NEC,  # Mode
        True,  # Use Repeat
        SW_HIGH,  # Active
    )

    # Send a stream of commands to each and verify that they were received
    for i in range(9):
        irTx8.write((i + 80) & 0xFF)
        irTx18.write((i + 180) & 0xFF)

    delay(3000)
    for i in range(9):
        _test("irRx8 basic stream", irRx8.read(), i + 180)
        _test("irRx18 basic stream", irRx18.read(), i + 80)

    # Test Repeat
    irRx18.begin(
        19,
        IR_RX_PUBLIC_DATA_DATACOUNT,
        IR_MODE_NEC,  # Mode
        True,  # Use Repeat
        SW_HIGH,  # Active
    )
    irTx8.begin(SW18B_UnitTest_globals.SW18ABPinTo8BPin(19), 0x1234)

    irTx18.begin(
        18,
        0x2345,  # Address
    )
    irRx8.begin(
        SW18B_UnitTest_globals.SW18ABPinTo8BPin(18),
        IR_RX_PUBLIC_DATA_DATACOUNT,
        IR_MODE_NEC,  # Mode
        True,  # Use Repeat
        SW_HIGH,  # Active
    )

    # Send a command and 14 repeat commands. Verify that the right number (15) are received
    irTx8.sendMessage(80, 0x5678, 14)
    irTx18.sendMessage(180, 0x6789, 14)

    delay(10000)
    for i in range(20):
        if i < 15:
            _test("irRx8 repeat", irRx8.read(), 180)
            _test("irRx18 repeat", irRx18.read(), 80)
        else:
            _test("irRx8 repeat end", irRx8.read(), -1)
            _test("irRx18 repeat end", irRx18.read(), -1)

    # Test Addressing
    irRx18.begin(
        19,
        IR_RX_PUBLIC_DATA_DATACOUNT,
        IR_MODE_NEC,  # Mode
        True,  # Use Repeat
        SW_HIGH,  # Active
        1000,  # Timeout period
        65535,  # timeoutValue
        True,  # Use Address Filter
        0x1234,  # Address
    )
    irTx8.begin(SW18B_UnitTest_globals.SW18ABPinTo8BPin(19), 0x1234)

    irTx18.begin(
        18,
        0x2345,  # Address
    )
    irRx8.begin(
        SW18B_UnitTest_globals.SW18ABPinTo8BPin(18),
        IR_RX_PUBLIC_DATA_DATACOUNT,
        IR_MODE_NEC,  # Mode
        True,  # Use Repeat
        SW_HIGH,  # Active
        1000,  # Timeout period
        65535,  # timeoutValue
        True,  # Use Address Filter
        0x2345,  # Address
    )

    # Send a command and 14 repeat commands, and then a message with wrong address.
    # Verify that the right number (15) are received
    irTx8.sendMessage(80, 0x1234, 14)
    irTx18.sendMessage(180, 0x2345, 14)
    irTx8.sendMessage(80, 0x89AB, 14)
    irTx18.sendMessage(180, 0x89AB, 14)

    delay(10000)
    for i in range(20):
        if i < 15:
            _test("irRx8 addressed repeat", irRx8.read(), 180)
            _test("irRx18 addressed repeat", irRx18.read(), 80)
        else:
            _test("irRx8 addressed repeat end", irRx8.read(), -1)
            _test("irRx18 addressedrepeat end", irRx18.read(), -1)

    _test("irRx8 addressed repeat public data count", irRx8.readPublicData(), 15)
    _test("irRx18 addressed repeat public data count", irRx18.readPublicData(), 15)

    # Test public data Address
    irRx18.begin(
        19,
        IR_RX_PUBLIC_DATA_ADDRESS,
        IR_MODE_NEC,  # Mode
        True,  # Use Repeat
        SW_HIGH,  # Active
        1000,  # Timeout period
        65535,  # timeoutValue
        True,  # Use Address Filter
        0x1234,  # Address
    )
    irTx8.begin(SW18B_UnitTest_globals.SW18ABPinTo8BPin(19), 0x1234)

    irTx18.begin(
        18,
        0x2345,  # Address
    )
    irRx8.begin(
        SW18B_UnitTest_globals.SW18ABPinTo8BPin(18),
        IR_RX_PUBLIC_DATA_ADDRESS,
        IR_MODE_NEC,  # Mode
        True,  # Use Repeat
        SW_HIGH,  # Active
        1000,  # Timeout period
        65535,  # timeoutValue
        True,  # Use Address Filter
        0x2345,  # Address
    )

    # Send a command and 14 repeat commands, and then a message with wrong address.
    # Verify that the right number (15) are received
    irTx8.sendMessage(80, 0x1234, 14)
    irTx18.sendMessage(180, 0x2345, 14)
    delay(10000)
    _test("irRx8 addressed repeat public data address A1 ", irRx8.readPublicData(), 0x2345)
    _test("irRx18 addressed repeat public data address B1 ", irRx18.readPublicData(), 0x1234)

    irTx8.sendMessage(80, 0x89AB, 14)
    irTx18.sendMessage(180, 0x89AB, 14)

    delay(10000)
    for i in range(20):
        if i < 15:
            _test("irRx8 addressed repeat B", irRx8.read(), 180)
            _test("irRx18 addressed repeat B", irRx18.read(), 80)
        else:
            _test("irRx8 addressed repeat end B", irRx8.read(), -1)
            _test("irRx18 addressedrepeat end B", irRx18.read(), -1)

    _test("irRx8 addressed repeat public data address A1 ", irRx8.readPublicData(), 0x89AB)
    _test("irRx18 addressed repeat public data address B1 ", irRx18.readPublicData(), 0x89AB)

    # Test public data Command
    irRx18.begin(
        19,
        IR_RX_PUBLIC_DATA_COMMAND,
        IR_MODE_NEC,  # Mode
        True,  # Use Repeat
        SW_HIGH,  # Active
        1000,  # Timeout period
        65535,  # timeoutValue
        True,  # Use Address Filter
        0x1234,  # Address
    )
    irTx8.begin(SW18B_UnitTest_globals.SW18ABPinTo8BPin(19), 0x1234)

    irTx18.begin(
        18,
        0x2345,  # Address
    )
    irRx8.begin(
        SW18B_UnitTest_globals.SW18ABPinTo8BPin(18),
        IR_RX_PUBLIC_DATA_COMMAND,
        IR_MODE_NEC,  # Mode
        True,  # Use Repeat
        SW_HIGH,  # Active
        1000,  # Timeout period
        65535,  # timeoutValue
        True,  # Use Address Filter
        0x2345,  # Address
    )

    # Send a command and 14 repeat commands, and then a message with wrong address.
    # Verify that the right number (15) are received
    irTx8.sendMessage(80, 0x1234, 14)
    irTx18.sendMessage(180, 0x2345, 14)
    delay(250)
    _test("irRx8 addressed repeat public data addressed C1", irRx8.readPublicData(), 180)
    _test("irRx18 addressed repeat public data addressed D1", irRx18.readPublicData(), 80)

    irTx8.sendMessage(80, 0x89AB, 14)
    irTx18.sendMessage(180, 0x89AB, 14)

    delay(10000)
    for i in range(20):
        if i < 15:
            _test("irRx8 addressed repeat C", irRx8.read(), 180)
            _test("irRx18 addressed repeat C", irRx18.read(), 80)
        else:
            _test("irRx8 addressed repeat end C", irRx8.read(), -1)
            _test("irRx18 addressedrepeat end C", irRx18.read(), -1)

    _test("irRx8 addressed repeat public data addressed C", irRx8.readPublicData(), 65535)  # Timeout
    _test("irRx18 addressed repeat public data addressed D", irRx18.readPublicData(), 65535)  # Timeout
