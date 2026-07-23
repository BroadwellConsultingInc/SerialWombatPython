# Converted from PinModes/UART/HardwareUART/HW_UART_EX02_LoopbackTest/HW_UART_EX02_LoopbackTest.ino
import SerialWombat
from ArduinoFunctions import delay, delayMicroseconds, millis
import random

import SerialWombat_interface
# >>> IMPORTANT: Set this to the configured I2C address of your Serial Wombat chip.
SERIAL_WOMBAT_ADDRESS = 0x6B
sw = SerialWombat_interface.SerialWombatChipInstance(SERIAL_WOMBAT_ADDRESS)


# Interface independent code starts here:
import SerialWombatUART

def arduino_random(low, high=None):
  if high is None:
    return random.randrange(low)
  return random.randrange(low, high)

# ===== Arduino tab: HW_UART_EX02_LoopbackTest.ino =====
# sw is provided by the selected Python interface block above
# Declare a Serial Wombat chip
SWUart = SerialWombatUART.SerialWombatUART(sw)
# Declare a Serial Wombat UART  Only one UART can be assigned on the SerialWombat 4B.   On SW8B the rx and tx pins must be 6 and 7
# There is a video tutorial to go with this example at:  https://youtu.be/C1FjcaiBYZs
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
  if not sw.isLatestFirmware():
    print("Firmware version mismatch. Download latest Serial Wombat Arduino Library and update Serial Wombat Firmware to latest version")
  if sw.isSW08() and not sw.isPinModeSupported(SerialWombat.SerialWombatPinMode_t.PIN_MODE_UART_RX_TX):
    print("The required pin mode does not appear to be supported in this firmware build. Do you need to download a different firmware?")
    while 1:
      delay(100)
  # sw.registerErrorHandler(...) is Arduino-specific; Python errors are returned by library calls
  # Register an error handler that will print communication errors to Serial
  # Optional Error handling code end
  print("Start SWUart...")
  SWUart.begin(57600, 1, 0, 1)
  print("Initialization Complete...")
# 32,7,5,3,2,1
MASK = 0x80000057
BUFFER_SIZE = 128
random1 = 6
random2 = 6
iteration = 0
fails = 0
passes = 0
tx = bytearray(BUFFER_SIZE)
rx = bytearray(BUFFER_SIZE)

def next_random(seed):
  """Return a 16-bit value and the updated 32-bit LFSR state."""
  output = 0
  for _ in range(16):
    if seed & 0x00000001:
      seed = ((seed ^ MASK) >> 1) | 0x80000000
    else:
      seed >>= 1
    output = (output << 1) | (seed & 0x01)
  return output & 0xFFFF, seed & 0xFFFFFFFF

def loop():
  global random1, random2, iteration, fails, passes
  while SWUart.read() != -1:
    print("Flush")

  value, random1 = next_random(random1)
  txcount = value % BUFFER_SIZE
  for x in range(txcount):
    value, random1 = next_random(random1)
    tx[x] = value & 0xFF
  SWUart.write(tx, txcount)

  value, random2 = next_random(random2)
  rxcount = value % BUFFER_SIZE
  received = SWUart.readBytes(rxcount)
  received = bytes(received) if received is not None else b""
  mismatch = len(received) != rxcount

  for x in range(rxcount):
    value, random2 = next_random(random2)
    expected = value & 0xFF
    actual = received[x] if x < len(received) else None
    if actual != expected:
      mismatch = True
      fails += 1
      print("Mismatch:", iteration, x, expected, actual)

  if not mismatch:
    passes += 1
    print("P ", passes, " F ", fails)
  iteration += 1

setup()
while True:
  loop()
