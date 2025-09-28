"""
Copyright 2024 Broadwell Consulting Inc.

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
from SerialWombat import SerialWombatCommands, SW_LE16
import SerialWombatQueue

"""! @file SerialWombat18ABDataLogger.py
"""

class DataLoggerPeriod:
    """!
    @brief Period choices for data logger sampling intervals
    """
    PERIOD_1024mS = 10
    PERIOD_512mS  = 9
    PERIOD_256mS  = 8
    PERIOD_128mS  = 7
    PERIOD_64mS   = 6
    PERIOD_32mS   = 5
    PERIOD_16mS   = 4
    PERIOD_8mS    = 3
    PERIOD_4mS    = 2
    PERIOD_2mS    = 1
    PERIOD_1mS    = 0


"""!
\brief A Class representing the Serial Wombat 18AB Data Logger module
"""
class SerialWombat18ABDataLogger:
    def __init__(self, serial_wombat):
        """!
        \brief Constructor for SerialWombat18ABDataLogger class
        \param serial_wombat SerialWombat chip on which the driver will run
        """
        self._sw = serial_wombat

    def begin(self, queueAddress, queueSizeBytes, queueFrameIndex,
              queueOnChange = False, period = DataLoggerPeriod.PERIOD_1mS):
        """!
        \brief Initialize the Serial Wombat Data logger.  
        It will create a queue with the given parameters

        \param queueAddress  Index in User RAM area of the Queue to be created
        \param queueSizeBytes The length in bytes of available queue space
        \param queueFrameIndex Whether or not to queue the 16-bit frame number before each entry
        \param queueOnChange  True: log on data change, False: log on time
        \param period The time between entries if queueOnChange is False
        \return A nonnegative result on success, or a negative error code
        """
        swq = SerialWombatQueue.SerialWombatQueue(self._sw)
        result = swq.begin(queueAddress, queueSizeBytes)
        if result < 0:
            return result
        tx = bytearray([
            SerialWombatCommands.COMMAND_BINARY_CONFIG_DATALOGGER,
            0,   # Initial Config
        ]) + SW_LE16(queueAddress) + bytearray([
            int(period),
            1 if queueFrameIndex else 0,
            1 if queueOnChange else 0
        ])
        result, _ = self._sw.sendPacket(tx)
        return result

    def enable(self, enable = True):
        """!
        \brief Enable or disable the data logger

        \param enable True = enable, False = disable
        \return A nonnegative result on success, or a negative error code
        """
        tx = bytearray([
            SerialWombatCommands.COMMAND_BINARY_CONFIG_DATALOGGER,
            1,  # Logger total enable/disable
            1 if enable else 0
        ])
        result, _ = self._sw.sendPacket(tx)
        return result

    def configurePin(self, pin, queueLowByte, queueHighByte):
        """!
        \brief Configure individual pins for data logging

        \param pin Pin number to configure
        \param queueLowByte True if low byte of pin data should be queued
        \param queueHighByte True if high byte of pin data should be queued
        \return A nonnegative result on success, or a negative error code
        """
        tx = bytearray([
            SerialWombatCommands.COMMAND_BINARY_CONFIG_DATALOGGER,
            2,   # Configure individual pins
            pin,
            1 if queueLowByte else 0,
            1 if queueHighByte else 0
        ])
        result, _ = self._sw.sendPacket(tx)
        return result

