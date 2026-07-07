# Converted from PinModes/FrequencyOutput/FrequencyOutput_Ex03_FrequencyConverter/FrequencyOutput_Ex03_FrequencyConverter.ino
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
import SerialWombatAbstractProcessedInput
import SerialWombatFrequencyOutput
import SerialWombatPulseTimer

#
#This example shows how to add an offset or multiplier to an incoming frequency and output a modified frequency.
#This functionality can be very useful as "glue hardware" connecting two pieces of hardware that have different
#scaling for what frequency means.  For instance, changing the diameter of a tire can cause a speedometer to
#display an incorrect speed.  This functionalty could be used inbetween the wheel sensor and the speedometer to
#correct the output.  In the example below, we will increase the frequency by 5%.
#
#
#
#In this example pins 0 and 1 should be connected together.
#Pin 0 will use the frequency output mode.  We will use this pin to simulate an incoming waveform.
#
#Pin 1 will be in Pulse Measurement mode, configured to measure frequency, with an mx+b modification
#provided using the processed input functionality available on may numerical input pins.  This pin would be attached
#to an actual input in a non-example situation.
#
#Pin 2 will be in frequency output mode, and will output the frequency measured on pin 1 using the scaled output mode.
#
#A video demonstrating the use of the Freiquency Output  is available at:
#TODO
#
#

# sw is provided by the selected interface block above
freqOutput = SerialWombatFrequencyOutput.SerialWombatFrequencyOutput_18AB(sw)
freqSim = SerialWombatFrequencyOutput.SerialWombatFrequencyOutput_18AB(sw)

pulseTimerIn = SerialWombatPulseTimer.SerialWombatPulseTimer_18AB(sw)  # Your serial wombat chip may be named something else than sw

FREQUENCY_OUTPUT_PIN = 2
FREQUENCY_INPUT_PIN = 1
FREQUENCY_INPUT_SIMULATION = 0  # Connect this to pin 1 if you want something to measure


def setup():
  # put your setup code here, to run once:
  # Wire.begin() is handled by the selected Python interface block

  # Serial.begin() is not used in this Python example
  delay(3000)
  print("1Hz Blink Example")


  sw.begin()  # Python interface was configured above

  #Optional Error handling code begin:
  if sw.isSW04():
    print("This Example is not supported on the Serial Wombat 4B chip.  An 8B or 18AB chip is required.")
    while True:
      delay(100)
  if not sw.isLatestFirmware():
    print("Firmware version mismatch.  Download latest Serial Wombat Arduino Library and update Serial Wombat Firmware to latest version")
  if sw.isSW08()  and  not (sw.isPinModeSupported(PIN_MODE_FREQUENCY_OUTPUT)  and  sw.isPinModeSupported(PIN_MODE_PULSETIMER)):
    print("The required pin mode does not appear to be supported in this firmware build.  Do you need to download a different firmware?")
    while True:
      delay(100)
  sw.registerErrorHandler(SerialWombatSerialErrorHandlerBrief);  #Register an error handler that will print communication errors to Serial
  #Optional Error handling code end

  # Set up the simulated input and output frequency pins, set the low freqeuency option
  freqOutput.begin(FREQUENCY_OUTPUT_PIN, 150, True)
  freqSim.begin(FREQUENCY_INPUT_SIMULATION, 150, True)


  # Set up the input.  Since we're using slow (hundreds of Hz or less) frequencies, we'll measure in
  # mS rather than uS.

  pulseTimerIn.begin(FREQUENCY_INPUT_PIN,  #Pin
  SW_PULSETIMER_mS,  #Units
  False);  # Pull Up enabled

  pulseTimerIn.configurePublicDataOutput( FREQUENCY_ON_LTH_TRANSITION)
  # Configure the pulse timer to output frequency rather than pulse high time.
  pulseTimerIn.configureOutputValue(RAW)

  #Enable the Processed Input functionality on the pulse timer, and set the mx+b to a 10% increase
  pulseTimerIn.writeProcessedInputEnable(True)
  pulseTimerIn.writeTransformLinearMXB(282,  # m in 1/256ths, = to a 10% increase.
  0)

  #Set up pin 19 to output a frequency based on pin 18's scaled output
  freqOutput.writeScalingEnabled(True,  #Enabled
  18);  #DataSource



simulatedFrequency = 50
def loop():
  freqSim.writePublicData(simulatedFrequency)
  delay(2000)
  print("In frequency: "); Serial.print(simulatedFrequency); Serial.print(" Out frequency: ", end="")
  print(pulseTimerIn.readPublicData())

  simulatedFrequency += 5
  if simulatedFrequency > 100:
    simulatedFrequency = 10


setup()
while True:
    loop()
