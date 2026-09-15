import SW18B_UnitTest_globals
import SerialWombatUART

try:
    from ArduinoFunctions import delay
except ImportError:
    import time

    def delay(milliseconds):
        time.sleep(milliseconds / 1000.0)


SWUART_TEST_QUEUE_MAX_LENGTH = 32

txSeed = [1]
countSeed = [1]
swUartTestQueueLength = 32
numberOfSWUarts = 4

uart18Rx = [bytearray(SWUART_TEST_QUEUE_MAX_LENGTH) for _ in range(4)]
uart18Tx = [bytearray(SWUART_TEST_QUEUE_MAX_LENGTH) for _ in range(4)]
uart8Rx = [bytearray(SWUART_TEST_QUEUE_MAX_LENGTH) for _ in range(4)]
uart8Tx = [bytearray(SWUART_TEST_QUEUE_MAX_LENGTH) for _ in range(4)]

software18UART0 = SerialWombatUART.SerialWombatSWUART(SW18B_UnitTest_globals.SW18AB_6B)  # 7 9
software18UART1 = SerialWombatUART.SerialWombatSWUART(SW18B_UnitTest_globals.SW18AB_6B)  # 19 18
software18UART2 = SerialWombatUART.SerialWombatSWUART(SW18B_UnitTest_globals.SW18AB_6B)  # 17 16
software18UART3 = SerialWombatUART.SerialWombatSWUART(SW18B_UnitTest_globals.SW18AB_6B)  # 0 6
software8UART0 = SerialWombatUART.SerialWombatSWUART(SW18B_UnitTest_globals.SW8B_68)
software8UART1 = SerialWombatUART.SerialWombatSWUART(SW18B_UnitTest_globals.SW8B_68)
software8UART2 = SerialWombatUART.SerialWombatSWUART(SW18B_UnitTest_globals.SW8B_68)
software8UART3 = SerialWombatUART.SerialWombatSWUART(SW18B_UnitTest_globals.SW8B_68)
swUart7Rx = SerialWombatUART.SerialWombatUART(SW18B_UnitTest_globals.SW4B_6C)
swUart17Rx = SerialWombatUART.SerialWombatUART(SW18B_UnitTest_globals.SW4B_6E)

software18Uarts = [software18UART0, software18UART1, software18UART2, software18UART3]
software8Uarts = [software8UART0, software8UART1, software8UART2, software8UART3]


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

    return bytearray(uart.readBytes(count))


def _drainUART(uart):
    while uart.read() != -1:
        delay(0)


def uartSWTest():
    global swUartTestQueueLength, numberOfSWUarts

    print("Pin Memory Queue SWUART TEST")
    txSeed[0] = 1
    countSeed[0] = 1
    swUartTestQueueLength = 32
    numberOfSWUarts = 4

    software18UART0.begin(19200, 9, 9, 7)
    software8UART0.begin(19200, 5, 5, 4)

    software18UART1.begin(300, 19, 19, 18)
    software8UART1.begin(300, 6, 6, 7)

    software18UART2.begin(2400, 17, 17, 16)
    software8UART2.begin(2400, 2, 2, 3)

    software18UART3.begin(9600, 0, 0, 6)
    software8UART3.begin(9600, 0, 0, 1)

    swUart7Rx.begin(19200, 0, 0, 255)
    swUart17Rx.begin(19200, 3, 3, 255)  # SW8B Transmit on pin 3 to correspond to this

    swUARTLoop()

    print("User Memory Queue SWUART TEST")
    txSeed[0] = 1
    countSeed[0] = 1
    swUartTestQueueLength = 12
    numberOfSWUarts = 2

    software18UART0.beginUserMemoryQueues(19200, 9, 9, 7, 0, swUartTestQueueLength, swUartTestQueueLength)
    software8UART0.beginUserMemoryQueues(19200, 5, 5, 4, 0, swUartTestQueueLength, swUartTestQueueLength)

    software18UART1.beginUserMemoryQueues(9600, 19, 19, 18, 50, swUartTestQueueLength, swUartTestQueueLength)
    software8UART1.beginUserMemoryQueues(9600, 6, 6, 7, 50, swUartTestQueueLength, swUartTestQueueLength)

    swUARTLoop()
    return 0


def swUARTLoop():
    delay(1000)
    for uart_i in range(numberOfSWUarts):
        _drainUART(software18Uarts[uart_i])
        _drainUART(software8Uarts[uart_i])

    for iteration in range(200):
        txCount18 = [0] * 4
        txCount8 = [0] * 4
        rxSeed = [txSeed[0]]

        for uart_i in range(numberOfSWUarts):
            txCount18[uart_i] = _wrandom(countSeed) % swUartTestQueueLength

            for i in range(txCount18[uart_i]):
                uart18Tx[uart_i][i] = _wrandom(txSeed) & 0xFF

            txCount8[uart_i] = _wrandom(countSeed) % swUartTestQueueLength

            for i in range(txCount8[uart_i]):
                uart8Tx[uart_i][i] = _wrandom(txSeed) & 0xFF

            bytesWritten = software18Uarts[uart_i].write(uart18Tx[uart_i], txCount18[uart_i])
            _test("SWU 018", bytesWritten, txCount18[uart_i])

            bytesWritten = software8Uarts[uart_i].write(uart8Tx[uart_i], txCount8[uart_i])
            _test("SWU 08W", bytesWritten, txCount8[uart_i])

        doneTransmitting = False
        while not doneTransmitting:
            doneTransmitting = True
            for uart_i in range(numberOfSWUarts):
                doneTransmitting = doneTransmitting and (software18Uarts[uart_i].bytesToTransmit() == 0)
                if not doneTransmitting:
                    continue
                doneTransmitting = doneTransmitting and (software8Uarts[uart_i].bytesToTransmit() == 0)
                if not doneTransmitting:
                    continue
            delay(0)

        delay(45)  # Allow last byte to send
        for uart_i in range(numberOfSWUarts):
            rxData = _readBytes(software8Uarts[uart_i], txCount18[uart_i])
            bytesRead = len(rxData)
            _test("SWU 1", bytesRead, txCount18[uart_i])
            for i in range(txCount18[uart_i]):
                value = -1
                if i < len(rxData):
                    value = rxData[i]
                _test("SWU 1_8", value, _wrandom(rxSeed) & 0xFF)

            rxData = _readBytes(software18Uarts[uart_i], txCount8[uart_i])
            bytesRead = len(rxData)
            _test("SWU 2", bytesRead, txCount8[uart_i])
            for i in range(txCount8[uart_i]):
                value = -1
                if i < len(rxData):
                    value = rxData[i]
                _test("SWU 2_8", value, _wrandom(rxSeed) & 0xFF)
