# Converted from PinModes/OscillatorTuning/OscillatorTuning.ino
import SerialWombat
from ArduinoFunctions import delay, delayMicroseconds, millis

import SerialWombat_interface
# >>> IMPORTANT: Set this to the configured I2C address of your Serial Wombat chip.
SERIAL_WOMBAT_ADDRESS = 0x60
sw = SerialWombat_interface.SerialWombatChipInstance(SERIAL_WOMBAT_ADDRESS)


# Interface independent code starts here:

# ===== Arduino tab: OscillatorTuning.ino =====
#
# This example shows how to tune the Serial Wombat 18AB chip's internal FRC oscillator against
# the host's millis() function to reduce the error in the FRC from as much as +/- 1.5% at room
# temperature to less than 0.1% .
#
# This sketch runs for 1 minute to profile and display the nominal error in the FRC vs. millis()
# then begins calling the update function of SerialWombat18ABOscillatorTuner.  The system then displays
# the improvement in accurary as the oscillator is tuned.
#
# A video demonstrating the use of the SerialWombat18ABOscillatorTuner class on the Serial Wombat 18AB chip is available at:
# https://youtu.be/T2uBQM3s_JM
# Documentation for the SerialWombat18ABOscillatorTuner Arduino class is available at:
# https://broadwellconsultinginc.github.io/SerialWombatArdLib/class_serial_wombat18_a_b_oscillator_tuner.html
# sw is provided by the selected Python interface block above
millisStart = 0
framesStart = 0
nextUpdate = 0
oscTun = SerialWombat.SerialWombat18ABOscillatorTuner(sw)
def setup():
  global framesStart, millisStart, nextUpdate
  # put your setup code here, to run once:
  # Wire.begin() is handled by the selected Python interface block
  # Initialize the I2C Bus on default pins
  # Serial.begin() is not used in this Python example
  delay(3000)
  print("High Speed Counter Example")
  sw.begin()  # Python interface was configured above
  # Scan the bus for Serial Wombat chips, and initialize the first one found
  # Optional Error handling code begin:
  if not sw.isSW18():
    print("This Example is not supported on the Serial Wombat 4B or 8B chip. An 18AB chip is required.")
    while 1:
      delay(100)
  if not sw.isLatestFirmware():
    print("Firmware version mismatch. Download latest Serial Wombat Arduino Library and update Serial Wombat Firmware to latest version")
  # sw.registerErrorHandler(...) is Arduino-specific; Python errors are returned by library calls
  # Register an error handler that will print communication errors to Serial
  # Optional Error handling code end
  framesStartmsb = sw.readPublicData(SerialWombat.SerialWombatDataSource.SW_DATA_SOURCE_FRAMES_RUN_MSW)
  framesStartlsb = sw.readPublicData(SerialWombat.SerialWombatDataSource.SW_DATA_SOURCE_FRAMES_RUN_LSW)
  if framesStartmsb != sw.readPublicData(SerialWombat.SerialWombatDataSource.SW_DATA_SOURCE_FRAMES_RUN_MSW):
    framesStartlsb = sw.readPublicData(SerialWombat.SerialWombatDataSource.SW_DATA_SOURCE_FRAMES_RUN_LSW)
    framesStartmsb = sw.readPublicData(SerialWombat.SerialWombatDataSource.SW_DATA_SOURCE_FRAMES_RUN_MSW)
  framesStart = framesStartmsb <<16
  framesStart += framesStartlsb
  millisStart = millis()
  nextUpdate = millis() + 60000
  print("System will test Serial Wombat frame count for 1 minute, then start tuning algorithm, and show results every minute.")
def loop():
  global framesStart, millisStart, nextUpdate
  # put your main code here, to run repeatedly:
  m = millis()
  if m > nextUpdate:
    frameslsb = sw.readPublicData(SerialWombat.SerialWombatDataSource.SW_DATA_SOURCE_FRAMES_RUN_LSW)
    frames = sw.readPublicData(SerialWombat.SerialWombatDataSource.SW_DATA_SOURCE_FRAMES_RUN_MSW)
    if frames != sw.readPublicData(SerialWombat.SerialWombatDataSource.SW_DATA_SOURCE_FRAMES_RUN_MSW):
      frameslsb = sw.readPublicData(SerialWombat.SerialWombatDataSource.SW_DATA_SOURCE_FRAMES_RUN_LSW)
      frames = sw.readPublicData(SerialWombat.SerialWombatDataSource.SW_DATA_SOURCE_FRAMES_RUN_MSW)
    frames <<= 16
    frames += frameslsb
    print("millis elapsed: ", end="")
    print(m - millisStart, end="")
    print(" frames run: ", end="")
    print(frames-framesStart, end="")
    print(" d: ", end="")
    print((m - millisStart) - (frames-framesStart), end="")
    print(" % (+ is SW too slow): ", end="")
    print(((m - millisStart) - (frames-framesStart))/ (m - millisStart) * 100)
    nextUpdate = millis() + 60000
    framesStart = frames
    millisStart = m
  if millis() > 70000:
    oscTun.update()
    # Start tuning after the first minute.

setup()
while True:
  loop()
