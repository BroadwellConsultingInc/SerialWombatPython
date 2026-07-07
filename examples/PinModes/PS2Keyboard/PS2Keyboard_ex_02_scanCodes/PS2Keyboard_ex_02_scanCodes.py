# Converted from PinModes/PS2Keyboard/PS2Keyboard_ex_02_scanCodes/PS2Keyboard_ex_02_scanCodes.ino
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
import SerialWombatPS2Keyboard
import SerialWombatTM1637
tm1637Decimal16 = SerialWombatTM1637.SWTM1637Mode.tm1637Decimal16
tm1637Hex16 = SerialWombatTM1637.SWTM1637Mode.tm1637Hex16
tm1637CharArray = SerialWombatTM1637.SWTM1637Mode.tm1637CharArray
tm1637RawArray = SerialWombatTM1637.SWTM1637Mode.tm1637RawArray
tm1637Animation = SerialWombatTM1637.SWTM1637Mode.tm1637Animation
for _name in dir(SerialWombatPS2Keyboard):
    if _name.startswith("SCANCODE_"):
        globals()[_name] = getattr(SerialWombatPS2Keyboard, _name)

#
#This example shows how to configure two pins to work together to connect to an IBM PS2 Keyboard
#and read raw scan codes.
#
#This example assumes a Serial Wombat 18AB chip is attached to the Arduino board via I2C.
#
#
#Keyboard data and clock lines should be pulled up to +5v using a 2k resistor.  5V tollerant pins (9-12, 14, 15) should
#be used.
#
#A video demonstrating the use of the PS2 Keyboard pin mode on the Serial Wombat 18AB chip is available at:
#https://www.youtube.com/watch?v=YV00GfyxFJU
#
#Documentation for the SerialWombatTM1637 Arduino class is available at:
#https://broadwellconsultinginc.github.io/SerialWombatArdLib/class_serial_wombat_p_s2_keyboard.html
#
#

# sw is provided by the selected interface block above
myKeyboard = SerialWombatPS2Keyboard.SerialWombatPS2Keyboard(sw)
PS2_CLK_PIN = 10  # <<<<<<<<<   Set this to the Serial Wombat pin connected to your Keyboard Clock Pin
PS2_DATA_PIN = 11  # <<<<<<<<<   Set this to the Serial Wombat pin connected to your Keyboard Data Pin

def setup():
  # put your setup code here, to run once:
  # Wire.begin() is handled by the selected Python interface block

  # Serial.begin() is not used in this Python example
  delay(3000)
  print("PS2 Keyboard Queueing Example")


  sw.begin()  # Python interface was configured above

  #Optional Error handling code begin:
  if sw.isSW04():
    print("This Example is not supported on the Serial Wombat 4B chip.  An 8B or 18AB chip is required.")
    while True:
      delay(100)
  if not sw.isLatestFirmware():
    print("Firmware version mismatch.  Download latest Serial Wombat Arduino Library and update Serial Wombat Firmware to latest version")
  if sw.isSW08()  and  not sw.isPinModeSupported(PIN_MODE_PS2KEYBOARD):
    print("The required pin mode does not appear to be supported in this firmware build.  Do you need to download a different firmware?")
    while True:
      delay(100)
  sw.registerErrorHandler(SerialWombatSerialErrorHandlerBrief);  #Register an error handler that will print communication errors to Serial
  #Optional Error handling code end

  print("Serial Wombat 18AB PS2 Keyboard Example.")
  print("Connect Clock line to pin ", end="")
  print(PS2_CLK_PIN)
  print(" and data pin to pin ", end="")
  print(PS2_DATA_PIN)


  myKeyboard.begin(PS2_CLK_PIN,  #Clk Pin
  PS2_DATA_PIN,  # Data Pin
  2);  # All scan codes


count = 0  # How many on the line?

lastCodeTimestamp = 0
def loop():

  x = 0
  x = myKeyboard.read();  # Read the keyboard queue.  Returns -1 if no characters available
  while x > 0:


    if count > 25 or millis() > lastCodeTimestamp + 1000:
      # start a new line if we've printed 25 codes or if it's been more than 1 second since the last code.
      print()
      count = 0

    Serial.print(x, HEX);  # Send the code to the serial interface
    print(' ', end="")
    ++ count
    lastCodeTimestamp = millis()

    x = myKeyboard.read();  # Read the keyboard queue.  Returns -1 if no characters available


setup()
while True:
    loop()
