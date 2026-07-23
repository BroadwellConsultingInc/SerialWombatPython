# Converted from PinModes/PulseTimer/PulseTimer_Ex04_RCReceiverWithScaling/PulseTimer_Ex04_RCReceiverWithScaling.ino
import SerialWombat
from ArduinoFunctions import delay, delayMicroseconds, millis

import SerialWombat_interface
# >>> IMPORTANT: Set this to the configured I2C address of your Serial Wombat chip.
SERIAL_WOMBAT_ADDRESS = 0x60
sw = SerialWombat_interface.SerialWombatChipInstance(SERIAL_WOMBAT_ADDRESS)


# Interface independent code starts here:
import SerialWombatPulseTimer

# ===== Arduino tab: PulseTimer_Ex04_RCReceiverWithScaling.ino =====
#
# This example shows how to measure servo pulses from a radio control reciever on a Serial Wombat 8B or 18AB chip.
#
# IMPORTANT:   This example requires firmware version 2.1.1 or later to work.
#
# This example assumes 6 channels of RC receiver hooked up to pins 14 through 19.  The measured pulse length  is
# printed to Serial as a proportion of its range (0 to 65535).
#
# This sketch makes use of the SerialWombat18ABOscillatorTuner to improve the meaurement accuracy.  About 1 minute of
# runtime is required after reset to achieve full accuracy improvement.
#
# A video demonstrating the use of the SerialWombatPulseTimer.SerialWombatPulseTimer_18AB class for RC measurement  on the Serial Wombat 18AB chip is available at:
# TBD
#
# Documentation for the SerialWombatPulseTimer.SerialWombatPulseTimer_18AB Arduino class is available at:
# https://broadwellconsultinginc.github.io/SerialWombatArdLib/class_serial_wombat_pulse_timer__18_a_b.html
#
# Documentation for the SerialWombatAbstractProcessedInput class that provides the scaling for SerialWombatPulseTimer.SerialWombatPulseTimer_18AB
# is available here:
# https://broadwellconsultinginc.github.io/SerialWombatArdLib/class_serial_wombat_abstract_processed_input.html
#
#
# sw is provided by the selected Python interface block above
rcWheel = SerialWombatPulseTimer.SerialWombatPulseTimer_18AB(sw)
rcThrottle = SerialWombatPulseTimer.SerialWombatPulseTimer_18AB(sw)
rcSwitch3 = SerialWombatPulseTimer.SerialWombatPulseTimer_18AB(sw)
rcSwitch4 = SerialWombatPulseTimer.SerialWombatPulseTimer_18AB(sw)
rcKnob5 = SerialWombatPulseTimer.SerialWombatPulseTimer_18AB(sw)
rcKnob6 = SerialWombatPulseTimer.SerialWombatPulseTimer_18AB(sw)
oscTun = SerialWombat.SerialWombat18ABOscillatorTuner(sw)
def setup():
  # put your setup code here, to run once:
  # Wire.begin() is handled by the selected Python interface block
  # Initialize the I2C Bus on default pins
  # Serial.begin() is not used in this Python example
  delay(3000)
  print("6 Channel RC Receiver Pulse Measurement with scaling Example")
  sw.begin()  # Python interface was configured above
  # Scan the bus for Serial Wombat chips, and initialize the first one found
  # Optional Error handling code begin:
  if sw.isSW04():
    print("This Example is not supported on the Serial Wombat 4B chip. An 8B or 18AB chip is required.")
    while 1:
      delay(100)
  if not sw.isLatestFirmware():
    print("Firmware version mismatch. Download latest Serial Wombat Arduino Library and update Serial Wombat Firmware to latest version")
  if sw.isSW08() and not sw.isPinModeSupported(SerialWombat.SerialWombatPinMode_t.PIN_MODE_PULSETIMER):
    print("The required pin mode does not appear to be supported in this firmware build. Do you need to download a different firmware?")
    while 1:
      delay(100)
  # sw.registerErrorHandler(...) is Arduino-specific; Python errors are returned by library calls
  # Register an error handler that will print communication errors to Serial
  # Optional Error handling code end
  rcWheel.begin(14)
  rcWheel.writeProcessedInputEnable(True)
  rcWheel.writeTransformScaleRange(925,2115)
  # See YouTube video for origin of numbers
  rcThrottle.begin(15)
  rcThrottle.writeProcessedInputEnable(True)
  rcThrottle.writeTransformScaleRange(890,2100)
  rcSwitch3.begin(16)
  rcSwitch3.writeProcessedInputEnable(True)
  rcSwitch3.writeTransformScaleRange(1500,1501)
  rcSwitch4.begin(17)
  rcSwitch4.writeProcessedInputEnable(True)
  rcSwitch4.writeTransformScaleRange(1350,1650)
  rcKnob5.begin(18)
  rcKnob5.writeProcessedInputEnable(True)
  rcKnob5.writeTransformScaleRange(925,2075)
  rcKnob6.begin(19)
  rcKnob6.writeProcessedInputEnable(True)
  rcKnob6.writeTransformScaleRange(925,2075)
def loop():
  # put your main code here, to run repeatedly:
  s = bytearray(80)
  s = "%5d %5d %5d %5d %5d %5d" % (rcWheel.readPublicData(), rcThrottle.readPublicData(), rcSwitch3.readPublicData(), rcSwitch4.readPublicData(), rcKnob5.readPublicData(), rcKnob6.readPublicData())
  print(s)
  delay(200)
  oscTun.update()

setup()
while True:
  loop()
