# Converted from PinModes/UltrasonicDistanceSensor/UDS_Ex03_ManualTriggering/UDS_Ex03_ManualTriggering.ino
import SerialWombat
from ArduinoFunctions import delay, delayMicroseconds, millis

import SerialWombat_interface
# >>> IMPORTANT: Set this to the configured I2C address of your Serial Wombat chip.
SERIAL_WOMBAT_ADDRESS = 0x60
sw = SerialWombat_interface.SerialWombatChipInstance(SERIAL_WOMBAT_ADDRESS)


# Interface independent code starts here:
import SerialWombatUltrasonicDistanceSensor

# ===== Arduino tab: UDS_Ex03_ManualTriggering.ino =====
#
# This example shows how to manually trigger ultrasonic distance sensor measurements.  This is useful if you don't want
# multiple sensors runing simultaneously as they may interfere with each other.
#
# In this example we will use 6 sensors, one for straight ahead, one for forward left, one for left, one for foward right,
# and one for reverse.
#
# The host will trigger each sensor in succession and print the name of the sensor if an object is near (less than 100mm)
#
# This sketch assumes an 18AB chip due to the number of pins required, but could be adapted to use 4 sensors on a Serial Wombat 8B
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
# sw is provided by the selected Python interface block above
rearSensor = SerialWombatUltrasonicDistanceSensor.SerialWombatUltrasonicDistanceSensor(sw)
leftSensor = SerialWombatUltrasonicDistanceSensor.SerialWombatUltrasonicDistanceSensor(sw)
flSensor = SerialWombatUltrasonicDistanceSensor.SerialWombatUltrasonicDistanceSensor(sw)
frontSensor = SerialWombatUltrasonicDistanceSensor.SerialWombatUltrasonicDistanceSensor(sw)
frSensor = SerialWombatUltrasonicDistanceSensor.SerialWombatUltrasonicDistanceSensor(sw)
rightSensor = SerialWombatUltrasonicDistanceSensor.SerialWombatUltrasonicDistanceSensor(sw)
def setup():
  # put your setup code here, to run once:
  # Wire.begin() is handled by the selected Python interface block
  # Initialize the I2C Bus on default pins
  # Serial.begin() is not used in this Python example
  delay(3000)
  print("Ultrasonic Distance Sensor Manual Triggering Example ")
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
  # Initialize all the sensors without autotrigger
  # Echo pin is on pin 10
  # HC_SR04 driver
  # Trigger pin on pin 11.
  leftSensor.begin(10, SerialWombatUltrasonicDistanceSensor.HC_SR04, 16, False)
  # Echo pin is on pin 11
  # HC_SR04 driver
  # Trigger pin on pin 17.
  # no Autotrigger; no pull-up parameters
  flSensor.begin(11, SerialWombatUltrasonicDistanceSensor.HC_SR04, 17, False)
  # Echo pin is on pin 12
  # HC_SR04 driver
  # Trigger pin on pin 18.
  # no Autotrigger; no pull-up parameters
  frontSensor.begin(12, SerialWombatUltrasonicDistanceSensor.HC_SR04, 18, False)
  # Echo pin is on pin 14
  # HC_SR04 driver
  # Trigger pin on pin 13.
  # no Autotrigger; no pull-up parameters
  flSensor.begin(14, SerialWombatUltrasonicDistanceSensor.HC_SR04, 13, False)
  # Echo pin is on pin 14
  # HC_SR04 driver
  # Trigger pin on pin 19.
  # no Autotrigger; no pull-up parameters
  rightSensor.begin(15, SerialWombatUltrasonicDistanceSensor.HC_SR04, 19, False)
  # no Autotrigger; no pull-up parameters
  DETECTION_DISTANCE_MM = 100
MEASUREMENT_TIME_mS = 50
# In the loop we will constantly read the average value, and print it to Serial When it changes
def loop():
  leftSensor.manualTrigger()
  delay(MEASUREMENT_TIME_mS)
  # Allow time for measurement
  if leftSensor.readPublicData() < DETECTION_DISTANCE_MM:
    print("OBJECT LEFT ", end="")
  flSensor.manualTrigger()
  delay(MEASUREMENT_TIME_mS)
  # Allow time for measurement
  if flSensor.readPublicData() < DETECTION_DISTANCE_MM:
    print('OBJECT FRONTLEFT ')
  frontSensor.manualTrigger()
  delay(MEASUREMENT_TIME_mS)
  # Allow time for measurement
  if frontSensor.readPublicData() < DETECTION_DISTANCE_MM:
    print('OBJECT FRONT ')
  frSensor.manualTrigger()
  delay(MEASUREMENT_TIME_mS)
  # Allow time for measurement
  if frSensor.readPublicData() < DETECTION_DISTANCE_MM:
    print('OBJECT FRONTRIGHT ')
  rightSensor.manualTrigger()
  delay(MEASUREMENT_TIME_mS)
  # Allow time for measurement
  if rightSensor.readPublicData() < DETECTION_DISTANCE_MM:
    print('OBJECT RIGHT ')
  rearSensor.manualTrigger()
  delay(MEASUREMENT_TIME_mS)
  # Allow time for measurement
  if rearSensor.readPublicData() < DETECTION_DISTANCE_MM:
    print('OBJECT REAR ')

setup()
while True:
  loop()
