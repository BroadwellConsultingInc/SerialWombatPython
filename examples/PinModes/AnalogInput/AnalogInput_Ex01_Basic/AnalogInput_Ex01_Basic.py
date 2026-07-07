# Converted from PinModes/AnalogInput/AnalogInput_Ex01_Basic/AnalogInput_Ex01_Basic.ino
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
import SerialWombatAnalogInput


# sw is provided by the selected interface block above
leftPot = SerialWombatAnalogInput.SerialWombatAnalogInput(sw)  #5k linear Pot
rightPot = SerialWombatAnalogInput.SerialWombatAnalogInput(sw)  #5k linear Pot
temperatureSensor = SerialWombatAnalogInput.SerialWombatAnalogInput(sw)

# This example is explained in a video tutorial at: https://youtu.be/_EKlrEVaEhg

LEFT_POT_PIN = 2
RIGHT_POT_PIN = 1
TEMPERATURE_SENSOR_PIN = 0  # Set this pin to 3 if using SW4B, as 0 doesn't have Analog

def setup():
  # put your setup code here, to run once:
  # Wire.begin() is handled by the selected Python interface block

  # Serial.begin() is not used in this Python example
  delay(3000)
  print("1Hz Blink Example")


  sw.begin()  # Python interface was configured above

  #Optional Error handling code begin:
  if not sw.isLatestFirmware():
    print("Firmware version mismatch.  Download latest Serial Wombat Arduino Library and update Serial Wombat Firmware to latest version")
  if sw.isSW08()  and  not sw.isPinModeSupported(PIN_MODE_ANALOGINPUT):
    print("The required pin mode does not appear to be supported in this firmware build.  Do you need to download a different firmware?")
    while True:
      delay(100)
  sw.registerErrorHandler(SerialWombatSerialErrorHandlerBrief);  #Register an error handler that will print communication errors to Serial
  #Optional Error handling code end


  leftPot.begin(LEFT_POT_PIN)
  rightPot.begin(RIGHT_POT_PIN)

  temperatureSensor.begin(TEMPERATURE_SENSOR_PIN,64,65417);  #  average 64 samples, .5 Hz Low Pass filter.


def loop():

  print("Source V: ", end="")
  supplyVoltage = sw.readSupplyVoltage_mV()
  print(supplyVoltage, end="")
  print("mV      Left Pot: ", end="")
  print(leftPot.readCounts(), end="")
  print(" ", end="")

  leftVoltage = leftPot.readVoltage_mV()
  print(leftVoltage, end="")
  print("mV      Right Pot:", end="")

  print(rightPot.readCounts(), end="")
  print(" ", end="")
  rightVoltage = rightPot.readVoltage_mV()
  print(rightVoltage, end="")

  print("mV      T:", end="")

  print(temperatureSensor.readCounts(), end="")
  print(" ", end="")
  print(temperatureSensor.readVoltage_mV(), end="")
  print("mV ", end="")


  tempSensor_mV = temperatureSensor.readAveraged_mV()

  #See datasheet for TMP36 Temperature sensor for conversion
  temperature = (tempSensor_mV - 750) / 10.0 + 25

  print(temperature, end="")
  print(" deg C ", end="")


  print()
  delay(200)


setup()
while True:
    loop()
