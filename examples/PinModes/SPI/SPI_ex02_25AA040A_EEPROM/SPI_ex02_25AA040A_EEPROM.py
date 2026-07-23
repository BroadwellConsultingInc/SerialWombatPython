# Converted from PinModes/SPI/SPI_ex02_25AA040A_EEPROM/SPI_ex02_25AA040A_EEPROM.ino
import SerialWombat
from ArduinoFunctions import delay, delayMicroseconds, millis

import SerialWombat_interface
# >>> IMPORTANT: Set this to the configured I2C address of your Serial Wombat chip.
SERIAL_WOMBAT_ADDRESS = 0x60
sw = SerialWombat_interface.SerialWombatChipInstance(SERIAL_WOMBAT_ADDRESS)


# Interface independent code starts here:
import SerialWombatSPI

# ===== Arduino tab: SPI_ex02_25AA040A_EEPROM.ino =====
#   This example shows how to use the Serial Wombat SPI Pin mode to read And write data from a Microchip 25AA040A
#   512 byte EEPROM.
#
#   This example is compatible with the Serial Wombat 18AB and 8B chips.
#
#
#   Video on SPI pin mode:
#
#   TODO coming soon
#
#   SerialWombatIRRx pin mode documentation:
#
#   TODO
#
# sw is provided by the selected Python interface block above
spi = SerialWombatSPI.SerialWombatSPI(sw)
SPI_CLOCK_PIN = 4
SPI_MISO_PIN = 5
SPI_MOSI_PIN = 7
SPI_CS_PIN = 3
def setup():
  # put your setup code here, to run once:
  # Wire.begin() is handled by the selected Python interface block
  # Initialize the I2C Bus on default pins
  # Serial.begin() is not used in this Python example
  delay(3000)
  print("SPI 25AA040A EEPROM Example")
  sw.begin()  # Python interface was configured above
  # Scan the bus for Serial Wombat chips, and initialize the first one found
  # Optional Error handling code begin:
  if sw.isSW04():
    print("This Example is not supported on the Serial Wombat 4B chip. An 8B or 18AB chip is required.")
    while 1:
      delay(100)
  if not sw.isLatestFirmware():
    print("Firmware version mismatch. Download latest Serial Wombat Arduino Library and update Serial Wombat Firmware to latest version")
  if sw.isSW08() and not (sw.isPinModeSupported(SerialWombat.SerialWombatPinMode_t.PIN_MODE_SPI) ):
    print("The required pin mode does not appear to be supported in this firmware build. Do you need to download a different firmware?")
    while 1:
      delay(100)
  # sw.registerErrorHandler(...) is Arduino-specific; Python errors are returned by library calls
  # Register an error handler that will print communication errors to Serial
  # Optional Error handling code end
  # Mode 0
  spi.begin( SPI_CLOCK_PIN, 0, SPI_MOSI_PIN, SPI_MISO_PIN, SPI_CS_PIN)
  spi.transfer(0x06)
  # Enable Writes on EEPROM.  Be sure to cast single byte constants so compiler interprets them that way.
  buf = [0x02, 0x10, 0x30, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38,0x39, 0x61, 0x62,0x63,0x64,0x65,0x66]
  # Write "0123456789ABCDEF" to addres 0x010
  spi.transfer(buf,18)
  # Transfer 18 bytes
  delay(2000)
  # Allow time for write to complete
  spi.transfer(0x06)
  # Enable Writes on EEPROM.  Be sure to cast single byte constants so compiler interprets them that way.
  buf = [0x02, 0xFF, 0xD7]
  # Write 0x D7 to addres 0x1FF
  spi.transfer(buf,3)
  # Transfer 3 bytes
  delay(10)
  # Allow time for write to complete
  spi.transfer(0x06)
  # Enable Writes on EEPROM.  Be sure to cast single byte constants so compiler interprets them that way.
  buf = [0x02, 0x00, 0x67]
  # Write 0x67 to addres 0x000
  spi.transfer(buf,3)
  # Transfer 3 bytes
readBuf = bytearray(514)
def loop():
  readBuf[0] = 0x03
  # Read command
  readBuf[1] = 0x00
  # Start at address 0x00
  spi.transfer(readBuf,514)
  for row in range(0, 32):
    r = bytearray(10)
    r = "%03X: " % (row * 16,)
    print(r, end="")
    for column in range(0, 16):
      s = bytearray(10)
      s = "%02X " % (readBuf[row * 16 + column + 2],)
      print(s, end="")
    print()
  print()
  print()
  print()
  delay(5000)

setup()
while True:
  loop()
