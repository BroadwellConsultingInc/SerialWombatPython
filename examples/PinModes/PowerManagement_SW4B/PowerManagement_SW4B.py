# Converted from PinModes/PowerManagement_SW4B/PowerManagement_SW4B.ino
import SerialWombat
from ArduinoFunctions import delay, delayMicroseconds, millis

import SerialWombat_interface
# >>> IMPORTANT: Set this to the configured I2C address of your Serial Wombat chip.
SERIAL_WOMBAT_ADDRESS = 0x60
sw = SerialWombat_interface.SerialWombatChipInstance(SERIAL_WOMBAT_ADDRESS)


# Interface independent code starts here:
import SerialWombatAnalogInput
import SerialWombatPWM

# ===== Arduino tab: PowerManagement_SW4B.ino =====
# This example is explained in a video tutorial at: https://youtu.be/jVkQ1YoqcpI
# sw is provided by the selected Python interface block above
pwm = SerialWombatPWM.SerialWombatPWM(sw)
pot = SerialWombatAnalogInput.SerialWombatAnalogInput(sw)
PWMPIN = 1
ANALOGPIN = 2
POTHIGHPIN = 3
def setup():
  # put your setup code here, to run once:
  # Serial.begin() is not used in this Python example
  # Wire.begin() is handled by the selected Python interface block
  delay(500)
  i2cAddress = sw.find()
  sw.begin()  # Python interface was configured above
  # Initialize the Serial Wombat library to use the primary I2C port
  # sw.registerErrorHandler(...) is Arduino-specific; Python errors are returned by library calls
  # Register an error handler that will print communication errors to Serial
  pwm.begin(PWMPIN,0x8000)
  pot.begin(ANALOGPIN)
  sw.pinMode(POTHIGHPIN,SerialWombat.ArduinoInputOutput.OUTPUT)
  delay(5000)
  # Serial.begin() is not used in this Python example
  # For debug output.
def loop():
  # put your main code here, to run repeatedly:
  sw.digitalWrite(POTHIGHPIN,0)
  # Turn off POT high-side before going to sleep.
  sw.sleep()
  delay(5000)
  sw.wake()
  sw.digitalWrite(POTHIGHPIN,1)
  # Turn on POT High side
  delay(250)
  # Give the Serial Wombat chip time to make readings
  print(pot.readVoltage_mV())
  delay(5000)

setup()
while True:
  loop()
