# Converted from Testing/SW4B_SW18AB_SW08B_AutomatedTest/Servo.ino
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
import SerialWombatServo

SERVO_DEFAULT_BASE = 544
SERVO_DEFAULT_VARIABLE = 1856

PRINT_FAILURES = True



SW18AB_Servo0 = SerialWombatServo.SerialWombatServo_18AB(SW18AB_6B)
#SerialWombatServo_18AB SW18AB_Servo1(SW18AB_6B);
#SerialWombatServo_18AB SW18AB_Servo2(SW18AB_6B);
#SerialWombatServo_18AB SW18AB_Servo3(SW18AB_6B);
#SerialWombatServo_18AB SW18AB_Servo4(SW18AB_6B);
SW18AB_Servo5 = SerialWombatServo.SerialWombatServo_18AB(SW18AB_6B)
SW18AB_Servo6 = SerialWombatServo.SerialWombatServo_18AB(SW18AB_6B)
SW18AB_Servo7 = SerialWombatServo.SerialWombatServo_18AB(SW18AB_6B)
SW18AB_Servo8 = SerialWombatServo.SerialWombatServo_18AB(SW18AB_6B)
SW18AB_Servo9 = SerialWombatServo.SerialWombatServo_18AB(SW18AB_6B)
SW18AB_Servo10 = SerialWombatServo.SerialWombatServo_18AB(SW18AB_6B)
SW18AB_Servo11 = SerialWombatServo.SerialWombatServo_18AB(SW18AB_6B)
SW18AB_Servo12 = SerialWombatServo.SerialWombatServo_18AB(SW18AB_6B)
SW18AB_Servo13 = SerialWombatServo.SerialWombatServo_18AB(SW18AB_6B)
SW18AB_Servo14 = SerialWombatServo.SerialWombatServo_18AB(SW18AB_6B)
SW18AB_Servo15 = SerialWombatServo.SerialWombatServo_18AB(SW18AB_6B)
SW18AB_Servo16 = SerialWombatServo.SerialWombatServo_18AB(SW18AB_6B)
SW18AB_Servo17 = SerialWombatServo.SerialWombatServo_18AB(SW18AB_6B)
SW18AB_Servo18 = SerialWombatServo.SerialWombatServo_18AB(SW18AB_6B)
SW18AB_Servo19 = SerialWombatServo.SerialWombatServo_18AB(SW18AB_6B)

# TODO_MANUAL_CONVERSION: SerialWombatServo_18AB* SW18ABServos[] = {
SW18AB_Servo0,
None,
None,
None,
None,
SW18AB_Servo5,
SW18AB_Servo6,
SW18AB_Servo7,
SW18AB_Servo8,
SW18AB_Servo9,
SW18AB_Servo10,
SW18AB_Servo11,
SW18AB_Servo12,
SW18AB_Servo13,
SW18AB_Servo14,
SW18AB_Servo15,
SW18AB_Servo16,
SW18AB_Servo17,
SW18AB_Servo18,
SW18AB_Servo19


SW8B_Servo0 = SerialWombatServo.SerialWombatServo_18AB(SW8B_68)
SW8B_Servo1 = SerialWombatServo.SerialWombatServo_18AB(SW8B_68)
SW8B_Servo2 = SerialWombatServo.SerialWombatServo_18AB(SW8B_68)
SW8B_Servo3 = SerialWombatServo.SerialWombatServo_18AB(SW8B_68)
SW8B_Servo4 = SerialWombatServo.SerialWombatServo_18AB(SW8B_68)
SW8B_Servo5 = SerialWombatServo.SerialWombatServo_18AB(SW8B_68)
SW8B_Servo6 = SerialWombatServo.SerialWombatServo_18AB(SW8B_68)
SW8B_Servo7 = SerialWombatServo.SerialWombatServo_18AB(SW8B_68)

# TODO_MANUAL_CONVERSION: SerialWombatServo_18AB* SW8BServos[] = {
SW8B_Servo0,
SW8B_Servo1,
SW8B_Servo2,
SW8B_Servo3,
SW8B_Servo4,
SW8B_Servo5,
SW8B_Servo6,
SW8B_Servo7



SW4B_Servo1 = SerialWombatServo.SerialWombatServo(SW4B_6C)
SW4B_Servo2 = SerialWombatServo.SerialWombatServo(SW4B_6C)
SW4B_Servo3 = SerialWombatServo.SerialWombatServo(SW4B_6C)

