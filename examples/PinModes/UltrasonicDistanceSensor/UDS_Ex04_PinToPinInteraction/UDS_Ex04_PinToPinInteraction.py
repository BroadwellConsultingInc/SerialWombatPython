# Converted from PinModes/UltrasonicDistanceSensor/UDS_Ex04_PinToPinInteraction/UDS_Ex04_PinToPinInteraction.ino
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
import SerialWombatAbstractProcessedInput
import SerialWombatUltrasonicDistanceSensor
import SerialWombatWS2812
ws2812ModeBuffered = SerialWombatWS2812.SWWS2812Mode.ws2812ModeBuffered
ws2812ModeAnimation = SerialWombatWS2812.SWWS2812Mode.ws2812ModeAnimation
ws2812ModeChase = SerialWombatWS2812.SWWS2812Mode.ws2812ModeChase

#
#This example shows how to set up a pin-to-pin interaction within the Serial Wombat Chip using
#the Ultrasonic Distance Sensor and a strip of WS2812 LEDs. This example builds on example 2
#by adding the WS2812 strip.
#
#The LEDs will light depending on the distance measurement from the sensor.
#
#This sketch was last tested with version 2.2.2 of the firmware.
#
#An HC_SR04 sensor needs to be powered by 5V, and outputs a 5V signal.  The echo pin should be connected to one of the
#Serial Wombat 18AB chip's 5V tolerant pins (9,10,11,12, 14 and 15)
#
#A video demonstrating the use of the UltrasonicDistanceSensor pin mode on the Serial Wombat 18AB chip is available at:
#https://youtu.be/Mv7zrP8mtjo
#
#Documentation for the SerialWombatUltrasonicDistanceSensor class is available at:
#https://broadwellconsultinginc.github.io/SerialWombatArdLib/class_serial_wombat_ultrasonic_distance_sensor.html
#
#For reference, the source code to the firmware (looking at this isn't required, but is interesting) is available here:
#https://github.com/BroadwellConsultingInc/SerialWombat/blob/main/SerialWombatPinModes/ultrasonicDistance.c
#
#

# sw is provided by the selected interface block above
distanceSensor = SerialWombatUltrasonicDistanceSensor.SerialWombatUltrasonicDistanceSensor(sw)
lightStrip = SerialWombatWS2812.SerialWombatWS2812(sw)

WS2812_PIN = 19  # Must be an enhanced performance pin: 0,1,2,3,4,7,9,10-19
NUMBER_OF_LEDS = 20
WS2812_USER_BUFFER_INDEX = 0x0000  # Set this to an index into the on-chip user buffer.  Can't overlap with area used by other pins.



def setup():
  # put your setup code here, to run once:
  # Wire.begin() is handled by the selected Python interface block

  # Serial.begin() is not used in this Python example
  delay(3000)
  print("Ultrasonic Distance Sensor Pin to Pin Example ")


  sw.begin()  # Python interface was configured above

  #Optional Error handling code begin:
  if not sw.isSW18():
    print("This Example is not supported on the Serial Wombat 4B or 8B chip.  An 18AB chip is required.")
    while True:
      delay(100)
  if not sw.isLatestFirmware():
    print("Firmware version mismatch.  Download latest Serial Wombat Arduino Library and update Serial Wombat Firmware to latest version")
  if sw.isSW08()  and  not sw.isPinModeSupported(PIN_MODE_ULTRASONIC_DISTANCE):
    print("The required pin mode does not appear to be supported in this firmware build.  Do you need to download a different firmware?")
    while True:
      delay(100)
  sw.registerErrorHandler(SerialWombatSerialErrorHandlerBrief);  #Register an error handler that will print communication errors to Serial
  #Optional Error handling code end
  distanceSensor.begin(10,  # Echo pin is on pin 10
  HC_SR04,  # HC_SR04 driver
  11);  # Trigger pin on pin 11.    no parameters for autoTrigger (True) and pullUp (False)

  distanceSensor.writeAveragingNumberOfSamples(100);  #Inherited from SerialWombatAbstractProcessedInput

  lightStrip.begin(WS2812_PIN,
  NUMBER_OF_LEDS,
  WS2812_USER_BUFFER_INDEX)

  lightStrip.barGraph(10,  # Get the bar graph data from pin 10, the Ultrasonic Sensor
  0x00050000,  # Off value = dim red
  0x00000020,  # on value = blue
  0,  # Min value 0
  300);  # Max value 300mm


lastMeasurement = 0

# In the loop we will constantly read the average value, and print it to Serial When it changes
# Note that the loop does nothing to update the WS2812 strip.  This happens completely on the
# Serial Wombat Chip.

def loop():
  newMeasurement = distanceSensor.readAverage()
  if newMeasurement != lastMeasurement:
    print(newMeasurement, end="")
    print(" mm")
    lastMeasurement = newMeasurement


setup()
while True:
    loop()
