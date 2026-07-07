# Converted from YouTube/Elegoo37SensorKit/MatrixKeypad/MatrixKeypad.ino
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
import SerialWombatTM1637
tm1637Decimal16 = SerialWombatTM1637.SWTM1637Mode.tm1637Decimal16
tm1637Hex16 = SerialWombatTM1637.SWTM1637Mode.tm1637Hex16
tm1637CharArray = SerialWombatTM1637.SWTM1637Mode.tm1637CharArray
tm1637RawArray = SerialWombatTM1637.SWTM1637Mode.tm1637RawArray
tm1637Animation = SerialWombatTM1637.SWTM1637Mode.tm1637Animation


#
#This example shows how to initialize a 16 key, 8 pin 4x4 matrix keypad using the
#Serial Wombat 18AB chip'sSerialWombatMatrixKeypad class.
#
#This example shows how to treat the matrix keypad as a stream input
#so that it can be treated as if keypresses are Serial Input
#
#Note that firmware versions prior to 2.0.7 have a bug that may cause slow recognition of
#button presses.
#
#This example assumes a 4x4 keypad attached with rows connected to pins 10,11,12,13
#and columns attached to pins 16,17,18,19 .  This can be changed in the keypad.begin
#statement to fit your circuit.
#
#This example uses default modes for the SerialWombatMatrixKeypad.  The default values
#send ASCII to the queue assuming a standard
#
#123A
#456B
#789C
#*0#D
#
#keypad format.   See the pin mode documentation (link below) for more information on the
#possible buffer and queue modes It is assumed that the Serial Wombat chip is at I2C
#address 0x6B.
#
#
#A video demonstrating the use of the SerialWombatMatrixKeypad class on the Serial Wombat 18AB chip is available at:
#https://youtu.be/hxLda6lBWNg
#
#Documentation for the SerialWombatTM1637 Arduino class is available at:
#https://broadwellconsultinginc.github.io/SerialWombatArdLib/class_serial_wombat_w_s2812.html#details
#
#
# sw is provided by the selected interface block above
keypad = SerialWombatMatrixKeypadold.SerialWombatMatrixKeypad(sw)

def setup():

  # Serial.begin() is not used in this Python example
  # Wire.begin() is handled by the selected Python interface block
  delay(100)
  sw.begin()  # Python interface was configured above

  keypad.begin(19,  # Command pin, typically the same as the row0 pin
  19,  #row 0
  18,  # row 1
  17,  # row 2
  16,  # row 3
  15,  # column 0
  14,  # column 1
  13,  # column 2
  12);  # column 3

def loop():

  i = keypad.read()  # returns a byte, or -1 if no value is avaialble
  if i >0:
    Serial.write(i);  # We got a keypress.  Dump it to the Serial Terminal


setup()
while True:
    loop()
