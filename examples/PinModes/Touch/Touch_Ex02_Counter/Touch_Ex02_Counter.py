# Converted from PinModes/Touch/Touch_Ex02_Counter/Touch_Ex02_Counter.ino
import SerialWombat
from ArduinoFunctions import delay, delayMicroseconds, millis

import SerialWombat_interface
# >>> IMPORTANT: Set this to the configured I2C address of your Serial Wombat chip.
SERIAL_WOMBAT_ADDRESS = 0x6B
sw = SerialWombat_interface.SerialWombatChipInstance(SERIAL_WOMBAT_ADDRESS)


# Interface independent code starts here:
import SerialWombat18CapTouch
import SerialWombatDebouncedInput

# ===== Arduino tab: Touch_Ex02_Counter.ino =====
#
# This example shows how to configure two Serial Wombat 18AB pins to Touch input and use the
# SerialWombat18CapTouchCounter class to implement a two touch sensor interface to increment
# a counter at various speeds by two different increments.
#
# The example was created using a Serial Wombat 18AB chip in I2C mode with a Node MCU clone Arduino
# and a penny and quarter both covered with electrial tape wired to pins WP16 and WP17.
#
# When the penny is touched briefly the total will increment by 1 cent.  When the quarter is touched
# the total will increment by 25 cents.  If a finger is held on them then they will increment slowly, then
# more quickly, then very quickly.  This type of interface could be easily integrated into a complete solution
# for user configuration of parameters.
#
# SerialWombat18CapTouch class documentation can be found here:
# https://broadwellconsultinginc.github.io/SerialWombatArdLib/class_serial_wombat18_cap_touch.html#details
#
# A demonstration video of this class can be found here:
# https://youtu.be/c4B0_DRVHs0
#
#
PENNY_PIN = 16  # Must be an Analog capable pin:  0,1,2,3,4,16,17,18,19
QUARTER_PIN = 17  # Must be an Analog capable pin:  0,1,2,3,4,16,17,18,19
penny = SerialWombat18CapTouch.SerialWombat18CapTouch(sw)
quarter = SerialWombat18CapTouch.SerialWombat18CapTouch(sw)
quarterCounter = SerialWombatDebouncedInput.SerialWombatButtonCounter(quarter)
pennyCounter = SerialWombatDebouncedInput.SerialWombatButtonCounter(penny)
moneyCount = 0
# Place to keep track of total money count in pennies
def setup():
  # put your setup code here, to run once:
  # Wire.begin() is handled by the selected Python interface block
  # Initialize the I2C Bus on default pins
  # Serial.begin() is not used in this Python example
  delay(3000)
  print("High Speed Clock Example")
  sw.begin()  # Python interface was configured above
  # Scan the bus for Serial Wombat chips, and initialize the first one found
  # Optional Error handling code begin:
  if not sw.isSW18():
    print("This Example is not supported on the Serial Wombat 4B or 8B chip. An 18AB chip is required.")
    while 1:
      delay(100)
  if not sw.isLatestFirmware():
    print("Firmware version mismatch. Download latest Serial Wombat Arduino Library and update Serial Wombat Firmware to latest version")
  # sw.registerErrorHandler(...) is Arduino-specific; Python errors are returned by library calls
  # Register an error handler that will print communication errors to Serial
  # Optional Error handling code end
  # Initialize the Penny sensor
  # 9000 based on previous calibration of this penny on this pin with this wire using the Calibration example
  penny.begin(PENNY_PIN,9000,0)
  # Initialize the Penny sensor
  # 9250 based on previous calibration of this quarter on this pin with this wire using the Calibration example
  quarter.begin(QUARTER_PIN,9250,0)
  delay(500)
  penny.makeDigital(53985,57620,1,0,0,0)
  # Low and High limits based on previous calibration of this penny on this pin with this wire
  quarter.makeDigital(54349,57792,1,0,0,0)
  # Low and High limits based on previous calibration of this quarter on this pin with this wire
  delay(250)
  # moneyCount is the variable we want to increment.
  # Increment by 1
  # Every 500 ms
  # for 2000ms, then...
  # by 1
  # every 250ms
  # for 5000 ms, then
  # by 1
  pennyCounter.begin(1, 500, 2000, 1, 250, 5000, 1, 100)
  # every 100ms
  # Initialization of the quarter Counter is the same, but incrments by 25.
  quarterCounter.begin(25, 500, 2000, 25, 250, 5000, 25, 100)
  print("Touch or hold the penny or the quarter:")
lastCount = -1
# A copy of moneyCount so we can send a Serial update on changes.
def loop():
  global moneyCount, lastCount
  _, moneyCount = quarterCounter.update(moneyCount)
  # Service the counter periodically
  _, moneyCount = pennyCounter.update(moneyCount)
  # Service the counter periodically
  if lastCount != moneyCount:
    # Yes, the counter changed
    lastCount = moneyCount
    # Make a copy for comparison, then build a string and send it.
    moneyCountStr = "$%d.%02d" % (moneyCount // 100, moneyCount % 100)
    print(moneyCountStr)

setup()
while True:
  loop()
