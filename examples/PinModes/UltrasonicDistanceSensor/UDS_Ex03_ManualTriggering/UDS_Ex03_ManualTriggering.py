# Converted from PinModes/UltrasonicDistanceSensor/UDS_Ex03_ManualTriggering/UDS_Ex03_ManualTriggering.ino
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
import SerialWombatUltrasonicDistanceSensor

#
#This example shows how to manually trigger ultrasonic distance sensor measurements.  This is useful if you don't want
#multiple sensors runing simultaneously as they may interfere with each other.
#
#In this example we will use 6 sensors, one for straight ahead, one for forward left, one for left, one for foward right,
#and one for reverse.
#
#The host will trigger each sensor in succession and print the name of the sensor if an object is near (less than 100mm)
#
#This sketch assumes an 18AB chip due to the number of pins required, but could be adapted to use 4 sensors on a Serial Wombat 8B
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

# sw is provided by the selected interface block above
rearSensor = SerialWombatUltrasonicDistanceSensor.SerialWombatUltrasonicDistanceSensor(sw)
leftSensor = SerialWombatUltrasonicDistanceSensor.SerialWombatUltrasonicDistanceSensor(sw)
flSensor = SerialWombatUltrasonicDistanceSensor.SerialWombatUltrasonicDistanceSensor(sw)
frontSensor = SerialWombatUltrasonicDistanceSensor.SerialWombatUltrasonicDistanceSensor(sw)
frSensor = SerialWombatUltrasonicDistanceSensor.SerialWombatUltrasonicDistanceSensor(sw)
rightSensor = SerialWombatUltrasonicDistanceSensor.SerialWombatUltrasonicDistanceSensor(sw)


def setup():
  # put your setup code here, to run once:
  # Wire.begin() is handled by the selected Python interface block

  # Serial.begin() is not used in this Python example
  delay(3000)
  print("Ultrasonic Distance Sensor Manual Triggering Example ")


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
  #Initialize all the sensors without autotrigger
  # TODO_MANUAL_CONVERSION: leftSensor.begin(10,  # Echo pin is on pin 10
  HC_SR04,  # HC_SR04 driver
  16,  # Trigger pin on pin 11.
  # TODO_MANUAL_CONVERSION: False);no Autotrigger,      no parameters for  pullUp (False)

  # TODO_MANUAL_CONVERSION: flSensor.begin(11,  # Echo pin is on pin 11
  HC_SR04,  # HC_SR04 driver
  17,  # Trigger pin on pin 17.
  # TODO_MANUAL_CONVERSION: False);no Autotrigger,      no parameters for  pullUp (False)

  # TODO_MANUAL_CONVERSION: frontSensor.begin(12,  # Echo pin is on pin 12
  HC_SR04,  # HC_SR04 driver
  18,  # Trigger pin on pin 18.
  # TODO_MANUAL_CONVERSION: False);no Autotrigger,      no parameters for  pullUp (False)

  # TODO_MANUAL_CONVERSION: flSensor.begin(14,  # Echo pin is on pin 14
  HC_SR04,  # HC_SR04 driver
  13,  # Trigger pin on pin 13.
  # TODO_MANUAL_CONVERSION: False);no Autotrigger,      no parameters for  pullUp (False)

  # TODO_MANUAL_CONVERSION: rightSensor.begin(15,  # Echo pin is on pin 14
  HC_SR04,  # HC_SR04 driver
  19,  # Trigger pin on pin 19.
  # TODO_MANUAL_CONVERSION: False);no Autotrigger,      no parameters for  pullUp (False)




DETECTION_DISTANCE_MM = 100
MEASUREMENT_TIME_mS = 50

# In the loop we will constantly read the average value, and print it to Serial When it changes
def loop():
  leftSensor.manualTrigger()
  delay(MEASUREMENT_TIME_mS);  # Allow time for measurement
  # TODO_MANUAL_CONVERSION: if leftSensor.readPublicData() < DETECTION_DISTANCE_MM) Serial.print("OBJECT LEFT ": 

    # TODO_MANUAL_CONVERSION_INDENT: flSensor.manualTrigger()
    # TODO_MANUAL_CONVERSION_INDENT: delay(MEASUREMENT_TIME_mS);  # Allow time for measurement
    # TODO_MANUAL_CONVERSION: if flSensor.readPublicData() < DETECTION_DISTANCE_MM) Serial.println("OBJECT FRONTLEFT ": 

      # TODO_MANUAL_CONVERSION_INDENT: frontSensor.manualTrigger()
      # TODO_MANUAL_CONVERSION_INDENT: delay(MEASUREMENT_TIME_mS);  # Allow time for measurement
      # TODO_MANUAL_CONVERSION: if frontSensor.readPublicData() < DETECTION_DISTANCE_MM) Serial.println("OBJECT FRONT ": 

        # TODO_MANUAL_CONVERSION_INDENT: frSensor.manualTrigger()
        # TODO_MANUAL_CONVERSION_INDENT: delay(MEASUREMENT_TIME_mS);  # Allow time for measurement
        # TODO_MANUAL_CONVERSION: if frSensor.readPublicData() < DETECTION_DISTANCE_MM) Serial.println("OBJECT FRONTRIGHT ": 

          # TODO_MANUAL_CONVERSION_INDENT: rightSensor.manualTrigger()
          # TODO_MANUAL_CONVERSION_INDENT: delay(MEASUREMENT_TIME_mS);  # Allow time for measurement
          # TODO_MANUAL_CONVERSION: if rightSensor.readPublicData() < DETECTION_DISTANCE_MM) Serial.println("OBJECT RIGHT ": 

            # TODO_MANUAL_CONVERSION_INDENT: rearSensor.manualTrigger()
            # TODO_MANUAL_CONVERSION_INDENT: delay(MEASUREMENT_TIME_mS);  # Allow time for measurement
            # TODO_MANUAL_CONVERSION: if rearSensor.readPublicData() < DETECTION_DISTANCE_MM) Serial.println("OBJECT REAR ":


setup()
while True:
    loop()
