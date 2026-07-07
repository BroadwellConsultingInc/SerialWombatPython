# Converted from _SerialWombatChipFinder/_SerialWombatChipFinder.ino
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


# TODO_MANUAL_CONVERSION: pinModeArray = [
"DIGITAL_IO",
"CONTROLLED",
"ANALOGINPUT",
"SERVO",
"THROUGHPUT_CONSUMER",
"QUADRATURE_ENC",
"HBRIDGE",
"WATCHDOG",
"PROTECTEDOUTPUT",
"COUNTER",
"DEBOUNCE",
"TM1637",
"WS2812",
"SW_UART",
"INPUT_PROCESSOR",
"MATRIX_KEYPAD",
"PWM",
"UART0_TXRX",
"PULSE_TIMER",
"DMA_PULSE_OUTPUT",
"ANALOG_THROUGHPUT",
"FRAME_TIMER",
"TOUCH",
"UART1_TXRX",
"RESISTANCE_INPUT",
"PULSE_ON_CHANGE",
"HF_SERVO",
"ULTRASONIC_DISTANCE",
"LIQUID_CRYSTAL",
"HS_CLOCK",
"HS_COUNTER",
"VGA",
"PS2_KEYBOARD",
"I2C_CONTROLLER",
"QUEUED_PULSE_OUTPUT",
"MAX7219MATRIX",
"FREQUENCY_OUTPUT",
"IR_RX",
"IR_TX",
"RC_PPM",  # 39
"BLINK",  #40
"SPI",  #41


# A video tutorial on this example is available at:
# sw is provided by the selected interface block above

def setup():
  # put your setup code here, to run once:
  # Wire.begin() is handled by the selected Python interface block
  # Serial.begin() is not used in this Python example
  while not Serial:
    delay(200)

    print("Serial Wombat chip Finder")
    print()

    print()
    print("Special Thanks to SW8B Kickstarter Backers Joshua Sefchek and Joshua De Yonge")
    print("=======================================================")
    print()



  def loop():
    # put your main code here, to run repeatedly:
    for i2cAddress in range(0x0E, (0x77) + 1):
      # Scan through all valid addresses
      # Wire.begin() is handled by the selected Python interface block
      error = Wire.endTransmission()


      if error == 0:
        #Got an Ack. Does it behave like a Serial Wombat Chip?
        print("I2C Device found at address 0x", end="")
        print(hex(i2cAddress))
        sw.begin()  # Python interface was configured above
        if sw.queryVersion():
          # Does the response to a version query look reasonable?
          #Yes
          print("Serial Wombat chip Found.")
          if sw.inBoot:
            print("Serial Wombat chip is in boot mode.")
          print("Model: ", end="")
          # TODO_MANUAL_CONVERSION: print((char*)sw.model)
          if sw.inBoot:
            print("Boot ", end="")
          print("FW Version: ", end="")
          # TODO_MANUAL_CONVERSION: print((char*)sw.fwVersion)


          print("UniqueID: ", end="")
          for i in range(0, sw.uniqueIdentifierLength):
            st = [0] * (5)
            st = ("%X ") % (sw.uniqueIdentifier[i])
            print(st, end="")
          print()

          print("Microcontroller DeviceId: ", end="")
          print(sw.deviceIdentifier)

          print("Microcontroller DeviceRevision: ", end="")
          print(sw.deviceRevision)
          print("Source voltage (mV):  ", end="")
          print(sw.readSupplyVoltage_mV())

          if sw.isSW18()  or  sw.isSW08():
            print("Supported Pin Modes: ")
            for pinModeNumber in range(0, 256):
              tx = [201, 1, pinModeNumber, 0x55, 0x55, 0x55, 0x55, 0x55]
              returnVal = sw.sendPacket(tx)
              # TODO_MANUAL_CONVERSION: return Val *= -1
              if returnVal == SW_ERROR_PIN_CONFIG_WRONG_ORDER  or  returnVal == SW_ERROR_INVALID_PIN_COMMAND:

                if pinModeNumber <= 41:
                  pass
                  # TODO_MANUAL_CONVERSION: print(const __FlashStringHelper *)(pinModeArray[pinModeNumber][0], end="")
                print(" ("); Serial.print(pinModeNumber);  Serial.println(")", end="")


          if sw.isSW18():
            print()
            print("Low Accuracy Temperature (deg C):  ", end="")
            temperature = sw.readTemperature_100thsDegC()
            print(temperature / 100, end="")
            print(".", end="")
            print(temperature % 100)

            print("Birthday: ", end="")
            print(sw.readBirthday())
            brand = [0] * (33)
            sw.readBrand(brand)
            print("Brand: ", end="")
            print(brand)


        else:
          #No
          print("Device did not respond properly to Serial Wombat version information inquiry")
        print()
        print()
    delay(10000);  # Wait 10 seconds and do it again.
    print("Serial Wombat chip Finder")
    print("=======================================================")
    print()


setup()
while True:
    loop()
