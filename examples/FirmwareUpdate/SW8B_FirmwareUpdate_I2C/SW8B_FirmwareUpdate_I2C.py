# Converted from FirmwareUpdate/SW8B_FirmwareUpdate_I2C/SW8B_FirmwareUpdate_I2C.ino
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


#This file is used to update the Serial Wombat 8B chip to a desired firmware.  Firmware
#images are stored in C arrays
#
#
#This sketch will connect to a single Serial Wombat 8B chip at the address
#specified by the I2C_ADDRESS below.    Use the SerialWombatChipFinder example to scan the
#I2C bus if you're unsure of the address of your chip.
#
#Comment in one of the XXX_FIRMWARE #define's to determine which firmware to load
#
#Open a serial terminal at 115200 to monitor progress.
#
#The user is required to send a Capital Y and Enter to confirm desire to update firmware.
#In arduino this can be done at the top of the terminal window.
#
#
#--- THIS SKETCH HAS ONLY BEEN TESTED ON THE Arduino UNO, ESP8266, ESP32 and SEEDUINO XIAO AT THIS TIME ---
#
#

##define I2C_ADDRESS 0x60 // Comment me in and set your I2C address
# sw is provided by the selected interface block above

appStartAddress = 0x00000000
const

uint16_t
# #ifdef ESP8266
PROGMEM
# #endif
# #ifdef ARDUINO_AVR_UNO
PROGMEM
# #endif

# comment in one of the firmware defines below or else appimage will be undefined at compile
##define DEFAULT_FIRMWARE
##define BRUSHED_MOTOR_FIRMWARE
##define COMMUNICATIONS_FIRMWARE
##define FRONT_PANEL_FIRMWARE
##define KEYPAD_FIRMWARE
##define TM1637_FIRMWARE
##define ULTRASONIC_FIRMWARE
##define IR_FIRMWARE



# #ifndef I2C_ADDRESS
# #error I2C Address is not defined.  Comment in and set the I2C address on line 23 of this sketch.
# #endif
# #ifndef FIRMWARE_INCLUDED
# #error You must pick a firmware image to download.  Comment in one of the #defines ending in _FIRMWARE
# #endif

