# Converted from Boards/PCB0031_SW8B_GRIP/GRIP_Ex01_ClawGrip/GRIP_Ex01_ClawGrip.ino
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
import PCB0031_Grip

#
#This video shows how to use the PCB0031 Grip's current feedback capabilites to
#automatically calibrate a servo based gripper claw.
#
#A good sample platform is an SG90 Servo and this 3d printed Gripper https://www.thingiverse.com/thing:5664874
#
#In this example the library and Serial Wombat firmware automatically cycle
#through the range of the servo taking current readings at various positions.
#
#By looking for a current spike caused by motor stall the software can determine
#the range of motion of the gripper and its open and closed points
#
#The sketch then alternates between gripping and releasing.  Feedback control of
#commanded servo position vs. current is used to limit how hard the gripper
#squeezes.
#
#By checking if the servo stopped short of full closed position inference of
#an object in the gripper can be made.
#
#Every servo / gripper combination is a bit different.  There are parameters
#in the example you can adjust.  These are explained in the comments.
#
#This example assumes the servo is attached to pin 0.  For pins 1 2 or 3 change
#gs0 to gs1, gs2, or gs3 .
#
#Be sure to use pull up resistors on the I2C bus or enable the on board pull ups
#on the Grip board via the solder jumper.
#
#The Grip board must be provided with 5V electronics input for proper operation of the current sensors.
#
#Note that this example attempts to push the servo through its full 180 degree
#range in order to take current measurements.  Do not use this example if that
#could cause damage to your gripper mechanics.
#
#A video demonstrating this example is available at
#https://youtu.be/TODO
#
#Documentation for the Grip board classes are available at:
#https://broadwellconsultinginc.github.io/SerialWombatArdLib/class_p_c_b0031___grip.html
#
#




GRIP_I2C_ADDRESS = 0x60
grip = PCB0031_Grip.PCB0031_Grip(sw)


def setup():

  # Wire.begin() is handled by the selected Python interface block

  # Serial.begin() is not used in this Python example

  delay(500)

  grip.begin(0x60, True)
  grip.registerErrorHandler(SerialWombatSerialErrorHandlerBrief);  #Register an error handler that will print communication errors to Serial
  if not grip.isLatestFirmware():
    print("Firmware version mismatch.  Download latest Serial Wombat Arduino Library and update Serial Wombat Firmware to latest version")

  print("Calibrating the gripper.  This can take 20 seconds to measure current at 65 different positions.  The gripper may appear to stop moving for a bit.")
  grip.gs0.calibrateGripper();  # Add the parameter True to reverse servo direction if your servo opens the gripper at higher values
  print("Calibration Complete.")


def loop():

  delay(5000)

  grip.gs0.grip(32768);  #Try to grip an object.  Increase or decrease the paramter to grip harder or softer.  Max 65535

  # Note that the grip function returns immediatley and does not block or delay.  The gripping algorithm is executed on the
  # Serial Wombat chip, not on the Arduino.

  delay(1500);  # Allow the gripper time to settle before object detection

  if grip.gs0.objectPresent(60):
    # Increase the parameter to detect smaller objects.  Reduce the parmeter to reduce false positives
    print("Object Grasped")
  else:
    print("No Object")
  delay(3500)

  grip.gs0.release()


setup()
while True:
    loop()
