# Converted from Boards/PCB0035_SW8B_CRAZY8/SW8B_CRAZY8_PWMDemo/SW8B_CRAZY8_PWMDemo.ino
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

#
#This example shows creating 8 instances of the Serial Wombat class and 64 instances of the SerialWombatPWM_18AB class
#to drive 64 PWMs at different frequencies on a SW8B PCB0035 8x board.  This board has 8 Serial Wombat 8B chips on
#addresses 0x60 to 0x67, resulting in 64 total outputs.
#
#This example sets each pin (00,01..07, 10,11,12..17, ...   76,77) to a frequency of
#1000 * the tens digit of the pin, and 100 * the ones digit HZ.  This can be measured to determine that all
#pins are being independently manipulated.
#
#The SerialWombatPWM_18AB class applies to both the SW8B and SW18AB firmware.
#
#The Serial Wombat Arduino C++ library uses references instead of pointers for most operations as
#these are easier for beginners.  However, it is not possible to create an array of references in
#C++.  The SerialWombatPWM_18AB class requires a reference to a Serial Wombat Chip when it is created.
#
#As such I see no way around explictly declaring all 8 Serial Wombat chips and all
#64 pwm instances as shown in this example.
#An array of pointers is then made to the explictly declared objects, and used iteratively for
#the begin and frequency set calls.
#
#Beginners to C++ should note that this results in a -> operator to get from the array of
#Serial Wombat chips or PWMs instead of the typical '.' operator.
#
#If anyone knows of a more elegant solution that doesn't require changing the underlying library,
#please send me an example at help@serialwombat.com
#
#A video demonstrating this example is available at:
#TODO
#
#Documentation for the SerialWombatPWM_18AB class is available at:
#https://broadwellconsultinginc.github.io/SerialWombatArdLib/class_serial_wombat_p_w_m__18_a_b.html
#

sw0 = SerialWombat.SerialWombatChip()
sw1 = SerialWombat.SerialWombatChip()
sw2 = SerialWombat.SerialWombatChip()
sw3 = SerialWombat.SerialWombatChip()
sw4 = SerialWombat.SerialWombatChip()
sw5 = SerialWombat.SerialWombatChip()
sw6 = SerialWombat.SerialWombatChip()
sw7 = SerialWombat.SerialWombatChip()  # Arrays of references are not allowed in C++, and the PWM Declaration requires a reference.



# TODO_MANUAL_CONVERSION: SerialWombatChip* sw[8] = {sw0,sw1,sw2,sw3,sw4,sw5,sw6,sw7}

