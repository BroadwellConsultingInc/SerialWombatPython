import time
import board
import bitbangio
import digitalio
import memorymap
import usb_cdc


# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------

RECEIVE_TIMEOUT = 2.0

# Serial Wombat devices normally use addresses in this range.
SERIAL_WOMBAT_MIN_ADDRESS = 0x60
SERIAL_WOMBAT_MAX_ADDRESS = 0x6F


# -----------------------------------------------------------------------------
# RP2040 GPIO drive strength
# -----------------------------------------------------------------------------

def rp2040_set_pad_drive(pin_number, drive):
    """
    Set the RP2040 GPIO pad drive strength.

    drive:
        0 = 2 mA
        1 = 4 mA
        2 = 8 mA
        3 = 12 mA

    Note that the RP2040 drive-strength setting is not a current regulator.
    It selects the output driver's strength.
    """

    pads_bank0 = memorymap.AddressRange(
        start=0x4001C000,
        length=0x4000
    )

    # GPIO pad registers begin at offset 0x04 and occupy four bytes each.
    register_offset = pin_number * 4 + 4

    pad_ctrl = int.from_bytes(
        pads_bank0[register_offset:register_offset + 4],
        "little"
    )

    # The DRIVE field is bits 5:4. Calculate which bits must toggle to
    # change the current setting to the requested setting.
    xor_bits = ((pad_ctrl >> 4) & 0x03) ^ (drive & 0x03)
    xor_bits <<= 4

    # RP2040 peripheral registers have an atomic XOR alias at +0x1000.
    xor_offset = register_offset + 0x1000
    pads_bank0[xor_offset:xor_offset + 4] = xor_bits.to_bytes(4, "little")


# -----------------------------------------------------------------------------
# Fixed output pin
# -----------------------------------------------------------------------------

# GP2 is driven HIGH with the 12 mA drive-strength setting.
gp2 = digitalio.DigitalInOut(board.GP2)
gp2.switch_to_output(value=True)
rp2040_set_pad_drive(2, 3)


# -----------------------------------------------------------------------------
# On-board LED
# -----------------------------------------------------------------------------

led = digitalio.DigitalInOut(board.LED)
led.switch_to_output(value=False)


# -----------------------------------------------------------------------------
# I2C setup
# -----------------------------------------------------------------------------

# Raspberry Pi Pico / RP2040:
# GP2 = fixed HIGH (physical pin 4)
# SCL = GP3 (physical pin 5)
# SDA = GP4 (physical pin 6)
#
# bitbangio.I2C is used so the bridge can start even if there are no external
# I2C pull-up resistors present yet. This allows an I2C device to be hot-plugged
# after startup.
#
# If I2C initialization fails for any reason, wait one second and try again.
# The LED stays off while initialization is being retried.
i2c = None

while i2c is None:
    try:
        i2c = bitbangio.I2C(
            scl=board.GP3,
            sda=board.GP4,
            frequency=100000,
            timeout=100000
        )
    except Exception:
        time.sleep(1.0)

# I2C has initialized. Solid LED means the bridge is ready.
led.value = True


# -----------------------------------------------------------------------------
# USB serial setup
# -----------------------------------------------------------------------------

# This is the CDC data port enabled in boot.py.
serial = usb_cdc.data

# Reads should be non-blocking.
serial.timeout = 0


# -----------------------------------------------------------------------------
# Find a Serial Wombat on the I2C bus
# -----------------------------------------------------------------------------

def find_serial_wombat():
    """
    Scan the I2C bus for a Serial Wombat address.

    Returns the first device found between 0x60 and 0x6F.
    Returns 0 if none is found.
    """

    while not i2c.try_lock():
        pass

    try:
        addresses = i2c.scan()
    finally:
        i2c.unlock()

    for address in addresses:
        if SERIAL_WOMBAT_MIN_ADDRESS <= address <= SERIAL_WOMBAT_MAX_ADDRESS:
            return address

    return 0


i2c_address = find_serial_wombat()


# -----------------------------------------------------------------------------
# Packet buffers
# -----------------------------------------------------------------------------

tx = bytearray(9)
rx = bytearray(8)

count = 0
last_receive = time.monotonic()


# -----------------------------------------------------------------------------
# Execute one Serial Wombat transaction
# -----------------------------------------------------------------------------

def execute_packet(address, packet):
    """
    Send an 8-byte Serial Wombat packet over I2C and read the 8-byte response.

    address:
        I2C address of the Serial Wombat.

    packet:
        8-byte bytes/bytearray object.

    Returns:
        An 8-byte bytearray containing the response.
    """

    while not i2c.try_lock():
        pass

    try:
        i2c.writeto(address, packet)

        # Match the Arduino sketch's delayMicroseconds(100).
        time.sleep(0.0001)

        i2c.readfrom_into(address, rx)

    finally:
        i2c.unlock()

    return rx


# -----------------------------------------------------------------------------
# Main loop
# -----------------------------------------------------------------------------

while True:

    # Process everything currently waiting in the USB CDC receive buffer.
    while serial.in_waiting:

        data = serial.read(1)

        if not data:
            break

        x = data[0]
        last_receive = time.monotonic()

        if count > 0:

            tx[count] = x
            count += 1

            if count >= 9:

                try:
                    # If the first byte of the actual Serial Wombat packet is
                    # 0x55, 'x', or space, discard the entire packet.
                    if (
                        tx[1] != 0x55
                        and tx[1] != ord("x")
                        and tx[1] != ord(" ")
                    ):

                        # Address 0xFF means use the automatically detected
                        # Serial Wombat address.
                        if tx[0] != 0xFF:
                            address = tx[0]
                        else:
                            address = i2c_address

                        response = execute_packet(
                            address,
                            memoryview(tx)[1:9]
                        )

                        # Send the 8-byte Serial Wombat response back
                        # to the PC.
                        serial.write(response)

                except OSError:
                    # The Arduino sketch does not define an error protocol,
                    # so don't insert any additional bytes into the stream.
                    pass

                finally:
                    # Packet processing is complete. After the first packet,
                    # LED off means idle.
                    led.value = False
                    count = 0

        else:

            # When waiting for the first byte of a packet, discard
            # synchronization characters.
            if (
                x != 0x55
                and x != ord("x")
                and x != ord(" ")
            ):
                # A new packet has started. Turn the activity LED on.
                led.value = True
                tx[0] = x
                count = 1

    # Throw away a partial packet if no additional byte has arrived
    # for two seconds.
    if count != 0:
        if time.monotonic() - last_receive > RECEIVE_TIMEOUT:
            count = 0
            led.value = False
