# Converted from PinModes/PulseOnChange/PulseOnChange_Ex02_BeepOnButtons/PulseOnChange_Ex02_BeepOnButtons.ino
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
import SerialWombatDebouncedInput
import SerialWombatPulseOnChange

#
#
#THIS EXAMPLE REQUIRES SW18AB Firmware Version 2.1.0 or Higher!
#
#This example shows how to create a PulseOnChange pin configured to pulse when any of a set of
#configured pins or data sources changes.
#
#This example assumes a piezo is attached to Pin 8 (The kind of piezo without a built in driver)
#through a resistor.  Pin 8 is chosen because this example requires minimal hardware
#support (Analog, enhanced digital capability, etc.) and pin 8 has none of these things.
#
#The pulse on change pin mode looks at pins 19,18, and 17 which are configured as debounced inputs.
#When the value of any of those pins increases (the button is pressed) then a tone is generated.
#
#Documentation for the SerialWombatPulseOnChange Arduino class is available at:
#https://broadwellconsultinginc.github.io/SerialWombatArdLib/class_serial_wombat_pulse_on_change.html#details
#
#

# sw is provided by the selected interface block above
poc = SerialWombatPulseOnChange.SerialWombatPulseOnChange(sw)
dbi19 = SerialWombatDebouncedInput.SerialWombatDebouncedInput(sw)
dbi18 = SerialWombatDebouncedInput.SerialWombatDebouncedInput(sw)
dbi17 = SerialWombatDebouncedInput.SerialWombatDebouncedInput(sw)

def setup():
  # put your setup code here, to run once:
  # Wire.begin() is handled by the selected Python interface block

  # Serial.begin() is not used in this Python example
  delay(3000)
  print("Pulse on Change multiple input Example")


  sw.begin()  # Python interface was configured above

  #Optional Error handling code begin:
  if sw.isSW04():
    print("This Example is not supported on the Serial Wombat 4B chip.  An 8B or 18AB chip is required.")
    while True:
      delay(100)
  if not sw.isLatestFirmware():
    print("Firmware version mismatch.  Download latest Serial Wombat Arduino Library and update Serial Wombat Firmware to latest version")
  if sw.isSW08()  and  not (sw.isPinModeSupported(PIN_MODE_PULSE_ON_CHANGE)  and  sw.isPinModeSupported(PIN_MODE_DEBOUNCE)):
    print("The required pin mode does not appear to be supported in this firmware build.  Do you need to download a different firmware?")
    while True:
      delay(100)
  sw.registerErrorHandler(SerialWombatSerialErrorHandlerBrief);  #Register an error handler that will print communication errors to Serial
  #Optional Error handling code end

  dbi19.begin(19)
  dbi18.begin(18)
  dbi17.begin(17)


  poc.begin(8);  # Implied values active high, inactive low, 50mS pulse time, 50mS pulse off, OR entries, No PWM

  poc.setEntryOnIncrease(0,  # first entry (valid values are 0-7)
  19);  # The data source we're monitoring for change
  poc.setEntryOnIncrease(1,  # first entry (valid values are 0-7)
  18);  # The data source we're monitoring for change
  poc.setEntryOnIncrease(2,  # first entry (valid values are 0-7)
  17);  # The data source we're monitoring for change



def loop():

  #Nothing to do...  The Serial Wombat chip is handling this internally.
  delay(1000)


setup()
while True:
    loop()
