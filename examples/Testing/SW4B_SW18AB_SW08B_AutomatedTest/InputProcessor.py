# Converted from Testing/SW4B_SW18AB_SW08B_AutomatedTest/InputProcessor.ino
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
import SerialWombatPWM
import SerialWombatProcessedInputPin

ipInput18 = SerialWombatPWM.SerialWombatPWM_18AB(SW18AB_6B)
ipInput8 = SerialWombatPWM.SerialWombatPWM_18AB(SW8B_68)
processedInput18 = SerialWombatProcessedInputPin.SerialWombatProcessedInputPin(SW18AB_6B)
processedInput8 = SerialWombatProcessedInputPin.SerialWombatProcessedInputPin(SW8B_68)
SerialWombatPWM_18AB* ipInputPtr
SerialWombatProcessedInputPin* ipProcessedInputPtr

def inputProcessorTest(sw, pin):
  if sw == SW18AB_6B:
    ipInputPtr = ipInput18
    ipProcessedInputPtr = processedInput18
  elif sw == SW8B_68:
    ipInputPtr = ipInput8
    ipProcessedInputPtr = processedInput8
  ipDisabledTest(pin)
  ipExclusionTest(pin)
  ipAverageTest(pin)
  ipMxbTest(pin)

def ipDisabledTest(pin):
  resetAll()
  ipInputPtr.begin(pin + 1)
  ipProcessedInputPtr.begin(pin,pin + 1)

  # TODO_MANUAL_CONVERSION: for (int32_t i = 0; i < 65536; i += 13) {
    # TODO_MANUAL_CONVERSION_INDENT: ipInputPtr.writePublicData(i)
    # TODO_MANUAL_CONVERSION_INDENT: result = ipProcessedInputPtr.readPublicData()
    # TODO_MANUAL_CONVERSION_INDENT: test("IP_DIS_01", result, i)
    # TODO_MANUAL_CONVERSION_INDENT: delay(0)
  ipProcessedInputPtr.writeInverted(True)
  # TODO_MANUAL_CONVERSION: for (int32_t i = 0; i < 65536; i += 13) {
    # TODO_MANUAL_CONVERSION_INDENT: ipInputPtr.writePublicData(i)
    # TODO_MANUAL_CONVERSION_INDENT: result = ipProcessedInputPtr.readPublicData()
    # TODO_MANUAL_CONVERSION_INDENT: test("IP_DIS_02", result, i)
    # TODO_MANUAL_CONVERSION_INDENT: delay(0)
  ipProcessedInputPtr.writeProcessedInputEnable(True)
  # TODO_MANUAL_CONVERSION: for (int32_t i = 0; i < 65536; i += 13) {
    # TODO_MANUAL_CONVERSION_INDENT: ipInputPtr.writePublicData(i)
    # TODO_MANUAL_CONVERSION_INDENT: result = ipProcessedInputPtr.readPublicData()
    # TODO_MANUAL_CONVERSION_INDENT: test("IP_INV_01", result, 65535 - i)
    # TODO_MANUAL_CONVERSION_INDENT: delay(0)
  ipProcessedInputPtr.writeInverted(False)
  # TODO_MANUAL_CONVERSION: for (int32_t i = 0; i < 65536; i += 13) {
    # TODO_MANUAL_CONVERSION_INDENT: ipInputPtr.writePublicData(i)
    # TODO_MANUAL_CONVERSION_INDENT: result = ipProcessedInputPtr.readPublicData()
    # TODO_MANUAL_CONVERSION_INDENT: test("IP_INV_02", result, i)
    # TODO_MANUAL_CONVERSION_INDENT: delay(0)


def ipExclusionTest(pin):
  resetAll()
  ipInputPtr.begin(pin + 1)
  ipProcessedInputPtr.begin(pin,pin + 1)
  ipProcessedInputPtr.writeProcessedInputEnable(True)
  ipInputPtr.writePublicData(12500)
  ipProcessedInputPtr.writeExcludeBelowAbove(20000,40000)

  # TODO_MANUAL_CONVERSION: for (int32_t i = 0; i < 19999; i += 13) {
    # TODO_MANUAL_CONVERSION_INDENT: ipInputPtr.writePublicData(i)
    # TODO_MANUAL_CONVERSION_INDENT: result = ipProcessedInputPtr.readPublicData()
    # TODO_MANUAL_CONVERSION_INDENT: test("IP_EX_01", result, 12500)
    # TODO_MANUAL_CONVERSION_INDENT: delay(0)
  lastVal = 0
  # TODO_MANUAL_CONVERSION: for (int32_t i = 20000; i < 40001; i += 13) {
    # TODO_MANUAL_CONVERSION_INDENT: ipInputPtr.writePublicData(i)
    # TODO_MANUAL_CONVERSION_INDENT: lastVal = ipProcessedInputPtr.readPublicData()
    # TODO_MANUAL_CONVERSION_INDENT: test("IP_EX_02", lastVal, i)
    # TODO_MANUAL_CONVERSION_INDENT: delay(0)
  # TODO_MANUAL_CONVERSION: for (int32_t i = 40001; i < 65536; i += 13) {
    # TODO_MANUAL_CONVERSION_INDENT: ipInputPtr.writePublicData(i)
    # TODO_MANUAL_CONVERSION_INDENT: result = ipProcessedInputPtr.readPublicData()
    # TODO_MANUAL_CONVERSION_INDENT: test("IP_EX_03", result, lastVal)
    # TODO_MANUAL_CONVERSION_INDENT: delay(0)


