# Converted from PinModes/TM1637/TM1637_Ex02_PublicData/TM1637_Ex02_PublicData.ino
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
import SerialWombatTM1637
tm1637Decimal16 = SerialWombatTM1637.SWTM1637Mode.tm1637Decimal16
tm1637Hex16 = SerialWombatTM1637.SWTM1637Mode.tm1637Hex16
tm1637CharArray = SerialWombatTM1637.SWTM1637Mode.tm1637CharArray
tm1637RawArray = SerialWombatTM1637.SWTM1637Mode.tm1637RawArray
tm1637Animation = SerialWombatTM1637.SWTM1637Mode.tm1637Animation


#
#This example shows how to display a number on a TM1637 display based on the public data of a Serial Wombat pin or other
#data source within the Serial Wombat chip.
#
#If you haven't already, run the SW_Ard_TM1637_012345 example to ensure your display displays digits in
#the correct order.  If necessary, correct the call to writeDigitOrder below as described in that example.
#For four digit displays, you'll likely want to use writeDigitOrder(2,3,4,5,0,1) in order to show the least
#significant digits.
#
#This sketch assumes a potentiometer output dividing ground and 3.3v  is connected to pin 0 as an analog input.
#
#This sketch is designed to be experimented with.  Comment in #define's in the  CONFIG sections below to try out different options and how they affect the display
#
#A video demonstrating the use of the TM1637 pin mode on the Serial Wombat 18AB chip is available at:
#https://youtu.be/AwW12n6o_T0
#
#Documentation for the SerialWombatTM1637 Arduino class is available at:
#https://broadwellconsultinginc.github.io/SerialWombatArdLib/class_serial_wombat_t_m1637.html#details
#
#Serial Wombat is a registered trademark in the United States of Broadwell Consulting Inc.
#
#

# sw is provided by the selected interface block above
myDisplay = SerialWombatTM1637.SerialWombatTM1637(sw)
DISPLAY_CLK_PIN = 19  # <<<<<<<<<   Set this to the Serial Wombat pin connected to your Display Clock Pin
DISPLAY_DIN_PIN = 18  # <<<<<<<<<   Set this to the Serial Wombat pin connected to your Display Data Pin

potentiometer = SerialWombatAnalogInput.SerialWombatAnalogInput(sw)

#CONFIG:  Which mode... Hex or decimal?  Comment in one...
TM1637_MODE = tm1637Decimal16
##define TM1637_MODE tm1637Hex16


#Config:  What data source?  Comment in one
##define DATA_SOURCE SW_DATA_SOURCE_PIN_0
DATA_SOURCE = SW_DATA_SOURCE_INCREMENTING_NUMBER
##define DATA_SOURCE SW_DATA_SOURCE_TEMPERATURE


#Config:  blank leading zeros?   Make True or false
SURPRESS_LEADING_ZEROS = True


def setup():
  # put your setup code here, to run once:
  # Wire.begin() is handled by the selected Python interface block

  # Serial.begin() is not used in this Python example
  delay(3000)
  print("TM1637 Public Data Display Example")


  sw.begin()  # Python interface was configured above

  #Optional Error handling code begin:
  if sw.isSW04():
    print("This Example is not supported on the Serial Wombat 4B chip.  An 8B or 18AB chip is required.")
    while True:
      delay(100)
  if not sw.isLatestFirmware():
    print("Firmware version mismatch.  Download latest Serial Wombat Arduino Library and update Serial Wombat Firmware to latest version")
  if sw.isSW08()  and  not sw.isPinModeSupported(PIN_MODE_TM1637):
    print("The required pin mode does not appear to be supported in this firmware build.  Do you need to download a different firmware?")
    while True:
      delay(100)
  sw.registerErrorHandler(SerialWombatSerialErrorHandlerBrief);  #Register an error handler that will print communication errors to Serial
  #Optional Error handling code end

  myDisplay.begin(19,  #Clk Pin
  18,  # Data Pin
  6,  # Number of digits
  TM1637_MODE,  # Mode enumeration
  DATA_SOURCE,
  4);  # Brightness

  myDisplay.writeDigitOrder(0,1,2,3,4,5)

  myDisplay.suppressLeadingZeros(SURPRESS_LEADING_ZEROS)

  potentiometer.begin(0,64,0)

def loop():
  pass


setup()
while True:
    loop()
