# Converted from PinModes/IRRx/IRRx_ex04_multipleRemotes/IRRx_ex04_multipleRemotes.ino
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

#This example shows how to use the Serial Wombat IR Receive (IRRx) pin mode.  It assumes two  NEC compatible IR Transmitters with different addresses
#*   (most inexpensive Arduino kit remotes are compatible) and a 38kHz receiver module that goes low when a modulated IR signal is
#*   present.
#*
#*   This example is compatible with the Serial Wombat 18AB and 8B chips.
#*
#*   This example shows how to simultaneously monitor for two different IR Transmitters (with different addresses)
#*
#*   In order to achieve this, a single IR receiver module is routed to multiple Serial Wombat pins, each of which
#*   is configured to SerialWombatIRRx pin mode.  Each pin mode is configured to filter to a different address.
#*
#*   In this example commands are received from the pin mode and printed to Serial, along with either A or B depending on
#*   which remote sent the command.
#*   Note that if both transmitters transmit at the same time their signals may interfere with each other.
#*
#*   Example 2 can help find the address of a given transmitter.
#*
#*
#*   NEC compatible transmitters may either use and 8 bit address and then send the complement of the
#*   address in the alternative byte, or may use all 16 bits for one address.  The Serial Wombat IRRx pin mode
#*   treats both of these cases as a single 16 bit address.
#*
#*   Video on IRRx pin mode:
#*
#*   TODO coming soon
#*
#*   SerialWombatIRRx pin mode documentation:
#*
#*   TODO
#


# sw is provided by the selected interface block above
irrx1 = SerialWombatIRRx.SerialWombatIRRx(sw)
irrx2 = SerialWombatIRRx.SerialWombatIRRx(sw)

IRRX_FIRST_REMOTE_PIN = 7
IRRX_SECOND_REMOTE_PIN = 8
def setup():
  # put your setup code here, to run once:
  # Wire.begin() is handled by the selected Python interface block

  # Serial.begin() is not used in this Python example
  delay(3000)
  print("IR Multiple Remote Example")


  sw.begin()  # Python interface was configured above

  #Optional Error handling code begin:
  if sw.isSW04():
    print("This Example is not supported on the Serial Wombat 4B chip.  An 8B or 18AB chip is required.")
    while True:
      delay(100)
  if not sw.isLatestFirmware():
    print("Firmware version mismatch.  Download latest Serial Wombat Arduino Library and update Serial Wombat Firmware to latest version")
  if sw.isSW08()  and  not (sw.isPinModeSupported(PIN_MODE_IRRX) ):
    print("The required pin mode does not appear to be supported in this firmware build.  Do you need to download a different firmware?")
    while True:
      delay(100)
  sw.registerErrorHandler(SerialWombatSerialErrorHandlerBrief);  #Register an error handler that will print communication errors to Serial
  #Optional Error handling code end
  irrx1.begin(IRRX_FIRST_REMOTE_PIN,
  DATACOUNT,  # Make data count the output
  0,  #Mode 0 : NEC
  True,  # Use repeat
  SW_LOW,  # Active Low
  1000,  # 1000 ms Public Data Timeout
  0xFFFF,  # Default public data
  True,  # Use Address Filtering
  0xEF00);  # Filter to address 0xEF00  (This value was determined for a given remote using example 2
  #irrx1.enablePullup(true);   //Comment in this line if your receiver is open drain type without pullup .  Only one pin needs its pull up enabled
  irrx2.begin(IRRX_SECOND_REMOTE_PIN,
  DATACOUNT,  # Make data count the output
  0,  #Mode 0 : NEC
  True,  # Use repeat
  SW_LOW,  # Active Low
  1000,  # 1000 ms Public Data Timeout
  0xFFFF,  # Default public data
  True,  # Use Address Filtering
  0xFF00);  # Filter to address 0xFF00  (This value was determined for a given remote using example 2


def loop():
  receivedData = irrx1.read()

  if receivedData >=0:
    s = [0] * (10)
    print("A: ", end="")
    print(receivedData)

  receivedData = irrx2.read()

  if receivedData >=0:
    s = [0] * (10)
    print("B: ", end="")
    print(receivedData)


setup()
while True:
    loop()
