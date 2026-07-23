# Converted from PinModes/SPI/SPI_ex03_SNx4HC595_ShiftRegister/SPI_ex03_SNx4HC595_ShiftRegister.ino
import SerialWombat
from ArduinoFunctions import delay, delayMicroseconds, millis

import SerialWombat_interface
# >>> IMPORTANT: Set this to the configured I2C address of your Serial Wombat chip.
SERIAL_WOMBAT_ADDRESS = 0x60
sw = SerialWombat_interface.SerialWombatChipInstance(SERIAL_WOMBAT_ADDRESS)


# Interface independent code starts here:
import SerialWombatSPI

# ===== Arduino tab: SPI_ex03_SNx4HC595_ShiftRegister.ino =====
#   This example shows how to use the Serial Wombat SPI Pin mode to output digital
#   signals on a SNx4HC595 shift register.
#
#   If you're considering this, I'd consider just buying more SW8B boards.  They're
#   cheap, much more versatile, and likely make your design adaptable for the future.
#
#   This will cycle through a variety of output values to show patterns on an LED array
#
#   SNxHC595 Pinout:
#                  +----\/----+
#  Qb      1  ---- |1      16| ---- VCC
#  Qc      2  ---- |2      15| ---- Qa
#  Qd      3  ---- |3      14| ---- SER (DS)  <-- Serial Wombat MOSI Pin
#  Qe      4  ---- |4      13| ---- OE        <-- GND (enable outputs)
#  Qf      5  ---- |5      12| ---- RCLK      <-- Serial Wombat CS pin
#  Qg      6  ---- |6      11| ---- SRCLK     <-- Serial Wombat SPI Clock pin
#  Qh      7  ---- |7      10| ---- SRCLR     <-- VCC (no reset)
#  GND     8  ---- |8       9| ---- Qh' (cascade out)
#                  +-----------+ *
#   This example is compatible with the Serial Wombat 18AB and 8B chips.
#
#   The calls to spi transfer on this example are compatible with other spi.transfer
#   calls using the normal Arduino SPI library.  However, calls to beginTransation()
#   and end() are unnecessary, and bit order and clock frequency are not configurable.
#
#   Video on SPI pin mode:
#
#   TODO coming soon
#
#   SerialWombatSPI pin mode documentation:
#
#   TODO
#
# sw is provided by the selected Python interface block above
spi = SerialWombatSPI.SerialWombatSPI(sw)
SPI_CLOCK_PIN = 4
SPI_MISO_PIN = 5
SPI_MOSI_PIN = 7
SPI_CS_PIN = 6
def setup():
  # put your setup code here, to run once:
  # Wire.begin() is handled by the selected Python interface block
  # Initialize the I2C Bus on default pins
  # Serial.begin() is not used in this Python example
  delay(3000)
  print("SPI SNx4HC595 Shfit Register Example")
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
outputArray = [ 0xFF, 0x55, 0xAA, 0xF0, 0x0F, 0xC3, 0x3C, 0x00, ]
outputIndex = 0
def loop():
  global outputIndex
  spi.transfer(outputArray[outputIndex])
  outputIndex += 1
  if outputIndex >= len(outputArray):
    outputIndex = 0
  delay(300)

setup()
while True:
  loop()
