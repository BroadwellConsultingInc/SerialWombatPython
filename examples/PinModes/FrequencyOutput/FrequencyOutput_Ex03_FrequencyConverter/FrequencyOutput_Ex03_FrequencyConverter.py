# Converted from PinModes/FrequencyOutput/FrequencyOutput_Ex03_FrequencyConverter/FrequencyOutput_Ex03_FrequencyConverter.ino
import SerialWombat
from ArduinoFunctions import delay, delayMicroseconds, millis

import SerialWombat_interface
# >>> IMPORTANT: Set this to the configured I2C address of your Serial Wombat chip.
SERIAL_WOMBAT_ADDRESS = 0x60
sw = SerialWombat_interface.SerialWombatChipInstance(SERIAL_WOMBAT_ADDRESS)


# Interface independent code starts here:
import SerialWombatAbstractProcessedInput
import SerialWombatFrequencyOutput
import SerialWombatPulseTimer

# ===== Arduino tab: FrequencyOutput_Ex03_FrequencyConverter.ino =====
#
#   This example shows how to add an offset or multiplier to an incoming frequency and output a modified frequency.
#   This functionality can be very useful as "glue hardware" connecting two pieces of hardware that have different
#   scaling for what frequency means.  For instance, changing the diameter of a tire can cause a speedometer to
#   display an incorrect speed.  This functionalty could be used inbetween the wheel sensor and the speedometer to
#   correct the output.  In the example below, we will increase the frequency by 5%.
#
#
#
#   In this example pins 0 and 1 should be connected together.
#   Pin 0 will use the frequency output mode.  We will use this pin to simulate an incoming waveform.
#
#   Pin 1 will be in Pulse Measurement mode, configured to measure frequency, with an mx+b modification
#   provided using the processed input functionality available on may numerical input pins.  This pin would be attached
#   to an actual input in a non-example situation.
#
#   Pin 2 will be in frequency output mode, and will output the frequency measured on pin 1 using the scaled output mode.
#
#   A video demonstrating the use of the Freiquency Output  is available at:
#   TODO
#
# sw is provided by the selected Python interface block above
freqOutput = SerialWombatFrequencyOutput.SerialWombatFrequencyOutput_18AB(sw)
freqSim = SerialWombatFrequencyOutput.SerialWombatFrequencyOutput_18AB(sw)
pulseTimerIn = SerialWombatPulseTimer.SerialWombatPulseTimer_18AB(sw)
# Your serial wombat chip may be named something else than sw
FREQUENCY_OUTPUT_PIN = 2
FREQUENCY_INPUT_PIN = 1
FREQUENCY_INPUT_SIMULATION = 0  # Connect this to pin 1 if you want something to measure
def setup():
  # put your setup code here, to run once:
  # Wire.begin() is handled by the selected Python interface block
  # Initialize the I2C Bus on default pins
  # Serial.begin() is not used in this Python example
  delay(3000)
  print("1Hz Blink Example")
  sw.begin()  # Python interface was configured above
  # Scan the bus for Serial Wombat chips, and initialize the first one found
  # Optional Error handling code begin:
  if sw.isSW04():
    print("This Example is not supported on the Serial Wombat 4B chip. An 8B or 18AB chip is required.")
    while 1:
      delay(100)
  if not sw.isLatestFirmware():
    print("Firmware version mismatch. Download latest Serial Wombat Arduino Library and update Serial Wombat Firmware to latest version")
  if sw.isSW08() and not (sw.isPinModeSupported(SerialWombat.SerialWombatPinMode_t.PIN_MODE_FREQUENCY_OUTPUT) and sw.isPinModeSupported(SerialWombat.SerialWombatPinMode_t.PIN_MODE_PULSETIMER)):
    print("The required pin mode does not appear to be supported in this firmware build. Do you need to download a different firmware?")
    while 1:
      delay(100)
  # sw.registerErrorHandler(...) is Arduino-specific; Python errors are returned by library calls
  # Register an error handler that will print communication errors to Serial
  # Optional Error handling code end
  # Set up the simulated input and output frequency pins, set the low freqeuency option
  freqOutput.begin(FREQUENCY_OUTPUT_PIN, 150, True)
  freqSim.begin(FREQUENCY_INPUT_SIMULATION, 150, True)
  # Set up the input.  Since we're using slow (hundreds of Hz or less) frequencies, we'll measure in
  # mS rather than uS.
  # Pin
  # Units
  pulseTimerIn.begin(FREQUENCY_INPUT_PIN, SerialWombatPulseTimer.SW_PULSETIMER_mS, False)
  # Pull Up enabled
  pulseTimerIn.configurePublicDataOutput( SerialWombatPulseTimer.SerialWombatPulseTimer_18AB.publicDataOutput.FREQUENCY_ON_LTH_TRANSITION)
  # Configure the pulse timer to output frequency rather than pulse high time.
  pulseTimerIn.configureOutputValue(SerialWombatAbstractProcessedInput.SerialWombatAbstractProcessedInput.OutputValue.RAW)
  # Enable the Processed Input functionality on the pulse timer, and set the mx+b to a 10% increase
  pulseTimerIn.writeProcessedInputEnable(True)
  # m in 1/256ths, = to a 10% increase.
  pulseTimerIn.writeTransformLinearMXB(282, 0)
  # Set up pin 19 to output a frequency based on pin 18's scaled output
  # Enabled
  freqOutput.writeScalingEnabled(True, 18)
  # DataSource
simulatedFrequency = 50
def loop():
  global simulatedFrequency
  freqSim.writePublicData(simulatedFrequency)
  delay(2000)
  print("In frequency: ", end="")
  print(simulatedFrequency, end="")
  print(" Out frequency: ", end="")
  print(pulseTimerIn.readPublicData())
  simulatedFrequency += 5
  if simulatedFrequency > 100:
    simulatedFrequency = 10

setup()
while True:
  loop()
