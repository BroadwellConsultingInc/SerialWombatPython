# Converted from Testing/SW4B_SW18AB_SW08B_AutomatedTest/Debounce.ino
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
import SerialWombatDebouncedInput
import SerialWombatPWM

debouncedInput18 = SerialWombatDebouncedInput.SerialWombatDebouncedInput(SW18AB_6B)
DBPWM5 = SerialWombatPWM.SerialWombatPWM_4AB(SW4B_6D)
def debounceTest(sw):
  SerialWombatDebouncedInput* debouncedInput
  if sw == SW18AB_6B:
    SW18ABpin = 5
    debouncedInput = debouncedInput18
    DBPWM5.begin(SW18ABPinTo4BPin(SW18ABpin))
    DBPWM5.setFrequency_SW4AB(SW4AB_PWMFrequency_125_Hz)
    DBPWM5.writeDutyCycle(0x8000);  # 4 ms
    debouncedInput.begin(SW18ABpin,6,False,False);  # 6ms time.
    delay(500)
    debouncedInput.readTransitionsState()

    if debouncedInput.transitions < 2:
      pass
      # TODO_MANUAL_CONVERSION: pass(1)
    else:
      fail(1)

    DBPWM5.setFrequency_SW4AB(SW4AB_PWMFrequency_63_Hz)
    DBPWM5.writeDutyCycle(0x8000);  # 8 ms
    delay(500)
    debouncedInput.readTransitionsState()
    if debouncedInput.transitions < 15:
      fail(1)
    else:
      pass
      # TODO_MANUAL_CONVERSION: pass(1)

    DBPWM5.begin(SW18ABPinTo4BPin(SW18ABpin))
    DBPWM5.setFrequency_SW4AB(SW4AB_PWMFrequency_125_Hz)
    DBPWM5.writeDutyCycle(0xF000)
    delay(100)
    if debouncedInput.readTransitionsState():
      pass
      # TODO_MANUAL_CONVERSION: pass(1)
    else:
      fail(1)

    DBPWM5.writeDutyCycle(0x1000)
    delay(100)
    if debouncedInput.readTransitionsState():
      fail(1)
    else:
      pass
      # TODO_MANUAL_CONVERSION: pass(1)
  elif sw == SW8B_68:
    test ("Debounce for SW8B Not Implemented. ", 0)
  elif sw == SW4B_6C:
    test ("Debounce for SW4B Not Implemented. ", 0)
