import board
import busio
import time

from SerialWombat_interface import SerialWombatChip_cp_i2c

# Initialize I2C
i2c = busio.I2C(board.SCL, board.SDA)

while not i2c.try_lock():
    pass

try:
    devices = i2c.scan()
    i2c.unlock()

    if not devices:
        print("No I2C devices found.")
    else:
        print("I2C devices found:")
        for address in devices:
            print(f"  0x{address:02X}")

        print()

        for address in devices:

            # Only check addresses used by Serial Wombat
            if address < 0x60 or address > 0x6F:
                continue

            print(f"Testing device at 0x{address:02X}...")

            try:
                sw = SerialWombatChip_cp_i2c(address, i2c)
                print ("Initialized")
                result = sw.begin()
                print("begin complete")
                if result >= 0:
                    sw.queryVersion()

                    print("  Serial Wombat detected!")
                    print(f"  Model:            {sw.model.decode('ascii')}")
                    print(f"  Firmware Version: {sw.fwVersion.decode('ascii')}")
                    print(f"  Unique ID:        {sw.uniqueIdentifier}")
                    print(f"  Device Revision:  {sw.deviceRevision}")
                    print(f"  Supply Voltage:   {sw.readSupplyVoltage_mV()} mV")
                else:
                    print("  Device does not appear to be a Serial Wombat chip.")

            except Exception as e:
                print(f"  Error communicating with device: {e}")

            print()

finally:
    i2c.unlock()