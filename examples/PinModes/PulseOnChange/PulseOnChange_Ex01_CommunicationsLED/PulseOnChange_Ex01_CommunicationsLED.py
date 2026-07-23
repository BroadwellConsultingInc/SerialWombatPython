# Converted from PinModes/PulseOnChange/PulseOnChange_Ex01_CommunicationsLED/PulseOnChange_Ex01_CommunicationsLED.ino
import SerialWombat
from ArduinoFunctions import delay, delayMicroseconds, millis

import SerialWombat_interface
# >>> IMPORTANT: Set this to the configured I2C address of your Serial Wombat chip.
SERIAL_WOMBAT_ADDRESS = 0x60
sw = SerialWombat_interface.SerialWombatChipInstance(SERIAL_WOMBAT_ADDRESS)


# Interface independent code starts here:
import SerialWombatPulseOnChange

# ===== Arduino tab: PulseOnChange_Ex01_CommunicationsLED.ino =====
#
#   This example shows how create an output that pulses high when the Serial Wombat 8B or 18AB Chip
#   receives a communication packet.  This allows easy creation of a communication LED.
#
#   This example assumes an LED with appropriate current limiting resistor is attached to a pin of the Serial Wombat
#   chip.
#
#   The pulse on change pin mode looks at other pins or public 16-bit data to determine when to pulse.
#
#   Data providers 0-63 correspond to physical pins on the Serial Wombat chip (only 0-19 are implemented on
#   the SW18AB).  64 and up correspond to system values.
#
#   Avaialble public data is enumerated in the firmware (not all values suppored by all chips):
#   https://github.com/BroadwellConsultingInc/SerialWombat/blob/main/SerialWombatCommon/serialWombat.h
#
#   which is also available as an enumeration in the Arduino Library SerialWombatDataSource enum:
#   https://broadwellconsultinginc.github.io/SerialWombatArdLib/_serial_wombat_8h.html#aa93a00ab6275924ab4d521604780f6fa
#
#
#   In this case we will use SW_DATA_SOURCE_PACKETS_RECEIVED (enum value 71) which changes each time a packet
#   addressed to this Serial Wombat chip is received.
#
#   We will pulse the LED high for 50mS with a delay of 50mS for low time (The default values).
#
#   Each Pulse on Change pin has up to 4 state machine entries that can cause the pin to become active.  This is
#   useful if you want to have more than one source capable of driving a pulse (such as multiple buttons leading to a
#   feedback led or piezo).
#
#   For this example we will only use one which will be configured to pulse on change of SW_DATA_SOURCE_PACKETS_RECEIVED.
#
#
#
#   Documentation for the SerialWombatPulseOnChange Arduino class is available at:
#   https://broadwellconsultinginc.github.io/SerialWombatArdLib/class_serial_wombat_pulse_on_change.html#details
#
# sw is provided by the selected Python interface block above
poc = SerialWombatPulseOnChange.SerialWombatPulseOnChange(sw)
PULSE_ON_CHANGE_PIN = 1
def setup():
  # put your setup code here, to run once:
  # Wire.begin() is handled by the selected Python interface block
  # Initialize the I2C Bus on default pins
  # Serial.begin() is not used in this Python example
  delay(3000)
  print("Pulse on Change Example")
  sw.begin()  # Python interface was configured above
  # Scan the bus for Serial Wombat chips, and initialize the first one found
  # Optional Error handling code begin:
  if sw.isSW04():
    print("This Example is not supported on the Serial Wombat 4B chip. An 8B or 18AB chip is required.")
    while 1:
      delay(100)
  if not sw.isLatestFirmware():
    print("Firmware version mismatch. Download latest Serial Wombat Arduino Library and update Serial Wombat Firmware to latest version")
  if sw.isSW08() and not sw.isPinModeSupported(SerialWombat.SerialWombatPinMode_t.PIN_MODE_PULSE_ON_CHANGE):
    print("The required pin mode does not appear to be supported in this firmware build. Do you need to download a different firmware?")
    while 1:
      delay(100)
  # sw.registerErrorHandler(...) is Arduino-specific; Python errors are returned by library calls
  # Register an error handler that will print communication errors to Serial
  # Optional Error handling code end
  poc.begin ( PULSE_ON_CHANGE_PIN)
  # Implied values active high, inactive low, 50mS pulse time, 50mS pulse off, OR entries, No PWM
  # first entry (valid values are 0-7)
  poc.setEntryOnChange(0, SerialWombat.SerialWombatDataSource.SW_DATA_SOURCE_PACKETS_RECEIVED)
  # The data source we're monitoring for change
def loop():
  # Cause 3 packets to be sent
  for i in range(0, 3):
    x = sw.readPublicData(SerialWombat.SerialWombatDataSource.SW_DATA_SOURCE_PACKETS_RECEIVED)
    print(x)
  # then delay
  delay(1000)

setup()
while True:
  loop()
