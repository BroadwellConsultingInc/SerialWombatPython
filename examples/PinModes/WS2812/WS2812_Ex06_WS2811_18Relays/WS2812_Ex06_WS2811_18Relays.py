# Converted from PinModes/WS2812/WS2812_Ex06_WS2811_18Relays/WS2812_Ex06_WS2811_18Relays.ino
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
#This example shows how to control 18 relays using WS2811 breakout boards.  This example assumes that the first relay is
#attached to R, the 2nd to G, the 3rd to B, and so on for 6 LEDs.  The swapRG member of ws2812 is set to true since
#the R and G data positions on the WS2811 silicon are swapped compared to the WS2812 silicon.
#
#The WS2811 does not drive the Relays directly (WS2811s aren't designed for inductive loads), but rather through
#a relay driver on the relay boards.  Note that the WS2811 is designed to switch the low side of an LED, so it's an open drain
#style output (active low on, high-impedance off) so the relay board needs to be low-input active.
#
#Try to keep the power lines running the relays away from the signal line for the WS2811's, as the noise created by the
#relays' coils may induce glitches if the wires are near the signal line, and this can cause the WS2811's to output unexpected
#data.
#
#Relays are binary devices, so we set each LED driver "color" to either 0  (inactive) or 0xFF (active).
#
#
#
#Change the WS2812_PIN below to fit your circuit.
#
#A video demonstrating the use of the WS2812b pin mode on the Serial Wombat 18AB chip is available at:
#//TODO
#
#Documentation for the SerialWombatTM1637 Arduino class is available at:
#https://broadwellconsultinginc.github.io/SerialWombatArdLib/class_serial_wombat_w_s2812.html#details
#
#


# sw is provided by the selected interface block above
ws2812 = SerialWombatWS2812.SerialWombatWS2812(sw)

WS2812_PIN = 19  # Must be an enhanced performance pin: 0,1,2,3,4,7,9,10-19
NUMBER_OF_LEDS = 6
WS2812_USER_BUFFER_INDEX = 0x0000  # Set this to an index into the on-chip user buffer.  Can't overlap with area used by other pins.

ledArray = [0,0,0,0,0,0]

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
  ws2812.swapRG = True;  #WS2811 swaps R and G vs WS2812



def loop():
  for x in range(0, 6):
    # Cycle through 6 LEDs (3 relays for each LED)
    for i in range(0, 6):
      ledArray[i] = 0;  # Set the color array to all off

    ledArray[x] = 0xFF0000;  # Red
    ws2812.write(0,6,ledArray)
    delay(1000)

    ledArray[x] = 0xFF00;  # Green
    ws2812.write(0,6,ledArray)
    delay(1000)

    ledArray[x] = 0xFF;  # Blue
    ws2812.write(0,6,ledArray)
    delay(1000)

  for i in range(0, 6):
    ledArray[i] = 0
  ws2812.write(0,6,ledArray)
  delay(1000)

  #All LEDs on
  for i in range(0, 6):
    ledArray[i] = 0xFFFFFF
  ws2812.write(0,6,ledArray)
  delay(1000)

  #All LEDs off
  for i in range(0, 6):
    ledArray[i] = 0
  ws2812.write(0,6,ledArray)
  delay(1000)


setup()
while True:
    loop()