p00 = SerialWombatPWM.SerialWombatPWM_18AB(sw0)
p01 = SerialWombatPWM.SerialWombatPWM_18AB(sw0)
p02 = SerialWombatPWM.SerialWombatPWM_18AB(sw0)
p03 = SerialWombatPWM.SerialWombatPWM_18AB(sw0)
p04 = SerialWombatPWM.SerialWombatPWM_18AB(sw0)
p05 = SerialWombatPWM.SerialWombatPWM_18AB(sw0)
p06 = SerialWombatPWM.SerialWombatPWM_18AB(sw0)
p07 = SerialWombatPWM.SerialWombatPWM_18AB(sw0)
p10 = SerialWombatPWM.SerialWombatPWM_18AB(sw1)
p11 = SerialWombatPWM.SerialWombatPWM_18AB(sw1)
p12 = SerialWombatPWM.SerialWombatPWM_18AB(sw1)
p13 = SerialWombatPWM.SerialWombatPWM_18AB(sw1)
p14 = SerialWombatPWM.SerialWombatPWM_18AB(sw1)
p15 = SerialWombatPWM.SerialWombatPWM_18AB(sw1)
p16 = SerialWombatPWM.SerialWombatPWM_18AB(sw1)
p17 = SerialWombatPWM.SerialWombatPWM_18AB(sw1)
p20 = SerialWombatPWM.SerialWombatPWM_18AB(sw2)
p21 = SerialWombatPWM.SerialWombatPWM_18AB(sw2)
p22 = SerialWombatPWM.SerialWombatPWM_18AB(sw2)
p23 = SerialWombatPWM.SerialWombatPWM_18AB(sw2)
p24 = SerialWombatPWM.SerialWombatPWM_18AB(sw2)
p25 = SerialWombatPWM.SerialWombatPWM_18AB(sw2)
p26 = SerialWombatPWM.SerialWombatPWM_18AB(sw2)
p27 = SerialWombatPWM.SerialWombatPWM_18AB(sw2)
p30 = SerialWombatPWM.SerialWombatPWM_18AB(sw3)
p31 = SerialWombatPWM.SerialWombatPWM_18AB(sw3)
p32 = SerialWombatPWM.SerialWombatPWM_18AB(sw3)
p33 = SerialWombatPWM.SerialWombatPWM_18AB(sw3)
p34 = SerialWombatPWM.SerialWombatPWM_18AB(sw3)
p35 = SerialWombatPWM.SerialWombatPWM_18AB(sw3)
p36 = SerialWombatPWM.SerialWombatPWM_18AB(sw3)
p37 = SerialWombatPWM.SerialWombatPWM_18AB(sw3)
p40 = SerialWombatPWM.SerialWombatPWM_18AB(sw4)
p41 = SerialWombatPWM.SerialWombatPWM_18AB(sw4)
p42 = SerialWombatPWM.SerialWombatPWM_18AB(sw4)
p43 = SerialWombatPWM.SerialWombatPWM_18AB(sw4)
p44 = SerialWombatPWM.SerialWombatPWM_18AB(sw4)
p45 = SerialWombatPWM.SerialWombatPWM_18AB(sw4)
p46 = SerialWombatPWM.SerialWombatPWM_18AB(sw4)
p47 = SerialWombatPWM.SerialWombatPWM_18AB(sw4)
p50 = SerialWombatPWM.SerialWombatPWM_18AB(sw5)
p51 = SerialWombatPWM.SerialWombatPWM_18AB(sw5)
p52 = SerialWombatPWM.SerialWombatPWM_18AB(sw5)
p53 = SerialWombatPWM.SerialWombatPWM_18AB(sw5)
p54 = SerialWombatPWM.SerialWombatPWM_18AB(sw5)
p55 = SerialWombatPWM.SerialWombatPWM_18AB(sw5)
p56 = SerialWombatPWM.SerialWombatPWM_18AB(sw5)
p57 = SerialWombatPWM.SerialWombatPWM_18AB(sw5)
p60 = SerialWombatPWM.SerialWombatPWM_18AB(sw6)
p61 = SerialWombatPWM.SerialWombatPWM_18AB(sw6)
p62 = SerialWombatPWM.SerialWombatPWM_18AB(sw6)
p63 = SerialWombatPWM.SerialWombatPWM_18AB(sw6)
p64 = SerialWombatPWM.SerialWombatPWM_18AB(sw6)
p65 = SerialWombatPWM.SerialWombatPWM_18AB(sw6)
p66 = SerialWombatPWM.SerialWombatPWM_18AB(sw6)
p67 = SerialWombatPWM.SerialWombatPWM_18AB(sw6)
p70 = SerialWombatPWM.SerialWombatPWM_18AB(sw7)
p71 = SerialWombatPWM.SerialWombatPWM_18AB(sw7)
p72 = SerialWombatPWM.SerialWombatPWM_18AB(sw7)
p73 = SerialWombatPWM.SerialWombatPWM_18AB(sw7)
p74 = SerialWombatPWM.SerialWombatPWM_18AB(sw7)
p75 = SerialWombatPWM.SerialWombatPWM_18AB(sw7)
p76 = SerialWombatPWM.SerialWombatPWM_18AB(sw7)
p77 = SerialWombatPWM.SerialWombatPWM_18AB(sw7)

# TODO_MANUAL_CONVERSION: SerialWombatPWM_18AB* sw8bPins[8][8]=
    # TODO_MANUAL_CONVERSION_INDENT: p00,p01,p02,p03,p04,p05,p06,p07
  # TODO_MANUAL_CONVERSION_INDENT: ,
    # TODO_MANUAL_CONVERSION_INDENT: p10,p11,p12,p13,p14,p15,p16,p17
  # TODO_MANUAL_CONVERSION_INDENT: ,
    # TODO_MANUAL_CONVERSION_INDENT: p20,p21,p22,p23,p24,p25,p26,p27
  # TODO_MANUAL_CONVERSION_INDENT: ,
    # TODO_MANUAL_CONVERSION_INDENT: p30,p31,p32,p33,p34,p35,p36,p37
  # TODO_MANUAL_CONVERSION_INDENT: ,
    # TODO_MANUAL_CONVERSION_INDENT: p40,p41,p42,p43,p44,p45,p46,p47
  # TODO_MANUAL_CONVERSION_INDENT: ,
    # TODO_MANUAL_CONVERSION_INDENT: p50,p51,p52,p53,p54,p55,p56,p57
  # TODO_MANUAL_CONVERSION_INDENT: ,
    # TODO_MANUAL_CONVERSION_INDENT: p60,p61,p62,p63,p64,p65,p66,p67
  # TODO_MANUAL_CONVERSION_INDENT: ,
    # TODO_MANUAL_CONVERSION_INDENT: p70,p71,p72,p73,p74,p75,p76,p77
  # TODO_MANUAL_CONVERSION_INDENT: ,



def setup():

  # Wire.begin() is handled by the selected Python interface block

  # Serial.begin() is not used in this Python example

  delay(100)
  for chip in range(0, 8):
    sw[chip].begin(Wire, 0x60 + chip)
    sw[chip].queryVersion()
    for pinOnChip in range(0, 8):
      sw8bPins[chip][pinOnChip].begin(pinOnChip,0x8000)
      sw8bPins[chip][pinOnChip].writeFrequency_Hz(chip*1000 + 100*pinOnChip)

def loop():
  pass


setup()
while True:
    loop()
