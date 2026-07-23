# Converted from PinModes/UltrasonicDistanceSensor/UDS_Ex02_AveragedValues/UDS_Ex02_AveragedValues.ino
import SerialWombat
from ArduinoFunctions import delay, delayMicroseconds, millis

import SerialWombat_interface
# >>> IMPORTANT: Set this to the configured I2C address of your Serial Wombat chip.
SERIAL_WOMBAT_ADDRESS = 0x60
sw = SerialWombat_interface.SerialWombatChipInstance(SERIAL_WOMBAT_ADDRESS)


# Interface independent code starts here:
import SerialWombatUltrasonicDistanceSensor

# ===== Arduino tab: UDS_Ex02_AveragedValues.ino =====
#
# This example builds on Example 1.  It sets the Serial Wombat Input Processor to average 100 pulses, and return that average.
#
# This sketch was last tested with version 2.2.2 of the firmware.
#
# The Serial Wombat 8B must be loaded with the UltrasonicDistanceSensor firmware build, or other build that includes
# ultrasonic distance sensor and servo pin modes.
#
# An HC_SR04 sensor needs to be powered by 5V, and outputs a 5V signal.  The echo pin should be connected to one of the
# Serial Wombat 18AB chip's 5V tolerant pins (9,10,11,12, 14 and 15).  The trigger pin can be any pin.
#
# A Serial Wombat 8B chip should be powered by 5V to accomodate the 5V input.
#
# See this video on combining 5V SW8B's with 3.3V logic (such as ESP32):
# https://www.youtube.com/watch?v=kaUU5FH0hvc
#
#
# A video demonstrating the use of the UltrasonicDistanceSensor pin mode on the Serial Wombat 18AB chip is available at:
# https://youtu.be/Mv7zrP8mtjo
#
# Documentation for the SerialWombatUltrasonicDistanceSensor class is available at:
# https://broadwellconsultinginc.github.io/SerialWombatArdLib/class_serial_wombat_ultrasonic_distance_sensor.html
#
# For reference, the source code to the firmware (looking at this isn't required, but is interesting) is available here:
# https://github.com/BroadwellConsultingInc/SerialWombat/blob/main/SerialWombatPinModes/ultrasonicDistance.c
#
# sw is provided by the selected Python interface block above
distanceSensor = SerialWombatUltrasonicDistanceSensor.SerialWombatUltrasonicDistanceSensor(sw)
# Comment the following in for SW18AB  (you can use most pins, but be careful with 5V ones)
# #define UDS_ECHO_PIN 10 //On SW18AB this should be a 5V capable pin
# #define UDS_TRIGGER_PIN 11 //  Can be 5 or 3.3V pin
# Comment the following in for SW8B (Run the chip on 5V, since there's a 5V input).
# Any pin can be used for any function, but the 50k pull down on pin 0 may
# be problematic if the echo pin has a weak pull up, so suggest using 0 for
# trigger rather than Echo.
UDS_ECHO_PIN = 4  # Probably best not to use pin 0 for this one
UDS_TRIGGER_PIN = 5
def setup():
  # put your setup code here, to run once:
  # Wire.begin() is handled by the selected Python interface block
  # Initialize the I2C Bus on default pins
  # Serial.begin() is not used in this Python example
  delay(3000)
  print("Ultrasonic Distance Sensor Averaging Example ")
  sw.begin()  # Python interface was configured above
  # Scan the bus for Serial Wombat chips, and initialize the first one found
  # Optional Error handling code begin:
  if sw.isSW04():
    print("This Example is not supported on the Serial Wombat 4B chip. An 8B or 18AB chip is required.")
    while 1:
      delay(100)
  if not sw.isLatestFirmware():
    print("Firmware version mismatch. Download latest Serial Wombat Arduino Library and update Serial Wombat Firmware to latest version")
  if sw.isSW08() and not sw.isPinModeSupported(SerialWombat.SerialWombatPinMode_t.PIN_MODE_ULTRASONIC_DISTANCE):
    print("The required pin mode does not appear to be supported in this firmware build. Do you need to download a different firmware?")
    while 1:
      delay(100)
  # sw.registerErrorHandler(...) is Arduino-specific; Python errors are returned by library calls
  # Register an error handler that will print communication errors to Serial
  # Optional Error handling code end
  # HC_SR04 driver
  distanceSensor.begin(UDS_ECHO_PIN, SerialWombatUltrasonicDistanceSensor.HC_SR04, UDS_TRIGGER_PIN)
  # no parameters for autoTrigger (true) and pullUp (false)
  distanceSensor.writeAveragingNumberOfSamples(100)
  # Inherited from SerialWombatAbstractProcessedInput
lastMeasurement = 0
# In the loop we will constantly read the average value, and print it to Serial When it changes
def loop():
  global lastMeasurement
  newMeasurement = distanceSensor.readAverage()
  if newMeasurement != lastMeasurement:
    print(newMeasurement, end="")
    print(" mm")
    lastMeasurement = newMeasurement

setup()
while True:
  loop()
