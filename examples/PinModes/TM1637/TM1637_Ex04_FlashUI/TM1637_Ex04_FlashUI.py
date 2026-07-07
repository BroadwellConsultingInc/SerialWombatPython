# Converted from PinModes/TM1637/TM1637_Ex04_FlashUI/TM1637_Ex04_FlashUI.ino
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
import SerialWombatTM1637
tm1637Decimal16 = SerialWombatTM1637.SWTM1637Mode.tm1637Decimal16
tm1637Hex16 = SerialWombatTM1637.SWTM1637Mode.tm1637Hex16
tm1637CharArray = SerialWombatTM1637.SWTM1637Mode.tm1637CharArray
tm1637RawArray = SerialWombatTM1637.SWTM1637Mode.tm1637RawArray
tm1637Animation = SerialWombatTM1637.SWTM1637Mode.tm1637Animation


PENNY_PIN = 16  #Must be an Analog capable pin:  0,1,2,3,4,16,17,18,19
QUARTER_PIN = 17  #Must be an Analog capable pin:  0,1,2,3,4,16,17,18,19


#
#This example shows how to configure two Serial Wombat 18AB pins to Touch input and use the
#SerialWombat18CapTouchCounter class to implement a two touch sensor interface to increment
#a counter at various speeds by two different increments.
#
#The example was created using a Serial Wombat 18AB chip in I2C mode with a Node MCU clone Arduino
#and a penny and quarter both covered with electrial tape wired to pins WP16 and WP17.
#
#When the penny is touched briefly the total will increment by 1 cent.  When the quarter is touched
#the total will increment by 25 cents.  If a finger is held on them then they will increment slowly, then
#more quickly, then very quickly.  This type of interface could be easily integrated into a complete solution
#for user configuration of parameters.
#
#A video demonstrating the use of the TM1637 pin mode on the Serial Wombat 18AB chip is available at:
#https://youtu.be/AwW12n6o_T0
#
#Documentation for the SerialWombatTM1637 Arduino class is available at:
#https://broadwellconsultinginc.github.io/SerialWombatArdLib/class_serial_wombat_t_m1637.html#details
#


# sw is provided by the selected interface block above
penny = SerialWombat18CapTouch.SerialWombat18CapTouch(sw)
quarter = SerialWombat18CapTouch.SerialWombat18CapTouch(sw)
myDisplay = SerialWombatTM1637.SerialWombatTM1637(sw)
quarterCounter = SerialWombatDebouncedInput.SerialWombatButtonCounter(quarter)



digitChange = 0
displayString = "000000"
currentDigit = 6  # 6 means none, 0-5 are the displayed digits

def setup():
  # put your setup code here, to run once:
  # Wire.begin() is handled by the selected Python interface block

  # Serial.begin() is not used in this Python example
  delay(3000)
  print("TM1637 Public Data Display Example")


  sw.begin()  # Python interface was configured above

  #Optional Error handling code begin:
  if sw.isSW04():
    print("This Example is not supported on the Serial Wombat 4B chip.  An 8B or 18AB chip is required.")
    while True:
      delay(100)
  if not sw.isLatestFirmware():
    print("Firmware version mismatch.  Download latest Serial Wombat Arduino Library and update Serial Wombat Firmware to latest version")
  if sw.isSW08()  and  not sw.isPinModeSupported(PIN_MODE_TM1637):
    print("The required pin mode does not appear to be supported in this firmware build.  Do you need to download a different firmware?")
    while True:
      delay(100)
  sw.registerErrorHandler(SerialWombatSerialErrorHandlerBrief);  #Register an error handler that will print communication errors to Serial
  #Optional Error handling code end


  # Initialize the Penny sensor
  #9000 based on previous calibration of this penny on this pin with this wire using the Calibration example
  penny.begin(PENNY_PIN, 9000, 0)

  # Initialize the Penny sensor
  #9250 based on previous calibration of this quarter on this pin with this wire using the Calibration example
  quarter.begin(QUARTER_PIN, 9250, 0)

  delay(500)

  penny.makeDigital(53985, 57620, 1, 0, 0, 0);  #Low and High limits based on previous calibration of this penny on this pin with this wire
  quarter.makeDigital(54349, 57792, 1, 0, 0, 0);  #Low and High limits based on previous calibration of this quarter on this pin with this wire
  delay(250)

  quarterCounter.begin(digitChange,
  1,  #Increment by 1
  500,  #Every 500 ms
  2000,  # for 2000ms, then...
  1,  # by 1
  250,  # every 250ms
  5000,  # for 5000 ms, then
  1,  # by 1
  100);  # every 100ms

  myDisplay.begin(19,  #Clk Pin
  18,  # Data Pin
  6,  # Number of digits
  tm1637CharArray,  # Mode enumeration
  0x55,  # Source pin Not used in tm1637CharArray mode
  4);  # Brightness
  myDisplay.writeDigitOrder(2, 1, 0, 5, 4, 3)
  myDisplay.writeArray(displayString)





def loop():


  if penny.readTransitionsState()  and  penny.transitions > 0:
    # The penny was touched.  Move to next digit
    nextDigit()

  quarterCounter.update()

  if currentDigit < 6  and  digitChange != 0:
    displayString[currentDigit] += digitChange
    if displayString[currentDigit] > 'z':
      displayString[currentDigit] = ' '

    if displayString[currentDigit] < ' ':
      displayString[currentDigit] = 'z'

    digitChange = 0
    myDisplay.writeArray(displayString)


def nextDigit():
  digitChange = 0
  ++currentDigit
  if currentDigit > 6:
    currentDigit = 0

  # TODO_MANUAL_CONVERSION: switch (currentDigit) {
    # TODO_MANUAL_CONVERSION: case 0:
      # TODO_MANUAL_CONVERSION_INDENT: case 1:
        # TODO_MANUAL_CONVERSION_INDENT: case 2:
          # TODO_MANUAL_CONVERSION_INDENT: case 3:
            # TODO_MANUAL_CONVERSION_INDENT: case 4:
              # TODO_MANUAL_CONVERSION_INDENT: case 5:
                  # TODO_MANUAL_CONVERSION_INDENT: myDisplay.writeBlinkBitmap(0x01 << currentDigit);  # Update which digit blinks

                # TODO_MANUAL_CONVERSION_INDENT: break

                # TODO_MANUAL_CONVERSION_INDENT: case 6:
                    # TODO_MANUAL_CONVERSION_INDENT: myDisplay.writeBlinkBitmap(0);  # Turn off blinking.
                  # TODO_MANUAL_CONVERSION_INDENT: break

                  # TODO_MANUAL_CONVERSION_INDENT: default:
                      # TODO_MANUAL_CONVERSION_INDENT: currentDigit = 6
                      # TODO_MANUAL_CONVERSION_INDENT: myDisplay.writeBlinkBitmap(0);  # Turn off blinking.
                    # TODO_MANUAL_CONVERSION_INDENT: break


                  # TODO_MANUAL_CONVERSION_INDENT: return 0


setup()
while True:
    loop()
