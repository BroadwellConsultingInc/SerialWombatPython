# Converted from PinModes/SPI/SPI_ex01_MCP3201_ADC/SPI_ex01_MCP3201_ADC.ino
import SerialWombat
from ArduinoFunctions import delay, delayMicroseconds, millis

import SerialWombat_interface
# >>> IMPORTANT: Set this to the configured I2C address of your Serial Wombat chip.
SERIAL_WOMBAT_ADDRESS = 0x60
sw = SerialWombat_interface.SerialWombatChipInstance(SERIAL_WOMBAT_ADDRESS)


# Interface independent code starts here:
import SerialWombatSPI

# ===== Arduino tab: SPI_ex01_MCP3201_ADC.ino =====
#   This example shows how to use the Serial Wombat SPI Pin mode to read ADC readings from a Microchip MCP3201 ADC.
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
SPI_CS_PIN = 6
def setup():
  # put your setup code here, to run once:
  # Wire.begin() is handled by the selected Python interface block
  # Initialize the I2C Bus on default pins
  # Serial.begin() is not used in this Python example
  delay(3000)
  print("SPI MCP3201 Read Example")
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
  # 255 = None - No MOSI pin
  spi.begin( SPI_CLOCK_PIN, 0, 255, SPI_MISO_PIN, SPI_CS_PIN)
def loop():
  delay(250)
  dummyData = 0
  # for 16 bit transfer
  rawdata = spi.transfer(dummyData)
  result = (((rawdata & 0x1F) << 7) + ( rawdata >>9))
  # The bits are not organized as a little-endian number.  Adjust.
  print(result)

setup()
while True:
  loop()
