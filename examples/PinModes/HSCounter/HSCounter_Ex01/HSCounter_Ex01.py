# Converted from PinModes/HSCounter/HSCounter_Ex01/HSCounter_Ex01.ino
import SerialWombat
from ArduinoFunctions import delay, delayMicroseconds, millis

import SerialWombat_interface
# >>> IMPORTANT: Set this to the configured I2C address of your Serial Wombat chip.
SERIAL_WOMBAT_ADDRESS = 0x60
sw = SerialWombat_interface.SerialWombatChipInstance(SERIAL_WOMBAT_ADDRESS)


# Interface independent code starts here:
import SerialWombatHSClock
import SerialWombatHSCounter

# ===== Arduino tab: HSCounter_Ex01.ino =====
#
# This example shows how to measure the frequency and pulse count of a high speed signal
# with the High Speed Counter pin mode
#
# Only one pin on the Serial Wombat 18AB chip can be configured to this mode at a time.
#
# For this example, we will generate a high speed signal on pin 19, and
# measure it on pin 18.  These pins  need to be connected with a wire.
#
# It is suggested to use the SerialWombat18ABOscillator tuner when using
# this pin mode to improve accuracy
#
# A video demonstrating the use of the High Counter is available at:
# TODO
#
# Documentation for the SerialWombatHighCounter class is available at:
# https://broadwellconsultinginc.github.io/SerialWombatArdLib/class_serial_wombat_h_s_clock.htmll
# sw is provided by the selected Python interface block above
oscTun = SerialWombat.SerialWombat18ABOscillatorTuner(sw)
hsClock = SerialWombatHSClock.SerialWombatHSClock(sw)
hsCounter = SerialWombatHSCounter.SerialWombatHSCounter(sw)
HSCLOCK_PIN = 19  # Must be an enhanced digital capability pin.
HSCOUNTER_PIN = 18  # Must be an enhanced digital capability pin.
def setup():
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
  if sw.isSW08() and not sw.isPinModeSupported(SerialWombat.SerialWombatPinMode_t.PIN_MODE_HS_COUNTER):
    print("The required pin mode does not appear to be supported in this firmware build. Do you need to download a different firmware?")
    while 1:
      delay(100)
  # sw.registerErrorHandler(...) is Arduino-specific; Python errors are returned by library calls
  # Register an error handler that will print communication errors to Serial
  # Optional Error handling code end
  hsClock.begin(HSCLOCK_PIN, 2000000)
  # 2MHz output.  Note that only integer divisors of 32MHz are possible.  See documentation
  hsCounter.begin( HSCOUNTER_PIN)
def loop():
  delay(2000)
  oscTun.update()
  # Call this periodically to improve oscillator frequency accuracy.  See https://youtu.be/T2uBQM3s_JM
  print(hsCounter.readFrequency())

setup()
while True:
  loop()
