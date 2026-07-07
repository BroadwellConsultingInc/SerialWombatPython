# Converted from PinModes/UART/HardwareUART/HW_UART_EX02_LoopbackTest/HW_UART_EX02_LoopbackTest.ino
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
import SerialWombatUART


# sw is provided by the selected interface block above
SWUart = SerialWombatUART.SerialWombatUART(sw)  # Declare a Serial Wombat UART  Only one UART can be assigned on the SerialWombat 4B.   On SW8B the rx and tx pins must be 6 and 7

# There is a video tutorial to go with this example at:  https://youtu.be/C1FjcaiBYZs
def setup():
  # put your setup code here, to run once:
  # Wire.begin() is handled by the selected Python interface block

  # Serial.begin() is not used in this Python example
  delay(3000)
  print("1Hz Blink Example")


  sw.begin()  # Python interface was configured above

  #Optional Error handling code begin:

  if not sw.isLatestFirmware():
    print("Firmware version mismatch.  Download latest Serial Wombat Arduino Library and update Serial Wombat Firmware to latest version")
  if sw.isSW08()  and  not sw.isPinModeSupported(PIN_MODE_UART_RX_TX):
    print("The required pin mode does not appear to be supported in this firmware build.  Do you need to download a different firmware?")
    while True:
      delay(100)
  sw.registerErrorHandler(SerialWombatSerialErrorHandlerBrief);  #Register an error handler that will print communication errors to Serial
  #Optional Error handling code end

  print("Start SWUart...")
  SWUart.begin(57600, 1, 0, 1)
  print("Initialization Complete...")

#32,7,5,3,2,1
MASK = 0x80000057
def random(seed):

  output = 0
  for util_local_i in range(0, 16):
    # TODO_MANUAL_CONVERSION: if *seed  0x00000001:
      # TODO_MANUAL_CONVERSION: *seed = (((*seed ^ MASK) >> 1) | 0x80000000)
    # TODO_MANUAL_CONVERSION: else:
      # TODO_MANUAL_CONVERSION: *seed >>= 1
    output <<= 1
    # TODO_MANUAL_CONVERSION: output |= *seed  0x01
  return (output)

random1 = 6
random2 = 6
iteration = 0
fails = 0
passes = 0
BUFFER_SIZE = 128

tx = [0] * (BUFFER_SIZE)
rx = [0] * (BUFFER_SIZE)

def loop():
  # put your main code here, to run repeatedly:


  while SWUart.read() != -1:
    Serial.println("Flush");  # Flush rx


  # Fill the TX buffer with random data
  txcount = random(random1) % BUFFER_SIZE
  for x in range(0, txcount):
    tx[x] = random(random1)

  SWUart.write(tx, txcount)



  # read the bytes back in and compare them against the random # generator
  rxcount = random(random2) % BUFFER_SIZE
  # TODO_MANUAL_CONVERSION: c = SWUart.readBytes((char*)rx, rxcount)
  mismatch = False
  for x in range(0, rxcount):
    b = 0
    b = random(random2)
    if b != rx[x]:
      mismatch = True
      ++fails
      Serial.write("Mismatch: ")
      print(iteration, end="")
      Serial.write(' ')
      print(x, end="")
      Serial.write(' ')
      print(b, end="")
      Serial.write(' ')
      print(rx[x])

  if not mismatch:
    ++passes
    Serial.write("P  ")
    print(passes, end="")
    Serial.write(" F ")
    print(fails)
  ++iteration


setup()
while True:
    loop()
