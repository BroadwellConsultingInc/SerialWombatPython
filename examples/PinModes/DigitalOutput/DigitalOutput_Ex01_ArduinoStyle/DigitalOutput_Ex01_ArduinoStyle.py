# Converted from PinModes/DigitalOutput/DigitalOutput_Ex01_ArduinoStyle/DigitalOutput_Ex01_ArduinoStyle.ino
import SerialWombat
from ArduinoFunctions import delay, delayMicroseconds, millis

import SerialWombat_interface
# >>> IMPORTANT: Set this to the configured I2C address of your Serial Wombat chip.
SERIAL_WOMBAT_ADDRESS = 0x60
sw = SerialWombat_interface.SerialWombatChipInstance(SERIAL_WOMBAT_ADDRESS)


# Interface independent code starts here:

# ===== Arduino tab: DigitalOutput_Ex01_ArduinoStyle.ino =====
# There is an tutorial video to go with this example at https://youtu.be/uFLlIoolQ_M
# sw is provided by the selected Python interface block above
# Declare a Serial Wombat chip
GREEN_LED_SW_PIN = 2
def setup():
  # put your setup code here, to run once:
  # Wire.begin() is handled by the selected Python interface block
  # Initialize the I2C Bus on default pins
  # Serial.begin() is not used in this Python example
  delay(3000)
  print("Digital Output Example (Arduino Style)")
  sw.begin()  # Python interface was configured above
  # Scan the bus for Serial Wombat chips, and initialize the first one found
  # Optional Error handling code begin:
  if not sw.isLatestFirmware():
    print("Firmware version mismatch. Download latest Serial Wombat Arduino Library and update Serial Wombat Firmware to latest version")
  if not sw.isPinModeSupported(SerialWombat.SerialWombatPinMode_t.PIN_MODE_DIGITALIO):
    print("The required pin mode does not appear to be supported in this firmware build. Do you need to download a different firmware?")
    while 1:
      delay(100)
  # sw.registerErrorHandler(...) is Arduino-specific; Python errors are returned by library calls
  # Register an error handler that will print communication errors to Serial
  # Optional Error handling code end
  sw.pinMode(GREEN_LED_SW_PIN,SerialWombat.ArduinoInputOutput.OUTPUT)
def loop():
  # put your main code here, to run repeatedly:
  sw.digitalWrite(GREEN_LED_SW_PIN,1)
  delay(1000)
  sw.digitalWrite(GREEN_LED_SW_PIN,0)
  delay(1000)

setup()
while True:
  loop()
