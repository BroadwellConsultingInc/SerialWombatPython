# Converted from Testing/SW4B_SW18AB_SW08B_AutomatedTest/HSCounter.ino
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
import SerialWombatHSCounter
import SerialWombatPWM

HSCounter = SerialWombatHSCounter.SerialWombatHSCounter(SW18AB_6B)

def hsCounterTest():
  SWPWM19 = SerialWombatPWM.SerialWombatPWM_4AB(SW4B_6E)
  resetAll()


    # TODO_MANUAL_CONVERSION_INDENT: resetAll()
    # TODO_MANUAL_CONVERSION_INDENT: SWPWM19.begin(1)
    # TODO_MANUAL_CONVERSION_INDENT: SWPWM19.setFrequency_SW4AB(SW4AB_PWMFrequency_31250_Hz)
    # TODO_MANUAL_CONVERSION_INDENT: SWPWM19.writeDutyCycle(0x8000)
    # TODO_MANUAL_CONVERSION_INDENT: HSCounter.begin(19)
    # TODO_MANUAL_CONVERSION_INDENT: delay(1000)
    # TODO_MANUAL_CONVERSION_INDENT: pulseRead(SW18AB_6B,15)
    # TODO_MANUAL_CONVERSION_INDENT: test("HSCounter_00", HSCounter.readFrequency(), 31250,500)
    # TODO_MANUAL_CONVERSION_INDENT: test("HSCounter_00a", HSCounter.readPublicData(), 31250,500)


    # TODO_MANUAL_CONVERSION_INDENT: startTime = millis()
    # TODO_MANUAL_CONVERSION_INDENT: counts = HSCounter.readCounts(True)
    # TODO_MANUAL_CONVERSION_INDENT: counts = HSCounter.readCounts(False)
    # TODO_MANUAL_CONVERSION_INDENT: while millis() - startTime < 500:

      # TODO_MANUAL_CONVERSION_INDENT: delay(0)

      # TODO_MANUAL_CONVERSION_INDENT: counts1 = HSCounter.readCounts(False)

      # TODO_MANUAL_CONVERSION_INDENT: while millis() - startTime < 1000:
        # TODO_MANUAL_CONVERSION_INDENT: delay(0)
        # TODO_MANUAL_CONVERSION_INDENT: counts2 = HSCounter.readCounts(False)
        # TODO_MANUAL_CONVERSION_INDENT: test("HSCounter_01a", counts, 0,500)
        # TODO_MANUAL_CONVERSION_INDENT: test("HSCounter_01", counts1, 15625,500)
        # TODO_MANUAL_CONVERSION_INDENT: test("HSCounter_02", counts2, 31250,500)
        # TODO_MANUAL_CONVERSION_INDENT: resetAll()
        # TODO_MANUAL_CONVERSION_INDENT: SWPWM19.begin(1)
        # TODO_MANUAL_CONVERSION_INDENT: SWPWM19.setFrequency_SW4AB(SW4AB_PWMFrequency_125_Hz)
        # TODO_MANUAL_CONVERSION_INDENT: SWPWM19.writeDutyCycle(0x8000)
        # TODO_MANUAL_CONVERSION_INDENT: HSCounter.begin(19,  PULSE_COUNT)
        # TODO_MANUAL_CONVERSION_INDENT: delay(10000)
        # TODO_MANUAL_CONVERSION_INDENT: test("HSCounter_10", HSCounter.readPublicData(), 1250,50)



        # TODO_MANUAL_CONVERSION_INDENT: resetAll()
        # TODO_MANUAL_CONVERSION_INDENT: SWPWM19.begin(1)
        # TODO_MANUAL_CONVERSION_INDENT: SWPWM19.setFrequency_SW4AB(SW4AB_PWMFrequency_125_Hz)
        # TODO_MANUAL_CONVERSION_INDENT: SWPWM19.writeDutyCycle(0x8000)
        # TODO_MANUAL_CONVERSION_INDENT: HSCounter.begin(19,  PULSE_COUNT,8000)
        # TODO_MANUAL_CONVERSION_INDENT: delay(10000)
        # TODO_MANUAL_CONVERSION_INDENT: test("HSCounter_20", HSCounter.readPublicData(), 1000,50)

        # TODO_MANUAL_CONVERSION_INDENT: resetAll()
        # TODO_MANUAL_CONVERSION_INDENT: SWPWM19.begin(1)
        # TODO_MANUAL_CONVERSION_INDENT: SWPWM19.setFrequency_SW4AB(SW4AB_PWMFrequency_31250_Hz)
        # TODO_MANUAL_CONVERSION_INDENT: SWPWM19.writeDutyCycle(0x8000)
        # TODO_MANUAL_CONVERSION_INDENT: HSCounter.begin(19,  PULSE_COUNT,100,100)
        # TODO_MANUAL_CONVERSION_INDENT: delay(10000)
        # TODO_MANUAL_CONVERSION_INDENT: test("HSCounter_30", HSCounter.readPublicData(), 3125,10)

      # TODO_MANUAL_CONVERSION_INDENT: resetAll()
