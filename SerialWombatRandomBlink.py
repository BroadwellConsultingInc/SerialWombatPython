"""
Copyright 2026 Broadwell Consulting Inc.

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

"""! @file SerialWombatRandomBlink.py
"""

import SerialWombat
from SerialWombat import SW_LE16
from SerialWombatPin import SerialWombatPin
from SerialWombatAbstractScaledOutput import SerialWombatAbstractScaledOutput


class SerialWombatRandomBlink(SerialWombatAbstractScaledOutput):
    """!
    @brief A class representing a Serial Wombat Random Blink output

    An instance of this class should be declared for each pin to be used as a
    Serial Wombat Random Blink output.

    This pin mode is intended for use in decorative situations such as train sets,
    cosplay, holiday decorations, props, and other applications where lights blink
    in a random pattern.   Clearly this is easily implmeneted in any microcontroller
    or software system, but this pin mode provides a convenient way to achieve this
    without needing to burden the main host controller.

    The Random Blink pin mode alternates between an on state and an off state.
    The duration of each state is chosen randomly between configured minimum and
    maximum values.  The PWM value used during each state is also chosen randomly
    between configured minimum and maximum values.

    The firmware runs the PWM output at 120 Hz.  PWM values are 16-bit values from
    0 to 65535, with 0 being fully off and 65535 being fully on.

    By default the pins are configured as hard driving outputs, but they can also
    be configured as open drain outputs.  If this is the case, the output scaling
    module can be used to invert output so that 65535 remains "on".

    The scaled output filtering module can be used to make the output ramp from
    off to on rather than a hard blink.
    """

    def __init__(self, serial_wombat):
        """!
        @brief Constructor for SerialWombatRandomBlink class
        @param serial_wombat Serial Wombat chip on which the Random Blink will run
        """
        SerialWombatPin.__init__(self, serial_wombat)
        SerialWombatAbstractScaledOutput.__init__(self, serial_wombat)

    def begin(self, pin, onTimeMax, offTimeMax, onTimeMin=0, offTimeMin=0,
              onPWMMin=0xFFFF, onPWMMax=0xFFFF, offPWMMin=0, offPWMMax=0):
        """!
        @brief Initialize a pin as Random Blink with common LED defaults.

        @param pin The pin to become a Random Blink output.
        @param onTimeMax Maximum randomly selected on time.
        @param offTimeMax Maximum randomly selected off time.
        @param onTimeMin Minimum randomly selected on time.
        @param offTimeMin Minimum randomly selected off time.
        @param onPWMMin Minimum randomly selected PWM value during the on state.
        @param onPWMMax Maximum randomly selected PWM value during the on state.
        @param offPWMMin Minimum randomly selected PWM value during the off state.
        @param offPWMMax Maximum randomly selected PWM value during the off state.
        @return 0 or a positive value if successful, otherwise negative error code.
        """
        self._pin = pin
        self._pinMode = SerialWombat.SerialWombatPinMode_t.PIN_MODE_RANDOMBLINK

        result = self.initPacketNoResponse(0, SW_LE16(onTimeMax), SW_LE16(offTimeMax))
        if result < 0:
            return result

        result = self.initPacketNoResponse(1, SW_LE16(onPWMMin), SW_LE16(onPWMMax))
        if result < 0:
            return result

        result = self.initPacketNoResponse(2, SW_LE16(offPWMMin), SW_LE16(offPWMMax))
        if result < 0:
            return result

        return self.initPacketNoResponse(3, SW_LE16(onTimeMin), SW_LE16(offTimeMin))

    def pin(self):
        """!
        @brief fulfills a virtual function requirement of SerialWombatAbstractScaledOutput
        @return current pin number
        """
        return self._pin

    def swPinModeNumber(self):
        """!
        @brief fulfills a virtual function requirement of SerialWombatAbstractScaledOutput
        @return current pin mode number
        """
        return self._pinMode
