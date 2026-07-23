# Converted from PinModes/IRRx/IRRx_ex05_pulseOnChange/IRRx_ex05_pulseOnChange.ino
import SerialWombat
from ArduinoFunctions import delay, delayMicroseconds, millis

import SerialWombat_interface
# >>> IMPORTANT: Set this to the configured I2C address of your Serial Wombat chip.
SERIAL_WOMBAT_ADDRESS = 0x60
sw = SerialWombat_interface.SerialWombatChipInstance(SERIAL_WOMBAT_ADDRESS)


# Interface independent code starts here:
import SerialWombatBlink
import SerialWombatIRRx

# ===== Arduino tab: IRRx_ex05_pulseOnChange.ino =====
#   This example shows how to use the Serial Wombat IR Receive (IRRx) pin mode.  It assumes an NEC compatible IR Transmitter
#      (most inexpensive Arduino kit remotes are compatible) and a 38kHz receiver module that goes low when a modulated IR signal is
#      present.
#
#      This example is compatible with the Serial Wombat 18AB and 8B chips.
#
#
#      In this example commands are received from the pin mode and printed to Serial,
#
#      By default the pin mode provides a command byte as its 16 bit public data value.  However, it can be reconfigured
#      so that the 16 bit public data value increments each time a command (or a repeat code) is received.  A Blink
#      pin mode can then read this value to chirp a buzzer or blink an LED when IR commands are received.  Note that this is
#      more sophisticated than the visible LED on some IR Receivers.  The Serial Wombat Blink pin will only pulse
#      when data is successfully received and decoded.  An LED on an IR Receivers blinks to indicate presense of an IR signal,
#      not successful receiption of an IR packet.
#
#
#      Video on IRRx pin mode:
#
#      TODO coming soon
#
#      SerialWombatIRRx pin mode documentation:
#
#      https://broadwellconsultinginc.github.io/SerialWombatArdLib/class_serial_wombat_i_r_rx.html
# sw is provided by the selected Python interface block above
irrx = SerialWombatIRRx.SerialWombatIRRx(sw)
swBlink = SerialWombatBlink.SerialWombatBlink(sw)
IRRX_PIN = 7
BLINK_PIN = 1
def setup():
  # put your setup code here, to run once:
  # Wire.begin() is handled by the selected Python interface block
  # Initialize the I2C Bus on default pins
  # Serial.begin() is not used in this Python example
  delay(3000)
  print("IR Address Filtering Example")
  sw.begin()  # Python interface was configured above
  # Scan the bus for Serial Wombat chips, and initialize the first one found
  # Optional Error handling code begin:
  if sw.isSW04():
    print("This Example is not supported on the Serial Wombat 4B chip. An 8B or 18AB chip is required.")
    while 1:
      delay(100)
  if not sw.isLatestFirmware():
    print("Firmware version mismatch. Download latest Serial Wombat Arduino Library and update Serial Wombat Firmware to latest version")
  if sw.isSW08() and not (sw.isPinModeSupported(SerialWombat.SerialWombatPinMode_t.PIN_MODE_IRRX) and sw.isPinModeSupported(SerialWombat.SerialWombatPinMode_t.PIN_MODE_BLINK)):
    print("The required pin mode does not appear to be supported in this firmware build. Do you need to download a different firmware?")
    while 1:
      delay(100)
  # sw.registerErrorHandler(...) is Arduino-specific; Python errors are returned by library calls
  # Register an error handler that will print communication errors to Serial
  # Optional Error handling code end
  # Make data count the output
  # Mode 0 : NEC
  # Use repeat
  # Active Low
  # 1000 ms Public Data Timeout
  # Default public data
  # Use Address Filtering
  # Transmitter Address (not used)
  irrx.begin(IRRX_PIN, SerialWombatIRRx.publicDataOutput.DATACOUNT, 0, True, SerialWombat.SerialWombatPinState_t.SW_LOW, 1000, 0xFFFF, False, 0x0000 )
  # irrx.enablePullup(true);   //Comment in this line if your receiver is open drain type without pullup
  swBlink.begin (BLINK_PIN, IRRX_PIN)
  delay(1000)
def loop():
  receivedData = irrx.read()
  if receivedData >= 0:
    print(irrx.readPublicData(), end="")
    print(":", end="")
    print(receivedData)

setup()
while True:
  loop()
