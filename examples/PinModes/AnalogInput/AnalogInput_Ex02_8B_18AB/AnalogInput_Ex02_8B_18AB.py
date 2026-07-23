# Converted from PinModes/AnalogInput/AnalogInput_Ex02_8B_18AB/AnalogInput_Ex02_8B_18AB.ino
import SerialWombat
from ArduinoFunctions import delay, delayMicroseconds, millis

import SerialWombat_interface
# >>> IMPORTANT: Set this to the configured I2C address of your Serial Wombat chip.
SERIAL_WOMBAT_ADDRESS = 0x60
sw = SerialWombat_interface.SerialWombatChipInstance(SERIAL_WOMBAT_ADDRESS)


# Interface independent code starts here:
import SerialWombatAnalogInput
import SerialWombatServo

# ===== Arduino tab: AnalogInput_Ex02_8B_18AB.ino =====
# sw is provided by the selected Python interface block above
swAn0 = SerialWombatAnalogInput.SerialWombatAnalogInput(sw)
swServo = SerialWombatServo.SerialWombatServo(sw)
def setup():
  # put your setup code here, to run once:
  # Wire.begin() is handled by the selected Python interface block
  # Initialize the I2C Bus on default pins
  # Serial.begin() is not used in this Python example
  delay(3000)
  print("Analog Input Example")
  sw.begin()  # Python interface was configured above
  # Scan the bus for Serial Wombat chips, and initialize the first one found
  # Optional Error handling code begin:
  if sw.isSW04():
    print("This Example is not supported on the Serial Wombat 4B chip. An 8B or 18AB chip is required.")
    while 1:
      delay(100)
  if not sw.isLatestFirmware():
    print("Firmware version mismatch. Download latest Serial Wombat Arduino Library and update Serial Wombat Firmware to latest version")
  if sw.isSW08() and not (sw.isPinModeSupported(SerialWombat.SerialWombatPinMode_t.PIN_MODE_ANALOGINPUT) and sw.isPinModeSupported(SerialWombat.SerialWombatPinMode_t.PIN_MODE_SERVO)):
    print("The required pin mode does not appear to be supported in this firmware build. Do you need to download a different firmware?")
    while 1:
      delay(100)
  # sw.registerErrorHandler(...) is Arduino-specific; Python errors are returned by library calls
  # Register an error handler that will print communication errors to Serial
  # Optional Error handling code end
  swAn0.begin(0)
  swServo.attach(1,1000,15000)
def loop():
  # put your main code here, to run repeatedly:
  pot = swAn0.readCounts()
  print(pot)
  swServo.write16bit(pot)
  delay(100)

setup()
while True:
  loop()