# TODO_MANUAL_CONVERSION: SerialWombatServo* SW4BServos[] = {
SW4B_Servo1,  # This should never be used
SW4B_Servo1,
SW4B_Servo2,
SW4B_Servo3



# #if 0
SWHFServo10 = SerialWombatServo.SerialWombatHighFrequencyServo(SW18AB_6B)
SWHFServo11 = SerialWombatServo.SerialWombatHighFrequencyServo(SW18AB_6B)
SWHFServo12 = SerialWombatServo.SerialWombatHighFrequencyServo(SW18AB_6B)
SWHFServo13 = SerialWombatServo.SerialWombatHighFrequencyServo(SW18AB_6B)
SWHFServo14 = SerialWombatServo.SerialWombatHighFrequencyServo(SW18AB_6B)
SWHFServo15 = SerialWombatServo.SerialWombatHighFrequencyServo(SW18AB_6B)
# #endif

SERVO_TEST_INCREMENTS = 100
def servoTest(sw, startPin, endPin):

  resetAll()
  for pin in range(startPin, (endPin) + 1):

    if not test_pinCanBeOutput(sw,pin):
      continue

    initializePulseReaduS(sw,pin)

  # TODO_MANUAL_CONVERSION: SerialWombatServo** ServoArray = None
  if sw == SW18AB_6B:
    pass
    # TODO_MANUAL_CONVERSION: ServoArray = (SerialWombatServo**) SW18ABServos
  elif sw == SW8B_68:
    pass
    # TODO_MANUAL_CONVERSION: ServoArray = (SerialWombatServo**) SW8BServos
  elif sw == SW4B_6C:
    ServoArray = SW4BServos
  else:
    print("Invalid chip for servo test")
    return

  for variable in range(800, (2000) + 1):
    print(" iteration "); Serial.print((variable - 800) / 100); Serial.println(" of 13", end="")
    for base in range(500, (1200) + 1):
      for reverse in range(0, 2):
        for i in range(0, SERVO_TEST_INCREMENTS):

          for pin in range(startPin, (endPin) + 1):

            if not test_pinCanBeOutput(sw,pin):
              continue



            ServoArray[pin]. attach(pin, base, base + variable, reverse)
            ServoArray[pin].write16bit((i * 65535 ) / SERVO_TEST_INCREMENTS + (pin * 65535 / NUM_TEST_PINS))
          delay(100)
          for pin in range(startPin, (endPin) + 1):

            if not test_pinCanBeOutput(sw,pin):
              continue



            result = pulseRead(sw,pin)
            # TODO_MANUAL_CONVERSION: setting = i * 65535 ) / SERVO_TEST_INCREMENTS + (pin * 65535 / NUM_TEST_PINS
            if reverse:
              setting = (65535 - setting)
            expected = (variable) * setting / 65536 + base

            if (result < (expected + (expected / 20)) + 20)  and  (result > (expected - (expected / 20) - 20)):
              pass
              # 2% clock error on receiver, 2% error on sender, worst case 4% either way plus a little round off error, +/- 20 for quant. error in DMA.
              #
              #Serial.print(pin);
              #Serial.print(" ");
              #Serial.print(result);
              #Serial.print(" ");
              #Serial.print(expected);
              #Serial.print(" ");
              #Serial.print ("Pass");
              #Serial.println();
              #
              # TODO_MANUAL_CONVERSION: pass(i)
            else:
              # #ifdef PRINT_FAILURES
              print(pin);Serial.print(" ");Serial.print(result, end="")
              print(" ");Serial.print(expected);Serial.print(" ", end="")
              # TODO_MANUAL_CONVERSION: print("Fail");Serial.println(, end="")
              # #endif

              fail(i)


  # #ifdef TODO
  testHSServo()
  # #endif
# #if 0

