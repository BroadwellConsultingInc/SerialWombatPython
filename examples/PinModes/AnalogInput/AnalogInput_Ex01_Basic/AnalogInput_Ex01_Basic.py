# Converted from PinModes/AnalogInput/AnalogInput_Ex01_Basic/AnalogInput_Ex01_Basic.ino
import SerialWombat
from ArduinoFunctions import delay, delayMicroseconds, millis

import SerialWombat_interface
# >>> IMPORTANT: Set this to the configured I2C address of your Serial Wombat chip.
SERIAL_WOMBAT_ADDRESS = 0x60
sw = SerialWombat_interface.SerialWombatChipInstance(SERIAL_WOMBAT_ADDRESS)


# Interface independent code starts here:
import SerialWombatAnalogInput

# ===== Arduino tab: AnalogInput_Ex01_Basic.ino =====
# sw is provided by the selected Python interface block above
# Declare a Serial Wombat
leftPot = SerialWombatAnalogInput.SerialWombatAnalogInput(sw)
# 5k linear Pot
rightPot = SerialWombatAnalogInput.SerialWombatAnalogInput(sw)
# 5k linear Pot
temperatureSensor = SerialWombatAnalogInput.SerialWombatAnalogInput(sw)
# This example is explained in a video tutorial at: https://youtu.be/_EKlrEVaEhg
LEFT_POT_PIN = 2
RIGHT_POT_PIN = 1
TEMPERATURE_SENSOR_PIN = 0  # Set this pin to 3 if using SW4B, as 0 doesn't have Analog
def setup():
  # put your setup code here, to run once:
  # Wire.begin() is handled by the selected Python interface block
  # Initialize the I2C Bus on default pins
  # Serial.begin() is not used in this Python example
  delay(3000)
  print("1Hz Blink Example")
  sw.begin()  # Python interface was configured above
  # Scan the bus for Serial Wombat chips, and initialize the first one found
  # Optional Error handling code begin:
  if not sw.isLatestFirmware():
    print("Firmware version mismatch. Download latest Serial Wombat Arduino Library and update Serial Wombat Firmware to latest version")
  if sw.isSW08() and not sw.isPinModeSupported(SerialWombat.SerialWombatPinMode_t.PIN_MODE_ANALOGINPUT):
    print("The required pin mode does not appear to be supported in this firmware build. Do you need to download a different firmware?")
    while 1:
      delay(100)
  # sw.registerErrorHandler(...) is Arduino-specific; Python errors are returned by library calls
  # Register an error handler that will print communication errors to Serial
  # Optional Error handling code end
  leftPot.begin(LEFT_POT_PIN)
  rightPot.begin(RIGHT_POT_PIN)
  temperatureSensor.begin(TEMPERATURE_SENSOR_PIN,64,65417)
  # average 64 samples, .5 Hz Low Pass filter.
def loop():
  print("Source V: ", end="")
  supplyVoltage = sw.readSupplyVoltage_mV()
  print(supplyVoltage, end="")
  print("mV Left Pot: ", end="")
  print(leftPot.readCounts(), end="")
  print(" ", end="")
  leftVoltage = leftPot.readVoltage_mV()
  print(leftVoltage, end="")
  print("mV Right Pot:", end="")
  print(rightPot.readCounts(), end="")
  print(" ", end="")
  rightVoltage = rightPot.readVoltage_mV()
  print(rightVoltage, end="")
  print("mV T:", end="")
  print(temperatureSensor.readCounts(), end="")
  print(" ", end="")
  print(temperatureSensor.readVoltage_mV(), end="")
  print("mV ", end="")
  tempSensor_mV = temperatureSensor.readAveraged_mV()
  # See datasheet for TMP36 Temperature sensor for conversion
  temperature = (tempSensor_mV - 750) / 10.0 + 25
  print(temperature, end="")
  print(" deg C ", end="")
  print()
  delay(200)

setup()
while True:
  loop()
