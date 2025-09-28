"""
Copyright 2025 Broadwell Consulting Inc.

"Serial Wombat" is a registered trademark of Broadwell Consulting Inc. in
the United States.  See SerialWombat.com for usage guidance.

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
"""

import SerialWombat
import SerialWombatPin
import SerialWombatAbstractScaledOutput
from SerialWombat import SW_LE16, SerialWombatPinMode_t

"""! @file SerialWombatFrequencyOutput.py
"""

"""!
\brief A class representing a Serial Wombat Frequency Output 

An instance of this class should be declared for each pin
to be used as a Serial Wombat Frequency Output.  

Serial Wombat 18AB PWM outputs are driven either by hardware peripherals
or by a DMA based software PWM scheme.  Up to 6 hardware PWM outputs are avaialble
on Enhanced Digital Performance pins (0-4,7,9-19).  The first six Enhanced Digitial
Performance pins configured after reset will claim hardware resources.  Any additional
pins configured for Frequency output will use DMA based output.  Hardware capable pins can 
generate high resolution signals up to about 100kHz.  DMA based output is limited
to transitions every 17uS, so a 1kHz output will have about 6 bits of resolution and
a 100 Hz output will have about 9 bit resolution.  Since the DMA runs at only 57600 Hz, 
frequency accuarcy will suffer on DMA pins as frequency increases, unless the desired frequency
is an integer divisor of 57600.

For very slow signals (under 20 Hz) the low frequency option should be used.  Otherwise these signals
cannot be generated.  The low frequency option works on a mS rather than uS timer, so its resolution
becomes increasingly poor at higher frequencies, but may be useful for applications such as simulation of
speedometers or tachometers which operate at relatively low freqeuencies.

A single very high speed frequency output is available on the Serial Wombat 18AB through the
High Speed Clock Output function
"""
class SerialWombatFrequencyOutput(SerialWombatPin.SerialWombatPin):
    def __init__(self, serial_wombat):
        """!
        \brief Constructor for SerialWombatFrequencyOutput class
        \param serial_wombat SerialWombat chip on which the FrequencyOutput will run
        """
        super().__init__(serial_wombat)

    def begin(self, pin, maxFrequency_Hz = 65535, lowFrequency = False, dutyCycle = 0x8000):
        """!
        \brief Initialize a pin that has been declared as FrequencyOutput. 
        
        \param pin Pin to use for Frequency Output.  Use an enhanced Digital Capability pin for high frequencies
        \param maxFrequency_Hz Maximum frequency to be output (used to pick best timing hardware)
        \param lowFrequency  Set to true if signals slower than 20Hz need to be generated.  
                             Has negative effect on higher frequencies
        \param dutyCycle  Duty cycle of frequency to be output
        \return A nonnegative result on success, or a negative error code
        """
        self._pin = pin
        self._pinMode = SerialWombatPinMode_t.PIN_MODE_FREQUENCY_OUTPUT
        return self.initPacketNoResponse(
            0,
            SW_LE16(dutyCycle),
            SW_LE16(maxFrequency_Hz),
            1 if lowFrequency else 0
        )


"""!
\brief Extends the SerialWombatFrequencyOutput class with SW18AB specific functionality, including SerialWombatAbstractScaledOutput
"""
class SerialWombatFrequencyOutput_18AB(SerialWombatFrequencyOutput, SerialWombatAbstractScaledOutput.SerialWombatAbstractScaledOutput):
    def __init__(self, serial_wombat):
        SerialWombatFrequencyOutput.__init__(self, serial_wombat)
        SerialWombatAbstractScaledOutput.SerialWombatAbstractScaledOutput.__init__(self, serial_wombat)

    def pin(self):
        """!
        \brief fulfills a virtual function requirement of SerialWombatAbstractScaledOutput
        \return current pin number
        """
        return self._pin

    def swPinModeNumber(self):
        """!
        \brief fulfills a virtual function requirement of SerialWombatAbstractScaledOutput
        \return current pin mode number
        """
        return self._pinMode

