import SW18B_UnitTest_globals
import SW18B_UnitTest_Analog
import SerialWombatResistanceInput

try:
    from ArduinoFunctions import delay
except ImportError:
    import time

from SW18B_UnitTest_globals import analog1k, analogShutdown




def resistanceInputTest():
    resist16 = SerialWombatResistanceInput.SerialWombatResistanceInput(SW18B_UnitTest_globals.SW18AB_6B)

    for i in range(16, 19 + 1):
        analog1k(i)

        resist16.begin(i)
        delay(100)

        result = resist16.readPublicData()
        s = f"Resistance {i}"
        SW18B_UnitTest_globals.test_value(s, result, 1000, 100, 0)
        analogShutdown()
