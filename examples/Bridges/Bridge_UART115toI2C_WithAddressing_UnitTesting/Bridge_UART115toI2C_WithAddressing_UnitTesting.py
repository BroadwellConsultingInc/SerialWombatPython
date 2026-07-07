# Converted from Bridges/Bridge_UART115toI2C_WithAddressing_UnitTesting/Bridge_UART115toI2C_WithAddressing_UnitTesting.ino
import SerialWombat
from ArduinoFunctions import delay, delayMicroseconds, millis

# Import constants from the SerialWombat module so names match the Arduino examples.
for _name in dir(SerialWombat.SerialWombatPinMode_t):
    if _name.startswith("PIN_MODE_"):
        globals()[_name] = getattr(SerialWombat.SerialWombatPinMode_t, _name)
for _name in dir(SerialWombat.SerialWombatDataSource):
    if _name.startswith("SW_DATA_"):
        globals()[_name] = getattr(SerialWombat.SerialWombatDataSource, _name)
PERIOD_1mS = 0; PERIOD_2mS = 1; PERIOD_4mS = 2; PERIOD_8mS = 3; PERIOD_16mS = 4; PERIOD_32mS = 5; PERIOD_64mS = 6; PERIOD_128mS = 7; PERIOD_256mS = 8; PERIOD_512mS = 9; PERIOD_1024mS = 10
HC_SR04 = 0
RAW = 0; AVERAGE = 1; FILTERED = 2; MINIMUM = 3; MAXIMUM = 4
DATACOUNT = 2; ADDRESS = 3; COMMAND = 4

#Comment these lines in if you're connecting directly to a Serial Wombat Chip's UART through cPython serial Module
#Change the parameter of SerialWombatChip_cpy_serial to match the name of your Serial port
#import SerialWombat_cpy_serial
#sw = SerialWombat_cpy_serial.SerialWombatChip_cpy_serial("COM25")

#Comment these lines in if you're connecting to a Serial Wombat Chip's I2C port using cPython smbus2
#Change busNumber and swI2Caddress to match your configuration
#import SerialWombat_smbus2_i2c
#busNumber = 1
#swI2Caddress = 0x6B
#sw = SerialWombat_smbus2_i2c.SerialWombatChip_smbus2_i2c(busNumber, swI2Caddress)

#Comment these lines in if you're connecting to a Serial Wombat Chip's I2C port using CircuitPython's I2C interface
#Change sclPin, sdaPin, and swI2Caddress to match your configuration
#import board
#import busio
#import SerialWombat_cp_i2c
#swI2Caddress = 0x6B
#i2c = busio.I2C(board.SCL, board.SDA)
#sw = SerialWombat_cp_i2c.SerialWombatChip_cp_i2c(i2c, swI2Caddress)

#Comment these lines in if you're connecting to a Serial Wombat Chip's I2C port using Micropython's I2C interface
#Change the values for sclPin, sdaPin, and swI2Caddress to match your configuration
#import machine
#import SerialWombat_mp_i2c
#sclPin = 22
#sdaPin = 21
#swI2Caddress = 0x6B
#i2c = machine.I2C(0,
#            scl=machine.Pin(sclPin),
#            sda=machine.Pin(sdaPin),
#            freq=100000,timeout = 50000)
#sw = SerialWombat_mp_i2c.SerialWombatChip_mp_i2c(i2c,swI2Caddress)
#sw.address = swI2Caddress

#Comment these lines in if you're connecting to a Serial Wombat Chip's UART port using Micropython's UART interface
#Change the values for UARTnum, txPin, and rxPin to match your configuration
import machine
import SerialWombat_mp_UART
txPin = 12
rxPin = 14
UARTnum = 2
uart = machine.UART(UARTnum, baudrate=115200, tx=txPin, rx=rxPin)
sw = SerialWombat_mp_UART.SerialWombatChipUART(uart)

#Interface independent code starts here:

#
#This sketch is designed to allow UART communication with an I2C based Serial Wombat chip.
#It is a superset of the the normal version that includes a failure toggle pin, and support for MCP4728 chips
#
#It discards any 0x55, ' ' or 'x' initial bytes, then waits until 8 bytes are received,
#sends that as an I2C packet, and then sends the response back to the UART.
#

