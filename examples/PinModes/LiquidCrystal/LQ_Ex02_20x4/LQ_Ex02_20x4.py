# Converted from PinModes/LiquidCrystal/LQ_Ex02_20x4/LQ_Ex02_20x4.ino
import SerialWombat
from ArduinoFunctions import delay, delayMicroseconds, millis

import SerialWombat_interface
# >>> IMPORTANT: Set this to the configured I2C address of your Serial Wombat chip.
SERIAL_WOMBAT_ADDRESS = 0x60
sw = SerialWombat_interface.SerialWombatChipInstance(SERIAL_WOMBAT_ADDRESS)


# Interface independent code starts here:
import SerialWombatLiquidCrystal
import SerialWombatQueue

# ===== Arduino tab: LQ_Ex02_20x4.ino =====
# sw is provided by the selected Python interface block above
testString = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789One Two Three Four Five Six Seven Eight Nine Ten Uno Dos Tres Quatro Cinco Seis Siete Ocho Nueve 0x01 0x02 0x03 0x04 0x05 0x06 0x07 0x08 0x09 0x0A 0x0B 0x0C 0x0D 0x0E 0x0F 0x10 0x11"
# The Quick Brown Fox Jumped over the Lazy Dog.The Early bird gets the worm.Never eat soggy waffles.Righty Tighty Lefty Loosey";
lcd0 = SerialWombatLiquidCrystal.SerialWombatLiquidCrystal(sw, 5, 4, 3, 2, 1, 0)
q = SerialWombatQueue.SerialWombatQueue(sw)
def setup():
  # put your setup code here, to run once:
  # Wire.begin() is handled by the selected Python interface block
  # Initialize the I2C Bus on default pins
  # Serial.begin() is not used in this Python example
  delay(3000)
  print("Liquid Crystal Queue Example")
  sw.begin()  # Python interface was configured above
  # Scan the bus for Serial Wombat chips, and initialize the first one found
  # Optional Error handling code begin:
  if sw.isSW04():
    print("This Example is not supported on the Serial Wombat 4B chip. An 8B or 18AB chip is required.")
    while 1:
      delay(100)
  if not sw.isLatestFirmware():
    print("Firmware version mismatch. Download latest Serial Wombat Arduino Library and update Serial Wombat Firmware to latest version")
  if sw.isSW08() and not sw.isPinModeSupported(SerialWombat.SerialWombatPinMode_t.PIN_MODE_LIQUIDCRYSTAL):
    print("The required pin mode does not appear to be supported in this firmware build. Do you need to download a different firmware?")
    while 1:
      delay(100)
  # sw.registerErrorHandler(...) is Arduino-specific; Python errors are returned by library calls
  # Register an error handler that will print communication errors to Serial
  # Optional Error handling code end
  lcd0.begin(20, 4)
  lcd0.setRowOffsets(0, 0x40, 0x14, 0x54)
  lcd0.initializeBufferCopy(8, 20)
  q.begin(0, 80, SerialWombatQueue.SerialWombatQueueType.QUEUE_TYPE_RAM_BYTE_SHIFT)
def loop():
  i = 0
  # put your main code here, to run repeatedly:
  q.write(testString[i])
  delay(250)
  i += 1
  if i > len(testString):
    i = 0

setup()
while True:
  loop()
