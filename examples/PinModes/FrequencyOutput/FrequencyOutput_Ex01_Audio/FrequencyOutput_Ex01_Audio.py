# Converted from PinModes/FrequencyOutput/FrequencyOutput_Ex01_Audio/FrequencyOutput_Ex01_Audio.ino
import SerialWombat
from ArduinoFunctions import delay, delayMicroseconds, millis

import SerialWombat_interface
# >>> IMPORTANT: Set this to the configured I2C address of your Serial Wombat chip.
SERIAL_WOMBAT_ADDRESS = 0x60
sw = SerialWombat_interface.SerialWombatChipInstance(SERIAL_WOMBAT_ADDRESS)


# Interface independent code starts here:
import SerialWombatFrequencyOutput

# ===== Arduino tab: FrequencyOutput_Ex01_Audio.ino =====
#
#   This example shows how to generate varying frequencies with the Serial Wombat 18AB's frequency generator pin mode.
#
#
#   A video demonstrating the use of the Frequency Output is  available at:
#   TODO
#
#   Documentation for the SerialWombatHighSpeedClock class is available at:
#   https://broadwellconsultinginc.github.io/SerialWombatArdLib/class_serial_wombat_h_s_clock.html
# sw is provided by the selected Python interface block above
freqOutput = SerialWombatFrequencyOutput.SerialWombatFrequencyOutput(sw)
oscTun = SerialWombat.SerialWombat18ABOscillatorTuner(sw)
FREQUENCY_PIN = 7
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
  if sw.isSW04():
    print("This Example is not supported on the Serial Wombat 4B chip. An 8B or 18AB chip is required.")
    while 1:
      delay(100)
  if not sw.isLatestFirmware():
    print("Firmware version mismatch. Download latest Serial Wombat Arduino Library and update Serial Wombat Firmware to latest version")
  if sw.isSW08() and not sw.isPinModeSupported(SerialWombat.SerialWombatPinMode_t.PIN_MODE_FREQUENCY_OUTPUT):
    print("The required pin mode does not appear to be supported in this firmware build. Do you need to download a different firmware?")
    while 1:
      delay(100)
  # sw.registerErrorHandler(...) is Arduino-specific; Python errors are returned by library calls
  # Register an error handler that will print communication errors to Serial
  # Optional Error handling code end
  freqOutput.begin(FREQUENCY_PIN)
  #
def loop():
  oscTun.update()
  # Call this periodically to improve oscillator frequency accuracy.  See https://youtu.be/T2uBQM3s_JM
  print("2000 Hz")
  freqOutput.writePublicData(2000)
  delay(1000)
  print("1000 Hz")
  freqOutput.writePublicData(1000)
  delay(1000)
  print("Off")
  freqOutput.writePublicData(0)
  delay(10000)

setup()
while True:
  loop()
