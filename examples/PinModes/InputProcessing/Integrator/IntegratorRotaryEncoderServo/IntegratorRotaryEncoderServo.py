# Converted from PinModes/InputProcessing/Integrator/IntegratorRotaryEncoderServo/IntegratorRotaryEncoderServo.ino
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
import SerialWombatQuadEnc
import SerialWombatServo
import SerialWombatTM1637
tm1637Decimal16 = SerialWombatTM1637.SWTM1637Mode.tm1637Decimal16
tm1637Hex16 = SerialWombatTM1637.SWTM1637Mode.tm1637Hex16
tm1637CharArray = SerialWombatTM1637.SWTM1637Mode.tm1637CharArray
tm1637RawArray = SerialWombatTM1637.SWTM1637Mode.tm1637RawArray
tm1637Animation = SerialWombatTM1637.SWTM1637Mode.tm1637Animation

#
#This example shows how to integrate a rotary encoder to control the position
#of a servo by controlling the servo position based on the net result of the rotary encoder position
#over time, rather than directly correlating the servo's current position to the encoders's current
#position.
#
#The encoder will have 5 positions, fast left, slow left, stop, slow right, and fast right
#
#This integration function can be applied to any class that inherits from the ProcessedInput class.
#
#Servo is on pin 1.
#The rotary encoder is on pins 5 and 6.
#
#This example also outputs the current position on a TM1637 Display attached to pins 16 and 17.
#A video demonstrating the use of input integration function is avaialble at:
#TODO
#
#Documentation for the  class is available at:
#https://broadwellconsultinginc.github.io/SerialWombatArdLib/class_serial_wombat_abstract_processed_input.html
#
#

# sw is provided by the selected interface block above
rotary = SerialWombatQuadEnc.SerialWombatQuadEnc_18AB(sw)
servo = SerialWombatServo.SerialWombatServo_18AB(sw)
display = SerialWombatTM1637.SerialWombatTM1637(sw)


def setup():
  # put your setup code here, to run once:
  # Wire.begin() is handled by the selected Python interface block

  # Serial.begin() is not used in this Python example
  delay(3000)
  print("Integrator Quadrature Encoder Servo Example")


  sw.begin()  # Python interface was configured above

  #Optional Error handling code begin:
  if sw.isSW04():
    print("This Example is not supported on the Serial Wombat 4B chip.  An 8B or 18AB chip is required.")
    while True:
      delay(100)
  if not sw.isLatestFirmware():
    print("Firmware version mismatch.  Download latest Serial Wombat Arduino Library and update Serial Wombat Firmware to latest version")
  if sw.isSW08()  and  not (sw.isPinModeSupported(PIN_MODE_QUADRATUREENCODER)  and  sw.isPinModeSupported(PIN_MODE_SERVO)):
    print("The required pin mode does not appear to be supported in this firmware build.  Do you need to download a different firmware?")
    while True:
      delay(100)
  sw.registerErrorHandler(SerialWombatSerialErrorHandlerBrief);  #Register an error handler that will print communication errors to Serial
  #Optional Error handling code end

  rotary.begin(5,6)
  rotary.writeMinMaxIncrementTargetPin(0,6)

  rotary.configureIntegrator (0,  #negativeMaxIndex,
  2,  # negativeMidIndex,
  3,  # negativeDeadZone
  3,  #positiveDeadZone
  4,  # positiveMidIndex,
  6,  #positiveMaxIndex,
  5,  # midIncrement 5 counts per ms, 5000 counts per second
  40,  # maxIncrement 20 counts per ms, 20000 counts per second
  32768  #initialValue
  )
  rotary.writeProcessedInputEnable(True)


  servo.attach(1)
  servo.writeScalingEnabled(True,5);  #Position the servo based on Pin 5's output

  display.begin(16,  #Clk Pin
  17,  #Data pin
  6,  # 6 digits
  tm1637Decimal16,  #Decimal 16 mode
  5,  # Get data from pin 5
  4);  # Brightness 4
  display.writeDigitOrder(2,1,0,5,4,3)




def loop():
  #No action in loop.  Serial Wombat chip is driving the servo internally.  We can monitor the result:
  print(rotary.readPublicData())


setup()
while True:
    loop()
