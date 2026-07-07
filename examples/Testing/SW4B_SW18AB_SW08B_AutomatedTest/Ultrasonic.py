# Converted from Testing/SW4B_SW18AB_SW08B_AutomatedTest/Ultrasonic.ino
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
import SerialWombatPWM
import SerialWombatServo
import SerialWombatUltrasonicDistanceSensor
import SerialWombatWatchdog

USDSensor = SerialWombatUltrasonicDistanceSensor.SerialWombatUltrasonicDistanceSensor(SW18AB_6B)
usdWD = SerialWombatWatchdog.SerialWombatWatchdog(SW4B_6C)
usdsServo = SerialWombatServo.SerialWombatServo(SW18AB_6B)
SWPWM10 = SerialWombatPWM.SerialWombatPWM_4AB(SW4B_6C)

def usdSensorTest(pin):

  resetAll()

  USDSensor.begin(pin,  # Echo Pin, goes to SW6C pin 2
  HC_SR04,
  pin+1,  #Trigger Pin, goes to SW6C Pin 3
  True, False)
  usdWD.begin(SW18ABPinTo4BPin(pin), SW_HIGH, SW_LOW, 20, False)

  delay(30)
  test("USDSensor_00", USDSensor.readPublicData(), 3400, 500)

  USDServoSweep(pin)

def USDServoSweep(pin):
  servoPin = pin + 2
  resetAll()

  USDSensor.begin(pin,  # Echo Pin, goes to SW6C pin 2
  HC_SR04,
  pin+1,  #Trigger Pin, goes to SW6C Pin 3
  True, False)

  initializePulseReaduS(SW18AB_6B,servoPin)

  SWPWM10.begin(SW18ABPinTo4BPin(pin))
  SWPWM10.setFrequency_SW4AB(SW4AB_PWMFrequency_488_Hz)
  SWPWM10.writePublicData(0x8000);  # Setup PWM with frequency 1KHz to trick the echo to move the servof

  usdsServo.attach(servoPin, 1000,  # Min
  2600);  #Max  // Chosen so that each each increment of the servo should increase it by 100uS (1/16 of range)
  USDSensor.configureServoSweep(servoPin, 0x0000,  #memoryIndex
  8 ,  #Servo Positions
  0x1000,  # servoIncrement,
  False,  #Reverse
  1000,  # servoMoveDelay
  1000);  # uint16_t servoReturnDelay
  USDSensor.enableServoSweep()
  # Wait for servo reading to be between 1000 and 1100

  trycount = 0
  for trycount in range(0, 17):
    pulseTime = pulseRead(SW18AB_6B,servoPin)
    if pulseTime > 930  and  pulseTime < 1070:
      break
    delay(515)
  if trycount == 17:
    test("USDSensor_SS_00", 0, 1)
    return

  i = 0
  testtime = millis()
  for i in range(0, 8):
    # TODO_MANUAL_CONVERSION: while millis() < testtime) yield(:
      pulseTime = pulseRead(SW18AB_6B,servoPin)
      test("USDSensor_SS_01", pulseTime, 1000 + i * 100, 50)

      testtime += 1000
