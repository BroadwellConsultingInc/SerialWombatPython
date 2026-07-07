# Converted from PinModes/PulseTimer/PulseTimer_Ex02_multipleSW4B/PulseTimer_Ex02.ino
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
import SerialWombatPulseTimer


sw6C = SerialWombat.SerialWombatChip()  #Declare a Serial Wombat chip
steering = SerialWombatPulseTimer.SerialWombatPulseTimer(sw6C)
throttle = SerialWombatPulseTimer.SerialWombatPulseTimer(sw6C)
button = SerialWombatPulseTimer.SerialWombatPulseTimer(sw6C)
thumbSwitch = SerialWombatPulseTimer.SerialWombatPulseTimer(sw6C)

sw6D = SerialWombat.SerialWombatChip()  # Declare a second Serial Wombat
leftKnob = SerialWombatPulseTimer.SerialWombatPulseTimer(sw6D)
rightKnob = SerialWombatPulseTimer.SerialWombatPulseTimer(sw6D)

# This example is explained in a video tutorial at: https://youtu.be/YtQWUub9gYw

def setup():
  # put your setup code here, to run once:

  # Wire.begin() is handled by the selected Python interface block
  sw6C.begin()  # Python interface was configured above
  sw6D.begin()  # Python interface was configured above


  #Optional Error handling code begin:

  if not sw6C.isLatestFirmware()  or  not sw6D.isLatestFirmware():
    print("Firmware version mismatch.  Download latest Serial Wombat Arduino Library and update Serial Wombat Firmware to latest version")

  sw6C.registerErrorHandler(SerialWombatSerialErrorHandlerBrief);  #Register an error handler that will print communication errors to Serial
  sw6D.registerErrorHandler(SerialWombatSerialErrorHandlerBrief);  #Register an error handler that will print communication errors to Serial
  #Optional Error handling code end

  steering.begin(0);  # On sw6C
  throttle.begin(1)
  button.begin(2)
  thumbSwitch.begin(3)

  leftKnob.begin(0);  # On sw6D
  rightKnob.begin(1)

  # Serial.begin() is not used in this Python example

def clearTerminal():
  Serial.write(27);  # ESC command
  Serial.print("[2J");  # clear screen command
  Serial.write(27)
  Serial.println("[H");  # cursor to home command


def loop():
  clearTerminal()
  print(steering.readHighCounts())
  print(throttle.readHighCounts())
  print(button.readHighCounts())
  print(thumbSwitch.readHighCounts())
  print(leftKnob.readHighCounts())
  print(rightKnob.readHighCounts())

  delay(50)


setup()
while True:
    loop()
