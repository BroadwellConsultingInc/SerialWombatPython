import SerialWombat

class SerialWombatPin:
    _sw = 0 # will be serial wombat
    _pin = 255
    _pinMode = 255
    def __init__(self,sw):
        self._sw = sw

    def readPublicData(self):
        return self._sw.readPublicData(self._pin)

    def writePublicData(self,value):
        return self._sw.writePublicData(self._pin,value)

    def pinMode(self,mode, pullDown = False, openDrain = False):
        self._sw.pinMode(self._pin,mode, pullDown,openDrain)

    def digitalWrite(self,val):
        self._sw.digitalWrite(self._pin,val)

    def digitalRead(self):
        return self._sw.digitalRead(self._pin)

    def pin(self):
        return self._pin

    def swPinModeNumber(self):
        return (self._pinMode)

    def _flattenPacketBytes(self, values):
        data = bytearray()
        for value in values:
            if isinstance(value, (bytes, bytearray)):
                data += bytearray(value)
            elif isinstance(value, (list, tuple)):
                data += bytearray(value)
            else:
                data.append(int(value) & 0xFF)
        return data

    def initPacketNoResponse(self, packetNumber, *params):
        tx = bytearray([200 + packetNumber, self._pin, self._pinMode])
        tx += self._flattenPacketBytes(params)
        while len(tx) < 8:
            tx.append(0x55)
        tx = tx[:8]
        return self._sw.sendPacketNoResponse(tx)

    def disable(self):
        tx = bytearray([219, self._pin, self._pinMode, 0x55, 0x55, 0x55, 0x55, 0x55])
        result, rx = self._sw.sendPacket(tx)
        return result

    def enablePullup(self, enabled = True):
        tx = bytearray([SerialWombat.SerialWombatCommands.COMMAND_SET_PIN_HW, self._pin, 0, 1 if enabled else 0, 0x55, 0x55, 0x55, 0x55])
        result, rx = self._sw.sendPacket(tx)
        return result

    def enablePulldown(self, enabled = True):
        tx = bytearray([SerialWombat.SerialWombatCommands.COMMAND_SET_PIN_HW, self._pin, 1, 1 if enabled else 0, 0x55, 0x55, 0x55, 0x55])
        result, rx = self._sw.sendPacket(tx)
        return result

    def enableOpenDrain(self, enabled = True):
        tx = bytearray([SerialWombat.SerialWombatCommands.COMMAND_SET_PIN_HW, self._pin, 2, 1 if enabled else 0, 0x55, 0x55, 0x55, 0x55])
        result, rx = self._sw.sendPacket(tx)
        return result

    def forceDMA(self, enabled = True):
        tx = bytearray([SerialWombat.SerialWombatCommands.COMMAND_SET_PIN_HW, self._pin, 3, 1 if enabled else 0, 0x55, 0x55, 0x55, 0x55])
        result, rx = self._sw.sendPacket(tx)
        return result

    def setPinNumberForTesting(self, pin):
        self._pin = pin

