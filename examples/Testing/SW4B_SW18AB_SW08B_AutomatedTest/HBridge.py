# Converted from Testing/SW4B_SW18AB_SW08B_AutomatedTest/HBridge.ino
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
import SerialWombatHBridge
HBRIDGE_OFF_BOTH_LOW = SerialWombatHBridge.SerialWombatHBridgeDriverMode.HBRIDGE_OFF_BOTH_LOW
HBRIDGE_OFF_BOTH_HIGH = SerialWombatHBridge.SerialWombatHBridgeDriverMode.HBRIDGE_OFF_BOTH_HIGH
HBRIDGE_RELAY_AND_PWM = SerialWombatHBridge.SerialWombatHBridgeDriverMode.HBRIDGE_RELAY_AND_PWM

HBridge18 = SerialWombatHBridge.SerialWombatHBridge_18AB(SW18AB_6B)
HBridge8 = SerialWombatHBridge.SerialWombatHBridge_18AB(SW8B_68)

HBRIDGE_TEST_INCREMENTS = 100


def hBridgeTest(sw, hBridgeFirstPin, hBridgeSecondPin):
  resetAll()

  SerialWombatHBridge_18AB* HBridge

  if sw == SW18AB_6B:
    HBridge = HBridge18

  if sw == SW8B_68:
    HBridge = HBridge8


  HBridge.begin(hBridgeFirstPin, hBridgeSecondPin, 4000, HBRIDGE_OFF_BOTH_LOW);  # Should initialize to 32768.  250 cycles per second
  initializePulseReaduS(sw,hBridgeFirstPin)
  initializePulseReaduS(sw,hBridgeSecondPin)

    # TODO_MANUAL_CONVERSION_INDENT: firstPinCounts = pulseCounts(sw,hBridgeFirstPin)
    # TODO_MANUAL_CONVERSION_INDENT: secondPinCounts = pulseCounts(sw,hBridgeSecondPin)

    # TODO_MANUAL_CONVERSION_INDENT: delay(1000)

    # TODO_MANUAL_CONVERSION_INDENT: test("HBridge_00A", pulseCounts(sw,hBridgeFirstPin), firstPinCounts);  #There should have been no pulses on either.
    # TODO_MANUAL_CONVERSION_INDENT: test("HBridge_00B", pulseCounts(sw,hBridgeSecondPin), secondPinCounts)
    # TODO_MANUAL_CONVERSION_INDENT: HBridge.writePublicData(0x0000);  # One high, one low, no PWM
    # TODO_MANUAL_CONVERSION_INDENT: delay(100)
    # TODO_MANUAL_CONVERSION_INDENT: firstPinCounts = pulseCounts(sw,hBridgeFirstPin)
    # TODO_MANUAL_CONVERSION_INDENT: secondPinCounts = pulseCounts(sw,hBridgeSecondPin)
    # TODO_MANUAL_CONVERSION_INDENT: delay(1000)

    # TODO_MANUAL_CONVERSION_INDENT: test("HBridge_01A", pulseCounts(sw,hBridgeFirstPin), firstPinCounts);  #There should have been no pulses on either.
    # TODO_MANUAL_CONVERSION_INDENT: test("HBridge_01B", pulseCounts(sw,hBridgeSecondPin), secondPinCounts)
    # TODO_MANUAL_CONVERSION_INDENT: HBridge.writePublicData(0xFFFF);  # One high, one low, no PWM
    # TODO_MANUAL_CONVERSION_INDENT: delay(100)
    # TODO_MANUAL_CONVERSION_INDENT: firstPinCounts = pulseCounts(sw,hBridgeFirstPin)
    # TODO_MANUAL_CONVERSION_INDENT: secondPinCounts = pulseCounts(sw,hBridgeSecondPin)
    # TODO_MANUAL_CONVERSION_INDENT: delay(1000)

    # TODO_MANUAL_CONVERSION_INDENT: test("HBridge_02A", pulseCounts(sw,hBridgeFirstPin), firstPinCounts);  #There should have been no pulses on either.
    # TODO_MANUAL_CONVERSION_INDENT: test("HBridge_02B", pulseCounts(sw,hBridgeSecondPin), secondPinCounts)
    # TODO_MANUAL_CONVERSION_INDENT: HBridge.writePublicData(0xC000);  # One PWM, one low
    # TODO_MANUAL_CONVERSION_INDENT: delay(100)
    # TODO_MANUAL_CONVERSION_INDENT: firstPinCounts = pulseCounts(sw,hBridgeFirstPin)
    # TODO_MANUAL_CONVERSION_INDENT: secondPinCounts = pulseCounts(sw,hBridgeSecondPin)
    # TODO_MANUAL_CONVERSION_INDENT: delay(1000)

    # TODO_MANUAL_CONVERSION_INDENT: test("HBridge_03A", pulseCounts(sw,hBridgeFirstPin), firstPinCounts + 250, 15)
    # TODO_MANUAL_CONVERSION_INDENT: test("HBridge_03B", pulseCounts(sw,hBridgeSecondPin), secondPinCounts)
    # TODO_MANUAL_CONVERSION_INDENT: test("HBridge_03C", dutyCycleRead(sw,hBridgeFirstPin),0x8000,0x100)

    # TODO_MANUAL_CONVERSION_INDENT: HBridge.writePublicData(0xE000);  # One PWM, one low
    # TODO_MANUAL_CONVERSION_INDENT: delay(100)
    # TODO_MANUAL_CONVERSION_INDENT: firstPinCounts = pulseCounts(sw,hBridgeFirstPin)
    # TODO_MANUAL_CONVERSION_INDENT: secondPinCounts = pulseCounts(sw,hBridgeSecondPin)
    # TODO_MANUAL_CONVERSION_INDENT: delay(1000)

    # TODO_MANUAL_CONVERSION_INDENT: test("HBridge_04A", pulseCounts(sw,hBridgeFirstPin),firstPinCounts + 250, 15)
    # TODO_MANUAL_CONVERSION_INDENT: test("HBridge_04B", pulseCounts(sw,hBridgeSecondPin), secondPinCounts)
    # TODO_MANUAL_CONVERSION_INDENT: test("HBridge_04C", dutyCycleRead(sw,hBridgeFirstPin),0xC000,0x100)

    # TODO_MANUAL_CONVERSION_INDENT: HBridge.writePublicData(0xA000);  # One PWM, one low
    # TODO_MANUAL_CONVERSION_INDENT: delay(100)
    # TODO_MANUAL_CONVERSION_INDENT: firstPinCounts = pulseCounts(sw,hBridgeFirstPin)
    # TODO_MANUAL_CONVERSION_INDENT: secondPinCounts = pulseCounts(sw,hBridgeSecondPin)
    # TODO_MANUAL_CONVERSION_INDENT: delay(1000)

    # TODO_MANUAL_CONVERSION_INDENT: test("HBridge_05A", pulseCounts(sw,hBridgeFirstPin),firstPinCounts +  250, 15)
    # TODO_MANUAL_CONVERSION_INDENT: test("HBridge_05B", pulseCounts(sw,hBridgeSecondPin), secondPinCounts)
    # TODO_MANUAL_CONVERSION_INDENT: test("HBridge_05C", dutyCycleRead(sw,hBridgeFirstPin),0x4000,0x100)

    # TODO_MANUAL_CONVERSION_INDENT: HBridge.writePublicData(0x4000);  # One PWM, one low
    # TODO_MANUAL_CONVERSION_INDENT: delay(100)
    # TODO_MANUAL_CONVERSION_INDENT: firstPinCounts = pulseCounts(sw,hBridgeFirstPin)
    # TODO_MANUAL_CONVERSION_INDENT: secondPinCounts = pulseCounts(sw,hBridgeSecondPin)
    # TODO_MANUAL_CONVERSION_INDENT: delay(1000)

    # TODO_MANUAL_CONVERSION_INDENT: test("HBridge_06A", pulseCounts(sw,hBridgeFirstPin), firstPinCounts)
    # TODO_MANUAL_CONVERSION_INDENT: test("HBridge_06B", pulseCounts(sw,hBridgeSecondPin), secondPinCounts + 250, 15)
    # TODO_MANUAL_CONVERSION_INDENT: test("HBridge_06C", dutyCycleRead(sw,hBridgeSecondPin),0x8000,0x100)
    # TODO_MANUAL_CONVERSION_INDENT: HBridge.writePublicData(0x2000);  # One PWM, one low
    # TODO_MANUAL_CONVERSION_INDENT: delay(100)
    # TODO_MANUAL_CONVERSION_INDENT: firstPinCounts = pulseCounts(sw,hBridgeFirstPin)
    # TODO_MANUAL_CONVERSION_INDENT: secondPinCounts = pulseCounts(sw,hBridgeSecondPin)
    # TODO_MANUAL_CONVERSION_INDENT: delay(1000)

    # TODO_MANUAL_CONVERSION_INDENT: test("HBridge_07A", pulseCounts(sw,hBridgeFirstPin), firstPinCounts)
    # TODO_MANUAL_CONVERSION_INDENT: test("HBridge_07B", pulseCounts(sw,hBridgeSecondPin), secondPinCounts + 250, 15)
    # TODO_MANUAL_CONVERSION_INDENT: test("HBridge_07C", dutyCycleRead(sw,hBridgeSecondPin),0xC000,0x100)

    # TODO_MANUAL_CONVERSION_INDENT: HBridge.writePublicData(0x6000);  # One PWM, one low
    # TODO_MANUAL_CONVERSION_INDENT: delay(100)
    # TODO_MANUAL_CONVERSION_INDENT: firstPinCounts = pulseCounts(sw,hBridgeFirstPin)
    # TODO_MANUAL_CONVERSION_INDENT: secondPinCounts = pulseCounts(sw,hBridgeSecondPin)
    # TODO_MANUAL_CONVERSION_INDENT: delay(1000)

    # TODO_MANUAL_CONVERSION_INDENT: test("HBridge_08A", pulseCounts(sw,hBridgeFirstPin), firstPinCounts)
    # TODO_MANUAL_CONVERSION_INDENT: test("HBridge_08B", pulseCounts(sw,hBridgeSecondPin), secondPinCounts + 250, 15)
    # TODO_MANUAL_CONVERSION_INDENT: test("HBridge_08C", dutyCycleRead(sw,hBridgeSecondPin),0x4000,0x100)
  if sw == SW18AB_6B:
      #Frequency sweep
      for period in range(2500, (60000) + 1):
        freq = 1000000 / period
        HBridge.begin(hBridgeFirstPin, hBridgeSecondPin, period, HBRIDGE_OFF_BOTH_LOW)
        for i in range(1000, 65535):
          HBridge.writePublicData(i)
          delay(10)
          initializePulseReaduS(sw,hBridgeFirstPin)
          initializePulseReaduS(sw,hBridgeSecondPin)
          firstPinCounts = pulseCounts(sw,hBridgeFirstPin)
          secondPinCounts = pulseCounts(sw,hBridgeSecondPin)
          delay(1000)

          if i < 0x8000:
            test("HBridge_09A", pulseCounts(sw,hBridgeFirstPin), firstPinCounts)
            test("HBridge_09B", pulseCounts(sw,hBridgeSecondPin), secondPinCounts + freq, 15,10)
            test("HBridge_09C", dutyCycleRead(sw,hBridgeSecondPin),2* (0x8000-i),0x100, 10)
          else:
            test("HBridge_10A", pulseCounts(sw,hBridgeFirstPin),firstPinCounts +  freq, 15,10)
            test("HBridge_10B", pulseCounts(sw,hBridgeSecondPin), secondPinCounts)
            test("HBridge_10C", dutyCycleRead(sw,hBridgeFirstPin), 2*(i - 0x8000) ,0x100, 10)



      delay(100)
