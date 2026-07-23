import SerialWombat
from ArduinoFunctions import delay, delayMicroseconds, millis


import SerialWombat_interface
sw = SerialWombat_interface.SerialWombatChipInstance(0x61)  #Change the address to match your configuration




#Interface independent code starts here:
import SerialWombatRandomBlink

randomBlink0 = SerialWombatRandomBlink.SerialWombatRandomBlink(sw)
randomBlink1 = SerialWombatRandomBlink.SerialWombatRandomBlink(sw)
randomBlink2 = SerialWombatRandomBlink.SerialWombatRandomBlink(sw)
randomBlink3 = SerialWombatRandomBlink.SerialWombatRandomBlink(sw)
randomBlink4 = SerialWombatRandomBlink.SerialWombatRandomBlink(sw)
randomBlink5 = SerialWombatRandomBlink.SerialWombatRandomBlink(sw)
randomBlink6 = SerialWombatRandomBlink.SerialWombatRandomBlink(sw)
randomBlink7 = SerialWombatRandomBlink.SerialWombatRandomBlink(sw)

#  This example shows how to use the Serial Wombat Random Blink pin mode.
#
#    This example combines examples 1, 2 and 3 across 8 LEDs for a cool demo.
#
#     This example is compatible with the Serial Wombat 18AB and 8B chips,
#     when the RandomBlink pin mode is present in the firmware build.
#
#     In this example pin 1 is configured as a Random Blink output.  The pin
#     randomly alternates between on and off.  Each on time and off time is
#     randomly selected between 0 and 2000 ms.
#
#     The outputscaling module first order filter is used for smoothing.
#
#     This example assumes  LEDs and current limiting resistor with anodes connected
#     to Pins, and cathodes attached to ground (high side drive)
#
#     The on PWM value is fixed at 65535, fully on.  The off PWM value is fixed
#     at 0, fully off.
#
#     SerialWombatRandomBlink pin mode documentation:
#
#     TODO coming soon
#
#     SerialWombatRandomBlink tutorial video:
#
#     TODO coming soon


def halt():
  while True:
    delay(100)


def check_random_blink_requirements(require_pwm=False):
  #Optional Error handling code begin:
  if sw.isSW04():
    print("This Example is not supported on the Serial Wombat 4B chip.  An 8B or 18AB chip is required.")
    halt()

  if not sw.isLatestFirmware():
    print("Firmware version mismatch.  Download latest Serial Wombat Python Library and update Serial Wombat Firmware to latest version")

  if sw.isSW08():
    randomBlinkSupported = sw.isPinModeSupported(SerialWombat.SerialWombatPinMode_t.PIN_MODE_RANDOMBLINK)
    pwmSupported = True
    if require_pwm:
      pwmSupported = sw.isPinModeSupported(SerialWombat.SerialWombatPinMode_t.PIN_MODE_PWM)

    if not randomBlinkSupported or not pwmSupported:
      if require_pwm:
        print("The required pin modes do not appear to be supported in this firmware build.  Do you need to download a different firmware?")
      else:
        print("The required pin mode does not appear to be supported in this firmware build.  Do you need to download a different firmware?")
      halt()
  #Optional Error handling code end


def setup():
  # put your setup code here, to run once:
  # Wire.begin() is handled by the selected Python interface block

  # Serial.begin() is not used in this Python example
  delay(3000)
  print("Random Blink Example")


  sw.begin()  # Python interface was configured above

  check_random_blink_requirements()

  randomBlink0.begin(0, 2000, 2000)
  randomBlink1.begin(1, 2000, 2000)
  randomBlink2.begin(2, 500, 500)
  randomBlink3.begin(3, 1000, 2000, 0, 2000)
  randomBlink4.begin(4, 3000, 3000, 0, 0, 0x1000, 0x4000, 0x0400, 0x0400)
  randomBlink5.begin(5, 2000, 1000)
  randomBlink6.begin(6, 2000, 2000, 0, 0, 0x1000, 0x4000, 0x0400, 0x0400)
  randomBlink7.begin(7, 2000, 2000)


  # Add first order filtering using the Serial Wombat scaled output capability.
  # The Random Blink pin mode writes a target PWM value.  The scaled output block
  # filters that target before writing it to the physical output.
  # Higher filter constants produce slower transitions.
  randomBlink1.write1stOrderFiltering(randomBlink1.PERIOD_16mS, 0xF000)  # Values closer to zero slow things down, closer to 0xFFFF speed things up

  # Enable scaled output processing.  Use the same pin as the input source so
  # the Random Blink pin mode's generated target value is filtered.
  randomBlink1.writeScalingEnabled(True, 1)

  # Add first order filtering using the Serial Wombat scaled output capability.
  # The Random Blink pin mode writes a target PWM value.  The scaled output block
  # filters that target before writing it to the physical output.
  # Higher filter constants produce slower transitions.
  randomBlink6.write1stOrderFiltering(randomBlink6.PERIOD_16mS, 0xF000)  # Values closer to zero slow things down, closer to 0xFFFF speed things up

  # Enable scaled output processing.  Use the same pin as the input source so
  # the Random Blink pin mode's generated target value is filtered.
  randomBlink6.writeScalingEnabled(True, 6)



def loop():
  # The Serial Wombat chip controls the random blinking without any additional host activity.
  pass


setup()
while True:
    loop()
