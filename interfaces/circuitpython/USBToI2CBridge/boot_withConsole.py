import usb_cdc

# Keep the normal CircuitPython console and also create a separate
# USB CDC data port for the Serial Wombat bridge.
usb_cdc.enable(console=True, data=True)
