# Converted from Testing/SW4B_SW18AB_SW08B_AutomatedTest/Queue.ino
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

# Note: this uses the SimpleQueue Library by msilveus

QUEUETEST_MAX_QUEUE_SIZE = 513
ardQData = [0] * (QUEUETEST_MAX_QUEUE_SIZE)
queuetempData = [0] * (QUEUETEST_MAX_QUEUE_SIZE)
swqTempData = [0] * (QUEUETEST_MAX_QUEUE_SIZE)

QUEUE_TEST_NUMBER_ITERATIONS = 1000
def queueTest(sw):

  queueSizeMax = QUEUETEST_MAX_QUEUE_SIZE
  queueSizeMin = 4
  if sw == SW8B_68:
    queueSizeMax = 80
  for queueSize in range(queueSizeMin, queueSizeMax):

    s = [0] * (80)
    swq = SerialWombatQueue.SerialWombatQueue(sw)
    # TODO_MANUAL_CONVERSION: SimpleQueue q(ardQData,1,queueSize)


    lfsrSeed = queueSize
    queueOffset = wrandom(lfsrSeed)
    queueOffset = 0x3FE;  # Up to 1022, even numbers
    if sw == SW8B_68:
      queueOffset = 0xE;  # Up to 14
    swq.begin(queueOffset, queueSize)
    swq.setTimeout(0)
    for iteration in range(0, QUEUE_TEST_NUMBER_ITERATIONS):
      action = wrandom(lfsrSeed)
      # TODO_MANUAL_CONVERSION: switch (action >> 30) {
        # TODO_MANUAL_CONVERSION_INDENT: case 0:  #Add to queue
          # TODO_MANUAL_CONVERSION_INDENT: count = action % queueSize

          # TODO_MANUAL_CONVERSION_INDENT: aqSuccess = 0
          # TODO_MANUAL_CONVERSION_INDENT: swqSuccess = 0
          # TODO_MANUAL_CONVERSION_INDENT: for x in range(0, count):
            # TODO_MANUAL_CONVERSION_INDENT: queuetempData[x] =  wrandom(lfsrSeed)

            # TODO_MANUAL_CONVERSION_INDENT: if q.push(queuetempData[x]):
              #
              #Serial.print("s: ");
              #Serial.print(x);
              #Serial.print(" c: ");
              #Serial.println(q.count());
              #
              # TODO_MANUAL_CONVERSION_INDENT: aqSuccess++

            # TODO_MANUAL_CONVERSION_INDENT: else:
              #
              #Serial.print("f: ");
              #Serial.print(x);
              #Serial.print(" c: ");
              #Serial.println(q.count());
              #


          # TODO_MANUAL_CONVERSION_INDENT: swqSuccess = swq.write((const uint8_t*) queuetempData, count)


          # TODO_MANUAL_CONVERSION_INDENT: s = ("Q write: it: %d, count: %d, aq: %d, sw: %d") % (iteration, count,  aqSuccess, swqSuccess)
          # TODO_MANUAL_CONVERSION_INDENT: test(s, swqSuccess, aqSuccess)
          # TODO_MANUAL_CONVERSION_INDENT: if swqSuccess == aqSuccess:

          # TODO_MANUAL_CONVERSION_INDENT: else:
            # TODO_MANUAL_CONVERSION_INDENT: iteration = QUEUE_TEST_NUMBER_ITERATIONS

        # TODO_MANUAL_CONVERSION_INDENT: break
        # TODO_MANUAL_CONVERSION_INDENT: case 1:  #Remove from queue
          # TODO_MANUAL_CONVERSION_INDENT: count = action % queueSize

          # TODO_MANUAL_CONVERSION_INDENT: aqSuccess = 0
          # TODO_MANUAL_CONVERSION_INDENT: swqSuccess = 0
          # TODO_MANUAL_CONVERSION_INDENT: for x in range(0, count):

            # TODO_MANUAL_CONVERSION_INDENT: if q.pop(queuetempData[aqSuccess]):
              # TODO_MANUAL_CONVERSION_INDENT: aqSuccess++

          # TODO_MANUAL_CONVERSION_INDENT: swqSuccess = swq.readBytes((char*) swqTempData, aqSuccess)


          # TODO_MANUAL_CONVERSION_INDENT: s = ("Q read: it: %d, count: %d, aq: %d, sw: %d") % (iteration, count, swqSuccess, aqSuccess)
          # TODO_MANUAL_CONVERSION_INDENT: test(s, swqSuccess, aqSuccess)
          # TODO_MANUAL_CONVERSION_INDENT: if swqSuccess == aqSuccess:
            # TODO_MANUAL_CONVERSION_INDENT: for x in range(0, aqSuccess):
              # TODO_MANUAL_CONVERSION_INDENT: s = ("Q read: it: %d, count: %d, aq: %d, sw: %d, x: %d") % (iteration, count, swqSuccess, aqSuccess,x)
              # TODO_MANUAL_CONVERSION_INDENT: test(s, swqTempData[x], queuetempData[x])
          # TODO_MANUAL_CONVERSION_INDENT: else:
            # TODO_MANUAL_CONVERSION_INDENT: iteration = QUEUE_TEST_NUMBER_ITERATIONS

        # TODO_MANUAL_CONVERSION_INDENT: break


        # TODO_MANUAL_CONVERSION_INDENT: case 2:  # Check filled bytes
          # TODO_MANUAL_CONVERSION_INDENT: s = ("Q count: it: %d ") % (iteration)
          # TODO_MANUAL_CONVERSION_INDENT: test(s, swq.available(), q.count())
        # TODO_MANUAL_CONVERSION_INDENT: break
        # TODO_MANUAL_CONVERSION_INDENT: case 3:  # Check peek
          # TODO_MANUAL_CONVERSION_INDENT: s = ("Q peek: it: %d ") % (iteration)
          # TODO_MANUAL_CONVERSION_INDENT: value = *(uint8_t*)q.peek(0)
          # TODO_MANUAL_CONVERSION_INDENT: test(s,swq.peek(),value)

        # TODO_MANUAL_CONVERSION_INDENT: break
