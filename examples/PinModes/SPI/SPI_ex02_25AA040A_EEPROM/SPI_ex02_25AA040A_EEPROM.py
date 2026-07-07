# Converted from PinModes/SPI/SPI_ex02_25AA040A_EEPROM/SPI_ex02_25AA040A_EEPROM.ino
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
import SerialWombatIRRx
import SerialWombatSPI

#This example shows how to use the Serial Wombat SPI Pin mode to read And write data from a Microchip 25AA040A
#*   512 byte EEPROM.
#*
#*   This example is compatible with the Serial Wombat 18AB and 8B chips.
#*
#*
#*   Video on SPI pin mode:
#*
#*   TODO coming soon
#*
#*   SerialWombatIRRx pin mode documentation:
#*
#*   TODO
#


# sw is provided by the selected interface block above
spi = SerialWombatSPI.SerialWombatSPI(sw)

SPI_CLOCK_PIN = 4
SPI_MISO_PIN = 5
SPI_MOSI_PIN = 7
SPI_CS_PIN = 3
def setup():
  # put your setup code here, to run once:
  # Wire.begin() is handled by the selected Python interface block

  # Serial.begin() is not used in this Python example
  delay(3000)
  print("SPI 25AA040A EEPROM Example")


  sw.begin()  # Python interface was configured above

  #Optional Error handling code begin:
  if sw.isSW04():
    print("This Example is not supported on the Serial Wombat 4B chip.  An 8B or 18AB chip is required.")
    while True:
      delay(100)
  if not sw.isLatestFirmware():
    print("Firmware version mismatch.  Download latest Serial Wombat Arduino Library and update Serial Wombat Firmware to latest version")
  if sw.isSW08()  and  not (sw.isPinModeSupported(PIN_MODE_SPI) ):
    print("The required pin mode does not appear to be supported in this firmware build.  Do you need to download a different firmware?")
    while True:
      delay(100)
  sw.registerErrorHandler(SerialWombatSerialErrorHandlerBrief);  #Register an error handler that will print communication errors to Serial
  #Optional Error handling code end
  spi.begin(
  SPI_CLOCK_PIN,
  0,  #Mode 0
  SPI_MOSI_PIN,
  SPI_MISO_PIN,
  SPI_CS_PIN)
  spi.transfer(0x06);  # Enable Writes on EEPROM.  Be sure to cast single byte constants so compiler interprets them that way.

    # TODO_MANUAL_CONVERSION_INDENT: buf = [0x02, 0x10, 0x30, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38,0x39, 0x61, 0x62,0x63,0x64,0x65,0x66];  # Write "0123456789ABCDEF" to addres 0x010
    # TODO_MANUAL_CONVERSION_INDENT: spi.transfer(buf,18);  #Transfer 18 bytes
  delay(2000);  # Allow time for write to complete

  spi.transfer(0x06);  # Enable Writes on EEPROM.  Be sure to cast single byte constants so compiler interprets them that way.

    # TODO_MANUAL_CONVERSION_INDENT: buf = [0x02, 0xFF, 0xD7];  # Write 0x D7 to addres 0x1FF
    # TODO_MANUAL_CONVERSION_INDENT: spi.transfer(buf,3);  #Transfer 3 bytes
  delay(10);  # Allow time for write to complete
  spi.transfer(0x06);  # Enable Writes on EEPROM.  Be sure to cast single byte constants so compiler interprets them that way.

    # TODO_MANUAL_CONVERSION_INDENT: buf = [0x02, 0x00, 0x67];  # Write 0x67 to addres 0x000
    # TODO_MANUAL_CONVERSION_INDENT: spi.transfer(buf,3);  #Transfer 3 bytes


readBuf = [0] * (514)
def loop():

  readBuf[0] = 0x03;  #Read command
  readBuf[1] = 0x00;  # Start at address 0x00
  spi.transferBuffer(readBuf, readBuf, 514)

  for row in range(0, 32):
    r = [0] * (10)
    r = ("%03X: ") % (row * 16)
    print(r, end="")
    for column in range(0, 16):
      s = [0] * (10)
      s = ("%02X ") % (readBuf[row * 16 + column + 2])
      print(s, end="")
    print()
  print()
  print()
  print()
  delay(5000)


setup()
while True:
    loop()
