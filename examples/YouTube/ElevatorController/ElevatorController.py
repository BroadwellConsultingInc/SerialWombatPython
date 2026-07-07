# Converted from YouTube/ElevatorController/ElevatorController.ino
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
import SerialWombatHBridge
import SerialWombatMatrixKeypadold
import SerialWombatUltrasonicDistanceSensor
HBRIDGE_OFF_BOTH_LOW = SerialWombatHBridge.SerialWombatHBridgeDriverMode.HBRIDGE_OFF_BOTH_LOW
HBRIDGE_OFF_BOTH_HIGH = SerialWombatHBridge.SerialWombatHBridgeDriverMode.HBRIDGE_OFF_BOTH_HIGH
HBRIDGE_RELAY_AND_PWM = SerialWombatHBridge.SerialWombatHBridgeDriverMode.HBRIDGE_RELAY_AND_PWM

# sw is provided by the selected interface block above
distanceSensor = SerialWombatUltrasonicDistanceSensor.SerialWombatUltrasonicDistanceSensor(sw)
Pin0HBridge = SerialWombatHBridge.SerialWombatHBridge_18AB(sw)  # Your serial wombat chip may be named something else than sw

#Put this line before setup()
Pin12Keypad = SerialWombatMatrixKeypadold.SerialWombatMatrixKeypad(sw)  # Your serial wombat chip may be named something else than sw

TOP_FLOOR = 110
MID_FLOOR = 80
BOTTOM_FLOOR = 50

MOTOR_OFF = 32768
GO_UP = 65535
GO_DOWN = 0
def setup():
  # Wire.begin() is handled by the selected Python interface block
  # Serial.begin() is not used in this Python example
  sw.begin()  # Python interface was configured above


  distanceSensor.begin (10,  HC_SR04, 11)



  #Add this line to  setup():
  Pin12Keypad.begin(12,  #Control pin
  12,  #Row 0 pin
  13,  # Row 1 pin
  14,  # Row 2 pin
  15,  # Row 3 pin
  16,  # Col 0 pin
  17,  # Col 1 pin
  18,  # Col 2 pin
  19,  # Col 3 pin
  0,  #Public data mode
  1);  #Queue Mode


  #Put this line before setup()

  #Add this to  setup():
  Pin0HBridge.begin(0,  #Pin Number
  1,  # Second Pin
  1000,  # PWM Period in uS
  DRV8833);  # Driver

  #put this line in setup.
  Pin0HBridge.writeHysteresis(87,  #Low Limit
  MOTOR_OFF,  #Low Value
  88,  #High Limit
  MOTOR_OFF,  #High Value
  0);  # Initial output
  #put this line in setup.  Make this the last line after other
  # Output Scaling configurations for this pin
  Pin0HBridge.writeScalingEnabled(True,  #Enabled
  10);  #DataSource

  delay(500)

  if distanceSensor.readPublicData() > BOTTOM_FLOOR:
    Pin0HBridge.writeHysteresis(BOTTOM_FLOOR  + 2,  #Low Limit
    MOTOR_OFF,  #Low Value
    BOTTOM_FLOOR + 3,  #High Limit
    0,  #High Value
    GO_DOWN);  # Initial output


