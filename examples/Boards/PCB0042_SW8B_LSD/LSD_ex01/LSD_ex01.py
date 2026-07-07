# Converted from Boards/PCB0042_SW8B_LSD/LSD_ex01/LSD_ex01.ino
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
import PCB0042_LSD
import SerialWombatAnalogInput
import SerialWombatPWM

#This example shows how to use the Serial Wombat PCB0042 LSD to drive outputs 0 and 2 through 7
#*  And read the voltage feedback on output 1 (assumes the solder jumper is enabled for pin 1)
#*
#*  It cycles through each output setting it to 25, 50, 75, and 100% duty cycle then turning it back off
#
#Video on PCB0042 LSD:
#
#TODO coming soon
#
#SerialWombatPWM_18AB pin mode documentation:
#
#TODO
#SerialWombatAnalogInput_18AB pin mode documentation:
#
#TODO
#


swBoard = PCB0042_LSD.PCB0042_LSD_PWM(sw)

##define PCB0042_I2C_ADDRESS 0x60  // << COMMENT IN THIS LINE AND SET THE ADDRESS FOR YOUR BOARD!

# #ifndef PCB0042_I2C_ADDRESS
# #error "Comment in and set the Address define on line 22.  The default address is 0x60"
# #endif

def setup():
  # put your setup code here, to run once:
  # Wire.begin() is handled by the selected Python interface block

  # Serial.begin() is not used in this Python example
  delay(3000)
  print("PCB0042 PWM output Example. ")



  swBoard.begin(PCB0042_I2C_ADDRESS, True);  #  Initialize board and configure pin 1 to be an analog feedback.

  #Optional Error Checking Code starts here
  if not swBoard.isSW08():
    print("This Example requires a PCB0042 Remcon board")
    while True:
      delay(100)
  if not swBoard.isLatestFirmware():
    print("Firmware version mismatch.  Download latest Serial Wombat Arduino Library and update Serial Wombat Firmware to latest version")
  if not (swBoard.isPinModeSupported(PIN_MODE_PWM)  and   swBoard.isPinModeSupported(PIN_MODE_ANALOGINPUT)):
    print("The required pin mode does not appear to be supported in this firmware build.  Do you need to download a different firmware?")
    while True:
      delay(100)
  swBoard.registerErrorHandler(SerialWombatSerialErrorHandlerBrief);  #Register an error handler that will print communication errors to Serial
  #Optional Error handling code end

  delay(1000)


pin = 0
def loop():
  print("Input voltage is ", end="")
  print(swBoard.readVin_mV())

  swBoard.outputArray[pin].writePublicData(0x4000);  # 25% duty cycle
  delay(500)
  swBoard.outputArray[pin].writePublicData(0x8000);  # 50% duty cycle
  delay(500)
  swBoard.outputArray[pin].writePublicData(0xC000);  # 75% duty cycle
  delay(500)
  swBoard.outputArray[pin].writePublicData(0xFFFF);  # 100% duty cycle
  delay(500)
  swBoard.outputArray[pin].writePublicData(0);  # 0% duty cycle

  ++pin
  if pin == 1:
    ++pin
  # Using pin 1 for Vin analog input
  if pin == 8:
    pin = 0


setup()
while True:
    loop()
