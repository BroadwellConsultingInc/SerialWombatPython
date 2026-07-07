# Converted from PinModes/Touch/Touch_Ex02_Counter/Touch_Ex02_Counter.ino
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
#SerialWombat18CapTouch class documentation can be found here:
#https://broadwellconsultinginc.github.io/SerialWombatArdLib/class_serial_wombat18_cap_touch.html#details
#
#A demonstration video of this class can be found here:
#https://youtu.be/c4B0_DRVHs0
#
#


PENNY_PIN = 16  #Must be an Analog capable pin:  0,1,2,3,4,16,17,18,19
QUARTER_PIN = 17  #Must be an Analog capable pin:  0,1,2,3,4,16,17,18,19

# sw is provided by the selected interface block above
penny = SerialWombat18CapTouch.SerialWombat18CapTouch(sw)
quarter = SerialWombat18CapTouch.SerialWombat18CapTouch(sw)

quarterCounter = SerialWombatDebouncedInput.SerialWombatButtonCounter(quarter)
pennyCounter = SerialWombatDebouncedInput.SerialWombatButtonCounter(penny)

moneyCount = 0  #Place to keep track of total money count in pennies

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

  # Initialize the Penny sensor
  #9000 based on previous calibration of this penny on this pin with this wire using the Calibration example
  penny.begin(PENNY_PIN,9000,0)

  # Initialize the Penny sensor
  #9250 based on previous calibration of this quarter on this pin with this wire using the Calibration example
  quarter.begin(QUARTER_PIN,9250,0)

  delay(500)

  penny.makeDigital(53985,57620,1,0,0,0);  #Low and High limits based on previous calibration of this penny on this pin with this wire
  quarter.makeDigital(54349,57792,1,0,0,0);  #Low and High limits based on previous calibration of this quarter on this pin with this wire
  delay(250)

  pennyCounter.begin(moneyCount,  #moneyCount is the variable we want to increment.
  1,  #Increment by 1
  500,  #Every 500 ms
  2000,  # for 2000ms, then...
  1,  # by 1
  250,  # every 250ms
  5000,  # for 5000 ms, then
  1,  # by 1
  100);  # every 100ms

  #Initialization of the quarter Counter is the same, but incrments by 25.
  quarterCounter.begin(moneyCount, 25,500,2000,25,250,5000,25,100)

  print("Touch or hold the penny or the quarter:")



lastCount = -1  # A copy of moneyCount so we can send a Serial update on changes.
def loop():
  quarterCounter.update();  #Service the counter periodically
  pennyCounter.update();  #Serivce the counter periodically

  if lastCount != moneyCount:
    # Did the counter change the moneyCount variable?
    #Yes, the counter changed
    lastCount = moneyCount;  #Make a copy for comparison

    #Then build a string and send it.
    moneyCountStr = [0] * (20)
    moneyCountStr = ("$%ld.%02ld") % (moneyCount / 100, moneyCount%100)
    print(moneyCountStr)


setup()
while True:
    loop()
