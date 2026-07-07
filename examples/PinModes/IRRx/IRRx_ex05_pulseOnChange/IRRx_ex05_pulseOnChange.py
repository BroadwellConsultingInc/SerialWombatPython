# Converted from PinModes/IRRx/IRRx_ex05_pulseOnChange/IRRx_ex05_pulseOnChange.ino
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
import SerialWombatIRRx

#This example shows how to use the Serial Wombat IR Receive (IRRx) pin mode.  It assumes an NEC compatible IR Transmitter
#(most inexpensive Arduino kit remotes are compatible) and a 38kHz receiver module that goes low when a modulated IR signal is
#present.
#
#This example is compatible with the Serial Wombat 18AB and 8B chips.
#
#
#In this example commands are received from the pin mode and printed to Serial,
#
#By default the pin mode provides a command byte as its 16 bit public data value.  However, it can be reconfigured
#so that the 16 bit public data value increments each time a command (or a repeat code) is received.  A Blink
#pin mode can then read this value to chirp a buzzer or blink an LED when IR commands are received.  Note that this is
#more sophisticated than the visible LED on some IR Receivers.  The Serial Wombat Blink pin will only pulse
#when data is successfully received and decoded.  An LED on an IR Receivers blinks to indicate presense of an IR signal,
#not successful receiption of an IR packet.
#
#
#Video on IRRx pin mode:
#
#TODO coming soon
#
#SerialWombatIRRx pin mode documentation:
#
#https://broadwellconsultinginc.github.io/SerialWombatArdLib/class_serial_wombat_i_r_rx.html
#


# sw is provided by the selected interface block above
irrx = SerialWombatIRRx.SerialWombatIRRx(sw)
swBlink = SerialWombatBlink.SerialWombatBlink(sw)

IRRX_PIN = 7
BLINK_PIN = 1


def setup():
  # put your setup code here, to run once:
  # Wire.begin() is handled by the selected Python interface block

  # Serial.begin() is not used in this Python example
  delay(3000)
  print("IR Address Filtering Example")


  sw.begin()  # Python interface was configured above

  #Optional Error handling code begin:
  if sw.isSW04():
    print("This Example is not supported on the Serial Wombat 4B chip.  An 8B or 18AB chip is required.")
    while True:
      delay(100)
  if not sw.isLatestFirmware():
    print("Firmware version mismatch.  Download latest Serial Wombat Arduino Library and update Serial Wombat Firmware to latest version")
  if sw.isSW08()  and  not (sw.isPinModeSupported(PIN_MODE_IRRX)  and   sw.isPinModeSupported(PIN_MODE_BLINK)):
    print("The required pin mode does not appear to be supported in this firmware build.  Do you need to download a different firmware?")
    while True:
      delay(100)
  sw.registerErrorHandler(SerialWombatSerialErrorHandlerBrief);  #Register an error handler that will print communication errors to Serial
  #Optional Error handling code end
  irrx.begin(IRRX_PIN,
  DATACOUNT,  # Make data count the output
  0,  #Mode 0 : NEC
  True,  # Use repeat
  SW_LOW,  # Active Low
  1000,  # 1000 ms Public Data Timeout
  0xFFFF,  # Default public data
  False,  # Use Address Filtering
  0x0000  # Transmitter Address (not used)
  )

  #irrx.enablePullup(true);   //Comment in this line if your receiver is open drain type without pullup


  swBlink.begin  (BLINK_PIN, IRRX_PIN)

  delay(1000)

def loop():
  receivedData = irrx.read()

  if receivedData >= 0:
    print(irrx.readPublicData(), end="")
    print(":", end="")
    print(receivedData)


setup()
while True:
    loop()
