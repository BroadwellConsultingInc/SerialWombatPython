# Converted from PinModes/FrequencyOutput/FrequencyOutput_Ex02_Song/FrequencyOutput_Ex02_Song.ino
import SerialWombat
from ArduinoFunctions import delay, delayMicroseconds, millis

import SerialWombat_interface
# >>> IMPORTANT: Set this to the configured I2C address of your Serial Wombat chip.
SERIAL_WOMBAT_ADDRESS = 0x60
sw = SerialWombat_interface.SerialWombatChipInstance(SERIAL_WOMBAT_ADDRESS)


# Interface independent code starts here:
import SerialWombatFrequencyOutput

# ===== Arduino tab: FrequencyOutput_Ex02_Song.ino =====
#
#   This example shows how to generate varying frequencies with the Serial Wombat 18AB's frequency generator pin mode.  We will play "Twinkle Twinkle Little Star"
#
#
#   A video demonstrating the use of the Frequency Generator Pin Mode is available at:
#   TODO
#
#   Documentation for the SerialWombatHighSpeedClock class is available at:
#   https://broadwellconsultinginc.github.io/SerialWombatArdLib/class_serial_wombat_h_s_clock.htmll
# sw is provided by the selected Python interface block above
freqOutput = SerialWombatFrequencyOutput.SerialWombatFrequencyOutput(sw)
oscTun = SerialWombat.SerialWombat18ABOscillatorTuner(sw)
FREQUENCY_PIN = 7  # Must be an enhanced digital capability pin.
NOTE_QUARTER = 200
NOTE_HALF = (NOTE_QUARTER * 2)
NOTE_SEPARATION = 30
NOTE_C = 523
NOTE_D = 587
NOTE_E = 659
NOTE_F = 698
NOTE_G = 784
NOTE_A = 880
# Delay between replay
song = [ NOTE_C, NOTE_QUARTER, 0, NOTE_SEPARATION, NOTE_C, NOTE_QUARTER, 0, NOTE_SEPARATION, NOTE_G, NOTE_QUARTER, 0, NOTE_SEPARATION, NOTE_G, NOTE_QUARTER, 0, NOTE_SEPARATION, NOTE_A, NOTE_QUARTER, 0, NOTE_SEPARATION, NOTE_A, NOTE_QUARTER, 0, NOTE_SEPARATION, NOTE_G, NOTE_HALF, 0, NOTE_SEPARATION, NOTE_F, NOTE_QUARTER, 0, NOTE_SEPARATION, NOTE_F, NOTE_QUARTER, 0, NOTE_SEPARATION, NOTE_E, NOTE_QUARTER, 0, NOTE_SEPARATION, NOTE_E, NOTE_QUARTER, 0, NOTE_SEPARATION, NOTE_D, NOTE_QUARTER, 0, NOTE_SEPARATION, NOTE_D, NOTE_QUARTER, 0, NOTE_SEPARATION, NOTE_C, NOTE_HALF, 0, NOTE_SEPARATION, NOTE_G, NOTE_QUARTER, 0, NOTE_SEPARATION, NOTE_G, NOTE_QUARTER, 0, NOTE_SEPARATION, NOTE_F, NOTE_QUARTER, 0, NOTE_SEPARATION, NOTE_F, NOTE_QUARTER, 0, NOTE_SEPARATION, NOTE_E, NOTE_QUARTER, 0, NOTE_SEPARATION, NOTE_E, NOTE_QUARTER, 0, NOTE_SEPARATION, NOTE_D, NOTE_HALF, 0, NOTE_SEPARATION, NOTE_G, NOTE_QUARTER, 0, NOTE_SEPARATION, NOTE_G, NOTE_QUARTER, 0, NOTE_SEPARATION, NOTE_F, NOTE_QUARTER, 0, NOTE_SEPARATION, NOTE_F, NOTE_QUARTER, 0, NOTE_SEPARATION, NOTE_E, NOTE_QUARTER, 0, NOTE_SEPARATION, NOTE_E, NOTE_QUARTER, 0, NOTE_SEPARATION, NOTE_D, NOTE_HALF, 0, NOTE_SEPARATION, NOTE_C, NOTE_QUARTER, 0, NOTE_SEPARATION, NOTE_C, NOTE_QUARTER, 0, NOTE_SEPARATION, NOTE_G, NOTE_QUARTER, 0, NOTE_SEPARATION, NOTE_G, NOTE_QUARTER, 0, NOTE_SEPARATION, NOTE_A, NOTE_QUARTER, 0, NOTE_SEPARATION, NOTE_A, NOTE_QUARTER, 0, NOTE_SEPARATION, NOTE_G, NOTE_HALF, 0, NOTE_SEPARATION, NOTE_F, NOTE_QUARTER, 0, NOTE_SEPARATION, NOTE_F, NOTE_QUARTER, 0, NOTE_SEPARATION, NOTE_E, NOTE_QUARTER, 0, NOTE_SEPARATION, NOTE_E, NOTE_QUARTER, 0, NOTE_SEPARATION, NOTE_D, NOTE_QUARTER, 0, NOTE_SEPARATION, NOTE_D, NOTE_QUARTER, 0, NOTE_SEPARATION, NOTE_C, NOTE_HALF, 0, NOTE_SEPARATION, 0, 10000, ]
NUMBER_OF_NOTES = (len(song)/4)
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
  # The maximum frequency we need to be able to generate.  Providing this parameter helps the Serial Wombat Timing Resource Manager make optimal decicisions for allocating hardware modules
  freqOutput.begin(FREQUENCY_PIN, 1000 )
  #
i = 0
nextNote_millis = 0
def loop():
  global i, nextNote_millis
  oscTun.update()
  # Call this periodically to improve oscillator frequency accuracy.  See https://youtu.be/T2uBQM3s_JM
  if millis() > nextNote_millis:
    freqOutput.writePublicData(song[i * 2])
    nextNote_millis = millis() + song[i * 2 + 1]
    i += 1
    if i >= NUMBER_OF_NOTES:
      delay(2000)
      i = 0

setup()
while True:
  loop()
