# Converted from Testing/SW4B_SW18AB_SW08B_AutomatedTest/UARTSW.ino
import SerialWombat
from ArduinoFunctions import delay, delayMicroseconds, millis

# Import constants from the SerialWombat module so names match the Arduino examples.
for _name in dir(SerialWombat.SerialWombatPinMode_t):
    if _name.startswith("PIN_MODE_"):
        globals()[_name] = getattr(SerialWombat.SerialWombatPinMode_t, _name)
for _name in dir(SerialWombat.SerialWombatDataSource):
    if _name.startswith("SW_DATA_"):
        globals()[_name] = getattr(SerialWombat.SerialWombatDataSource, _name)
PERIOD_1mS = 0; PERIOD_2mS = 1; PERIOD_4mS = 2; PERIOD_8mS = 3; PERIOD_16mS = 4; PERIOD_32mS = 5; PERIOD_64mS = 6; PERIOD_128mS = 7; PERIOD_256mS = 8; PERIOD_512mS = 9; PERIOD_1024mS = 10
HC_SR04 = 0
RAW = 0; AVERAGE = 1; FILTERED = 2; MINIMUM = 3; MAXIMUM = 4
DATACOUNT = 2; ADDRESS = 3; COMMAND = 4

#Comment these lines in if you're connecting directly to a Serial Wombat Chip's UART through cPython serial Module
#Change the parameter of SerialWombatChip_cpy_serial to match the name of your Serial port
#import SerialWombat_cpy_serial
#sw = SerialWombat_cpy_serial.SerialWombatChip_cpy_serial("COM25")

#Comment these lines in if you're connecting to a Serial Wombat Chip's I2C port using cPython smbus2
#Change busNumber and swI2Caddress to match your configuration
#import SerialWombat_smbus2_i2c
#busNumber = 1
#swI2Caddress = 0x6B
#sw = SerialWombat_smbus2_i2c.SerialWombatChip_smbus2_i2c(busNumber, swI2Caddress)

#Comment these lines in if you're connecting to a Serial Wombat Chip's I2C port using CircuitPython's I2C interface
#Change sclPin, sdaPin, and swI2Caddress to match your configuration
#import board
#import busio
#import SerialWombat_cp_i2c
#swI2Caddress = 0x6B
#i2c = busio.I2C(board.SCL, board.SDA)
#sw = SerialWombat_cp_i2c.SerialWombatChip_cp_i2c(i2c, swI2Caddress)

#Comment these lines in if you're connecting to a Serial Wombat Chip's I2C port using Micropython's I2C interface
#Change the values for sclPin, sdaPin, and swI2Caddress to match your configuration
#import machine
#import SerialWombat_mp_i2c
#sclPin = 22
#sdaPin = 21
#swI2Caddress = 0x6B
#i2c = machine.I2C(0,
#            scl=machine.Pin(sclPin),
#            sda=machine.Pin(sdaPin),
#            freq=100000,timeout = 50000)
#sw = SerialWombat_mp_i2c.SerialWombatChip_mp_i2c(i2c,swI2Caddress)
#sw.address = swI2Caddress

#Comment these lines in if you're connecting to a Serial Wombat Chip's UART port using Micropython's UART interface
#Change the values for UARTnum, txPin, and rxPin to match your configuration
import machine
import SerialWombat_mp_UART
txPin = 12
rxPin = 14
UARTnum = 2
uart = machine.UART(UARTnum, baudrate=115200, tx=txPin, rx=rxPin)
sw = SerialWombat_mp_UART.SerialWombatChipUART(uart)

#Interface independent code starts here:
import SerialWombatUART

software18UART0 = SerialWombatUART.SerialWombatSWUART(SW18AB_6B)  # 7 9
software18UART1 = SerialWombatUART.SerialWombatSWUART(SW18AB_6B)  # 19 18
software18UART2 = SerialWombatUART.SerialWombatSWUART(SW18AB_6B)  # 17 16
software18UART3 = SerialWombatUART.SerialWombatSWUART(SW18AB_6B)  # 0 6
software8UART0 = SerialWombatUART.SerialWombatSWUART(SW8B_68)
software8UART1 = SerialWombatUART.SerialWombatSWUART(SW8B_68)
software8UART2 = SerialWombatUART.SerialWombatSWUART(SW8B_68)
software8UART3 = SerialWombatUART.SerialWombatSWUART(SW8B_68)
swUart7Rx = SerialWombatUART.SerialWombatUART(SW4B_6C)
swUart17Rx = SerialWombatUART.SerialWombatUART(SW4B_6E)

