# Converted from PinModes/UltrasonicDistanceSensor/UDS_Ex05_ServoSweep/UDS_Ex05_ServoSweep.ino
import SerialWombat
from ArduinoFunctions import delay, delayMicroseconds, millis

# Import constants from the SerialWombat module so names match the Arduino examples.
for _name in dir(SerialWombat.SerialWombatPinMode_t):
    if _name.startswith("PIN_MODE_"):
        globals()[_name] = getattr(SerialWombat.SerialWombatPinMode_t, _name)
for _name in dir(SerialWombat.SerialWombatDataSource):
    if _name.startswith("SW_DATA_"):
        globals()[_name] = getattr(SerialWombat.SerialWombatDataSource, _name)
PERIOD_1mS = 0; PERIOD_2mS = 1; PERIOD_4mS = 2; PERIOD_8mS = 3; PERIOD_16mS = 4; PERIOD_32mS = 5; PERIOD_64mS = 6; PERIOD_128mS = 7; PERIOD_256mS = 8; PERIOD_512mS = 9; PERIOD_1024mS = 10
HC_SR04 = 0
RAW = 0; AVERAGE = 1; FILTERED = 2; MINIMUM = 3; MAXIMUM = 4
DATACOUNT = 2; ADDRESS = 3; COMMAND = 4

#Comment these lines in if you're connecting directly to a Serial Wombat Chip's UART through cPython serial Module
#Change the parameter of SerialWombatChip_cpy_serial to match the name of your Serial port
#import SerialWombat_cpy_serial
#sw = SerialWombat_cpy_serial.SerialWombatChip_cpy_serial("COM25")

#Comment these lines in if you're connecting to a Serial Wombat Chip's I2C port using cPython smbus2
#Change busNumber and swI2Caddress to match your configuration
#import SerialWombat_smbus2_i2c
#busNumber = 1
#swI2Caddress = 0x6B
#sw = SerialWombat_smbus2_i2c.SerialWombatChip_smbus2_i2c(busNumber, swI2Caddress)

#Comment these lines in if you're connecting to a Serial Wombat Chip's I2C port using CircuitPython's I2C interface
#Change sclPin, sdaPin, and swI2Caddress to match your configuration
#import board
#import busio
#import SerialWombat_cp_i2c
#swI2Caddress = 0x6B
#i2c = busio.I2C(board.SCL, board.SDA)
#sw = SerialWombat_cp_i2c.SerialWombatChip_cp_i2c(i2c, swI2Caddress)

#Comment these lines in if you're connecting to a Serial Wombat Chip's I2C port using Micropython's I2C interface
#Change the values for sclPin, sdaPin, and swI2Caddress to match your configuration
#import machine
#import SerialWombat_mp_i2c
#sclPin = 22
#sdaPin = 21
#swI2Caddress = 0x6B
#i2c = machine.I2C(0,
#            scl=machine.Pin(sclPin),
#            sda=machine.Pin(sdaPin),
#            freq=100000,timeout = 50000)
#sw = SerialWombat_mp_i2c.SerialWombatChip_mp_i2c(i2c,swI2Caddress)
#sw.address = swI2Caddress

#Comment these lines in if you're connecting to a Serial Wombat Chip's UART port using Micropython's UART interface
#Change the values for UARTnum, txPin, and rxPin to match your configuration
import machine
import SerialWombat_mp_UART
txPin = 12
rxPin = 14
UARTnum = 2
uart = machine.UART(UARTnum, baudrate=115200, tx=txPin, rx=rxPin)
sw = SerialWombat_mp_UART.SerialWombatChipUART(uart)

#Interface independent code starts here:
import SerialWombatServo
import SerialWombatUltrasonicDistanceSensor

#
#This example shows how to configure a Serial Wombat 8B or 18AB to combine an HC_SR04 ultrasonic distance
#sensor with a servo to do automatic scanning of distances into a table.  This is accomplished entirely on
#the Serial Wombat Chip, greatly reducing the amount of logic necessary on the host to achieve this task.
#The host simply needs to download the table periodically to get the latest distances.
#
#The result is shown through Serial as a series of distances in mm, along with a crude bargraph of distance at each point.
#
#The table is stored in the User RAM Area.  This is a section of RAM on the Serial Wombat Chip which is independent
#of pin mode memory, and is allocated by the user.   The user must provide the index into the User RAM Area where
#the table will be stored.
#
#The user provides pin numbers for the echo, trigger, and servo pins (the servo should already be configured using
#the SerialWombatServo_18AB class (which works for both 18AB and 8B)).  The user provides the index into User RAM,
#the number of points to be taken across the arc, the amount of time to wait for servo movement from point to point
#to complete, and the amount of time to wait for the Servo to move from the final point back to the first point.
#
#The movement will often appear inconsistent during operation. This is due to the Ultrasonic distance sensor.
#The amount of time each measurement takes is proportional to the distance measurement (due to speed of sound).
#The servo will move more quickly when objects are close to the sensor than when they are further away.
#
#This sketch was last tested with version 2.2.2 of the firmware.
#
#The Serial Wombat 8B must be loaded with the UltrasonicDistanceSensor firmware build, or other build that includes
#ultrasonic distance sensor and servo pin modes.
#
#An HC_SR04 sensor needs to be powered by 5V, and outputs a 5V signal.  The echo pin should be connected to one of the
#Serial Wombat 18AB chip's 5V tolerant pins (9,10,11,12, 14 and 15).  The trigger pin can be any pin.
#
#A Serial Wombat 8B chip should be powered by 5V to accomodate the 5V input.
#
#See this video on combining 5V SW8B's with 3.3V logic (such as ESP32):
#https://www.youtube.com/watch?v=kaUU5FH0hvc
#
#
#A video demonstrating the use of the UltrasonicDistanceSensor pin mode on the Serial Wombat 18AB chip is available at:
#https://youtu.be/Mv7zrP8mtjo
#
#Documentation for the SerialWombatUltrasonicDistanceSensor class is available at:
#https://broadwellconsultinginc.github.io/SerialWombatArdLib/class_serial_wombat_ultrasonic_distance_sensor.html
#
#For reference, the source code to the firmware (looking at this isn't required, but is interesting) is available here:
#https://github.com/BroadwellConsultingInc/SerialWombat/blob/main/SerialWombatPinModes/ultrasonicDistance.c
#
#

