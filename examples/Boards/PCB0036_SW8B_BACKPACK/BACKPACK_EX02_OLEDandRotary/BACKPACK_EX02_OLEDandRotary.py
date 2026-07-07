# Converted from Boards/PCB0036_SW8B_BACKPACK/BACKPACK_EX02_OLEDandRotary/BACKPACK_EX02_OLEDandRotary.ino
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
import SerialWombatQuadEnc

SCREEN_WIDTH = 128  # OLED display width, in pixels
SCREEN_HEIGHT = 64  # OLED display height, in pixels

display = Adafruit_SH1106G(SCREEN_WIDTH, SCREEN_HEIGHT, Wire, -1)

# sw is provided by the selected interface block above
Pin6QuadEnc = SerialWombatQuadEnc.SerialWombatQuadEnc_18AB(sw)
conf = SerialWombatDebouncedInput.SerialWombatDebouncedInput(sw)
back = SerialWombatDebouncedInput.SerialWombatDebouncedInput(sw)
push = SerialWombatDebouncedInput.SerialWombatDebouncedInput(sw)
# TODO_MANUAL_CONVERSION: void redraw(void)

def setup():

  #Wire.begin(); // This is in Adafruit's display.begin, so we comment it out.  Call the display begin before other I2C devices

  # Serial.begin() is not used in this Python example
  delay(500)

  display.begin(0x3C, True)
  display.display()
  display.clearDisplay()
  display.setTextSize(1)
  display.setTextColor(SH110X_WHITE)
  display.setCursor(0, 0)
  display.write("Test")
  display.display()


  delay(500)

  sw.begin()  # Python interface was configured above
  sw.registerErrorHandler(SerialWombatSerialErrorHandlerBrief);  #Register an error handler that will print communication errors to Serial

  if not sw.isLatestFirmware():
    print("Firmware version mismatch.  Download latest Serial Wombat Arduino Library and update Serial Wombat Firmware to latest version")



  Pin6QuadEnc.begin(6,  #1st Pin
  5,  #2nd Pin
  0,  #DebouceTime in mS
  True,  #pull ups
  QE_READ_MODE_t .QE_ONHIGH_POLL  #Mode
  )
  Pin6QuadEnc.writeMinMaxIncrementTargetPin(0, 16);  # Min and max

  conf.begin(1,  #Pin
  20,  #Debounce Ms
  True,  # Invert
  True);  # Pull Up enabled
  back.begin(7,  #Pin
  20,  #Debounce Ms
  True,  # Invert
  True);  # Pull Up enabled

  push.begin(4,  #Pin
  20,  #Debounce Ms
  True,  # Invert
  True);  # Pull Up enabled

  redraw()

boxY = 0  # Value from 0 to 7
lastX = 0
boxOutline = True



def loop():
  if conf.readTransitionsState() ==  False  and  conf.transitions > 0:
    if boxY < 7:
      ++boxY
      redraw()

  if back.readTransitionsState() ==  False  and  back.transitions > 0:
    if boxY > 0:
      --boxY
      redraw()

  if push.readTransitionsState() ==  False  and  push.transitions > 0:
    boxOutline = not boxOutline
    redraw()

  newX = Pin6QuadEnc.readPublicData()

  if newX != lastX:
    lastX = newX
    redraw()



def redraw():
  display.clearDisplay()
  if boxOutline:
    display.drawRect(lastX * 8, boxY * 8, 8, 8, SH110X_WHITE)
  else:
    display.fillRect(lastX * 8, boxY * 8, 8, 8, SH110X_WHITE)
  display.display()


setup()
while True:
    loop()
