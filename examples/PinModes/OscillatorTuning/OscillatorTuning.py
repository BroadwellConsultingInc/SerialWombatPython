# Converted from PinModes/OscillatorTuning/OscillatorTuning.ino
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

#
#This example shows how to tune the Serial Wombat 18AB chip's internal FRC oscillator against
#the host's millis() function to reduce the error in the FRC from as much as +/- 1.5% at room
#temperature to less than 0.1% .
#
#This sketch runs for 1 minute to profile and display the nominal error in the FRC vs. millis()
#then begins calling the update function of SerialWombat18ABOscillatorTuner.  The system then displays
#the improvement in accurary as the oscillator is tuned.
#
#A video demonstrating the use of the SerialWombat18ABOscillatorTuner class on the Serial Wombat 18AB chip is available at:
#https://youtu.be/T2uBQM3s_JM
#Documentation for the SerialWombat18ABOscillatorTuner Arduino class is available at:
#https://broadwellconsultinginc.github.io/SerialWombatArdLib/class_serial_wombat18_a_b_oscillator_tuner.html
#


# sw is provided by the selected interface block above

millisStart = 0
framesStart = 0
nextUpdate = 0
oscTun = SerialWombat.SerialWombat18ABOscillatorTuner(sw)
def setup():
  # put your setup code here, to run once:
  # Wire.begin() is handled by the selected Python interface block

  # Serial.begin() is not used in this Python example
  delay(3000)
  print("High Speed Counter Example")


  sw.begin()  # Python interface was configured above

  #Optional Error handling code begin:
  if not sw.isSW18():
    print("This Example is not supported on the Serial Wombat 4B or 8B chip.  An  18AB chip is required.")
    while True:
      delay(100)
  if not sw.isLatestFirmware():
    print("Firmware version mismatch.  Download latest Serial Wombat Arduino Library and update Serial Wombat Firmware to latest version")

  sw.registerErrorHandler(SerialWombatSerialErrorHandlerBrief);  #Register an error handler that will print communication errors to Serial
  #Optional Error handling code end

  framesStartmsb = sw.readPublicData(SW_DATA_SOURCE_FRAMES_RUN_MSW)
  framesStartlsb = sw.readPublicData(SW_DATA_SOURCE_FRAMES_RUN_LSW)
  if framesStartmsb != sw.readPublicData(SW_DATA_SOURCE_FRAMES_RUN_MSW):
    framesStartlsb = sw.readPublicData(SW_DATA_SOURCE_FRAMES_RUN_LSW)
    framesStartmsb = sw.readPublicData(SW_DATA_SOURCE_FRAMES_RUN_MSW)
  framesStart = framesStartmsb <<16
  framesStart += framesStartlsb
  millisStart = millis()
  nextUpdate = millis() + 60000

  print("System will test Serial Wombat frame count for 1 minute, then start tuning algorithm, and show results every minute.")


def loop():
  # put your main code here, to run repeatedly:
  m = millis()
  if m > nextUpdate:
    frameslsb = sw.readPublicData(SW_DATA_SOURCE_FRAMES_RUN_LSW)
    frames = sw.readPublicData(SW_DATA_SOURCE_FRAMES_RUN_MSW)
    if frames != sw.readPublicData(SW_DATA_SOURCE_FRAMES_RUN_MSW):
      frameslsb = sw.readPublicData(SW_DATA_SOURCE_FRAMES_RUN_LSW)
      frames = sw.readPublicData(SW_DATA_SOURCE_FRAMES_RUN_MSW)
    frames <<= 16
    frames += frameslsb
    print("millis elapsed: ");  Serial.print (m - millisStart); Serial.print(" frames run: "); Serial.print(frames-framesStart, end="")
    print(" d: "); Serial.print((m - millisStart) - (frames-framesStart), end="")
    print(" % (+ is SW too slow): "); Serial.println((float)((m - millisStart) - (frames-framesStart))/ (m - millisStart) * 100, end="")
    nextUpdate = millis() + 60000
    framesStart = frames
    millisStart = m
  if millis() > 70000:
    oscTun.update();  # Start tuning after the first minute.


setup()
while True:
    loop()
