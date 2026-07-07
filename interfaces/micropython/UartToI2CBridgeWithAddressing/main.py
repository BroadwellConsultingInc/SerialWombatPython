# Bridge_UART115toI2C_WithAddressing_MicroPython.py
#
# MicroPython port of _Bridge_UART115toI2C_WithAddressing.ino
#
# Purpose:
#   Let a USB-connected Seeed Studio XIAO RP2040 or similar act as a bridge between a host
#   PC USB CDC serial port and an I2C-connected Serial Wombat chip.
#
# Host packet format:
#   9 bytes total:
#       byte 0    = I2C address, or 0xFF to use the auto-detected Serial Wombat address
#       bytes 1-8 = 8-byte Serial Wombat command packet
#
# XIAO RP2040 I2C pins for MicroPython:
#   SDA = D4 = GPIO6
#   SCL = D5 = GPIO7
#   I2C bus = I2C(1) on RP2040
#
# Save this file as main.py on the MicroPython board. The host should open the
# board's USB serial port at 115200 baud. For native USB CDC the baud rate is
# mostly symbolic, but it matches the Arduino sketch and existing host class.

import sys
import time
import select
from machine import I2C, Pin

RECEIVE_TIMEOUT_MS = 2000
I2C_FREQ_HZ = 100000
DEFAULT_SCAN_START = 0x60
DEFAULT_SCAN_END = 0x6F
ERROR_RESPONSE = b"E00048UU"

# Seeed XIAO RP2040 default I2C pins: D4/D5 = GPIO6/GPIO7.
I2C_ID = 1
SDA_PIN = 6
SCL_PIN = 7

# Initial bytes discarded by the Arduino bridge before packet collection starts.
DISCARD_INITIAL = (0x55, ord("x"), ord(" "))


def ticks_elapsed_ms(start, now):
    return time.ticks_diff(now, start)


def find_serial_wombat_address(i2c):
    """Return the first responding I2C address from 0x60 through 0x6F, or 0x60."""
    try:
        devices = i2c.scan()
        for address in range(DEFAULT_SCAN_START, DEFAULT_SCAN_END + 1):
            if address in devices:
                return address
    except OSError:
        pass
    return DEFAULT_SCAN_START


def i2c_write_then_read_8(i2c, address, packet8):
    """Write an 8-byte packet to I2C, then read and return the 8-byte response."""
    try:
        i2c.writeto(address, packet8)
        time.sleep_us(100)
        return i2c.readfrom(address, 8)
    except OSError:
        return ERROR_RESPONSE


def main():
    i2c = I2C(I2C_ID, sda=Pin(SDA_PIN), scl=Pin(SCL_PIN), freq=I2C_FREQ_HZ)
    detected_address = find_serial_wombat_address(i2c)

    poller = select.poll()
    poller.register(sys.stdin, select.POLLIN)

    tx = bytearray(9)
    count = 0
    last_receive = time.ticks_ms()

    while True:
        events = poller.poll(1)
        if events:
            data = sys.stdin.buffer.read(1)
            if data:
                x = data[0]
                last_receive = time.ticks_ms()

                if count > 0:
                    tx[count] = x
                    count += 1

                    if count >= 9:
                        # Match the Arduino behavior: if the first command byte is a
                        # sync/clear byte, discard the whole collected packet.
                        if tx[1] not in DISCARD_INITIAL:
                            address = detected_address if tx[0] == 0xFF else tx[0]
                            response = i2c_write_then_read_8(i2c, address, tx[1:9])
                            sys.stdout.buffer.write(response)
                        count = 0
                else:
                    if x not in DISCARD_INITIAL:
                        tx[0] = x
                        count = 1

        if count > 0 and ticks_elapsed_ms(last_receive, time.ticks_ms()) > RECEIVE_TIMEOUT_MS:
            count = 0


main()