def testHSServo():
  delay(10000)
  resetAll()

  initializePulseReaduS(10)
  SWHFServo10.attach(10,400,900,False)
  SWHFServo10.writeFrequency_Hz(700)

  initializePulseReaduS(11)
  SWHFServo11.attach(11,200,1000,False)
  SWHFServo11.writeFrequency_Hz(700)

  initializePulseReaduS(12)
  SWHFServo12.attach(12,200,500,False)
  SWHFServo12.writeFrequency_Hz(1100)

  initializePulseReaduS(13)
  SWHFServo13.attach(13,500,2500,False)
  SWHFServo13.writeFrequency_Hz(300)

  initializePulseReaduS(14)
  SWHFServo14.attach(14,500,1500,False)
  SWHFServo14.writeFrequency_Hz(300)

  initializePulseReaduS(15)
  SWHFServo15.attach(15,100,300,False)
  SWHFServo15.writeFrequency_Hz(1500)



  SWHFServo10.write16bit(0)
  SWHFServo11.write16bit(0)
  SWHFServo12.write16bit(0)
  SWHFServo13.write16bit(0)
  SWHFServo14.write16bit(0)
  SWHFServo15.write16bit(0)
  delay(10)
  result = pulseRead(10)
  test("HSSERVO_0_10", result, 400,0,3)
  result = pulseRead(11)
  test("HSSERVO_0_11", result, 200,0,3)
  result = pulseRead(12)
  test("HSSERVO_0_12", result, 200,0,3)
  result = pulseRead(13)
  test("HSSERVO_0_13", result, 500,0,3)
  result = pulseRead(14)
  test("HSSERVO_0_14", result, 500,0,3)
  result = pulseRead(15)
  test("HSSERVO_0_16", result, 100,0,3)



  SWHFServo10.write16bit(0x8000)
  SWHFServo11.write16bit(0x8000)
  SWHFServo12.write16bit(0x8000)
  SWHFServo13.write16bit(0x8000)
  SWHFServo14.write16bit(0x8000)
  SWHFServo15.write16bit(0x8000)
  delay(10)
  result = pulseRead(10)
  test("HSSERVO_1_10", result, 650,0,3)
  result = pulseRead(11)
  test("HSSERVO_1_11", result, 600,0,3)
  result = pulseRead(12)
  test("HSSERVO_1_12", result, 350,0,3)
  result = pulseRead(13)
  test("HSSERVO_1_13", result, 1500,0,3)
  result = pulseRead(14)
  test("HSSERVO_1_14", result, 1000,0,3)
  result = pulseRead(15)
  test("HSSERVO_1_15", result, 200,0,3)

  SWHFServo10.write16bit(0xFFFF)
  SWHFServo11.write16bit(0xFFFF)
  SWHFServo12.write16bit(0xFFFF)
  SWHFServo13.write16bit(0xFFFF)
  SWHFServo14.write16bit(0xFFFF)
  SWHFServo15.write16bit(0xFFFF)
  delay(10)

  result = pulseRead(10)

  test("HSSERVO_2_10", result, 900,0,3)
  result = pulseRead(11)
  test("HSSERVO_2_11", result, 1000,0,3)
  result = pulseRead(12)
  test("HSSERVO_2_12", result, 500,0,3)
  result = pulseRead(13)
  test("HSSERVO_2_13", result, 2500,0,3)
  result = pulseRead(14)
  test("HSSERVO_2_14", result, 1500,0,3)
  result = pulseRead(15)
  test("HSSERVO_2_15", result, 300,0,3)


  # #if 0
  second = 0
  expected = 0
  while second < 10000:
    print(second)
    first = PulseTimerArray[10].readPulses()
    delay(3000)
    second = PulseTimerArray[10].readPulses()

    expected = first + 3*700
  test("HSSERVO_3", second, expected,0,3)
  print("A")
  second = 0
  while second < 10000:
    print(second)
    first = PulseTimerArray[11].readPulses()
    delay(3000)
    second = PulseTimerArray[11].readPulses()

    expected = first + 3*700
  test("HSSERVO_3_11", second, expected,0,3)
  print("B")
  second = 0
  while second < 10000:
    print(second)
    first = PulseTimerArray[12].readPulses()
    delay(3000)
    second = PulseTimerArray[12].readPulses()

    expected = first + 3*1100
  test("HSSERVO_3_12", second, expected,0,3)
  print("C")
  second = 0
  while second < 10000:
    print(second)
    first = PulseTimerArray[13].readPulses()
    delay(3000)
    second = PulseTimerArray[13].readPulses()

    expected = first + 3*300
  test("HSSERVO_3_13", second, expected,0,3)
  print("D")
  second = 0
  while second < 10000:
    print(second)
    first = PulseTimerArray[14].readPulses()
    delay(3000)
    second = PulseTimerArray[14].readPulses()

    expected = first + 3*300
  test("HSSERVO_3_14", second, expected,0,3)
  print("E")
  second = 0
  while second < 10000:
    print(second)
    first = PulseTimerArray[15].readPulses()
    delay(3000)
    second = PulseTimerArray[15].readPulses()

    expected = first + 3*1500
  test("HSSERVO_3_15", second, expected,0,3)
  print("F")
  # #endif
# #endif