def ipAverageTest(pin):

  resetAll()

  ipProcessedInputPtr.begin(pin,SW_DATA_SOURCE_LFSR)


  ipProcessedInputPtr.writeAveragingNumberOfSamples(4000)

  ipProcessedInputPtr.writeProcessedInputEnable(True)

  delay(5000)

  result = ipProcessedInputPtr.readAverage()
  test("IP_AVG_01", result, 32768, 500);  # Random should average out to 32768, will allow +/- 500

  ipProcessedInputPtr.writeExcludeBelowAbove(40000,60000)

  delay(30000)


  result = ipProcessedInputPtr.readAverage()
  test("IP_AVG_01", result, 50000, 500);  # Random should average out to 50000, will allow +/- 500

def ipMxbTest(pin):
  resetAll()
  ipInputPtr.begin(pin + 1)
  ipProcessedInputPtr.begin(pin,pin + 1)
  ipProcessedInputPtr.writeProcessedInputEnable(True)

  ipProcessedInputPtr.writeTransformLinearMXB(5 * 256,32)

  # TODO_MANUAL_CONVERSION: for (int32_t i = 0; i < 65535; i += 13) {
    # TODO_MANUAL_CONVERSION_INDENT: ipInputPtr.writePublicData(i)
    # TODO_MANUAL_CONVERSION_INDENT: result = ipProcessedInputPtr.readPublicData()
    # TODO_MANUAL_CONVERSION_INDENT: expected = i * 5  + 32
    # TODO_MANUAL_CONVERSION_INDENT: if expected > 65535:
      # TODO_MANUAL_CONVERSION_INDENT: expected = 65535
    # TODO_MANUAL_CONVERSION_INDENT: test("IP_MXB_01", result, expected)
    # TODO_MANUAL_CONVERSION_INDENT: delay(0)

  ipProcessedInputPtr.writeTransformLinearMXB(5 * 256,-20000)

  # TODO_MANUAL_CONVERSION: for (int32_t i = 0; i < 65535; i += 13) {
    # TODO_MANUAL_CONVERSION_INDENT: ipInputPtr.writePublicData(i)
    # TODO_MANUAL_CONVERSION_INDENT: result = ipProcessedInputPtr.readPublicData()
    # TODO_MANUAL_CONVERSION_INDENT: expected = i * 5 - 20000
    # TODO_MANUAL_CONVERSION_INDENT: if expected > 65535:
      # TODO_MANUAL_CONVERSION_INDENT: expected = 65535
    # TODO_MANUAL_CONVERSION_INDENT: if expected < 0:
      # TODO_MANUAL_CONVERSION_INDENT: expected = 0

    # TODO_MANUAL_CONVERSION_INDENT: test("IP_MXB_02", result, expected)
    # TODO_MANUAL_CONVERSION_INDENT: delay(0)
  ipProcessedInputPtr.writeTransformLinearMXB(-5 * 256,100000)

  # TODO_MANUAL_CONVERSION: for (int32_t i = 0; i < 65535; i += 13) {
    # TODO_MANUAL_CONVERSION_INDENT: ipInputPtr.writePublicData(i)
    # TODO_MANUAL_CONVERSION_INDENT: result = ipProcessedInputPtr.readPublicData()
    # TODO_MANUAL_CONVERSION_INDENT: expected = i * -5  + 100000
    # TODO_MANUAL_CONVERSION_INDENT: if expected > 65535:
      # TODO_MANUAL_CONVERSION_INDENT: expected = 65535
    # TODO_MANUAL_CONVERSION_INDENT: if expected < 0:
      # TODO_MANUAL_CONVERSION_INDENT: expected = 0

    # TODO_MANUAL_CONVERSION_INDENT: test("IP_MXB_03", result, expected)
    # TODO_MANUAL_CONVERSION_INDENT: delay(0)
