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

class SerialWombatAbstractButton:
    """!
    @brief Common button interface for debounced inputs, cap touch and matrix keys.

    Subclasses supply the measurements.  SerialWombatButtonCounter can work
    with any object implementing these methods; no abc dependency is needed
    on MicroPython or CircuitPython.
    """
    def __init__(self, serial_wombat = None):
        self.transitions = 0

    def digitalRead(self):
        """! @brief Read the logical button state. @return True when active. """
        raise NotImplementedError

    def readDurationInTrueState_mS(self):
        """! @brief Read active duration. @return Milliseconds, or 0 if inactive. """
        raise NotImplementedError

    def readDurationInFalseState_mS(self):
        """! @brief Read inactive duration. @return Milliseconds, or 0 if active. """
        raise NotImplementedError

    def readTransitionsState(self, resetTransitionCounts = True):
        """!
        @brief Update transitions and return the current logical state.
        @param resetTransitionCounts Whether to clear the firmware transition count.
        @return True when active.
        """
        raise NotImplementedError
