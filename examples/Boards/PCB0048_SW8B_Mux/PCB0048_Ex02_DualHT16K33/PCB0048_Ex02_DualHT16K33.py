# Converted from Boards/PCB0048_SW8B_Mux/PCB0048_Ex02_DualHT16K33/PCB0048_Ex02_DualHT16K33.ino
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
import PCB0048_Mux

#This example shows how to use the Serial Wombat Mux board to control two I2C devices with
#*   the same address by separating them onto separate segments on the I2C bus controlled by mux chips
#*   from a Serial Wombat 8B chip.
#*
#*   This example assumes that four HT16K33 4 character alphanumeric displays are attached to
#*   a MUX board.  all have address 0x70.
#*
#*   The Example intializes one display after turning on MUX segment 2 to show SERI
#*   It then switches to MUX segment 3 and displays AL W on the second display, then
#*   OMBA on segment 1 and T 8B on segment 7.  The result will be "SERIAL WOMBAT 8B" across 4 displays.
#*   This order is designed to make the physical layout of the displays convenient based on the location
#*   of the bus segments on the PCB0048 board.
#*
#*   This example assumes the Adafruit LED Backpack and supporting libraries have been
#*   installed.
#*
#*   Video on the PCB0048 MUX:
#*
#*   TODO coming soon
#*
#*   PCB0048 Mux documentation:
#*
#*   https://serwom.com/p48
#



swMux = PCB0048_Mux.PCB0048_Mux(sw)
MUX_I2C_ADDRESS = 0x60
alpha4_1 = Adafruit_AlphaNum4()
alpha4_2 = Adafruit_AlphaNum4()
alpha4_3 = Adafruit_AlphaNum4()
alpha4_7 = Adafruit_AlphaNum4()

def setup():
  # put your setup code here, to run once:
  # Wire.begin() is handled by the selected Python interface block
  # Serial.begin() is not used in this Python example
  delay(200)
  swMux.begin(MUX_I2C_ADDRESS)



  swMux.enableBus2Only()
  alpha4_2.begin(0x70);  # pass in the address
  alpha4_2.setBrightness(0)
  alpha4_2.writeDigitAscii(0,'S')
  alpha4_2.writeDigitAscii(1,'E')
  alpha4_2.writeDigitAscii(2,'R')
  alpha4_2.writeDigitAscii(3,'I')
  alpha4_2.writeDisplay()

  swMux.enableBus3Only()
  alpha4_3.begin(0x70);  # pass in the address
  alpha4_3.setBrightness(0)
  alpha4_3.writeDigitAscii(0,'A')
  alpha4_3.writeDigitAscii(1,'L')
  alpha4_3.writeDigitAscii(2,' ')
  alpha4_3.writeDigitAscii(3,'W')
  alpha4_3.writeDisplay()

  swMux.enableBus1Only()
  alpha4_1.begin(0x70);  # pass in the address
  alpha4_1.setBrightness(0)
  alpha4_1.writeDigitAscii(0,'O')
  alpha4_1.writeDigitAscii(1,'M')
  alpha4_1.writeDigitAscii(2,'B')
  alpha4_1.writeDigitAscii(3,'A')
  alpha4_1.writeDisplay()

  swMux.enableBus7Only()
  alpha4_7.begin(0x70);  # pass in the address
  alpha4_7.setBrightness(0)
  alpha4_7.writeDigitAscii(0,'T')
  alpha4_7.writeDigitAscii(1,' ')
  alpha4_7.writeDigitAscii(2,'8')
  alpha4_7.writeDigitAscii(3,'B')
  alpha4_7.writeDisplay()

def loop():
  pass


setup()
while True:
    loop()
