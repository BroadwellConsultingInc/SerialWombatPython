# Converted from Boards/PCB0048_SW8B_Mux/PCB0048_Ex01_I2CFinder/PCB0048_Ex01_I2CFinder.ino
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
import SerialWombatAnalogInput

#This example shows how to use the Serial Wombat PCB0048 Mux board to attach or detacth I2C device
#*   from different bus segements.  It disconnects all segments then does a scan.  Any
#*   devices found (including the MUX board itself) are on the main trunk attached to the host.
#*
#*   The example then enables each segment in order and scans again for devices.
#*
#*   This example shows turning each segment on and off individually.  However,
#*   there are also convenient functions that disable all segments and enable one
#*   with a single call.  See PCB0048_Ex02 for an example.
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
swAnalog = SerialWombatAnalogInput.SerialWombatAnalogInput_18AB(swMux)
MUX_I2C_ADDRESS = 0x60

def setup():
  # put your setup code here, to run once:
  # Wire.begin() is handled by the selected Python interface block
  # Serial.begin() is not used in this Python example

  delay(200)
  swMux.begin(MUX_I2C_ADDRESS)

  swAnalog.begin(6);  # Set up an analog input on pin 6, just to show how to use other pins for Serial Wombat functions.



def scanI2C():

  for i2cAddress in range(0x0E, (0x77) + 1):
    # Scan through all valid addresses
    # Wire.begin() is handled by the selected Python interface block
    error = Wire.endTransmission()


    if error == 0:
      print("I2C Device found at address 0x", end="")
      print(hex(i2cAddress))
def loop():
  # put your main code here, to run repeatedly:

  print("All bus sections disabled:")
  swMux.bus1.writePublicData(0)
  swMux.bus2.writePublicData(0)
  swMux.bus3.writePublicData(0)
  swMux.bus7.writePublicData(0)
  scanI2C()

  print()
  print()
  print("Bus section 1:")
  swMux.bus1.writePublicData(0xFFFF)
  swMux.bus2.writePublicData(0)
  swMux.bus3.writePublicData(0)
  swMux.bus7.writePublicData(0)
  scanI2C()


  print()
  print()
  print("Bus section 2:")
  swMux.bus1.writePublicData(0)
  swMux.bus2.writePublicData(0xFFFF)
  swMux.bus3.writePublicData(0)
  swMux.bus7.writePublicData(0)
  scanI2C()


  print()
  print()
  print("Bus section 3:")
  swMux.bus1.writePublicData(0)
  swMux.bus2.writePublicData(0)
  swMux.bus3.writePublicData(0xFFFF)
  swMux.bus7.writePublicData(0)
  scanI2C()

  print()
  print()
  print("Bus section 7:")
  swMux.bus1.writePublicData(0)
  swMux.bus2.writePublicData(0)
  swMux.bus3.writePublicData(0)
  swMux.bus7.writePublicData(0xFFFF)
  scanI2C()

  print()
  print()
  delay(10000);  # Wait 10 seconds and do it again.


setup()
while True:
    loop()