def loop():
  # put your main code here, to run repeatedly:

  i = Pin12Keypad.read()
  if i > 0:
    i-= '0'
    print(i)

  print(distanceSensor.readPublicData())
  # TODO_MANUAL_CONVERSION: switch (i) {
    # TODO_MANUAL_CONVERSION_INDENT: case 1:  # Go to bottom floor
    # TODO_MANUAL_CONVERSION_INDENT: if distanceSensor.readPublicData() > BOTTOM_FLOOR:
      # Going down.
      # TODO_MANUAL_CONVERSION_INDENT: Pin0HBridge.writeHysteresis(BOTTOM_FLOOR  + 2,  #Low Limit
      # TODO_MANUAL_CONVERSION_INDENT: 32768,  #Low Value
      # TODO_MANUAL_CONVERSION_INDENT: BOTTOM_FLOOR + 3,  #High Limit
      # TODO_MANUAL_CONVERSION_INDENT: 0,  #High Value
      # TODO_MANUAL_CONVERSION_INDENT: GO_DOWN);  # Initial output
    # TODO_MANUAL_CONVERSION_INDENT: else:
      #Going up
      # TODO_MANUAL_CONVERSION_INDENT: Pin0HBridge.writeHysteresis(BOTTOM_FLOOR  - 3,  #Low Limit
      # TODO_MANUAL_CONVERSION_INDENT: GO_UP,  #Low Value
      # TODO_MANUAL_CONVERSION_INDENT: BOTTOM_FLOOR - 2,  #High Limit
      # TODO_MANUAL_CONVERSION_INDENT: MOTOR_OFF,  #High Value
      # TODO_MANUAL_CONVERSION_INDENT: 0);  # Initial output
    # TODO_MANUAL_CONVERSION_INDENT: break

    # TODO_MANUAL_CONVERSION_INDENT: case 2:  # Go to middle floor
    # TODO_MANUAL_CONVERSION_INDENT: if distanceSensor.readPublicData() > MID_FLOOR:
      # TODO_MANUAL_CONVERSION_INDENT: Pin0HBridge.writeHysteresis(MID_FLOOR  + 2,  #Low Limit
      # TODO_MANUAL_CONVERSION_INDENT: 32768,  #Low Value
      # TODO_MANUAL_CONVERSION_INDENT: MID_FLOOR + 3,  #High Limit
      # TODO_MANUAL_CONVERSION_INDENT: 0,  #High Value
      # TODO_MANUAL_CONVERSION_INDENT: GO_DOWN);  # Initial output
    # TODO_MANUAL_CONVERSION_INDENT: else:
      # TODO_MANUAL_CONVERSION_INDENT: Pin0HBridge.writeHysteresis(MID_FLOOR  - 3,  #Low Limit
      # TODO_MANUAL_CONVERSION_INDENT: GO_UP,  #Low Value
      # TODO_MANUAL_CONVERSION_INDENT: MID_FLOOR - 2,  #High Limit
      # TODO_MANUAL_CONVERSION_INDENT: MOTOR_OFF,  #High Value
      # TODO_MANUAL_CONVERSION_INDENT: 0);  # Initial output
    # TODO_MANUAL_CONVERSION_INDENT: break

    # TODO_MANUAL_CONVERSION_INDENT: case 3:  #Go to top floor
    # TODO_MANUAL_CONVERSION_INDENT: if distanceSensor.readPublicData() > TOP_FLOOR:
      # TODO_MANUAL_CONVERSION_INDENT: Pin0HBridge.writeHysteresis(TOP_FLOOR  + 2,  #Low Limit
      # TODO_MANUAL_CONVERSION_INDENT: 32768,  #Low Value
      # TODO_MANUAL_CONVERSION_INDENT: TOP_FLOOR + 3,  #High Limit
      # TODO_MANUAL_CONVERSION_INDENT: 0,  #High Value
      # TODO_MANUAL_CONVERSION_INDENT: GO_DOWN);  # Initial output
    # TODO_MANUAL_CONVERSION_INDENT: else:
      # TODO_MANUAL_CONVERSION_INDENT: Pin0HBridge.writeHysteresis(TOP_FLOOR  - 3,  #Low Limit
      # TODO_MANUAL_CONVERSION_INDENT: GO_UP,  #Low Value
      # TODO_MANUAL_CONVERSION_INDENT: TOP_FLOOR - 2,  #High Limit
      # TODO_MANUAL_CONVERSION_INDENT: MOTOR_OFF,  #High Value
      # TODO_MANUAL_CONVERSION_INDENT: 0);  # Initial output
    # TODO_MANUAL_CONVERSION_INDENT: break


setup()
while True:
    loop()