SWC = SerialWombat.SerialWombatChip()
i2cAddress = 0
# TODO_MANUAL_CONVERSION: uint8_t tx[9], rx[8], count
# TODO_MANUAL_CONVERSION: SoftWire softWire(2,3)

MCP4728_ADDR = 0x60
SW_FAILURE_PIN = 8  # If this #define is enabled, this pin will toggle when a 0x40 unit test failure packet is sent
# This is designed for internal unit testing with a specialized PCB board.

def setAnalogRatio(pin, ratio):
  # TODO_MANUAL_CONVERSION: switch (pin) {
    # TODO_MANUAL_CONVERSION: case 0:
      softWire.beginTransmission(MCP4728_ADDR)
      softWire.write(0x40)
      softWire.write((ratio >> 12))
      softWire.write((ratio >> 4))
      softWire.endTransmission()
      # TODO_MANUAL_CONVERSION: break

      # TODO_MANUAL_CONVERSION: case 7:
        # TODO_MANUAL_CONVERSION_INDENT: softWire.beginTransmission(MCP4728_ADDR)
        # TODO_MANUAL_CONVERSION_INDENT: softWire.write(0x42)
        # TODO_MANUAL_CONVERSION_INDENT: softWire.write((ratio >> 12))
        # TODO_MANUAL_CONVERSION_INDENT: softWire.write((ratio >> 4))
        # TODO_MANUAL_CONVERSION_INDENT: softWire.endTransmission()
        # TODO_MANUAL_CONVERSION_INDENT: break

        # TODO_MANUAL_CONVERSION_INDENT: case 9:
          # TODO_MANUAL_CONVERSION_INDENT: softWire.beginTransmission(MCP4728_ADDR)
          # TODO_MANUAL_CONVERSION_INDENT: softWire.write(0x44)
          # TODO_MANUAL_CONVERSION_INDENT: softWire.write((ratio >> 12))
          # TODO_MANUAL_CONVERSION_INDENT: softWire.write((ratio >> 4))
          # TODO_MANUAL_CONVERSION_INDENT: softWire.endTransmission()
          # TODO_MANUAL_CONVERSION_INDENT: break

          # TODO_MANUAL_CONVERSION_INDENT: case 6:
            # TODO_MANUAL_CONVERSION_INDENT: softWire.beginTransmission(MCP4728_ADDR)
            # TODO_MANUAL_CONVERSION_INDENT: softWire.write(0x46)
            # TODO_MANUAL_CONVERSION_INDENT: softWire.write((ratio >> 12))
            # TODO_MANUAL_CONVERSION_INDENT: softWire.write((ratio >> 4))
            # TODO_MANUAL_CONVERSION_INDENT: softWire.endTransmission()
            # TODO_MANUAL_CONVERSION_INDENT: break


            # TODO_MANUAL_CONVERSION_INDENT: case 16:
              # Wire.begin() is handled by the selected Python interface block
              # TODO_MANUAL_CONVERSION_INDENT: Wire.write(0x40)
              # TODO_MANUAL_CONVERSION_INDENT: Wire.write((ratio >> 12))
              # TODO_MANUAL_CONVERSION_INDENT: Wire.write((ratio >> 4))
              # TODO_MANUAL_CONVERSION_INDENT: Wire.endTransmission()
              #volt16171819.setChannelValue(MCP4728_CHANNEL_A, ratio >> 4, MCP4728_VREF_VDD, MCP4728_GAIN_1X, MCP4728_PD_MODE_NORMAL);
              # TODO_MANUAL_CONVERSION_INDENT: break

              # TODO_MANUAL_CONVERSION_INDENT: case 17:
                # Wire.begin() is handled by the selected Python interface block
                # TODO_MANUAL_CONVERSION_INDENT: Wire.write(0x42)
                # TODO_MANUAL_CONVERSION_INDENT: Wire.write((ratio >> 12))
                # TODO_MANUAL_CONVERSION_INDENT: Wire.write((ratio >> 4))
                # TODO_MANUAL_CONVERSION_INDENT: Wire.endTransmission()
                #volt16171819.setChannelValue(MCP4728_CHANNEL_B, ratio >> 4, MCP4728_VREF_VDD, MCP4728_GAIN_1X, MCP4728_PD_MODE_NORMAL);
                # TODO_MANUAL_CONVERSION_INDENT: break

                # TODO_MANUAL_CONVERSION_INDENT: case 18:
                  # Wire.begin() is handled by the selected Python interface block
                  # TODO_MANUAL_CONVERSION_INDENT: Wire.write(0x44)
                  # TODO_MANUAL_CONVERSION_INDENT: Wire.write((ratio >> 12))
                  # TODO_MANUAL_CONVERSION_INDENT: Wire.write((ratio >> 4))
                  # TODO_MANUAL_CONVERSION_INDENT: Wire.endTransmission()
                  #volt16171819.setChannelValue(MCP4728_CHANNEL_C, ratio >> 4, MCP4728_VREF_VDD, MCP4728_GAIN_1X, MCP4728_PD_MODE_NORMAL);
                  # TODO_MANUAL_CONVERSION_INDENT: break

                  # TODO_MANUAL_CONVERSION_INDENT: case 19:
                    # Wire.begin() is handled by the selected Python interface block
                    # TODO_MANUAL_CONVERSION_INDENT: Wire.write(0x46)
                    # TODO_MANUAL_CONVERSION_INDENT: Wire.write((ratio >> 12))
                    # TODO_MANUAL_CONVERSION_INDENT: Wire.write((ratio >> 4))
                    # TODO_MANUAL_CONVERSION_INDENT: Wire.endTransmission()
                    #volt16171819.setChannelValue(MCP4728_CHANNEL_D, ratio >> 4, MCP4728_VREF_VDD, MCP4728_GAIN_1X, MCP4728_PD_MODE_NORMAL);
                    # TODO_MANUAL_CONVERSION_INDENT: break


                # TODO_MANUAL_CONVERSION_INDENT: def analogShutdown():
                  #
                  #volt16171819.begin();
                  #volt16171819.setChannelValue(MCP4728_CHANNEL_A, 0, MCP4728_VREF_VDD, MCP4728_GAIN_1X, MCP4728_PD_MODE_GND_500K);
                  #volt16171819.setChannelValue(MCP4728_CHANNEL_B, 0, MCP4728_VREF_VDD, MCP4728_GAIN_1X, MCP4728_PD_MODE_GND_500K);
                  #volt16171819.setChannelValue(MCP4728_CHANNEL_C, 0, MCP4728_VREF_VDD, MCP4728_GAIN_1X, MCP4728_PD_MODE_GND_500K);
                  #volt16171819.setChannelValue(MCP4728_CHANNEL_D, 0, MCP4728_VREF_VDD, MCP4728_GAIN_1X, MCP4728_PD_MODE_GND_500K);
                  #
                  # TODO_MANUAL_CONVERSION_INDENT: for x in range(0x40, (0x46) + 1):
                    # TODO_MANUAL_CONVERSION_INDENT: softWire.beginTransmission(MCP4728_ADDR)
                    # TODO_MANUAL_CONVERSION_INDENT: softWire.write(x)
                    # TODO_MANUAL_CONVERSION_INDENT: softWire.write(0x60)
                    # TODO_MANUAL_CONVERSION_INDENT: softWire.write(0x00)
                    # TODO_MANUAL_CONVERSION_INDENT: softWire.endTransmission()


                    # Wire.begin() is handled by the selected Python interface block
                    # TODO_MANUAL_CONVERSION_INDENT: Wire.write(x)
                    # TODO_MANUAL_CONVERSION_INDENT: Wire.write(0x60)
                    # TODO_MANUAL_CONVERSION_INDENT: Wire.write(0x00)
                    # TODO_MANUAL_CONVERSION_INDENT: Wire.endTransmission()


                # TODO_MANUAL_CONVERSION_INDENT: def analog1k(pin):
                  # TODO_MANUAL_CONVERSION_INDENT: switch (pin) {
                    # TODO_MANUAL_CONVERSION_INDENT: case 16:

                      # Wire.begin() is handled by the selected Python interface block
                      # TODO_MANUAL_CONVERSION_INDENT: Wire.write(0x40)
                      # TODO_MANUAL_CONVERSION_INDENT: Wire.write((0x20));  #TODO Double check this...
                      # TODO_MANUAL_CONVERSION_INDENT: Wire.write((0))
                      # TODO_MANUAL_CONVERSION_INDENT: Wire.endTransmission()
                      #volt16171819.setChannelValue(MCP4728_CHANNEL_A, 0, MCP4728_VREF_VDD, MCP4728_GAIN_1X, MCP4728_PD_MODE_GND_1K);
                      # TODO_MANUAL_CONVERSION_INDENT: break

                      # TODO_MANUAL_CONVERSION_INDENT: case 17:
                        # Wire.begin() is handled by the selected Python interface block
                        # TODO_MANUAL_CONVERSION_INDENT: Wire.write(0x42)
                        # TODO_MANUAL_CONVERSION_INDENT: Wire.write((0x20));  #TODO Double check this...
                        # TODO_MANUAL_CONVERSION_INDENT: Wire.write((0))
                        # TODO_MANUAL_CONVERSION_INDENT: Wire.endTransmission()
                        #volt16171819.setChannelValue(MCP4728_CHANNEL_B, 0, MCP4728_VREF_VDD, MCP4728_GAIN_1X, MCP4728_PD_MODE_GND_1K);
                        # TODO_MANUAL_CONVERSION_INDENT: break

                        # TODO_MANUAL_CONVERSION_INDENT: case 18:
                          # Wire.begin() is handled by the selected Python interface block
                          # TODO_MANUAL_CONVERSION_INDENT: Wire.write(0x44)
                          # TODO_MANUAL_CONVERSION_INDENT: Wire.write((0x20));  #TODO Double check this...
                          # TODO_MANUAL_CONVERSION_INDENT: Wire.write((0))
                          # TODO_MANUAL_CONVERSION_INDENT: Wire.endTransmission()
                          #volt16171819.setChannelValue(MCP4728_CHANNEL_C, 0, MCP4728_VREF_VDD, MCP4728_GAIN_1X, MCP4728_PD_MODE_GND_1K);
                          # TODO_MANUAL_CONVERSION_INDENT: break

                          # TODO_MANUAL_CONVERSION_INDENT: case 19:
                            # Wire.begin() is handled by the selected Python interface block
                            # TODO_MANUAL_CONVERSION_INDENT: Wire.write(0x46)
                            # TODO_MANUAL_CONVERSION_INDENT: Wire.write((0x20));  #TODO Double check this...
                            # TODO_MANUAL_CONVERSION_INDENT: Wire.write((0))
                            # TODO_MANUAL_CONVERSION_INDENT: Wire.endTransmission()
                            #volt16171819.setChannelValue(MCP4728_CHANNEL_D, 0, MCP4728_VREF_VDD, MCP4728_GAIN_1X, MCP4728_PD_MODE_GND_1K);
                            # TODO_MANUAL_CONVERSION_INDENT: break



                        # TODO_MANUAL_CONVERSION_INDENT: def setup():

                          # #ifdef ARDUINO_ESP8266_GENERIC
                          # Wire.begin() is handled by the selected Python interface block
                          # #else
                          # Wire.begin() is handled by the selected Python interface block
                          # #endif
                          # TODO_MANUAL_CONVERSION_INDENT: Wire.setTimeout(1000)
                          # Serial.begin() is not used in this Python example

                          # TODO_MANUAL_CONVERSION_INDENT: delay(100)
                          # TODO_MANUAL_CONVERSION_INDENT: Serial.flush()
                          # TODO_MANUAL_CONVERSION_INDENT: count = 0
                          # TODO_MANUAL_CONVERSION_INDENT: i2cAddress = SWC.find(True)

                          # #ifdef SW_FAILURE_PIN  # This is used when this bridge is part of Jon's Unit test fixture
                          #warning FAILURE PIN IS ENABLED
                          # TODO_MANUAL_CONVERSION_INDENT: pinMode(SW_FAILURE_PIN,1)
                          # #endif




                        # TODO_MANUAL_CONVERSION_INDENT: lastReceive = 0
                        # TODO_MANUAL_CONVERSION_INDENT: RECEIVETIMEOUT = 2000



                        # TODO_MANUAL_CONVERSION_INDENT: def loop():


                          # TODO_MANUAL_CONVERSION_INDENT: x = Serial.read()

                          # TODO_MANUAL_CONVERSION_INDENT: while x >= 0:
                            # TODO_MANUAL_CONVERSION_INDENT: lastReceive = millis()
                            # TODO_MANUAL_CONVERSION_INDENT: if count > 0:
                              # TODO_MANUAL_CONVERSION_INDENT: tx[count] = x
                              # TODO_MANUAL_CONVERSION_INDENT: ++count
                              # TODO_MANUAL_CONVERSION_INDENT: if count >= 9:
                                # TODO_MANUAL_CONVERSION_INDENT: if tx[1] == 251:
                                  # TODO_MANUAL_CONVERSION_INDENT: analog1k(tx[2])
                                # TODO_MANUAL_CONVERSION_INDENT: elif tx[1] == 252:
                                  # TODO_MANUAL_CONVERSION_INDENT: analogShutdown()
                                # TODO_MANUAL_CONVERSION_INDENT: elif tx[1] == 253:

                                  # TODO_MANUAL_CONVERSION_INDENT: setAnalogRatio(tx[2],(tx[4]) * 256 + tx[3])

                                # TODO_MANUAL_CONVERSION_INDENT: elif tx[1] != 0x55  and  tx[1] != 'x'  and  tx[1] != ' ':
                                  # #ifdef SW_FAILURE_PIN
                                  # TODO_MANUAL_CONVERSION_INDENT: if tx[1] == 0x40:
                                    # TODO_MANUAL_CONVERSION_INDENT: digitalWrite(SW_FAILURE_PIN,not digitalRead(SW_FAILURE_PIN))
                                  # #endif
                                  # TODO_MANUAL_CONVERSION_INDENT: if tx[0] != 0xFF:
                                    # Wire.begin() is handled by the selected Python interface block
                                  # TODO_MANUAL_CONVERSION_INDENT: else:
                                    # Wire.begin() is handled by the selected Python interface block
                                  # TODO_MANUAL_CONVERSION_INDENT: Wire.write(tx[1], 8)
                                  # TODO_MANUAL_CONVERSION_INDENT: Wire.endTransmission()
                                  # TODO_MANUAL_CONVERSION_INDENT: delayMicroseconds(100)
                                  # TODO_MANUAL_CONVERSION_INDENT: if tx[0] != 0xFF:
                                    # TODO_MANUAL_CONVERSION_INDENT: Wire.requestFrom(tx[0], 8)
                                  # TODO_MANUAL_CONVERSION_INDENT: else:
                                    # TODO_MANUAL_CONVERSION_INDENT: Wire.requestFrom(i2cAddress, 8)
                                  # TODO_MANUAL_CONVERSION_INDENT: count = 0
                                  # TODO_MANUAL_CONVERSION_INDENT: r = 0
                                  # TODO_MANUAL_CONVERSION_INDENT: while r >= 0  and  count < 8:
                                    # TODO_MANUAL_CONVERSION_INDENT: r = Wire.read()

                                    # TODO_MANUAL_CONVERSION_INDENT: if r >= 0:
                                      # TODO_MANUAL_CONVERSION_INDENT: rx[count] =  r
                                      # TODO_MANUAL_CONVERSION_INDENT: ++count
                                    # TODO_MANUAL_CONVERSION_INDENT: else:
                                      # TODO_MANUAL_CONVERSION_INDENT: break

                                  # TODO_MANUAL_CONVERSION_INDENT: Serial.write(rx, 8)
                                # TODO_MANUAL_CONVERSION_INDENT: count = 0
                            # TODO_MANUAL_CONVERSION_INDENT: else:
                              # TODO_MANUAL_CONVERSION_INDENT: if x != 0x55  and  x != 'x'  and  x != ' ':
                                # TODO_MANUAL_CONVERSION_INDENT: tx[count] = x
                                # TODO_MANUAL_CONVERSION_INDENT: ++count
                            # TODO_MANUAL_CONVERSION_INDENT: x = Serial.read()
                          # TODO_MANUAL_CONVERSION_INDENT: if millis() > lastReceive + RECEIVETIMEOUT:
                            # TODO_MANUAL_CONVERSION_INDENT: count = 0


setup()
while True:
    loop()
