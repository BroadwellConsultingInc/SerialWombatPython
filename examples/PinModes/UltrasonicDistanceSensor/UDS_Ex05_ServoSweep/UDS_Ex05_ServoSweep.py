# Converted from PinModes/UltrasonicDistanceSensor/UDS_Ex05_ServoSweep/UDS_Ex05_ServoSweep.ino
import SerialWombat
from ArduinoFunctions import delay, delayMicroseconds, millis

import SerialWombat_interface
# >>> IMPORTANT: Set this to the configured I2C address of your Serial Wombat chip.
SERIAL_WOMBAT_ADDRESS = 0x60
sw = SerialWombat_interface.SerialWombatChipInstance(SERIAL_WOMBAT_ADDRESS)


# Interface independent code starts here:
import SerialWombatServo
import SerialWombatUltrasonicDistanceSensor

# ===== Arduino tab: UDS_Ex05_ServoSweep.ino =====
#
# This example shows how to configure a Serial Wombat 8B or 18AB to combine an HC_SR04 ultrasonic distance
# sensor with a servo to do automatic scanning of distances into a table.  This is accomplished entirely on
# the Serial Wombat Chip, greatly reducing the amount of logic necessary on the host to achieve this task.
# The host simply needs to download the table periodically to get the latest distances.
#
# The result is shown through Serial as a series of distances in mm, along with a crude bargraph of distance at each point.
#
# The table is stored in the User RAM Area.  This is a section of RAM on the Serial Wombat Chip which is independent
# of pin mode memory, and is allocated by the user.   The user must provide the index into the User RAM Area where
# the table will be stored.
#
# The user provides pin numbers for the echo, trigger, and servo pins (the servo should already be configured using
# the SerialWombatServo_18AB class (which works for both 18AB and 8B)).  The user provides the index into User RAM,
# the number of points to be taken across the arc, the amount of time to wait for servo movement from point to point
# to complete, and the amount of time to wait for the Servo to move from the final point back to the first point.
#
# The movement will often appear inconsistent during operation. This is due to the Ultrasonic distance sensor.
# The amount of time each measurement takes is proportional to the distance measurement (due to speed of sound).
# The servo will move more quickly when objects are close to the sensor than when they are further away.
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
distanceSensorServo = SerialWombatServo.SerialWombatServo_18AB(sw)
# Comment the following in for SW18AB  (you can use most pins, but be careful with 5V ones)
# #define UDS_ECHO_PIN 10 //On SW18AB this should be a 5V capable pin
# #define UDS_TRIGGER_PIN 11 //  Can be 5 or 3.3V pin
# #define SERVO_PIN 12
# Comment the following in for SW8B (Run the chip on 5V, since there's a 5V input).
# Any pin can be used for any function, but the 50k pull down on pin 0 may
# be problematic if the echo pin has a weak pull up, so suggest using 0 for
# trigger rather than Echo.
UDS_ECHO_PIN = 4  # Probably best not to use pin 0 for this one
UDS_TRIGGER_PIN = 5
SERVO_PIN = 3
TABLE_LOCATION_IN_USER_MEMORY = 0x0000
NUMBER_OF_TABLE_ENTRIES = 19  # About every 10 degrees, this is a fencepost problem, so 19 readings, not 18
SERVO_POSITION_INCREMENT = (65535 / (NUMBER_OF_TABLE_ENTRIES - 1))
DELAY_TIME_FOR_SERVO_INCREMENT_mS = 75
DELAY_TIME_FOR_SERVO_TO_RETURN_TO_0_mS = 700
ultrasonicDistanceTable = [0] * (NUMBER_OF_TABLE_ENTRIES)
def setup():
  # put your setup code here, to run once:
  # Wire.begin() is handled by the selected Python interface block
  # Initialize the I2C Bus on default pins
  # Serial.begin() is not used in this Python example
  delay(3000)
  print("Ultrasonic Distance Sensor Servo Sweep Example ")
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
  distanceSensorServo.attach(SERVO_PIN)
  # HC_SR04 driver
  distanceSensor.begin(UDS_ECHO_PIN, SerialWombatUltrasonicDistanceSensor.HC_SR04, UDS_TRIGGER_PIN)
  # no parameters for autoTrigger (true) and pullUp (false)
  distanceSensor.enableServoSweep()
  # Servo Reverse
  # Servo move delay
  # Servo return delay
  distanceSensor.configureServoSweep (SERVO_PIN, TABLE_LOCATION_IN_USER_MEMORY, NUMBER_OF_TABLE_ENTRIES, SERVO_POSITION_INCREMENT, False, DELAY_TIME_FOR_SERVO_INCREMENT_mS, DELAY_TIME_FOR_SERVO_TO_RETURN_TO_0_mS )
# In the loop we will constantly read the I2C value, and print it to Serial When it changes
def loop():
  print("\r\n\r\n\r\n\r\n", end="")
  # Table to read entries into
  # Number of entries to read
  distanceSensor.readServoSweepEntries ( ultrasonicDistanceTable, NUMBER_OF_TABLE_ENTRIES )
  for i in range(0, NUMBER_OF_TABLE_ENTRIES):
    distance = ultrasonicDistanceTable[i]
    s = "%5d " % distance
    if distance > 500:
      distance = 500
      # 500mm maximum for graph
    stars = int(distance / (500 / 50))
    # each star = 10mm
    s += "*" * stars
    print(s)
  delay(250)

setup()
while True:
  loop()
