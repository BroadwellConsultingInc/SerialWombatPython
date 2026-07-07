"""
Copyright 2024-2025 Broadwell Consulting Inc.

"Serial Wombat" is a registered trademark of Broadwell Consulting Inc. in
the United States.  See SerialWombat.com for usage guidance.

Permission is hereby granted, free of charge, to any person obtaining a
 * copy of this software and associated documentation files (the "Software"),
 * to deal in the Software without restriction, including without limitation
 * the rights to use, copy, modify, merge, publish, distribute, sublicense,
 * and/or sell copies of the Software, and to permit persons to whom the
 * Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
 * THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
 * OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
 * ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
 * OTHER DEALINGS IN THE SOFTWARE.
"""

import SerialWombat
import SerialWombatPin
import SerialWombatAbstractScaledOutput
from SerialWombat import SW_LE16
from SerialWombat import SerialWombatPinMode_t

"""! @file SerialWombatHBridge.py
"""

"""!
@brief A class representing a Serial Wombat H Bridge Output

An instance of this class should be declared for each pair of pins
to be used as a Serial Wombat H Bridge.

This module mirrors the style of `SerialWombatServo.py` to ease diff-based review
and side-by-side comparison.
"""

class SerialWombatHBridgeDriverMode:
    """!
    @brief Driver mode selection for the H-Bridge pin mode.

    The mode determines how the two pins are driven when the H-Bridge is off and how
    the bridge is controlled (relay-style or PWM-style when on).

    - HBRIDGE_OFF_BOTH_LOW: Both outputs are driven low when off.
    - HBRIDGE_OFF_BOTH_HIGH: Both outputs are driven high when off.
    - HBRIDGE_RELAY_AND_PWM: One pin acts as a relay direction control, the other uses PWM.
    """
    HBRIDGE_OFF_BOTH_LOW = 0
    HBRIDGE_OFF_BOTH_HIGH = 1
    HBRIDGE_RELAY_AND_PWM = 2


class SerialWombatHBridge(SerialWombatPin.SerialWombatPin):
    """!
    @brief Serial Wombat H-Bridge controller pin mode wrapper.

    This class configures a pair of Serial Wombat pins as an H-Bridge and sets the
    PWM period used to modulate the bridge. Instantiate one object per H-Bridge pair.
    """

    def __init__(self, serial_wombat):
        """!
        @brief Constructor for SerialWombatHBridge class
        @param serial_wombat SerialWombat chip on which the H-Bridge will run
        """
        super().__init__(serial_wombat)

    def begin(self, pin, secondPin, PWMPeriod_uS = 1000, driverMode = SerialWombatHBridgeDriverMode.HBRIDGE_OFF_BOTH_LOW):
        """!
        @brief Initialize two pins as an H-Bridge pair.

        This function must be called after the SerialWombatChip instance specified in the constructor
        has been initialized with a begin call.

        @param pin The first Serial Wombat pin to become the H-Bridge control.
        @param secondPin The second Serial Wombat pin to become the H-Bridge control.
        @param PWMPeriod_uS A value representing the period of the PWM duty cycle in microseconds.
        @param driverMode The driver mode to use (see SerialWombatHBridgeDriverMode).
        @return A negative value on error, or a non-negative status/result code on success.
        """
        self._pin = pin
        self._pinMode = SerialWombatPinMode_t.PIN_MODE_HBRIDGE

        # First stage: pair the pins and set driver mode. Mirrors C++ initPacketNoResponse(0, secondPin, driverMode).
        # The base class may provide initPacketNoResponse; if not, send a raw CONFIGURE_PIN_MODE_0 packet.
        result = self.initPacketNoResponse(0, secondPin, int(driverMode))
        if result is not None and result < 0:
            return result

        # Second stage: set PWM period via CONFIGURE_PIN_MODE_HW_0
        # Packet: [CONFIGURE_PIN_MODE_HW_0, pin, mode, period_L, period_H, 0x55, 0x55, 0x55]
        opcode_hw0 = getattr(SerialWombat.SerialWombatCommands, 'CONFIGURE_PIN_MODE_HW_0', 201)
        tx1 = bytearray([opcode_hw0, self._pin, self._pinMode]) + SW_LE16(PWMPeriod_uS) + bytearray([0x55, 0x55, 0x55])
        result_hw0, _ = self._sw.sendPacket(tx1)
        return result_hw0





class SerialWombatHBridge_18AB(SerialWombatHBridge, SerialWombatAbstractScaledOutput.SerialWombatAbstractScaledOutput):
    """!
    @brief Extends SerialWombatHBridge with SW18AB-specific functionality, including SerialWombatAbstractScaledOutput.

    This class fulfills the abstract scaled-output interface methods so it can be used with the
    scaling framework present on the 18AB device family.
    """

    def __init__(self, serial_wombat):
        SerialWombatHBridge.__init__(self, serial_wombat)
        SerialWombatAbstractScaledOutput.SerialWombatAbstractScaledOutput.__init__(self, serial_wombat)
        self._asosw = serial_wombat

    def pin(self):
        """!
        @brief Fulfills a virtual function requirement of SerialWombatAbstractScaledOutput.
        @return Current pin number.
        """
        return self._pin

    def swPinModeNumber(self):
        """!
        @brief Fulfills a virtual function requirement of SerialWombatAbstractScaledOutput.
        @return Current pin mode number.
        """
        return self._pinMode
