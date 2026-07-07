import machine
import time

from SerialWombat_interface import SerialWombatChip_mp_i2c

# Adjust pins/frequency as needed for your board
i2c = machine.I2C(1, scl=machine.Pin(7), sda=machine.Pin(6), freq=100000)

devices = i2c.scan()

if not devices:
    print("No I2C devices found.")
    print("Are scl and sda pins correct?  There are multiple I2C busses on some devices")
else:
    print("I2C devices found:")
    for address in devices:
        print("  0x%02X" % address)

    print()

    for address in devices:
        if address < 0x60 or address > 0x6F:
            continue

        print("Testing device at 0x%02X..." % address)

        try:
            sw = SerialWombatChip_mp_i2c(address, i2c)

            result = sw.begin()

            if result >= 0:
                sw.queryVersion()

                print("  Serial Wombat Chip detected!")
                print("  Model:            %s" % sw.model.decode("ascii"))
                print("  Firmware Version: %s" % sw.fwVersion.decode("ascii"))
                print("  Unique ID:        %s" % sw.uniqueIdentifier)
                print("  Device Revision:  %s" % sw.deviceRevision)
                print("  Supply Voltage:   %d mV" % sw.readSupplyVoltage_mV())
            else:
                print("  Device does not appear to be a Serial Wombat chip.")

        except Exception as e:
            print("  Error communicating with device: %s" % e)

        print()