import usb_cdc

# Expose only one USB CDC serial port for the Serial Wombat bridge.
# The normal CircuitPython console/REPL COM port is disabled.
usb_cdc.enable(console=False, data=True)
