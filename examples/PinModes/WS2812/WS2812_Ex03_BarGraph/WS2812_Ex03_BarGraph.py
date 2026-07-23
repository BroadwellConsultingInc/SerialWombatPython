# Converted from PinModes/WS2812/WS2812_Ex03_BarGraph/WS2812_Ex03_BarGraph.ino
import SerialWombat
from ArduinoFunctions import delay, delayMicroseconds, millis

import SerialWombat_interface
# >>> IMPORTANT: Set this to the configured I2C address of your Serial Wombat chip.
SERIAL_WOMBAT_ADDRESS = 0x60
sw = SerialWombat_interface.SerialWombatChipInstance(SERIAL_WOMBAT_ADDRESS)


# Interface independent code starts here:
import SerialWombatAnalogInput
import SerialWombatWS2812

# ===== Arduino tab: WS2812_Ex03_BarGraph.ino =====
ws2812 = SerialWombatWS2812.SerialWombatWS2812(sw)
pot = SerialWombatAnalogInput.SerialWombatAnalogInput(sw)
WS2812_PIN = 15  # Must be an enhanced performance pin: 0,1,2,3,4,7,9,10-19
NUMBER_OF_LEDS = 16
WS2812_USER_BUFFER_INDEX = 0x0000  # Set this to an index into the on-chip user buffer.  Can't overlap with area used by other pins.
# Config:  What data source?  Comment in one
DATA_SOURCE = SerialWombat.SerialWombatDataSource.SW_DATA_SOURCE_PIN_0
# #define DATA_SOURCE SerialWombatDataSource::SW_DATA_SOURCE_FRAMES_RUN_LSW // Increments every 1ms
# #define DATA_SOURCE SerialWombatDataSource::SW_DATA_SOURCE_TEMPERATURE
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
  pot.begin(0,64,0)
  ws2812.begin(WS2812_PIN, NUMBER_OF_LEDS, WS2812_USER_BUFFER_INDEX)
  # Off value = dim red
  # on value = blue
  # Min value 1000
  ws2812.barGraph(DATA_SOURCE, 0x00050000, 0x00000020, 1000, 64000)
  # Max value 64000
def loop():
  pass

setup()
while True:
  loop()
