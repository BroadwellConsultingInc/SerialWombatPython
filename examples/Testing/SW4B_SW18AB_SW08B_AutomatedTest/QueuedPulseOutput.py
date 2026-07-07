# Converted from Testing/SW4B_SW18AB_SW08B_AutomatedTest/QueuedPulseOutput.ino
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
import SerialWombatQueue
import SerialWombatQueuedPulseOutput
import SerialWombatUART


queuedPulseOutput = SerialWombatQueuedPulseOutput.SerialWombatQueuedPulseOutput(SW18AB_6B)


def queuedPulseOutputTest():
  pin = 10
    # Test 1 pulse internal queue, uS

    # TODO_MANUAL_CONVERSION_INDENT: queuedPulseOutput.begin(pin, 0,  # start low
    # TODO_MANUAL_CONVERSION_INDENT: 0,  # Idle state
    # TODO_MANUAL_CONVERSION_INDENT: 0,  # uS pulses
    # TODO_MANUAL_CONVERSION_INDENT: 0xFFFF);  # Use internal queue

    # TODO_MANUAL_CONVERSION_INDENT: initializePulseReaduS(SW18AB_6B,pin)

    # TODO_MANUAL_CONVERSION_INDENT: queuedPulseOutput.queuePulses(0x8000 | 500, 500);  # 500uS high, 500uS low
    # TODO_MANUAL_CONVERSION_INDENT: delay(5)

    # TODO_MANUAL_CONVERSION_INDENT: test("QueuedPulseOutput_00A", pulseRead(SW18AB_6B,pin), 500, 100)
    # TODO_MANUAL_CONVERSION_INDENT: test("QueuedPulseOutput_00B", pulseCounts(SW18AB_6B,pin), 1)

    # Test 2 pulses internal queue, uS
    # TODO_MANUAL_CONVERSION_INDENT: queuedPulseOutput.begin(pin, 0,  # start low
    # TODO_MANUAL_CONVERSION_INDENT: 0,  # Idle state
    # TODO_MANUAL_CONVERSION_INDENT: 0,  # uS pulses
    # TODO_MANUAL_CONVERSION_INDENT: 0xFFFF);  # Use internal queue

    # TODO_MANUAL_CONVERSION_INDENT: initializePulseReaduS(SW18AB_6B,pin)

    # TODO_MANUAL_CONVERSION_INDENT: queuedPulseOutput.queuePulses(0x8000 | 500, 500);  # 500uS high, 500uS low
    # TODO_MANUAL_CONVERSION_INDENT: queuedPulseOutput.queuePulses(0x8000 | 750, 500);  # 500uS high, 500uS low
    # TODO_MANUAL_CONVERSION_INDENT: delay(5)

    # TODO_MANUAL_CONVERSION_INDENT: test("QueuedPulseOutput_01A", pulseRead(SW18AB_6B,pin), 750, 100)
    # TODO_MANUAL_CONVERSION_INDENT: test("QueuedPulseOutput_01B", pulseCounts(SW18AB_6B,pin), 2)

    # Queuing 3 entries to an external queue, uS
    # TODO_MANUAL_CONVERSION_INDENT: q = SerialWombatQueue.SerialWombatQueue(SW18AB_6B)
    # TODO_MANUAL_CONVERSION_INDENT: queueIndex = 300
    # TODO_MANUAL_CONVERSION_INDENT: q.begin(queueIndex,  # Index
    # TODO_MANUAL_CONVERSION_INDENT: 100);  # 100 bytes

    # TODO_MANUAL_CONVERSION_INDENT: queuedPulseOutput.begin(pin, 0,  # start low
    # TODO_MANUAL_CONVERSION_INDENT: 0,  # Idle state
    # TODO_MANUAL_CONVERSION_INDENT: 0,  # uS pulses
    # TODO_MANUAL_CONVERSION_INDENT: queueIndex);  # External queue address

    # TODO_MANUAL_CONVERSION_INDENT: initializePulseReaduS(SW18AB_6B,pin)
    # TODO_MANUAL_CONVERSION_INDENT: queueData = [0x8000 | 500, 500, 0x8000 | 900, 500, 0x8000 | 300, 500]
    # TODO_MANUAL_CONVERSION_INDENT: q.write(queueData, 6)
    # TODO_MANUAL_CONVERSION_INDENT: delay(20)

    # TODO_MANUAL_CONVERSION_INDENT: test("QueuedPulseOutput_02A", pulseRead(SW18AB_6B,pin), 300, 100)
    # TODO_MANUAL_CONVERSION_INDENT: test("QueuedPulseOutput_02B", pulseCounts(SW18AB_6B,pin), 3)


    # Queuing 2 continuous high entries to internal queue,  uS

    # TODO_MANUAL_CONVERSION_INDENT: queuedPulseOutput.begin(pin, 0,  # start low
    # TODO_MANUAL_CONVERSION_INDENT: 0,  # Idle state
    # TODO_MANUAL_CONVERSION_INDENT: 0,  # uS pulses
    # TODO_MANUAL_CONVERSION_INDENT: 0xFFFF);  # Use internal queue

    # TODO_MANUAL_CONVERSION_INDENT: initializePulseReaduS(SW18AB_6B,pin)
    # TODO_MANUAL_CONVERSION_INDENT: queuedPulseOutput.queuePulses(0x8000 | 750, 0x8000 | 1000);  # 1750 high total
    # TODO_MANUAL_CONVERSION_INDENT: delay(20)

    # TODO_MANUAL_CONVERSION_INDENT: test("QueuedPulseOutput_03", pulseRead(SW18AB_6B,pin), 1750, 100)
    # TODO_MANUAL_CONVERSION_INDENT: test("QueuedPulseOutput_03B", pulseCounts(SW18AB_6B,pin), 1)

    # Queuing 2 continuous high entries to internal queue,  mS
    # TODO_MANUAL_CONVERSION_INDENT: queuedPulseOutput.begin(pin, 0,  # start low
    # TODO_MANUAL_CONVERSION_INDENT: 0,  # Idle state
    # TODO_MANUAL_CONVERSION_INDENT: 1,  # mS pulses
    # TODO_MANUAL_CONVERSION_INDENT: 0xFFFF);  # Use internal queue

    # TODO_MANUAL_CONVERSION_INDENT: initializePulseReaduS(SW18AB_6B,pin)
    # TODO_MANUAL_CONVERSION_INDENT: queuedPulseOutput.queuePulses(0x8000 | 10, 0x8000 | 10);  # 20000uS (20mS) high total
    # TODO_MANUAL_CONVERSION_INDENT: delay(50)

    # TODO_MANUAL_CONVERSION_INDENT: test("QueuedPulseOutput_04", pulseRead(SW18AB_6B,pin), 20000, 1000)
    # TODO_MANUAL_CONVERSION_INDENT: test("QueuedPulseOutput_04B", pulseCounts(SW18AB_6B,pin), 1)
    # Queuing 1 high entry to internal queue,  mS
    # TODO_MANUAL_CONVERSION_INDENT: queuedPulseOutput.begin(pin, 0,  # start low
    # TODO_MANUAL_CONVERSION_INDENT: 0,  # Idle state
    # TODO_MANUAL_CONVERSION_INDENT: 1,  # mS pulses
    # TODO_MANUAL_CONVERSION_INDENT: 0xFFFF);  # Use internal queue

    # TODO_MANUAL_CONVERSION_INDENT: initializePulseReaduS(SW18AB_6B,pin)
    # TODO_MANUAL_CONVERSION_INDENT: queuedPulseOutput.queuePulses(0x8000 | 10, 10);  # 10000uS (20mS) high total
    # TODO_MANUAL_CONVERSION_INDENT: delay(50)

    # TODO_MANUAL_CONVERSION_INDENT: test("QueuedPulseOutput_05", pulseRead(SW18AB_6B,pin), 10000, 500)
    # TODO_MANUAL_CONVERSION_INDENT: test("QueuedPulseOutput_05B", pulseCounts(SW18AB_6B,pin), 1)

    # 1200 baud UART output, idle high
    # TODO_MANUAL_CONVERSION_INDENT: resetAll()
    # TODO_MANUAL_CONVERSION_INDENT: q = SerialWombatQueue.SerialWombatQueue(SW18AB_6B)
    # TODO_MANUAL_CONVERSION_INDENT: queueIndex = 300
    # TODO_MANUAL_CONVERSION_INDENT: q.begin(queueIndex,  # Index
    # TODO_MANUAL_CONVERSION_INDENT: 100);  # 100 bytes

    # TODO_MANUAL_CONVERSION_INDENT: queuedPulseOutput.begin(pin, 1,  # start low
    # TODO_MANUAL_CONVERSION_INDENT: 1,  # Idle state
    # TODO_MANUAL_CONVERSION_INDENT: 0,  # uS pulses
    # TODO_MANUAL_CONVERSION_INDENT: queueIndex);  # External queue address
    # TODO_MANUAL_CONVERSION_INDENT: if pin != 10:
      #This test is pin specific because of matching the SW4B.  Update the pin or
      # fix the uart config below
      # TODO_MANUAL_CONVERSION_INDENT: test("QueuedPulseOutput_UARTCONFIG", 0, 1)
    # TODO_MANUAL_CONVERSION_INDENT: delay(100)
    # TODO_MANUAL_CONVERSION_INDENT: uart = SerialWombatUART.SerialWombatUART(SWChipAndPinTo4BChip(SW18AB_6B,pin))
    # TODO_MANUAL_CONVERSION_INDENT: uart.begin(1200, SW18ABPinTo4BPin(pin), SW18ABPinTo4BPin(pin), 255)
    # TODO_MANUAL_CONVERSION_INDENT: bitTime = 1000000 / 1200
    # TODO_MANUAL_CONVERSION_INDENT: asciiW = [ bitTime,  #Start Bit
    # TODO_MANUAL_CONVERSION_INDENT: (0x8000|bitTime),  # 1  W is 0x57
    # TODO_MANUAL_CONVERSION_INDENT: (0x8000|bitTime),  #
    # TODO_MANUAL_CONVERSION_INDENT: (0x8000|bitTime),  #
    # TODO_MANUAL_CONVERSION_INDENT: (bitTime),  #
    # TODO_MANUAL_CONVERSION_INDENT: (0x8000| bitTime),  #
    # TODO_MANUAL_CONVERSION_INDENT: (bitTime),  #
    # TODO_MANUAL_CONVERSION_INDENT: (0x8000|bitTime),  #
    # TODO_MANUAL_CONVERSION_INDENT: (bitTime),  #
    # TODO_MANUAL_CONVERSION_INDENT: (0x8000|bitTime),  #   Stop bit
    # TODO_MANUAL_CONVERSION_INDENT: ]
    # TODO_MANUAL_CONVERSION_INDENT: queuedPulseOutput.pause(True)
    # TODO_MANUAL_CONVERSION_INDENT: q.write(asciiW, 10)
    # TODO_MANUAL_CONVERSION_INDENT: queuedPulseOutput.pause(False)
    # TODO_MANUAL_CONVERSION_INDENT: delay(100)
    # TODO_MANUAL_CONVERSION_INDENT: data = uart.read()

    # TODO_MANUAL_CONVERSION_INDENT: test("QueuedPulseOutput_06A", data, 'W')
