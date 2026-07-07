# Converted from PinModes/PulseOnChange/PulseOnChange_Ex01_CommunicationsLED/PulseOnChange_Ex01_CommunicationsLED.ino
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
import SerialWombatPulseOnChange

#
#This example shows how create an output that pulses high when the Serial Wombat 8B or 18AB Chip
#receives a communication packet.  This allows easy creation of a communication LED.
#
#This example assumes an LED with appropriate current limiting resistor is attached to a pin of the Serial Wombat
#chip.
#
#The pulse on change pin mode looks at other pins or public 16-bit data to determine when to pulse.
#
#Data providers 0-63 correspond to physical pins on the Serial Wombat chip (only 0-19 are implemented on
#the SW18AB).  64 and up correspond to system values.
#
#Avaialble public data is enumerated in the firmware (not all values suppored by all chips):
#https://github.com/BroadwellConsultingInc/SerialWombat/blob/main/SerialWombatCommon/serialWombat.h
#
#which is also available as an enumeration in the Arduino Library SerialWombatDataSource enum:
#https://broadwellconsultinginc.github.io/SerialWombatArdLib/_serial_wombat_8h.html#aa93a00ab6275924ab4d521604780f6fa
#
#
#In this case we will use SW_DATA_SOURCE_PACKETS_RECEIVED (enum value 71) which changes each time a packet
#addressed to this Serial Wombat chip is received.
#
#We will pulse the LED high for 50mS with a delay of 50mS for low time (The default values).
#
#Each Pulse on Change pin has up to 4 state machine entries that can cause the pin to become active.  This is
#useful if you want to have more than one source capable of driving a pulse (such as multiple buttons leading to a
#feedback led or piezo).
#
#For this example we will only use one which will be configured to pulse on change of SW_DATA_SOURCE_PACKETS_RECEIVED.
#
#
#
#Documentation for the SerialWombatPulseOnChange Arduino class is available at:
#https://broadwellconsultinginc.github.io/SerialWombatArdLib/class_serial_wombat_pulse_on_change.html#details
#
#

# sw is provided by the selected interface block above
poc = SerialWombatPulseOnChange.SerialWombatPulseOnChange(sw)

PULSE_ON_CHANGE_PIN = 1

def setup():
  # put your setup code here, to run once:
  # Wire.begin() is handled by the selected Python interface block

  # Serial.begin() is not used in this Python example
  delay(3000)
  print("Pulse on Change Example")


  sw.begin()  # Python interface was configured above

  #Optional Error handling code begin:
  if sw.isSW04():
    print("This Example is not supported on the Serial Wombat 4B chip.  An 8B or 18AB chip is required.")
    while True:
      delay(100)
  if not sw.isLatestFirmware():
    print("Firmware version mismatch.  Download latest Serial Wombat Arduino Library and update Serial Wombat Firmware to latest version")
  if sw.isSW08()  and  not sw.isPinModeSupported(PIN_MODE_PULSE_ON_CHANGE):
    print("The required pin mode does not appear to be supported in this firmware build.  Do you need to download a different firmware?")
    while True:
      delay(100)
  sw.registerErrorHandler(SerialWombatSerialErrorHandlerBrief);  #Register an error handler that will print communication errors to Serial
  #Optional Error handling code end

  poc.begin  ( PULSE_ON_CHANGE_PIN);  # Implied values active high, inactive low, 50mS pulse time, 50mS pulse off, OR entries, No PWM
  poc.setEntryOnChange(0,  # first entry (valid values are 0-7)
  SW_DATA_SOURCE_PACKETS_RECEIVED);  # The data source we're monitoring for change



def loop():

  #Cause 3 packets to be sent
  for i in range(0, 3):
    x = sw.readPublicData(SW_DATA_SOURCE_PACKETS_RECEIVED)
    print(x)
  # then delay
  delay(1000)


setup()
while True:
    loop()
