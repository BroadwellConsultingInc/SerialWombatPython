# Converted from Boards/PCB0046_SW8B_HSD/HSD_Ex01/HSD_Ex01.ino
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
import PCB0046_HSD

#This example shows how to turn a channel on and off on the Serial Wombat PCB0046 HSD Board
#*  and monitor the current feedback and diagnostic lines.
#

PCB0046_I2C_BASE_ADDRESS = 0x60  # << COMMENT IN THIS LINE AND SET THE BASE (Even) ADDRESS FOR YOUR BOARD!  It uses this plus this + 1.
# #ifndef PCB0046_I2C_BASE_ADDRESS
# #error "Comment in and set the Address define below the main comment.  The default address is 0x60"
# #endif

hsd = PCB0046_HSD.PCB0046_HSD_PWM(sw, sw)
def setup():
  # put your setup code here, to run once:
  # Wire.begin() is handled by the selected Python interface block
  # Serial.begin() is not used in this Python example
  delay(3000)
  beginResult = hsd.begin(PCB0046_I2C_BASE_ADDRESS)

  #Optional Error Checking Code starts here
  if beginResult < 0:
    print("Something went wrong initializing the board.  This Example requires a PCB0046 HSD board")
    print("Error number: ");Serial.println(beginResult, end="")
    while True:
      delay(100)

  # Set up an error handler.  Need to do it for both Serial Wombat chips on the PCB0046
  hsd.sw0.registerErrorHandler(SerialWombatSerialErrorHandlerBrief);  #Register an error handler that will print communication errors to Serial
  hsd.sw1.registerErrorHandler(SerialWombatSerialErrorHandlerBrief);  #Register an error handler that will print communication errors to Serial
  #Optional Error handling code end

  hsd.selectCurrentFeedbackChannel(6)

def loop():

  hsd.output6.writePublicData(0xFFFF);  # Turn on the channel
  delay(10000);  #Wait 10 seconds


  #Read the current for the channel and get the diagnostics
  print(hsd.readCurrentFeedbackAverage_mA())
  if hsd.readChip0to3IsFaulted():
    print(" FAULT 0to3", end="")
  if hsd.readChip4to7IsFaulted():
    print(" FAULT 4to7", end="")
  print()





  hsd.output6.writePublicData(0);  # Turn off and wait 10 seconds
  delay(10000)
  print(hsd.readCurrentFeedbackAverage_mA())
  print(hsd.readVin_mV())


setup()
while True:
    loop()
