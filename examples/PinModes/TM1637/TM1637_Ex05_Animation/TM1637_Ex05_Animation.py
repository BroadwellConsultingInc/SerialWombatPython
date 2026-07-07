# Converted from PinModes/TM1637/TM1637_Ex05_Animation/TM1637_Ex05_Animation.ino
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
import SerialWombatTM1637
tm1637Decimal16 = SerialWombatTM1637.SWTM1637Mode.tm1637Decimal16
tm1637Hex16 = SerialWombatTM1637.SWTM1637Mode.tm1637Hex16
tm1637CharArray = SerialWombatTM1637.SWTM1637Mode.tm1637CharArray
tm1637RawArray = SerialWombatTM1637.SWTM1637Mode.tm1637RawArray
tm1637Animation = SerialWombatTM1637.SWTM1637Mode.tm1637Animation


#
#This example shows how to display an animation on a TM1637 display.  The animation is loaded to the Serial Wombat 18AB chip
#from the Arduino board.  The Serial Wombat chip then outputs the animation to the display without any intervention from
#the Arduino board.
#
#If you haven't already, run the SW_Ard_TM1637_012345 example to ensure your display displays digits in
#the correct order.  If necessary, correct the call to writeDigitOrder below as described in that example.
#4 digit displays should use settings to display 0123 in that test to work properly with this sketch.
#
#You can choose an animation to show by commenting in one of the options below //CONFIG:
#
#A video demonstrating the use of the TM1637 pin mode on the Serial Wombat 18AB chip is available at:
#https://youtu.be/AwW12n6o_T0
#
#Documentation for the SerialWombatTM1637 Arduino class is available at:
#https://broadwellconsultinginc.github.io/SerialWombatArdLib/class_serial_wombat_t_m1637.html#details
#
#Serial Wombat is a registered trademark in the United States of Broadwell Consulting Inc.
#

# sw is provided by the selected interface block above
myDisplay = SerialWombatTM1637.SerialWombatTM1637(sw)
DISPLAY_CLK_PIN = 6  # <<<<<<<<<   Set this to the Serial Wombat pin connected to your Display Clock Pin
DISPLAY_DIN_PIN = 7  # <<<<<<<<<   Set this to the Serial Wombat pin connected to your Display Data Pin


# CONFIG: pick one
##define ANIMATION_ARRAY snake_6_digit
ANIMATION_ARRAY = snake_4_digit
# #define ANIMATION_ARRAY leftToRight



#CONFIG:
##define SPEED 1000  // Slow -  delay 1000mS after updates
SPEED = 100  # Medium - delay 100mS after updates
##define SPEED 10  // Fast -   delay 10ms after updates


SEG_A = 0x1  #TOP
SEG_B = 0x2  # UPPER RIGHT
SEG_C = 0x4  # BOTTOM RIGHT
SEG_D = 0x8  # BOTTOM
SEG_E = 0x10  #BOTTOM LEFT
SEG_F = 0x20  #TOP LEFT
SEG_G = 0x40  # CENTER
SEG_POINT = 0x80
OFF__ = 0



VERTRIGHT = SEG_B | SEG_C
VERTLEFT = SEG_E | SEG_F
TOP = SEG_A
MID = SEG_G
BOT = SEG_D

