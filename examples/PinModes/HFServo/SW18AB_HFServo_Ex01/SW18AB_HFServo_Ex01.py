# Converted from PinModes/HFServo/SW18AB_HFServo_Ex01/SW18AB_HFServo_Ex01.ino
import SerialWombat
from ArduinoFunctions import delay, delayMicroseconds, millis

import SerialWombat_interface
# >>> IMPORTANT: Set this to the configured I2C address of your Serial Wombat chip.
SERIAL_WOMBAT_ADDRESS = 0x6B
sw = SerialWombat_interface.SerialWombatChipInstance(SERIAL_WOMBAT_ADDRESS)


# Interface independent code starts here:
import SerialWombatServo

# ===== Arduino tab: SW18AB_HFServo_Ex01.ino =====
# sw is provided by the selected Python interface block above
BoringNormalServo = SerialWombatServo.SerialWombatServo(sw)
ExcitingHighFrequencyServo = SerialWombatServo.SerialWombatHighFrequencyServo(sw)
def setup():
  # put your setup code here, to run once:
  # Wire.begin() is handled by the selected Python interface block
  # Initialize the I2C Bus on default pins
  # Serial.begin() is not used in this Python example
  delay(3000)
  print("High Speed Servo Example")
  sw.begin()  # Python interface was configured above
  # Scan the bus for Serial Wombat chips, and initialize the first one found
  # Optional Error handling code begin:
  if not sw.isSW18():
    print("This Example is not supported on the Serial Wombat 4B or 8B chip. An 18AB chip is required.")
    while 1:
      delay(100)
  if not sw.isLatestFirmware():
    print("Firmware version mismatch. Download latest Serial Wombat Arduino Library and update Serial Wombat Firmware to latest version")
  if sw.isSW08() and not sw.isPinModeSupported(SerialWombat.SerialWombatPinMode_t.PIN_MODE_HS_SERVO):
    print("The required pin mode does not appear to be supported in this firmware build. Do you need to download a different firmware?")
    while 1:
      delay(100)
  # sw.registerErrorHandler(...) is Arduino-specific; Python errors are returned by library calls
  # Register an error handler that will print communication errors to Serial
  # Optional Error handling code end
  ExcitingHighFrequencyServo.attach(19,500,1000)
  ExcitingHighFrequencyServo.writeFrequency_Hz(560)
  BoringNormalServo.attach(18)
position = 0
def loop():
  global position
  # put your main code here, to run repeatedly:
  position += 1000
  ExcitingHighFrequencyServo.write16bit(position)
  BoringNormalServo.write16bit(position)
  delay(50)

setup()
while True:
  loop()
