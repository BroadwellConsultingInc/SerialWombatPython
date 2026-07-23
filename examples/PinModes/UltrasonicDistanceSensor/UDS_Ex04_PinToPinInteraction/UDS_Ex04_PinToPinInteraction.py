# Converted from PinModes/UltrasonicDistanceSensor/UDS_Ex04_PinToPinInteraction/UDS_Ex04_PinToPinInteraction.ino
import SerialWombat
from ArduinoFunctions import delay, delayMicroseconds, millis

import SerialWombat_interface
# >>> IMPORTANT: Set this to the configured I2C address of your Serial Wombat chip.
SERIAL_WOMBAT_ADDRESS = 0x60
sw = SerialWombat_interface.SerialWombatChipInstance(SERIAL_WOMBAT_ADDRESS)


# Interface independent code starts here:
import SerialWombatUltrasonicDistanceSensor
import SerialWombatWS2812

# ===== Arduino tab: UDS_Ex04_PinToPinInteraction.ino =====
#
# This example shows how to set up a pin-to-pin interaction within the Serial Wombat Chip using
# the Ultrasonic Distance Sensor and a strip of WS2812 LEDs. This example builds on example 2
# by adding the WS2812 strip.
#
# The LEDs will light depending on the distance measurement from the sensor.
#
# This sketch was last tested with version 2.2.2 of the firmware.
#
# An HC_SR04 sensor needs to be powered by 5V, and outputs a 5V signal.  The echo pin should be connected to one of the
# Serial Wombat 18AB chip's 5V tolerant pins (9,10,11,12, 14 and 15)
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
lightStrip = SerialWombatWS2812.SerialWombatWS2812(sw)
WS2812_PIN = 19  # Must be an enhanced performance pin: 0,1,2,3,4,7,9,10-19
NUMBER_OF_LEDS = 20
WS2812_USER_BUFFER_INDEX = 0x0000  # Set this to an index into the on-chip user buffer.  Can't overlap with area used by other pins.
def setup():
  # put your setup code here, to run once:
  # Wire.begin() is handled by the selected Python interface block
  # Initialize the I2C Bus on default pins
  # Serial.begin() is not used in this Python example
  delay(3000)
  print("Ultrasonic Distance Sensor Pin to Pin Example ")
  sw.begin()  # Python interface was configured above
  # Scan the bus for Serial Wombat chips, and initialize the first one found
  # Optional Error handling code begin:
  if not sw.isSW18():
    print("This Example is not supported on the Serial Wombat 4B or 8B chip. An 18AB chip is required.")
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
  # Echo pin is on pin 10
  # HC_SR04 driver
  distanceSensor.begin(10, SerialWombatUltrasonicDistanceSensor.HC_SR04, 11)
  # Trigger pin on pin 11.    no parameters for autoTrigger (true) and pullUp (false)
  distanceSensor.writeAveragingNumberOfSamples(100)
  # Inherited from SerialWombatAbstractProcessedInput
  lightStrip.begin(WS2812_PIN, NUMBER_OF_LEDS, WS2812_USER_BUFFER_INDEX)
  # Get the bar graph data from pin 10, the Ultrasonic Sensor
  # Off value = dim red
  # on value = blue
  # Min value 0
  lightStrip.barGraph(10, 0x00050000, 0x00000020, 0, 300)
  # Max value 300mm
lastMeasurement = 0
# In the loop we will constantly read the average value, and print it to Serial When it changes
# Note that the loop does nothing to update the WS2812 strip.  This happens completely on the
# Serial Wombat Chip.
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
