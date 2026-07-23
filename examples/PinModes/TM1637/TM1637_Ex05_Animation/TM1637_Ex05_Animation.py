# Converted from PinModes/TM1637/TM1637_Ex05_Animation/TM1637_Ex05_Animation.ino
import SerialWombat
from ArduinoFunctions import delay, delayMicroseconds, millis

import SerialWombat_interface
# >>> IMPORTANT: Set this to the configured I2C address of your Serial Wombat chip.
SERIAL_WOMBAT_ADDRESS = 0x60
sw = SerialWombat_interface.SerialWombatChipInstance(SERIAL_WOMBAT_ADDRESS)


# Interface independent code starts here:
import SerialWombatTM1637

# ===== Arduino tab: TM1637_Ex05_Animation.ino =====
#
# This example shows how to display an animation on a TM1637 display.  The animation is loaded to the Serial Wombat 18AB chip
# from the Arduino board.  The Serial Wombat chip then outputs the animation to the display without any intervention from
# the Arduino board.
#
# If you haven't already, run the SW_Ard_TM1637_012345 example to ensure your display displays digits in
# the correct order.  If necessary, correct the call to writeDigitOrder below as described in that example.
# 4 digit displays should use settings to display 0123 in that test to work properly with this sketch.
#
# You can choose an animation to show by commenting in one of the options below //CONFIG:
#
# A video demonstrating the use of the TM1637 pin mode on the Serial Wombat 18AB chip is available at:
# https://youtu.be/AwW12n6o_T0
#
# Documentation for the SerialWombatTM1637 Arduino class is available at:
# https://broadwellconsultinginc.github.io/SerialWombatArdLib/class_serial_wombat_t_m1637.html#details
#
# Serial Wombat is a registered trademark in the United States of Broadwell Consulting Inc.
myDisplay = SerialWombatTM1637.SerialWombatTM1637(sw)
DISPLAY_CLK_PIN = 6  # <<<<<<<<<   Set this to the Serial Wombat pin connected to your Display Clock Pin
DISPLAY_DIN_PIN = 7  # <<<<<<<<<   Set this to the Serial Wombat pin connected to your Display Data Pin
# CONFIG: pick one
# #define ANIMATION_ARRAY snake_6_digit
ANIMATION_ARRAY = snake_4_digit
# #define ANIMATION_ARRAY leftToRight
# CONFIG:
# #define SPEED 1000  // Slow -  delay 1000mS after updates
SPEED = 100  # Medium - delay 100mS after updates
# #define SPEED 10  // Fast -   delay 10ms after updates
SEG_A = 0x1  # TOP
SEG_B = 0x2  # UPPER RIGHT
SEG_C = 0x4  # BOTTOM RIGHT
SEG_D = 0x8  # BOTTOM
SEG_E = 0x10  # BOTTOM LEFT
SEG_F = 0x20  # TOP LEFT
SEG_G = 0x40  # CENTER
SEG_POINT = 0x80
OFF__ = 0
VERTRIGHT = (SEG_B | SEG_C)
VERTLEFT = (SEG_E | SEG_F)
TOP = (SEG_A)
MID = (SEG_G)
BOT = (SEG_D)
# All arrays are 6 bytes wide, regardless of display width.
# putting multiple frames the same in looks like a delay
LeftToRight = [ [VERTLEFT, 0,0,0,0,0], [VERTRIGHT, 0,0,0,0,0], [0,VERTLEFT, 0,0,0,0], [0,VERTRIGHT, 0,0,0,0], [0,0,VERTLEFT, 0,0,0], [0,0,VERTRIGHT, 0,0,0], [0,0,0,VERTLEFT, 0,0], [0,0,0,VERTRIGHT, 0,0], [0,0,0,0,VERTLEFT, 0], [0,0,0,0,VERTRIGHT, 0], [0,0,0,0,0,VERTLEFT ], [0,0,0,0,0,VERTRIGHT], [0,0,0,0,0,0], [0,0,0,0,0,0], [0,0,0,0,0,0], [0,0,0,0,0,0], [0,0,0,0,0,0], [0,0,0,0,0,0], ]
snake_6_digit = [ [TOP,0,0,0,0,0], [0,TOP,0,0,0,0], [0,0,TOP,0,0,0], [0,0,0,TOP,0,0], [0,0,0,0,TOP,0], [0,0,0,0,0,TOP], [0,0,0,0,0,SEG_B], [0,0,0,0,0,MID], [0,0,0,0,MID,0], [0,0,0,MID,0,0], [0,0,MID,0,0,0], [0,MID,0,0,0,0], [MID,0,0,0,0,0], [SEG_E,0,0,0,0,0], [BOT,0,0,0,0,0], [0,BOT,0,0,0,0], [0,0,BOT,0,0,0], [0,0,0,BOT,0,0], [0,0,0,0,BOT,0], [0,0,0,0,0,BOT], [0,0,0,0,0,SEG_C], [0,0,0,0,0,MID], [0,0,0,0,MID,0], [0,0,0,MID,0,0], [0,0,MID,0,0,0], [0,MID,0,0,0,0], [MID,0,0,0,0,0], [SEG_F,0,0,0,0,0], ]
snake_4_digit = [ [TOP,0,0,0,0,0], [0,TOP,0,0,0,0], [0,0,TOP,0,0,0], [0,0,0,TOP,0,0], [0,0,0,SEG_B,0,0], [0,0,0,MID,0,0], [0,0,MID,0,0,0], [0,MID,0,0,0,0], [MID,0,0,0,0,0], [SEG_E,0,0,0,0,0], [BOT,0,0,0,0,0], [0,BOT,0,0,0,0], [0,0,BOT,0,0,0], [0,0,0,BOT,0,0], [0,0,0,SEG_C,0,0], [0,0,0,MID,0,0], [0,0,MID,0,0,0], [0,MID,0,0,0,0], [MID,0,0,0,0,0], [SEG_F,0,0,0,0,0], ]
def setup():
  # put your setup code here, to run once:
  # Wire.begin() is handled by the selected Python interface block
  # Initialize the I2C Bus on default pins
  # Serial.begin() is not used in this Python example
  delay(3000)
  print("TM1637 Public Data Display Example")
  sw.begin()  # Python interface was configured above
  # Scan the bus for Serial Wombat chips, and initialize the first one found
  # Optional Error handling code begin:
  if sw.isSW04():
    print("This Example is not supported on the Serial Wombat 4B chip. An 8B or 18AB chip is required.")
    while 1:
      delay(100)
  if not sw.isLatestFirmware():
    print("Firmware version mismatch. Download latest Serial Wombat Arduino Library and update Serial Wombat Firmware to latest version")
  if sw.isSW08() and not sw.isPinModeSupported(SerialWombat.SerialWombatPinMode_t.PIN_MODE_TM1637):
    print("The required pin mode does not appear to be supported in this firmware build. Do you need to download a different firmware?")
    while 1:
      delay(100)
  # sw.registerErrorHandler(...) is Arduino-specific; Python errors are returned by library calls
  # Register an error handler that will print communication errors to Serial
  # Optional Error handling code end
  # Clk Pin
  # Data Pin
  # Number of digits
  # Mode enumeration
  # source pin Not used in Animation mode
  myDisplay.begin(DISPLAY_CLK_PIN, DISPLAY_DIN_PIN, 4, SerialWombatTM1637.SWTM1637Mode.tm1637Animation, 0, 4)
  # Brightness
  # myDisplay.writeDigitOrder(0,1,2,3,4,5);
  # Place array at index 0x180 in the user buffer
  # Number of frames.  Suggest using sizeof like this to calculate.
  myDisplay.writeAnimation(0x0, SPEED, len(ANIMATION_ARRAY)/6, ANIMATION_ARRAY)
  # Array to load.
def loop():
  pass

setup()
while True:
  loop()
