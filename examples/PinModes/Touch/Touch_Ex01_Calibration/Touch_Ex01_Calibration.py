# Converted from PinModes/Touch/Touch_Ex01_Calibration/Touch_Ex01_Calibration.ino
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
import SerialWombat18CapTouch


#
#This example shows how to configure a Serial Wombat 18AB pin to Touch input and determine working
#calibration constants for the touch sensor.
#
#SerialWombat18CapTouch class documentation can be found here:
#https://broadwellconsultinginc.github.io/SerialWombatArdLib/class_serial_wombat18_cap_touch.html#details
#
#
#A demonstration video of this class can be found here:
#https://youtu.be/c4B0_DRVHs0
#
#

TOUCH_PIN = 17  #<<<<<< MODIFY THIS BASED ON WHICH PIN YOUR TOUCH SENSOR IS RUNNING ON
# sw is provided by the selected interface block above
capTouch = SerialWombat18CapTouch.SerialWombat18CapTouch(sw)

lastDigitalRead = 0
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


  #Iterate through increasing amounts of charge until we find a value that 90% saturates the sensor.
  print("Determining charge time.  Do not touch the sensor.")

  noTouchReading = 0
  chargeTime = 250
  capTouch.begin(TOUCH_PIN,chargeTime,0)
  delay(500)
  noTouchReading = sw.readPublicData(TOUCH_PIN)

  while noTouchReading < 60000:
    if noTouchReading < 30000:
      chargeTime += 250
    else:
      chargeTime += 250
    capTouch.begin(TOUCH_PIN,chargeTime,20)
    delay(500)
    noTouchReading = sw.readPublicData(TOUCH_PIN)
    print(chargeTime, end="")
    print(": ", end="")
    print(noTouchReading)

  recommendedChargeTime = chargeTime

  print("Recommended charge time: ", end="")
  print(recommendedChargeTime)
  print()


  # Now take a bunch of samples at that charge to see how much varation you get.  Find the
  # smallest returned value over 5 seconds.
  print("Calibrating High Limit...")
  HighLimit = 65535
  start = millis()
  while start + 5000 > millis():
    result = sw.readPublicData(TOUCH_PIN)

    if result < HighLimit:
      HighLimit = result
      print(HighLimit)

    delay(0)



  print("Lightly Hold finger on sensor until told to remove...")
  # Wait for the user to touch the sensor
  while sw.readPublicData(TOUCH_PIN) > HighLimit - 1500:
    delay(250)
    print(".", end="")
  print()


  # Now take 5 seconds worth of samples to determine the maximum value you're likely to see
  # while touched.
  LowLimit = 0
  start = millis()
  while start + 5000 > millis():
    result = sw.readPublicData(TOUCH_PIN)

    if result > LowLimit:
      LowLimit = result
      print(LowLimit)

  print("Remove Finger.")
  print("Recommended charge time: ", end="")
  print(recommendedChargeTime)
  print("Recommended High Limit: ", end="")
  print(LowLimit + (HighLimit - LowLimit)*3 / 4)
  print("Recommended Low Limit: ", end="")
  print(LowLimit + (HighLimit - LowLimit) / 4)

  print("Done.")

  print()
  print("Configuring Touch in digital mode using calibrations.  Code is:")
  print()
  print(" capTouch.begin(TOUCH_PIN,");Serial.print(recommendedChargeTime);Serial.println(",0);", end="")
  print("capTouch.makeDigital("); Serial.print(LowLimit);Serial.print(",");Serial.print(HighLimit);Serial.println(",1,0,0,0);", end="")
  print()

  capTouch.makeDigital(LowLimit,HighLimit,1,0,0,0)
  delay(250)
  lastDigitalRead = sw.readPublicData(TOUCH_PIN)



#In the loop look for a change in state on the sensor and print a 0 or 1
def loop():
  count = 0
  newValue = sw.readPublicData(TOUCH_PIN)

  if newValue != lastDigitalRead:
    print(newValue); Serial.print(" ", end="")
    lastDigitalRead = newValue
    ++ count
    if count > 20:
      count = 0
      print()


setup()
while True:
    loop()