mismatch = False
def setup():
  # put your setup code here, to run once:
  # Wire.begin() is handled by the selected Python interface block
  # Serial.begin() is not used in this Python example
  while not Serial:


    delay(500)
    print(F("Serial Wombat SW8B I2C Firmware Update"))
    print(F("Delaying 10 seconds to allow user to open terminal..."))

    delay(10000)
    # #if (defined(ESP8266)  || defined(ARDUINO_ARCH_SAMD)  || defined(ESP32)  |defined (ARDUINO_AVR_UNO ) )
    # #else
      # TODO_MANUAL_CONVERSION_INDENT: print(F("This Sketch is currently only tested with ESP8266, ESP32, SAMD21 and Arduino Uno based boards.  Attempting to run it on other processors may result in firmware update failure."))
      # TODO_MANUAL_CONVERSION_INDENT: while True:
        # TODO_MANUAL_CONVERSION_INDENT: yield()
    # #endif

    WombatFinder()


    sw.begin()  # Python interface was configured above


    delay(1000)
    sw.queryVersion()
    while Serial.available():
      t = Serial.read()
    print("Serial Wombat Firmware version ", end="")
    print(sw.readVersion_uint32(), end="")
    print("detected.")
    if sw.isLatestFirmware():
      print(F("Firmware is already the latest version.  Update?  Send 'Y' to update"))
      i = -1
      while i == -1:
        delay(50)
        i = Serial.read()

      if i != 'Y':
        print(F("Non 'Y' character received.  Going into infinite loop.  Reset to try again"))
        while True:
          delay(50)

    if not sw.inBoot:
      print(F("Jumping to boot"))
      sw.jumpToBoot()
      print("Resetting")
      sw.hardwareReset()
      delay(2000)
    else:
      print("Skipping reset...")

    WombatFinder()

    sw.begin()  # Python interface was configured above
    address = 0

    print("Connecting to Serial Wombat chip", end="")
    found = False
    while not found:
      found = sw.queryVersion()
      print('.', end="")
      delay(200)
    print()

    print("Erasing")
    sw.eraseFlashPage(0)

    for address in range(0, 0x1000):
      page = [0] * (16)
      #   Serial.printf("Loading words starting with 0x%X  :  ", address * 4);
      for i in range(0, 16):
        # #if defined(ESP8266)
        # TODO_MANUAL_CONVERSION: page[i] = pgm_read_byte(((uint8_t*)appImage) + 4 * (i + address))
        # TODO_MANUAL_CONVERSION: page[i] += pgm_read_byte(((uint8_t*)appImage) + 4 * (i + address) + 1) << 8
        # TODO_MANUAL_CONVERSION: page[i] += ( pgm_read_byte(((uint8_t*)appImage) + 4 * (i + address) + 2)) << 16
        # TODO_MANUAL_CONVERSION: page[i] += ( pgm_read_byte(((uint8_t*)appImage) + 4 * (i + address) + 3)) << 24
        #elif defined(ARDUINO_AVR_UNO)
        page[i] = pgm_read_word(appImage[(address + i) * 2]);  # 16 bit words on UNO
        page[i] += (pgm_read_word(appImage[(address + i) * 2 + 1])) << 16

        # #else
        page[i] = appImage[(address + i) * 2]
        page[i] += ((appImage[(address + i) * 2 + 1])) << 16

        # #endif

      dirty = False
      for i in range(0, 16):
        dirty |= (page[i] != 0xFFFFFFFF)
      if dirty:
        # TODO_MANUAL_CONVERSION: sw.writeUserBuffer(0, (uint8_t*)page, 64)
        sw.writeFlashRow(address * 4 + 0x08000000)
        s = [0] * (50)
        s = ("Programming address: 0x%X") % (address)
        print(s)
        delay(10)
      else:
        s = [0] * (50)
        s = ("Skipping blank Row  0x%X") % (address)
        print(s)



    #Verify step

    print("Beginning 100% verification...")
    successes = 0
    tries = 0
    for address in range(0, 0x1000):
      page = [0] * (16)

      for i in range(0, 16):
        ++tries
        # #if defined(ESP8266)
        # TODO_MANUAL_CONVERSION: page[i] = pgm_read_byte(((uint8_t*)appImage) + 4 * (i + address))
        # TODO_MANUAL_CONVERSION: page[i] += pgm_read_byte(((uint8_t*)appImage) + 4 * (i + address) + 1) << 8
        # TODO_MANUAL_CONVERSION: page[i] += ( pgm_read_byte(((uint8_t*)appImage) + 4 * (i + address) + 2)) << 16
        # TODO_MANUAL_CONVERSION: page[i] += ( pgm_read_byte(((uint8_t*)appImage) + 4 * (i + address) + 3)) << 24
        #elif defined(ARDUINO_AVR_UNO)
        page[i] = pgm_read_word(appImage[(address + i) * 2]);  # 16 bit words on UNO
        page[i] += (pgm_read_word(appImage[(address + i) * 2 + 1])) << 16

        # #else
        page[i] = appImage[(address + i) * 2]
        page[i] += ((appImage[(address + i) * 2 + 1])) << 16


        # #endif
        readback = sw.readFlashAddress((address + i) * 4 + 0x08000000)
        if readback != page[i]:
          mismatch = True
          s = [0] * (50)
          s = ("Verify fail at address: 0x%X") % (address + i)
          print(s)
          s = ("Expected: 0x%X  Got: 0x%X") % (page[i],readback)
        else:
          ++successes


    print(successes); Serial.print(" of ");Serial.print(tries);Serial.println(" words verified", end="")
    if not mismatch:
      tx = [ 164, 4, 0, 0, 0, 0, 0, 0 ];  # Set boot flag

      sw.sendPacket(tx)
      delay(100)
      sw.hardwareReset()






  def loop():

    # put your main code here, to run repeatedly:
    print("Serial Wombat chips found:")
    print()

    print()
    print("=======================================================")
    print()
    WombatFinder()

    print()
    if mismatch:
      print("Update failed.")

    else:
      print("Update complete.  Load a new sketch such as the SerialWombatChipFinder sketch, then power cycle the Arduino and Serial Wombat chip.")
    print()
    print("Resetting or power cycling without loading a new sketch will cause the flash download to happen again.")
    print()

    delay(5000)


setup()
while True:
    loop()
