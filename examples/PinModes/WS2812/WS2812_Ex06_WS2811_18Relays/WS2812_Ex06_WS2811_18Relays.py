# Converted from PinModes/WS2812/WS2812_Ex06_WS2811_18Relays/WS2812_Ex06_WS2811_18Relays.ino
import SerialWombat
from ArduinoFunctions import delay, delayMicroseconds, millis

import SerialWombat_interface
# >>> IMPORTANT: Set this to the configured I2C address of your Serial Wombat chip.
SERIAL_WOMBAT_ADDRESS = 0x60
sw = SerialWombat_interface.SerialWombatChipInstance(SERIAL_WOMBAT_ADDRESS)


# Interface independent code starts here:
import SerialWombatWS2812

# ===== Arduino tab: WS2812_Ex06_WS2811_18Relays.ino =====
#
#   This example shows how to control 18 relays using WS2811 breakout boards.  This example assumes that the first relay is
#   attached to R, the 2nd to G, the 3rd to B, and so on for 6 LEDs.  The swapRG member of ws2812 is set to true since
#   the R and G data positions on the WS2811 silicon are swapped compared to the WS2812 silicon.
#
#   The WS2811 does not drive the Relays directly (WS2811s aren't designed for inductive loads), but rather through
#   a relay driver on the relay boards.  Note that the WS2811 is designed to switch the low side of an LED, so it's an open drain
#   style output (active low on, high-impedance off) so the relay board needs to be low-input active.
#
#   Try to keep the power lines running the relays away from the signal line for the WS2811's, as the noise created by the
#   relays' coils may induce glitches if the wires are near the signal line, and this can cause the WS2811's to output unexpected
#   data.
#
#   Relays are binary devices, so we set each LED driver "color" to either 0  (inactive) or 0xFF (active).
#
#
#
#   Change the WS2812_PIN below to fit your circuit.
#
#   A video demonstrating the use of the WS2812b pin mode on the Serial Wombat 18AB chip is available at:
#   //TODO
#
#   Documentation for the SerialWombatTM1637 Arduino class is available at:
#   https://broadwellconsultinginc.github.io/SerialWombatArdLib/class_serial_wombat_w_s2812.html#details
#
ws2812 = SerialWombatWS2812.SerialWombatWS2812(sw)
WS2812_PIN = 19  # Must be an enhanced performance pin: 0,1,2,3,4,7,9,10-19
NUMBER_OF_LEDS = 6
WS2812_USER_BUFFER_INDEX = 0x0000  # Set this to an index into the on-chip user buffer.  Can't overlap with area used by other pins.
ledArray = [0,0,0,0,0,0]
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
  # The Pin connected to WS2812 array
  # The number of LEDs being used
  ws2812.begin(WS2812_PIN, NUMBER_OF_LEDS, WS2812_USER_BUFFER_INDEX)
  # A location in the Serial Wombat chip's user RAM area where LED output signals will be buffered
  ws2812.swapRG = True
  # WS2811 swaps R and G vs WS2812
def loop():
  for x in range(0, 6):
    for i in range(0, 6):
      ledArray[i] = 0
      # Set the color array to all off
    ledArray[x] = 0xFF0000
    # Red
    ws2812.write(0,6,ledArray)
    delay(1000)
    ledArray[x] = 0xFF00
    # Green
    ws2812.write(0,6,ledArray)
    delay(1000)
    ledArray[x] = 0xFF
    # Blue
    ws2812.write(0,6,ledArray)
    delay(1000)
  for i in range(0, 6):
    ledArray[i] = 0
  ws2812.write(0,6,ledArray)
  delay(1000)
  # All LEDs on
  for i in range(0, 6):
    ledArray[i] = 0xFFFFFF
  ws2812.write(0,6,ledArray)
  delay(1000)
  # All LEDs off
  for i in range(0, 6):
    ledArray[i] = 0
  ws2812.write(0,6,ledArray)
  delay(1000)

setup()
while True:
  loop()
