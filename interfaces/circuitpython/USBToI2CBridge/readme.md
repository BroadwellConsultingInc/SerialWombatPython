# Serial Wombat USB-to-I2C Bridge for Raspberry Pi Pico

This CircuitPython bridge allows a **Raspberry Pi Pico** to act as a USB-to-I2C interface for use with the **SerialWombatPanel** application.

SerialWombatPanel releases are available here:

https://github.com/BroadwellConsultingInc/SerialWombatCsharpLib/tree/main/WombatPanelReleases

A Raspberry Pi Pico board can be purchased here:

https://www.amazon.com/dp/B0BDLHMQ9C

## Install CircuitPython

1. Disconnect the Raspberry Pi Pico from USB.
2. Hold down the **BOOTSEL** button on the Pico.
3. While continuing to hold BOOTSEL, plug the Pico into the computer.
4. Release the BOOTSEL button.
5. The Pico should appear as a USB drive named `RPI-RP2`.
6. Download the CircuitPython firmware for the Raspberry Pi Pico from:

   https://circuitpython.org/board/raspberry_pi_pico/

7. Copy the downloaded CircuitPython `.uf2` file onto the `RPI-RP2` drive.
8. The Pico will reboot automatically and should then appear as a drive named `CIRCUITPY`.

## Install the Serial Wombat Bridge

Download `boot.py` and `code.py` from:

https://github.com/BroadwellConsultingInc/SerialWombatPython/tree/main/interfaces/circuitpython/USBToI2CBridge

Copy both files to the root directory of the `CIRCUITPY` drive.

After copying the files:

1. Unplug the Raspberry Pi Pico.
2. Plug it back in.
3. The bridge software will start automatically.

`boot.py` configures the Pico USB serial interface, and `code.py` runs automatically at startup and performs the USB-to-I2C bridge function.

## Wiring

Connect the Serial Wombat to the Raspberry Pi Pico as follows:

| Serial Wombat Pin | Raspberry Pi Pico Physical Pin | Pico GPIO / Function |
|---|---:|---|
| GND | Pin 3 | GND |
| VDD | Pin 36 (or pin 4 for programming only) Pin 4 | 3V3OUT (or GP2) |
| SCL | Pin 5 | GP3 |
| SDA | Pin 6 | GP4 |

Pull up resistors from SCL and SDA to VDD are necessary.  These can be added directly on the Serial Wombat board, or externally. 2.2k ohm is recommended.  

The bridge firmware drives **GP2 high** and uses it as the VDD connection shown above. GP3 is the I2C clock line and GP4 is the I2C data line.

## Using the Bridge

1. Connect the Serial Wombat to the Pico using the wiring table above.
2. Connect the Pico to the Windows PC over USB.
3. Start **SerialWombatPanel**.
4. Select the COM port associated with the Pico USB bridge.
5. Use SerialWombatPanel normally to communicate with the attached Serial Wombat over I2C.

The bridge receives Serial Wombat packets over USB serial, sends them to the Serial Wombat over I2C, reads the response, and returns the response packet to the host application.

## Status LED

The Pico onboard LED is used as a bridge status/activity indicator:

- **Solid ON after I2C initialization**: bridge is ready.
- **Turns ON when a host packet begins**.
- **Turns OFF after the response has been returned to the host**.

## I2C Behavior

The bridge uses CircuitPython bit-banged I2C on:

- **SCL: GP3**
- **SDA: GP4**

The I2C clock-stretch timeout is configured for **100 ms**.

Bit-banged I2C is used so the Pico can initialize even if no I2C device is connected at startup, allowing an I2C device to be connected afterward.

## Power Note

GP2 is a GPIO output, not a dedicated power-supply pin. The current bridge firmware configures GP2 as a high output with the RP2040 12 mA drive-strength setting. Use this connection only when the attached Serial Wombat configuration is appropriate for the available GPIO output current. For higher-current loads, power the Serial Wombat from a suitable external supply and connect the grounds together.

This option is available because it allows easy connection of many Serial Wombat boards with a 4 parallel wires, since many Serial Wombat boards use GND-Vdd-SCL-SDA pin order.  This is convenient for lightweight experimentation of boards, or configuring them to be Serial Wombat Widgets.