# sw is provided by the selected interface block above
distanceSensor = SerialWombatUltrasonicDistanceSensor.SerialWombatUltrasonicDistanceSensor(sw)
distanceSensorServo = SerialWombatServo.SerialWombatServo_18AB(sw)

#Comment the following in for SW18AB  (you can use most pins, but be careful with 5V ones)

##define UDS_ECHO_PIN 10 //On SW18AB this should be a 5V capable pin
##define UDS_TRIGGER_PIN 11 //  Can be 5 or 3.3V pin
##define SERVO_PIN 12

#Comment the following in for SW8B (Run the chip on 5V, since there's a 5V input).
# Any pin can be used for any function, but the 50k pull down on pin 0 may
# be problematic if the echo pin has a weak pull up, so suggest using 0 for
# trigger rather than Echo.

UDS_ECHO_PIN = 4  # Probably best not to use pin 0 for this one
UDS_TRIGGER_PIN = 5  #
SERVO_PIN = 3

TABLE_LOCATION_IN_USER_MEMORY = 0x0000
NUMBER_OF_TABLE_ENTRIES = 19  # About every 10 degrees, this is a fencepost problem, so 19 readings, not 18
SERVO_POSITION_INCREMENT = 65535 / (NUMBER_OF_TABLE_ENTRIES - 1)
DELAY_TIME_FOR_SERVO_INCREMENT_mS = 75
DELAY_TIME_FOR_SERVO_TO_RETURN_TO_0_mS = 700

ultrasonicDistanceTable = [0] * (NUMBER_OF_TABLE_ENTRIES)
def setup():
  # put your setup code here, to run once:
  # Wire.begin() is handled by the selected Python interface block

  # Serial.begin() is not used in this Python example
  delay(3000)
  print("Ultrasonic Distance Sensor Servo Sweep Example ")


  sw.begin()  # Python interface was configured above

  #Optional Error handling code begin:
  if sw.isSW04():
    print("This Example is not supported on the Serial Wombat 4B chip.  An 8B or 18AB chip is required.")
    while True:
      delay(100)
  if not sw.isLatestFirmware():
    print("Firmware version mismatch.  Download latest Serial Wombat Arduino Library and update Serial Wombat Firmware to latest version")
  if sw.isSW08()  and  not sw.isPinModeSupported(PIN_MODE_ULTRASONIC_DISTANCE):
    print("The required pin mode does not appear to be supported in this firmware build.  Do you need to download a different firmware?")
    while True:
      delay(100)
  sw.registerErrorHandler(SerialWombatSerialErrorHandlerBrief);  #Register an error handler that will print communication errors to Serial
  #Optional Error handling code end
  distanceSensorServo.attach(SERVO_PIN)
  distanceSensor.begin(UDS_ECHO_PIN,
  HC_SR04,  # HC_SR04 driver
  UDS_TRIGGER_PIN);  #    no parameters for autoTrigger (True) and pullUp (False)

  distanceSensor.enableServoSweep()
  distanceSensor.configureServoSweep (SERVO_PIN,
  TABLE_LOCATION_IN_USER_MEMORY,
  NUMBER_OF_TABLE_ENTRIES,
  SERVO_POSITION_INCREMENT,
  False,  # Servo Reverse
  DELAY_TIME_FOR_SERVO_INCREMENT_mS,  #Servo move delay
  DELAY_TIME_FOR_SERVO_TO_RETURN_TO_0_mS  # Servo return delay
  )





# In the loop we will constantly read the I2C value, and print it to Serial When it changes
def loop():
  print("\r\n\r\n\r\n\r\n", end="")
  distanceSensor.readServoSweepEntries  ( ultrasonicDistanceTable,  #Table to read entries into
  NUMBER_OF_TABLE_ENTRIES  # Number of entries to read
  )


  for i in range(0, NUMBER_OF_TABLE_ENTRIES):
    s = [0] * (90)
    distance = ultrasonicDistanceTable[i]
    s = ("%5d ") % (distance)
    if distance > 500:
      distance = 500;  # 500mm maximum for graph
    stars = distance / (500 / 50)  # each star = 10mm
    for d in range(0, stars):
      strcat(s,"*")
    print(s)


  delay(250)


setup()
while True:
    loop()
