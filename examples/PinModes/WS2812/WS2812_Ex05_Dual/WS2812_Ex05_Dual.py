# Converted from PinModes/WS2812/WS2812_Ex05_Dual/WS2812_Ex05_Dual.ino
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
import SerialWombatWS2812
tm1637Decimal16 = SerialWombatTM1637.SWTM1637Mode.tm1637Decimal16
tm1637Hex16 = SerialWombatTM1637.SWTM1637Mode.tm1637Hex16
tm1637CharArray = SerialWombatTM1637.SWTM1637Mode.tm1637CharArray
tm1637RawArray = SerialWombatTM1637.SWTM1637Mode.tm1637RawArray
tm1637Animation = SerialWombatTM1637.SWTM1637Mode.tm1637Animation
ws2812ModeBuffered = SerialWombatWS2812.SWWS2812Mode.ws2812ModeBuffered
ws2812ModeAnimation = SerialWombatWS2812.SWWS2812Mode.ws2812ModeAnimation
ws2812ModeChase = SerialWombatWS2812.SWWS2812Mode.ws2812ModeChase


#
#This example shows how to initialize an animation on a strip/board of WS2812b or equivalent LEDs.  This sketch uses
#the SerialWombat18AB's SerialWombatWS2812 class to configure a pin to drive the LEDs.  The
#selected pin must be an enhanced performance pin.
#
#When executed this sketch will download 3 frames of 3 leds each to the Serial Wombat chip's user buffer area.  It will cycle the frames
#out to the WS2812 LED array and delay between each frame based on a specified per-frame delay.  In this example a Green/Yellow/Red
#traffic light will be simulated, with red and green on for 5 seconds each, and yellow on for 1 second.
#
#Change the WS2812_PIN below to fit your circuit.
#
#A video demonstrating the use of the WS2812b pin mode on the Serial Wombat 18AB chip is available at:
#https://youtu.be/WoXvLBJFpXk
#
#Documentation for the SerialWombatTM1637 Arduino class is available at:
#https://broadwellconsultinginc.github.io/SerialWombatArdLib/class_serial_wombat_w_s2812.html#details
#
#


# sw is provided by the selected interface block above
ws2812 = SerialWombatWS2812.SerialWombatWS2812(sw)
ws2812_2 = SerialWombatWS2812.SerialWombatWS2812(sw)

WS2812_PIN = 15  # Must be an enhanced performance pin: 0,1,2,3,4,7,9,10-19
NUMBER_OF_LEDS = 3
WS2812_USER_BUFFER_INDEX = 0x0000  # Set this to an index into the on-chip user buffer.  Can't overlap with area used by other pins.


# Define colors.  prefix them with SW_ so we don't conflict with any other libraries, such as a graphic display library.
SW_RED = 0x000F0000  # Red, changed from 0x00FF0000 to reduce power
SW_GREEN = 0x0000F00
SW_WHITE = 0x000F0F0F
SW_YELLOW = 0x000F0F00
SW_BLUE = 0x0000000F
SW_OFF = 0x00000000
SW_PURPLE = 0x000F000F

NUMBER_OF_FRAMES = 3

# TODO_MANUAL_CONVERSION: Frames = 
    # TODO_MANUAL_CONVERSION_INDENT: SW_OFF,SW_OFF,SW_GREEN
  # TODO_MANUAL_CONVERSION_INDENT: ,
    # TODO_MANUAL_CONVERSION_INDENT: SW_OFF,SW_YELLOW,SW_OFF
  # TODO_MANUAL_CONVERSION_INDENT: ,
    # TODO_MANUAL_CONVERSION_INDENT: SW_RED,SW_OFF,SW_OFF
  # TODO_MANUAL_CONVERSION_INDENT: ,








def setup():
  # put your setup code here, to run once:
  # Wire.begin() is handled by the selected Python interface block

  # Serial.begin() is not used in this Python example
  delay(3000)
  print("High Speed Clock Example")


  sw.begin()  # Python interface was configured above

  #Optional Error handling code begin:
  if not sw.isSW18():
    print("This Example is not supported on the Serial Wombat 4B or 8B chip.  An  18AB chip is required.")
    while True:
      delay(100)
  if not sw.isLatestFirmware():
    print("Firmware version mismatch.  Download latest Serial Wombat Arduino Library and update Serial Wombat Firmware to latest version")

  sw.registerErrorHandler(SerialWombatSerialErrorHandlerBrief);  #Register an error handler that will print communication errors to Serial
  #Optional Error handling code end


  ws2812.begin(WS2812_PIN,  # The Pin connected to WS2812 array
  NUMBER_OF_LEDS,  # The number of LEDs being used
  WS2812_USER_BUFFER_INDEX);  # A location in the Serial Wombat chip's user RAM area where LED output signals will be buffered

  offset = ws2812.readBufferSize()  # We have a second location in the Serial Wombat chip's user buffer.  This is where
  # The animation frames are stored.  The readBufferSize() method gets the length of
  # buffer used by the configured number of LEDs.

  ws2812.writeAnimationUserBufferIndex(WS2812_USER_BUFFER_INDEX + offset,  # Location in memory to store the animation frames, after the main WS2812 buffer
  NUMBER_OF_FRAMES  # Number of frames
  )

  for i in range(0, NUMBER_OF_FRAMES):
    ws2812.writeAnimationFrame(i,Frames[i]);  # Transfer the frame to the animation buffer on the Serial Wombat chip
    ws2812.writeAnimationFrameDelay(i,5000);  # Initalize All Frames 5000 mS delay

  ws2812.writeAnimationFrameDelay(1,1000);  #Make the yellow frame (index 1 )  only 1000 mS instead of 5000.

  ws2812.writeMode(ws2812ModeAnimation)

  ws2812_2.begin(14,16,2000)
  ws2812_2.writeMode(ws2812ModeChase)


def loop():
  pass
  # No code in here.  The Serial Wombat chip handles generating the LED sequence with no additional
  # help from the Arduino.  In fact, you could unplug the I2C lines and it would continue working until
  # powered down.


setup()
while True:
    loop()