# TODO_MANUAL_CONVERSION: SerialWombatSWUART* software18Uarts[] = {software18UART0,software18UART1,software18UART2,software18UART3}
# TODO_MANUAL_CONVERSION: SerialWombatSWUART* software8Uarts[] = {software8UART0,software8UART1,software8UART2,software8UART3}
SWUART_TEST_QUEUE_MAX_LENGTH = 32
swUartTestQueueLength = 0
# TODO_MANUAL_CONVERSION: uint8_t uart18Rx[4][SWUART_TEST_QUEUE_MAX_LENGTH]
# TODO_MANUAL_CONVERSION: uint8_t uart18Tx[4][SWUART_TEST_QUEUE_MAX_LENGTH]
# TODO_MANUAL_CONVERSION: uint8_t uart8Rx[4][SWUART_TEST_QUEUE_MAX_LENGTH]
# TODO_MANUAL_CONVERSION: uint8_t uart8Tx[4][SWUART_TEST_QUEUE_MAX_LENGTH]
uart8TxLength = [0] * (4)
uart18TxLength = [0] * (4)
numberOfSWUarts = 0


def uartSWTest():
  print("Pin Memory Queue SWUART TEST")
  txSeed = 1
  countSeed = 1
  swUartTestQueueLength = 32
  numberOfSWUarts = 4
  software18UART0.begin(19200,9,9,7)
  software8UART0.begin(19200,5,5,4)

  software18UART1.begin(300,19,19,18)
  software8UART1.begin(300,6,6,7)

  software18UART2.begin(2400,17,17,16)
  software8UART2.begin(2400,2,2,3)

  software18UART3.begin(9600,0,0,6)
  software8UART3.begin(9600,0,0,1)

  swUart7Rx.begin(19200, 0, 0, 255)
  swUart17Rx.begin(19200, 3, 3, 255);  # SW8B Transmit on pin 3 to correspond to this

  swUARTLoop()

  print("User Memory Queue SWUART TEST")
  txSeed = 1
  countSeed = 1
  swUartTestQueueLength = 12
  numberOfSWUarts = 2
  software18UART0.begin(19200,9,9,7,0,swUartTestQueueLength,swUartTestQueueLength)
  software8UART0.begin(19200,5,5,4,0,swUartTestQueueLength,swUartTestQueueLength)

  software18UART1.begin(9600,19,19,18, 50,swUartTestQueueLength,swUartTestQueueLength)
  software8UART1.begin(9600,6,6,7,50,swUartTestQueueLength,swUartTestQueueLength)
  swUARTLoop()
  return 0

def swUARTLoop():
  delay(1000)
  for uart_i in range(0, numberOfSWUarts):
    while software18Uarts[uart_i].read() != -1:
      delay(0)
    while software8Uarts[uart_i].read() != -1:
      delay(0)


  for iteration in range(0, 200):

    txCount18 = [0] * (4)
    txCount8 = [0] * (4)
    rxSeed = txSeed

    for uart_i in range(0, numberOfSWUarts):
      txCount18[uart_i] = wrandom(countSeed) % swUartTestQueueLength

      for i in range(0, txCount18[uart_i]):
        uart18Tx[uart_i][i] = wrandom(txSeed)
      txCount8[uart_i] = wrandom(countSeed) % swUartTestQueueLength

      for i in range(0, txCount8[uart_i]):
        uart8Tx[uart_i][i] = wrandom(txSeed)

      bytesWritten = software18Uarts[uart_i].write(uart18Tx[uart_i], txCount18[uart_i])
      test("SWU 018",bytesWritten,txCount18[uart_i])

      bytesWritten = software8Uarts[uart_i].write(uart8Tx[uart_i], txCount8[uart_i])
      test("SWU 08W",bytesWritten,txCount8[uart_i])
    doneTransmitting = 0
    while not doneTransmitting:
      doneTransmitting = True
      for uart_i in range(0, numberOfSWUarts):
        doneTransmitting = (software18Uarts[uart_i].bytesToTransmit() == 0)
        if not doneTransmitting: continue
        doneTransmitting = (software8Uarts[uart_i].bytesToTransmit() == 0)
        if not doneTransmitting: continue
      delay(0)
    delay(45);  # Allow last byte to send
    for uart_i in range(0, numberOfSWUarts):
      # TODO_MANUAL_CONVERSION: bytesRead = software8Uarts[uart_i].readBytes((char*)uart8Rx[uart_i], txCount18[uart_i])
      test("SWU 1",bytesRead,txCount18[uart_i])
      for i in range(0, txCount18[uart_i]):
        test("SWU 1_8",uart8Rx[uart_i][i] ,wrandom(rxSeed))
      # TODO_MANUAL_CONVERSION: bytesRead = software18Uarts[uart_i].readBytes((char*)uart18Rx[uart_i], txCount8[uart_i])
      test("SWU 2",bytesRead,txCount8[uart_i])
      for i in range(0, txCount8[uart_i]):
        test("SWU 2_8",uart18Rx[uart_i][i] ,wrandom(rxSeed))
