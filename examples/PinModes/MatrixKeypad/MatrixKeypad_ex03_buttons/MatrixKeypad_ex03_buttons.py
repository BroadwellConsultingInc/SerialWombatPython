# Converted from PinModes/MatrixKeypad/MatrixKeypad_ex03_buttons/MatrixKeypad_ex03_buttons.ino
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
import SerialWombatDebouncedInput
import SerialWombatMatrixKeypadold
import SerialWombatTM1637
tm1637Decimal16 = SerialWombatTM1637.SWTM1637Mode.tm1637Decimal16
tm1637Hex16 = SerialWombatTM1637.SWTM1637Mode.tm1637Hex16
tm1637CharArray = SerialWombatTM1637.SWTM1637Mode.tm1637CharArray
tm1637RawArray = SerialWombatTM1637.SWTM1637Mode.tm1637RawArray
tm1637Animation = SerialWombatTM1637.SWTM1637Mode.tm1637Animation

#
#This example shows how to initialize a 16 key, 8 pin 4x4 matrix keypad using the
#Serial Wombat 18AB or 8B chip's SerialWombatMatrixKeypad class.
#
#Note that firmware versions prior to 2.0.7 have a bug that may cause slow recognition of
#button presses.
#
#This example shows how to treat the matrix keypad as if it were 16 separate digital
#inputs by creating 16 instances of SerialWombatMatrixButton from a single instance of
#SerialWombatMatrixKeypad.  The SerialWombatMatrixKeypad instance scans the keys and
#the SerialWombatMatrixButton class abstracts each one into a single digital input.
#
#After initialization the SerialWombatMatrixButton class has the same interfaces and
#is conceptually interchangable with instances of SerialWombatDebouncedInput and
#digitally configured SerialWombat18CapTouch instances.
#
#This example assumes a 4x4 keypad attached with rows connected to pins 10,11,12,13
#and columns attached to pins 16,17,18,19 .  This can be changed in the keypad.begin
#statement to fit your circuit.
#
#A video demonstrating the use of the SerialWombatMatrixKeypad class on the Serial Wombat 18AB chip is available at:
#https://youtu.be/hxLda6lBWNg
#
#Documentation for the SerialWombatTM1637 Arduino class is available at:
#https://broadwellconsultinginc.github.io/SerialWombatArdLib/class_serial_wombat_w_s2812.html#details
#
#

# sw is provided by the selected interface block above
keypad = SerialWombatMatrixKeypadold.SerialWombatMatrixKeypad(sw)
button0 = SerialWombatMatrixKeypadold.SerialWombatMatrixButton(keypad,0)
button1 = SerialWombatMatrixKeypadold.SerialWombatMatrixButton(keypad,1)
button2 = SerialWombatMatrixKeypadold.SerialWombatMatrixButton(keypad,2)
button3 = SerialWombatMatrixKeypadold.SerialWombatMatrixButton(keypad,3)
button4 = SerialWombatMatrixKeypadold.SerialWombatMatrixButton(keypad,4)
button5 = SerialWombatMatrixKeypadold.SerialWombatMatrixButton(keypad,5)
button6 = SerialWombatMatrixKeypadold.SerialWombatMatrixButton(keypad,6)
button7 = SerialWombatMatrixKeypadold.SerialWombatMatrixButton(keypad,7)
button8 = SerialWombatMatrixKeypadold.SerialWombatMatrixButton(keypad,8)
button9 = SerialWombatMatrixKeypadold.SerialWombatMatrixButton(keypad,9)
button10 = SerialWombatMatrixKeypadold.SerialWombatMatrixButton(keypad,10)
button11 = SerialWombatMatrixKeypadold.SerialWombatMatrixButton(keypad,11)
button12 = SerialWombatMatrixKeypadold.SerialWombatMatrixButton(keypad,12)
button13 = SerialWombatMatrixKeypadold.SerialWombatMatrixButton(keypad,13)
button14 = SerialWombatMatrixKeypadold.SerialWombatMatrixButton(keypad,14)
button15 = SerialWombatMatrixKeypadold.SerialWombatMatrixButton(keypad,15)

def setup():
  # put your setup code here, to run once:
  # Wire.begin() is handled by the selected Python interface block

  # Serial.begin() is not used in this Python example
  delay(3000)
  print("Matrix Keypad as Individual Buttons Example")


  sw.begin()  # Python interface was configured above

  #Optional Error handling code begin:
  if sw.isSW04():
    print("This Example is not supported on the Serial Wombat 4B chip.  An 8B or 18AB chip is required.")
    while True:
      delay(100)
  if not sw.isLatestFirmware():
    print("Firmware version mismatch.  Download latest Serial Wombat Arduino Library and update Serial Wombat Firmware to latest version")
  if sw.isSW08()  and  not sw.isPinModeSupported(PIN_MODE_MATRIX_KEYPAD):
    print("The required pin mode does not appear to be supported in this firmware build.  Do you need to download a different firmware?")
    while True:
      delay(100)

  keypad.begin(10,10,11,12,13,16,17,18,19)

def loop():
  # put your main code here, to run repeatedly:

  # If any of the 16 keys is pressed, print its index number.
  # TODO_MANUAL_CONVERSION: if button0.digitalRead())Serial.print("0 ": 
    # TODO_MANUAL_CONVERSION: if button1.digitalRead())Serial.print("1 ": 
      # TODO_MANUAL_CONVERSION: if button2.digitalRead())Serial.print("2 ": 
        # TODO_MANUAL_CONVERSION: if button3.digitalRead())Serial.print("3 ": 
          # TODO_MANUAL_CONVERSION: if button4.digitalRead())Serial.print("4 ": 
            # TODO_MANUAL_CONVERSION: if button5.digitalRead())Serial.print("5 ": 
              # TODO_MANUAL_CONVERSION: if button6.digitalRead())Serial.print("6 ": 
                # TODO_MANUAL_CONVERSION: if button7.digitalRead())Serial.print("7 ": 
                  # TODO_MANUAL_CONVERSION: if button8.digitalRead())Serial.print("8 ": 
                    # TODO_MANUAL_CONVERSION: if button9.digitalRead())Serial.print("9 ": 
                      # TODO_MANUAL_CONVERSION: if button10.digitalRead())Serial.print("10 ": 
                        # TODO_MANUAL_CONVERSION: if button11.digitalRead())Serial.print("11 ": 
                          # TODO_MANUAL_CONVERSION: if button12.digitalRead())Serial.print("12 ": 
                            # TODO_MANUAL_CONVERSION: if button13.digitalRead())Serial.print("13 ": 
                              # TODO_MANUAL_CONVERSION: if button14.digitalRead())Serial.print("14 ": 
                                # TODO_MANUAL_CONVERSION: if button15.digitalRead())Serial.print("15 ": 

                                  #Print how many times the lower right key has been pressed or released
                                  print(button15.transitions);  Serial.print (" ", end="")

                                  # Print how long the lower right key has been held down (0 if not pressed)
                                  print(button15.readDurationInTrueState_mS());  Serial.print (" ", end="")

                                  print()


setup()
while True:
    loop()
