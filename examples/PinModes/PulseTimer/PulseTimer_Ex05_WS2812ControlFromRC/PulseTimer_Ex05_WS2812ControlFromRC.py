# Converted from PinModes/PulseTimer/PulseTimer_Ex05_WS2812ControlFromRC/PulseTimer_Ex05_WS2812ControlFromRC.ino
import SerialWombat
from ArduinoFunctions import delay, delayMicroseconds, millis

import SerialWombat_interface
# >>> IMPORTANT: Set this to the configured I2C address of your Serial Wombat chip.
SERIAL_WOMBAT_ADDRESS = 0x6B
sw = SerialWombat_interface.SerialWombatChipInstance(SERIAL_WOMBAT_ADDRESS)


# Interface independent code starts here:
import SerialWombatPWM
import SerialWombatPulseTimer
import SerialWombatServo
import SerialWombatWS2812

# ===== Arduino tab: PulseTimer_Ex05_WS2812ControlFromRC.ino =====
#
# This example shows how to measure servo pulses from a radio control reciever on a Serial Wombat 18AB chip.
# This example shows how the Serial Wombat18AB can be used as a signal converter and scaler to convert one type of signal
# to another, such as:
#
# RC/Servo Pulse -> Scaled Servo Pulse
# RC/Servo Pulse -> PWM or digital output
# RC/Servo Pulse -> WS2812 Bargraph Display
#
# IMPORTANT:   This example requires firmware version 2.1.1 or later to work.
#
# This example assumes 6 channels of RC receiver hooked up to pins 14 through 19.  The measured pulse length in proportion
# of range (0 to 65535) is printed to Serial.
#
# Pan and Tilt Servos are hooked up to pins 0 and 1.
# A 16 led WS2812 Array is hooked up to pin 2.
# A continuous rotation servo is hooked up to pin 5.
# A standard servo is hooked up to pin 6.
# An active piezo buzzer is hooked up to pin 7.
#
# These ranges are used to then drive servos, a WS2812 Array, and a buzzer to allow remote control of these devices from
# the RC controller.   See the video for details.
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
servoSteer = SerialWombatServo.SerialWombatServo_18AB(sw)
servoDrive = SerialWombatServo.SerialWombatServo_18AB(sw)
servoPan = SerialWombatServo.SerialWombatServo_18AB(sw)
servoTilt = SerialWombatServo.SerialWombatServo_18AB(sw)
pwmHorn = SerialWombatPWM.SerialWombatPWM_18AB(sw)
lights = SerialWombatWS2812.SerialWombatWS2812(sw)
oscTun = SerialWombat.SerialWombat18ABOscillatorTuner(sw)
def setup():
  # put your setup code here, to run once:
  # Wire.begin() is handled by the selected Python interface block
  # Initialize the I2C Bus on default pins
  # Serial.begin() is not used in this Python example
  delay(3000)
  print("6 Channel RC Receiver Pulse Measurement Example")
  sw.begin()  # Python interface was configured above
  # Scan the bus for Serial Wombat chips, and initialize the first one found
  # Optional Error handling code begin:
  if not sw.isSW18():
    print("For This Example 18AB chip is required.")
    while 1:
      delay(100)
  if not sw.isLatestFirmware():
    print("Firmware version mismatch. Download latest Serial Wombat Arduino Library and update Serial Wombat Firmware to latest version")
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
  servoSteer.attach(6)
  servoSteer.writeScalingEnabled(True,14)
  servoDrive.attach(5)
  servoDrive.writeScalingEnabled(True,15)
  servoPan.attach(0)
  servoPan.writeScalingEnabled(True,18)
  servoPan.attach(1)
  servoPan.writeScalingEnabled(True,19)
  lights.begin(2,16,0x0000)
  lights.barGraph(17,0,0x202020,0,65535)
  pwmHorn.begin(8)
  pwmHorn.writeScalingEnabled(True,16)
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
