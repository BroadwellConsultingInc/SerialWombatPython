# Converted from PinModes/SPI/SPI_ex03_SNx4HC595_ShiftRegister/SPI_ex03_SNx4HC595_ShiftRegister.ino
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
import SerialWombatSPI

#This example shows how to use the Serial Wombat SPI Pin mode to output digital
#*   signals on a SNx4HC595 shift register.
#*
#*   If you're considering this, I'd consider just buying more SW8B boards.  They're
#*   cheap, much more versatile, and likely make your design adaptable for the future.
#*
#*   This will cycle through a variety of output values to show patterns on an LED array
#*
#*   SNxHC595 Pinout:
#+----\/----+
#Qb      1  ---- |1      16| ---- VCC
#Qc      2  ---- |2      15| ---- Qa
#Qd      3  ---- |3      14| ---- SER (DS)  <-- Serial Wombat MOSI Pin
#Qe      4  ---- |4      13| ---- OE        <-- GND (enable outputs)
#Qf      5  ---- |5      12| ---- RCLK      <-- Serial Wombat CS pin
#Qg      6  ---- |6      11| ---- SRCLK     <-- Serial Wombat SPI Clock pin
#Qh      7  ---- |7      10| ---- SRCLR     <-- VCC (no reset)
#GND     8  ---- |8       9| ---- Qh' (cascade out)
#+-----------+ *
#*   This example is compatible with the Serial Wombat 18AB and 8B chips.
#*
#*   The calls to spi transfer on this example are compatible with other spi.transfer
#*   calls using the normal Arduino SPI library.  However, calls to beginTransation()
#*   and end() are unnecessary, and bit order and clock frequency are not configurable.
#*
#*   Video on SPI pin mode:
#*
#*   TODO coming soon
#*
#*   SerialWombatSPI pin mode documentation:
#*
#*   TODO
#


# sw is provided by the selected interface block above
spi = SerialWombatSPI.SerialWombatSPI(sw)

SPI_CLOCK_PIN = 4
SPI_MISO_PIN = 5
SPI_MOSI_PIN = 7
SPI_CS_PIN = 6
def setup():
  # put your setup code here, to run once:
  # Wire.begin() is handled by the selected Python interface block

  # Serial.begin() is not used in this Python example
  delay(3000)
  print("SPI SNx4HC595 Shfit Register Example")


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


# TODO_MANUAL_CONVERSION: outputArray = 
  0xFF,
  0x55,
  0xAA,
  0xF0,
  0x0F,
  0xC3,
  0x3C,
  0x00,


outputIndex = 0
def loop():

  spi.transfer(outputArray[outputIndex])
  ++outputIndex
  if outputIndex >= sizeof(outputArray):
    outputIndex = 0

  delay(300)


setup()
while True:
    loop()
