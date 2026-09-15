import SW18B_UnitTest_globals
import SerialWombatUART

try:
    from ArduinoFunctions import delay
except ImportError:
    import time

    def delay(milliseconds):
        time.sleep(milliseconds / 1000.0)


baudArray = [
    300,
    1200,
    2400,
    4800,
    9600,
    19200,
    38400,
    57600,
    115200,
]

uartRx = bytearray(200)
uartTx = bytearray(200)
txSeed = [1]
countSeed = [1]

OUTPUT = 1
HIGH = 1


def _wrandom(seed):
    x = seed[0] & 0xFFFFFFFF
    x ^= (x << 13) & 0xFFFFFFFF
    x ^= (x >> 17) & 0xFFFFFFFF
    x ^= (x << 5) & 0xFFFFFFFF
    seed[0] = x & 0xFFFFFFFF
    return seed[0]


def _test(designator, value, expected):
    SW18B_UnitTest_globals.test_value(designator, value, expected, 0, 0)


def _readBytes(uart, count):
    if count == 0:
        return bytearray()

    data = uart.readBytes(count)
    return bytearray(data)


def _testReadData(prefix, baudIteration, iteration, rxData, txData, txcount):
    for i in range(txcount):
        value = -1
        if i < len(rxData):
            value = rxData[i]
        _test(f"{prefix} Baud: {baudIteration}, iter: {iteration}, i {i}", value, txData[i])


def _buildUARTs():
    sw18UART1 = SerialWombatUART.SerialWombatUART(SW18B_UnitTest_globals.SW18AB_6B)
    sw18UART2 = SerialWombatUART.SerialWombatUART(SW18B_UnitTest_globals.SW18AB_6B)
    sw8UART1 = SerialWombatUART.SerialWombatUART(SW18B_UnitTest_globals.SW8B_68)
    sw8UART2 = SerialWombatUART.SerialWombatUART(SW18B_UnitTest_globals.SW8B_68)
    UART1Match_6C = SerialWombatUART.SerialWombatUART(SW18B_UnitTest_globals.SW4B_6C)
    UART2Match_6E = SerialWombatUART.SerialWombatUART(SW18B_UnitTest_globals.SW4B_6E)

    return sw18UART1, sw18UART2, sw8UART1, sw8UART2, UART1Match_6C, UART2Match_6E


def uartHWTest(sw, rxPin0, txPin0, rxPin1, txPin1):
    sw18UART1, sw18UART2, sw8UART1, sw8UART2, UART1Match_6C, UART2Match_6E = _buildUARTs()

    hwUART1 = None
    hwUART2 = None
    UART1Match = None
    UART2Match = None

    if sw is SW18B_UnitTest_globals.SW18AB_6B:
        hwUART1 = sw18UART1
        hwUART2 = sw18UART2
        UART1Match = UART1Match_6C
        UART2Match = UART2Match_6E

        SW18B_UnitTest_globals.SW4B_6C.pinMode(1, OUTPUT)
        SW18B_UnitTest_globals.SW4B_6C.digitalWrite(1, HIGH)
        SW18B_UnitTest_globals.SW4B_6E.pinMode(1, OUTPUT)
        SW18B_UnitTest_globals.SW4B_6E.digitalWrite(1, HIGH)

    elif sw is SW18B_UnitTest_globals.SW8B_68:
        hwUART1 = sw8UART1
        hwUART2 = None
        UART1Match = sw18UART1
        UART2Match = None

    else:
        _test("HW UART Invalid SW Chip", 0, 1)
        return 0

    baudIteration = 0
    if sw is SW18B_UnitTest_globals.SW8B_68:
        baudIteration = 1

    while baudIteration < 9:
        delayMs = 10000 // baudArray[baudIteration]
        txcount = 0

        hwUART1.begin(baudArray[baudIteration], rxPin0, rxPin0, txPin0)

        if sw is SW18B_UnitTest_globals.SW18AB_6B:
            UART1Match.begin(baudArray[baudIteration], 0, 0, 1)
        elif sw is SW18B_UnitTest_globals.SW8B_68:
            UART1Match.begin(baudArray[baudIteration], 9, 9, 7)

        if sw is SW18B_UnitTest_globals.SW18AB_6B:
            hwUART2.begin(baudArray[baudIteration], rxPin1, rxPin1, txPin1, 2)
            UART2Match.begin(baudArray[baudIteration], 3, 3, 1)

        for iteration in range(500):
            txcount = _wrandom(countSeed) % 32

            for i in range(txcount):
                uartTx[i] = _wrandom(txSeed) & 0xFF
                #uartTx[i] = i & 0xFF

            SW18B_UnitTest_globals.SW18AB_6B.readPublicData(6)  # TODO Remove

            bytesWritten = hwUART1.write(uartTx, txcount)
            _test("HWU 0", bytesWritten, txcount)

            delay(delayMs * txcount)
            rxData = _readBytes(UART1Match, txcount)
            bytesRead = len(rxData)
            _test("HWU 1", bytesRead, txcount)
            _testReadData("HWU 2", baudIteration, iteration, rxData, uartTx, txcount)

            txcount = _wrandom(countSeed) % 32

            for i in range(txcount):
                uartTx[i] = _wrandom(txSeed) & 0xFF
                #uartTx[i] = i & 0xFF

            bytesWritten = UART1Match.write(uartTx, txcount)
            _test("HWU 4", bytesWritten, txcount)
            delay(delayMs * txcount)
            rxData = _readBytes(hwUART1, txcount)
            bytesRead = len(rxData)
            _test("HWU 5", bytesRead, txcount)
            _testReadData("HWU 6", baudIteration, iteration, rxData, uartTx, txcount)

            if sw is SW18B_UnitTest_globals.SW18AB_6B:
                txcount = _wrandom(countSeed) % 32

                for i in range(txcount):
                    uartTx[i] = _wrandom(txSeed) & 0xFF
                    #uartTx[i] = i & 0xFF

                bytesWritten = hwUART2.write(uartTx, txcount)
                _test("HWU 7", bytesWritten, txcount)
                delay(delayMs * txcount)
                rxData = _readBytes(UART2Match, txcount)
                bytesRead = len(rxData)
                _test("HWU 8", bytesRead, txcount)
                _testReadData("HWU 9", baudIteration, iteration, rxData, uartTx, txcount)

                txcount = _wrandom(countSeed) % 32

                for i in range(txcount):
                    uartTx[i] = _wrandom(txSeed) & 0xFF
                    #uartTx[i] = i & 0xFF

                bytesWritten = UART2Match.write(uartTx, txcount)
                _test("HWU 10", bytesWritten, txcount)
                delay(delayMs * txcount)
                rxData = _readBytes(hwUART2, txcount)
                bytesRead = len(rxData)
                _test("HWU 11", bytesRead, txcount)
                _testReadData("HWU 12", baudIteration, iteration, rxData, uartTx, txcount)

        baudIteration += 1

    return 0
