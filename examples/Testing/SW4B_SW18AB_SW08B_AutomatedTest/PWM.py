# Converted from Testing/SW4B_SW18AB_SW08B_AutomatedTest/PWM.ino
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


SW18AB_PWM0 = SerialWombatPWM.SerialWombatPWM_18AB(SW18AB_6B)
#SerialWombatPWM_18AB SW18AB_PWM1(SW18AB_6B);
#SerialWombatPWM_18AB SW18AB_PWM2(SW18AB_6B);
#SerialWombatPWM_18AB SW18AB_PWM3(SW18AB_6B);
#SerialWombatPWM_18AB SW18AB_PWM4(SW18AB_6B);
SW18AB_PWM5 = SerialWombatPWM.SerialWombatPWM_18AB(SW18AB_6B)
SW18AB_PWM6 = SerialWombatPWM.SerialWombatPWM_18AB(SW18AB_6B)
SW18AB_PWM7 = SerialWombatPWM.SerialWombatPWM_18AB(SW18AB_6B)
SW18AB_PWM8 = SerialWombatPWM.SerialWombatPWM_18AB(SW18AB_6B)
SW18AB_PWM9 = SerialWombatPWM.SerialWombatPWM_18AB(SW18AB_6B)
SW18AB_PWM10 = SerialWombatPWM.SerialWombatPWM_18AB(SW18AB_6B)
SW18AB_PWM11 = SerialWombatPWM.SerialWombatPWM_18AB(SW18AB_6B)
SW18AB_PWM12 = SerialWombatPWM.SerialWombatPWM_18AB(SW18AB_6B)
SW18AB_PWM13 = SerialWombatPWM.SerialWombatPWM_18AB(SW18AB_6B)
SW18AB_PWM14 = SerialWombatPWM.SerialWombatPWM_18AB(SW18AB_6B)
SW18AB_PWM15 = SerialWombatPWM.SerialWombatPWM_18AB(SW18AB_6B)
SW18AB_PWM16 = SerialWombatPWM.SerialWombatPWM_18AB(SW18AB_6B)
SW18AB_PWM17 = SerialWombatPWM.SerialWombatPWM_18AB(SW18AB_6B)
SW18AB_PWM18 = SerialWombatPWM.SerialWombatPWM_18AB(SW18AB_6B)
SW18AB_PWM19 = SerialWombatPWM.SerialWombatPWM_18AB(SW18AB_6B)

# TODO_MANUAL_CONVERSION: SerialWombatPWM_18AB* SW18ABPWMs[] = {
SW18AB_PWM0,
None,
None,
None,
None,
SW18AB_PWM5,
SW18AB_PWM6,
SW18AB_PWM7,
SW18AB_PWM8,
SW18AB_PWM9,
SW18AB_PWM10,
SW18AB_PWM11,
SW18AB_PWM12,
SW18AB_PWM13,
SW18AB_PWM14,
SW18AB_PWM15,
SW18AB_PWM16,
SW18AB_PWM17,
SW18AB_PWM18,
SW18AB_PWM19


SW8B_PWM0 = SerialWombatPWM.SerialWombatPWM_18AB(SW8B_68)
SW8B_PWM1 = SerialWombatPWM.SerialWombatPWM_18AB(SW8B_68)
SW8B_PWM2 = SerialWombatPWM.SerialWombatPWM_18AB(SW8B_68)
SW8B_PWM3 = SerialWombatPWM.SerialWombatPWM_18AB(SW8B_68)
SW8B_PWM4 = SerialWombatPWM.SerialWombatPWM_18AB(SW8B_68)
SW8B_PWM5 = SerialWombatPWM.SerialWombatPWM_18AB(SW8B_68)
SW8B_PWM6 = SerialWombatPWM.SerialWombatPWM_18AB(SW8B_68)
SW8B_PWM7 = SerialWombatPWM.SerialWombatPWM_18AB(SW8B_68)

# TODO_MANUAL_CONVERSION: SerialWombatPWM_18AB* SW8BPWMs[] = {
SW8B_PWM0,
SW8B_PWM1,
SW8B_PWM2,
SW8B_PWM3,
SW8B_PWM4,
SW8B_PWM5,
SW8B_PWM6,
SW8B_PWM7



SW4B_PWM1 = SerialWombatPWM.SerialWombatPWM(SW4B_6C)
SW4B_PWM2 = SerialWombatPWM.SerialWombatPWM(SW4B_6C)
SW4B_PWM3 = SerialWombatPWM.SerialWombatPWM(SW4B_6C)

# TODO_MANUAL_CONVERSION: SerialWombatPWM* SW4BPWMs[] = {
SW4B_PWM1,  # This should never be used
SW4B_PWM1,
SW4B_PWM2,
SW4B_PWM3




PWM_TEST_INCREMENTS = 100
def pwmTest(sw, startPin, endPin):

  resetAll()
  for pin in range(startPin, (endPin) + 1):

    if not test_pinCanBeOutput(sw, pin):
      continue

    initializePulseReaduS(sw, pin)

  # TODO_MANUAL_CONVERSION: SerialWombatPWM_18AB** PWMArray = None
  if sw == SW18AB_6B:
    PWMArray =  SW18ABPWMs
  elif sw == SW8B_68:
    PWMArray = SW8BPWMs
  #
  # #else if (&sw == &SW4B_6C)
  #{
    #PWMArray = SW4BPWMs;
    #}
    #
    # TODO_MANUAL_CONVERSION: else:
      # TODO_MANUAL_CONVERSION_INDENT: print("Invalid chip for pwm test")
      # TODO_MANUAL_CONVERSION_INDENT: return

    for pwmPeriod_uS in range(122, (50000) + 1):
      for pin in range(startPin, (endPin) + 1):

        if not test_pinCanBeOutput(sw, pin):
          continue
        PWMArray[pin]. begin(pin, 0 )
        PWMArray[pin].writePeriod_uS(pwmPeriod_uS)
      for duty in range(0x0100, (0xE000) + 1):
        for pin in range(startPin, (endPin) + 1):
          if not test_pinCanBeOutput(sw, pin):
            continue


          pinDuty = duty + 0x1000 * pin
          if pinDuty == 0:
            pinDuty = 0x1000
          PWMArray[pin]. writePublicData( pinDuty )

        delay(10 * pwmPeriod_uS / 1000)
        for pin in range(startPin, (endPin) + 1):

          if not test_pinCanBeOutput(sw, pin):
            continue


          pinDuty = duty + 0x1000 * pin
          result = pulseRead(sw, pin)
          setting = ((pwmPeriod_uS) * (pinDuty)) >> 16
          if setting < 50:
            continue
          #TODO if (reverse)
          #{
            #setting = (65535 - setting);
            #}
            #
            s = [0] * (70)
            s = ("PWM 01 Pin: %d Period: %lu Duty cycle: %d ") % (pin, pwmPeriod_uS, pinDuty)
            test(s, result, setting, 30, 5)
