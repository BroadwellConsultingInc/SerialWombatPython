# Converted from Boards/PCB0031_SW8B_GRIP/GRIP_Ex03_SpeedControl/GRIP_Ex03_SpeedControl.ino
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
import SerialWombatAbstractScaledOutput

#
#This example shows how to use the PCB0031 Grip's rate limiting control to offload servo movement speed control to the Serial Wombat firmware
#
#This example assumes the servo is attached to pin 0.  For pins 1 2 or 3 change
#gs0 to gs1, gs2, or gs3 .
#
#
#Be sure to use pull up resistors on the I2C bus or enable the on board pull ups
#on the Grip board via the solder jumper.
#
#
#A video demonstrating this example is available at
#https://youtu.be/TODO
#
#Documentation for the Grip board classes are available at:
#https://broadwellconsultinginc.github.io/SerialWombatArdLib/class_p_c_b0031___grip.html
#
#
#

GRIP_I2C_ADDRESS = 0x60
grip = PCB0031_Grip.PCB0031_Grip(sw)

SERVO_MOVEMENT_INCREASE_RATE = 1000
SERVO_MOVEMENT_DECREASE_RATE = 200


def setup():
  # Wire.begin() is handled by the selected Python interface block

  # Serial.begin() is not used in this Python example

  delay(500)

  grip.begin(0x60, True)
  grip.registerErrorHandler(SerialWombatSerialErrorHandlerBrief);  #Register an error handler that will print communication errors to Serial
  if not grip.isLatestFirmware():
    print("Firmware version mismatch.  Download latest Serial Wombat Arduino Library and update Serial Wombat Firmware to latest version")



  # Output Scaling configurations for this pin
  grip.gs0.writeScalingEnabled(True,  #Enabled
  grip.gs0.pin());  #DataSource
  #put this line in setup.
  grip.gs0.writeRateControl(PERIOD_16mS,  # Sampling Period
  SERVO_MOVEMENT_INCREASE_RATE,  #Maximum Increase Rate
  SERVO_MOVEMENT_DECREASE_RATE);  #Maximum Decrease Rate


def loop():
  grip.gs0.writePublicData(0)
  delay(5000)
  grip.gs0.writePublicData(65535)
  delay(5000)


setup()
while True:
    loop()
