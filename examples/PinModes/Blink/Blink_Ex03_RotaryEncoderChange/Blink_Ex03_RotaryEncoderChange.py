# Converted from PinModes/Blink/Blink_Ex03_RotaryEncoderChange/Blink_Ex03_RotaryEncoderChange.ino
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
import SerialWombatBlink
import SerialWombatQuadEnc

#
#This example shows how to configure a Serial Wombat 8B or 18AB chip to blink an LED any
#time the count on a rotary encoder changes
#
#This sketch was last tested with version 2.2.2 of the firmware.
#
#
#A video demonstrating the Blink pin mode is available here:
#TODO
#
#Documentation for the SerialWombatBlink class is available at:
#https://broadwellconsultinginc.github.io/SerialWombatArdLib/class_serial_wombat_blink.html
#
#For reference, the source code to the firmware (looking at this isn't required, but is interesting) is available here:
#https://github.com/BroadwellConsultingInc/SerialWombat/blob/main/SerialWombatPinModes/blink.c
#
#


# sw is provided by the selected interface block above
blinkPin = SerialWombatBlink.SerialWombatBlink(sw)
rotaryEncoder = SerialWombatQuadEnc.SerialWombatQuadEnc_18AB(sw)


BLINK_PIN = 1  # SW8B PCB0029 On Board LED is on pin 1 (must close solder jumper)

ROTARY_ENC_PIN_A = 5
ROTARY_ENC_PIN_B = 7

def setup():
  # put your setup code here, to run once:
  # Wire.begin() is handled by the selected Python interface block
  # Serial.begin() is not used in this Python example
  delay(3000)
  print("Rotary Encoder example.  Connect encoder to pins 5 and 6")


  sw.begin()  # Python interface was configured above

  #Optional Error handling code begin:
  if sw.isSW04():
    print("This Example is not supported on the Serial Wombat 4B chip.  An 8B or 18AB chip is required.")
    while True:
      delay(100)
  if not sw.isLatestFirmware():
    print("Firmware version mismatch.  Download latest Serial Wombat Arduino Library and update Serial Wombat Firmware to latest version")
  if not sw.isPinModeSupported(PIN_MODE_BLINK):
    print("The required pin mode does not appear to be supported in this firmware build.  Do you need to download a different firmware?")
    while True:
      delay(100)
  sw.registerErrorHandler(SerialWombatSerialErrorHandlerBrief);  #Register an error handler that will print communication errors to Serial
  #Optional Error handling code end

  rotaryEncoder.begin(ROTARY_ENC_PIN_A, ROTARY_ENC_PIN_B);  #depending on your rotary encoder, additional settings such as debounce time or read method may be required.  See rotary encoder documentation

  blinkPin.begin(BLINK_PIN, ROTARY_ENC_PIN_A );  # Blink when the Serial Wombat chip
  # Detects a rotary encoder change


oldRotaryEncoderReading = 0


#Note that in the loop we read the rotary encoder reading, but don't
# blink the LED.  The delay is to illustrate this.  The LED blink
# happens immediately giving user feedback of each change, but the host
# doesn't retreive the new value for some time.

def loop():
  newRotaryEncoderReading = rotaryEncoder.readPublicData()
  if newRotaryEncoderReading != oldRotaryEncoderReading:
    print(newRotaryEncoderReading)
    oldRotaryEncoderReading = newRotaryEncoderReading
  delay(4000);  # Wait 4 seconds between reads to simulate the host doing other stuff


setup()
while True:
    loop()
