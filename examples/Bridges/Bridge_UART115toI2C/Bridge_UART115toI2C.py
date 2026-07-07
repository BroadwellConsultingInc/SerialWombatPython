# Converted from Bridges/Bridge_UART115toI2C/Bridge_UART115toI2C.ino
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


#
#This sketch is designed to allow UART communication with an I2C based Serial Wombat chip.
#
#It accepts 9 bytes as a packet, and returns 8.   The first byte is an I2C address (or 0xFF for the first detected Serial Wombat chip on the bus).
#
#It discards any 0x55, ' ' or 'x' initial bytes, then waits until 8 bytes are received,
#sends that as an I2C packet, and then sends the response back to the UART.
#

SWC = SerialWombat.SerialWombatChip()
i2cAddress = 0
# TODO_MANUAL_CONVERSION: uint8_t tx[9], rx[8], count

def setup():

  # #ifdef ARDUINO_ESP8266_GENERIC
  # Wire.begin() is handled by the selected Python interface block
  # #else
  # Wire.begin() is handled by the selected Python interface block
  # #endif
  Wire.setTimeout(1000)
  # Serial.begin() is not used in this Python example

  delay(100)
  Serial.flush()
  count = 0

lastReceive = 0
RECEIVETIMEOUT = 2000
def loop():


  x = Serial.read()

  while x >= 0:
    lastReceive = millis()
    if count > 0:
      tx[count] = x
      ++count
      if count >= 9:
        # Wire.begin() is handled by the selected Python interface block
        Wire.write(tx[1], 8)
        Wire.endTransmission()
        delayMicroseconds(100)
        Wire.requestFrom(tx[0], 8)
        count = 0
        r = 0
        while r >= 0  and  count < 8:
          r = Wire.read()

          if r >= 0:
            rx[count] =  r
            ++count
          else:
            break
        count = 0
        Serial.write(rx, 8)
    else:
      if x != 0x55  and  x != 'x'  and  x != ' ':
        tx[count] = x
        ++count
    x = Serial.read()
  if millis() > lastReceive + RECEIVETIMEOUT:
    count = 0


setup()
while True:
    loop()
