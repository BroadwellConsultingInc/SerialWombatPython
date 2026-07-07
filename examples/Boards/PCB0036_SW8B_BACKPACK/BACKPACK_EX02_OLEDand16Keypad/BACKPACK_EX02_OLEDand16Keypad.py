# Converted from Boards/PCB0036_SW8B_BACKPACK/BACKPACK_EX02_OLEDand16Keypad/BACKPACK_EX02_OLEDand16Keypad.ino
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
import SerialWombatMatrixKeypadold


SCREEN_WIDTH = 128  # OLED display width, in pixels
SCREEN_HEIGHT = 64  # OLED display height, in pixels

display = Adafruit_SH1106G(SCREEN_WIDTH, SCREEN_HEIGHT, Wire, -1)

# sw is provided by the selected interface block above


Pin0Keypad = SerialWombatMatrixKeypadold.SerialWombatMatrixKeypad(sw)  # Your serial wombat chip may be named something else than sw

def setup():
  #Wire.begin();
  # Serial.begin() is not used in this Python example

  delay(500)
  print("Starting Display")
  delay(500)
  display.begin(0x3C, False)

  display.clearDisplay()
  display.setTextSize(3);  # Normal 1:1 pixel scale
  display.setTextColor(SH110X_WHITE);  # Draw white text
  display.setCursor(0, 0);  # Start at top-left corner
  display.write("READY")
  display.display()




  sw.begin()  # Python interface was configured above
  sw.registerErrorHandler(SerialWombatSerialErrorHandlerBrief);  #Register an error handler that will print communication errors to Serial
  if not sw.isLatestFirmware():
    print("Firmware version mismatch.  Download latest Serial Wombat Arduino Library and update Serial Wombat Firmware to latest version")




  Pin0Keypad.begin(0,  #Control pin
  4,  #Row 0 pin
  5,  # Row 1 pin
  6,  # Row 2 pin
  7,  # Row 3 pin
  0,  # Col 0 pin
  1,  # Col 1 pin
  2,  # Col 2 pin
  3,  # Col 3 pin
  1,  #Public data mode
  1,  #Queue Mode
  5);  # Row Delay in mS

  Pin0Keypad.writeAsciiTable(0, '1')
  Pin0Keypad.writeAsciiTable(1, '2')
  Pin0Keypad.writeAsciiTable(2, '3')
  Pin0Keypad.writeAsciiTable(3, 'A')
  Pin0Keypad.writeAsciiTable(4, '4')
  Pin0Keypad.writeAsciiTable(5, '5')
  Pin0Keypad.writeAsciiTable(6, '6')
  Pin0Keypad.writeAsciiTable(7, 'B')
  Pin0Keypad.writeAsciiTable(8, '7')
  Pin0Keypad.writeAsciiTable(9, '8')
  Pin0Keypad.writeAsciiTable(10, '9')
  Pin0Keypad.writeAsciiTable(11, 'C')
  Pin0Keypad.writeAsciiTable(12, '*')
  Pin0Keypad.writeAsciiTable(13, '0')
  Pin0Keypad.writeAsciiTable(14, '#')
  Pin0Keypad.writeAsciiTable(15, 'D')


def loop():

  x = Pin0Keypad.read()
  if x >=0:
    print(x, end="")
    display.clearDisplay()
    display.setTextSize(7);  # Normal 1:1 pixel scale
    display.setTextColor(SH110X_WHITE);  # Draw white text
    display.setCursor(40, 10);  # Start at top-left corner
    display.write(x)
    display.display()


setup()
while True:
    loop()