LeftToRight = [  # All arrays are 6 bytes wide, regardless of display width.
[VERTLEFT, 0,0,0,0,0],
[VERTRIGHT, 0,0,0,0,0],
[0,VERTLEFT, 0,0,0,0],
[0,VERTRIGHT, 0,0,0,0],
[0,0,VERTLEFT, 0,0,0],
[0,0,VERTRIGHT, 0,0,0],
[0,0,0,VERTLEFT, 0,0],
[0,0,0,VERTRIGHT, 0,0],
[0,0,0,0,VERTLEFT, 0],
[0,0,0,0,VERTRIGHT, 0],
[0,0,0,0,0,VERTLEFT ],
[0,0,0,0,0,VERTRIGHT],
[0,0,0,0,0,0],  # putting multiple frames the same in looks like a delay
[0,0,0,0,0,0],
[0,0,0,0,0,0],
[0,0,0,0,0,0],
[0,0,0,0,0,0],
[0,0,0,0,0,0],

]
snake_6_digit = [

[TOP,0,0,0,0,0],
[0,TOP,0,0,0,0],
[0,0,TOP,0,0,0],
[0,0,0,TOP,0,0],
[0,0,0,0,TOP,0],
[0,0,0,0,0,TOP],

[0,0,0,0,0,SEG_B],

[0,0,0,0,0,MID],
[0,0,0,0,MID,0],
[0,0,0,MID,0,0],
[0,0,MID,0,0,0],
[0,MID,0,0,0,0],
[MID,0,0,0,0,0],

[SEG_E,0,0,0,0,0],

[BOT,0,0,0,0,0],
[0,BOT,0,0,0,0],
[0,0,BOT,0,0,0],
[0,0,0,BOT,0,0],
[0,0,0,0,BOT,0],
[0,0,0,0,0,BOT],

[0,0,0,0,0,SEG_C],

[0,0,0,0,0,MID],
[0,0,0,0,MID,0],
[0,0,0,MID,0,0],
[0,0,MID,0,0,0],
[0,MID,0,0,0,0],
[MID,0,0,0,0,0],

[SEG_F,0,0,0,0,0],
]


snake_4_digit = [

[TOP,0,0,0,0,0],
[0,TOP,0,0,0,0],
[0,0,TOP,0,0,0],
[0,0,0,TOP,0,0],

[0,0,0,SEG_B,0,0],

[0,0,0,MID,0,0],
[0,0,MID,0,0,0],
[0,MID,0,0,0,0],
[MID,0,0,0,0,0],

[SEG_E,0,0,0,0,0],

[BOT,0,0,0,0,0],
[0,BOT,0,0,0,0],
[0,0,BOT,0,0,0],
[0,0,0,BOT,0,0],

[0,0,0,SEG_C,0,0],

[0,0,0,MID,0,0],
[0,0,MID,0,0,0],
[0,MID,0,0,0,0],
[MID,0,0,0,0,0],

[SEG_F,0,0,0,0,0],
]

def setup():
  # put your setup code here, to run once:
  # Wire.begin() is handled by the selected Python interface block

  # Serial.begin() is not used in this Python example
  delay(3000)
  print("TM1637 Public Data Display Example")


  sw.begin()  # Python interface was configured above

  #Optional Error handling code begin:
  if sw.isSW04():
    print("This Example is not supported on the Serial Wombat 4B chip.  An 8B or 18AB chip is required.")
    while True:
      delay(100)
  if not sw.isLatestFirmware():
    print("Firmware version mismatch.  Download latest Serial Wombat Arduino Library and update Serial Wombat Firmware to latest version")
  if sw.isSW08()  and  not sw.isPinModeSupported(PIN_MODE_TM1637):
    print("The required pin mode does not appear to be supported in this firmware build.  Do you need to download a different firmware?")
    while True:
      delay(100)
  sw.registerErrorHandler(SerialWombatSerialErrorHandlerBrief);  #Register an error handler that will print communication errors to Serial
  #Optional Error handling code end

  myDisplay.begin(DISPLAY_CLK_PIN,  #Clk Pin
  DISPLAY_DIN_PIN,  # Data Pin
  4,  # Number of digits
  tm1637Animation,  # Mode enumeration
  0,  # source pin Not used in Animation mode
  4);  # Brightness

  #myDisplay.writeDigitOrder(0,1,2,3,4,5);


  myDisplay.writeAnimation(0x0,  # Place array at index 0x180 in the user buffer
  SPEED,
  len(ANIMATION_ARRAY)/6,  #Number of frames.  Suggest using sizeof like this to calculate.
  ANIMATION_ARRAY);  # Array to load.

def loop():
  pass


setup()
while True:
    loop()
