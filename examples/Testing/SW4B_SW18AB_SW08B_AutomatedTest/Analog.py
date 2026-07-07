# Converted from Testing/SW4B_SW18AB_SW08B_AutomatedTest/Analog.ino
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
import SerialWombatAnalogInput

#Adafruit_MCP4728 volt16171819;
#Adafruit_MCP4728 volt00070906;
MCP4728_ADDR = 0x60
analog16 = SerialWombatAnalogInput.SerialWombatAnalogInput(SW18AB_6B)
analog17 = SerialWombatAnalogInput.SerialWombatAnalogInput(SW18AB_6B)
analog18 = SerialWombatAnalogInput.SerialWombatAnalogInput(SW18AB_6B)
analog19 = SerialWombatAnalogInput.SerialWombatAnalogInput(SW18AB_6B)
analog16SW4B = SerialWombatAnalogInput.SerialWombatAnalogInput(SW4B_6F)
analog17SW4B = SerialWombatAnalogInput.SerialWombatAnalogInput(SW4B_6E)
analog18SW4B = SerialWombatAnalogInput.SerialWombatAnalogInput(SW4B_6E)
analog19SW4B = SerialWombatAnalogInput.SerialWombatAnalogInput(SW4B_6E)
analog0SW8B = SerialWombatAnalogInput.SerialWombatAnalogInput(SW8B_68)
analog1SW8B = SerialWombatAnalogInput.SerialWombatAnalogInput(SW8B_68)
analog2SW8B = SerialWombatAnalogInput.SerialWombatAnalogInput(SW8B_68)
analog3SW8B = SerialWombatAnalogInput.SerialWombatAnalogInput(SW8B_68)
analog4SW8B = SerialWombatAnalogInput.SerialWombatAnalogInput(SW8B_68)
analog5SW8B = SerialWombatAnalogInput.SerialWombatAnalogInput(SW8B_68)
analog6SW8B = SerialWombatAnalogInput.SerialWombatAnalogInput(SW8B_68)
analog7SW8B = SerialWombatAnalogInput.SerialWombatAnalogInput(SW8B_68)


# TODO_MANUAL_CONVERSION: SerialWombatAnalogInput* SW8BAnalogs[] = {
analog0SW8B,
analog1SW8B,
analog2SW8B,
analog3SW8B,
analog4SW8B,
analog5SW8B,
analog6SW8B,
analog7SW8B


# TODO_MANUAL_CONVERSION: SerialWombatAnalogInput* SW18ABAnalogs[] = {
analog16,
analog16,
analog16,
analog16,
analog16,
analog16,
analog16,
analog16,
analog16,
analog16,
analog16,
analog16,
analog16,
analog16,
analog16,
analog16,
analog16,
analog17,
analog18,
analog19,


# TODO_MANUAL_CONVERSION: uint16_t wrandom(uint32_t *seed)

analogSeed = 1
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


                        # TODO_MANUAL_CONVERSION_INDENT: def analogInputTest(sw):
                          # TODO_MANUAL_CONVERSION_INDENT: resetAll()



                          # TODO_MANUAL_CONVERSION_INDENT: analogShutdown()
                          # TODO_MANUAL_CONVERSION_INDENT: if sw == SW18AB_6B:
                            # TODO_MANUAL_CONVERSION_INDENT: analogInputTest_SW18AB()
                            # TODO_MANUAL_CONVERSION_INDENT: return
                          # TODO_MANUAL_CONVERSION_INDENT: if sw == SW8B_68:
                            # TODO_MANUAL_CONVERSION_INDENT: analogInputTest_SW8B()
                            # TODO_MANUAL_CONVERSION_INDENT: return
                          # TODO_MANUAL_CONVERSION_INDENT: if sw == SW18AB_6B:
                            # TODO_MANUAL_CONVERSION_INDENT: analog16.begin(16)
                            # TODO_MANUAL_CONVERSION_INDENT: analog17.begin(17)
                            # TODO_MANUAL_CONVERSION_INDENT: analog18.begin(18)
                            # TODO_MANUAL_CONVERSION_INDENT: analog19.begin(19)
                          # TODO_MANUAL_CONVERSION_INDENT: if sw == SW4B_6C:
                            # TODO_MANUAL_CONVERSION_INDENT: analog16SW4B.begin(1)
                            # TODO_MANUAL_CONVERSION_INDENT: analog17SW4B.begin(3)
                            # TODO_MANUAL_CONVERSION_INDENT: analog18SW4B.begin(2)
                            # TODO_MANUAL_CONVERSION_INDENT: analog19SW4B.begin(1)
                          # TODO_MANUAL_CONVERSION_INDENT: for i in range(0, 65535):
                            # TODO_MANUAL_CONVERSION_INDENT: ratio = i
                            # TODO_MANUAL_CONVERSION_INDENT: setAnalogRatio(16, ratio)
                            # TODO_MANUAL_CONVERSION_INDENT: setAnalogRatio(17, ratio + 15000)
                            # TODO_MANUAL_CONVERSION_INDENT: setAnalogRatio(18, ratio + 30000)
                            # TODO_MANUAL_CONVERSION_INDENT: setAnalogRatio(19, ratio + 45000)

                            # TODO_MANUAL_CONVERSION_INDENT: delay(100)


                            # TODO_MANUAL_CONVERSION_INDENT: readResult = 0

                            # TODO_MANUAL_CONVERSION_INDENT: for x in range(0, 100):
                              # TODO_MANUAL_CONVERSION_INDENT: if sw == SW18AB_6B:
                                # TODO_MANUAL_CONVERSION_INDENT: SW18AB_6B.readTemperature_100thsDegC()
                                # TODO_MANUAL_CONVERSION_INDENT: readResult = analog16.readCounts()
                                # TODO_MANUAL_CONVERSION_INDENT: test("ANALOGIN_COUNTS_16", readResult, ratio, 256, 3)

                                # TODO_MANUAL_CONVERSION_INDENT: readResult = analog16.readAveragedCounts()
                                # TODO_MANUAL_CONVERSION_INDENT: test("ANALOGIN_AVERAGE_16", readResult, ratio, 256, 3)
                              # TODO_MANUAL_CONVERSION_INDENT: if sw == SW4B_6C:
                                # TODO_MANUAL_CONVERSION_INDENT: readResult = analog16SW4B.readCounts()
                                # TODO_MANUAL_CONVERSION_INDENT: test("ANALOGIN_COUNTS_16_4B", readResult, ratio, 256, 3)

                                # TODO_MANUAL_CONVERSION_INDENT: readResult = analog16SW4B.readAveragedCounts()
                                # TODO_MANUAL_CONVERSION_INDENT: test("ANALOGIN_AVERAGE_16_4B", readResult, ratio, 256, 3)


                              # TODO_MANUAL_CONVERSION_INDENT: if sw == SW8B_68:
                                # TODO_MANUAL_CONVERSION_INDENT: readResult = analog16SW4B.readCounts()
                                # TODO_MANUAL_CONVERSION_INDENT: test("ANALOGIN_COUNTS_16_4B", readResult, ratio, 256, 3)

                                # TODO_MANUAL_CONVERSION_INDENT: readResult = analog16SW4B.readAveragedCounts()
                                # TODO_MANUAL_CONVERSION_INDENT: test("ANALOGIN_AVERAGE_16_4B", readResult, ratio, 256, 3)

                              # TODO_MANUAL_CONVERSION_INDENT: delay(0)

                            # TODO_MANUAL_CONVERSION_INDENT: ratio += 15000

                            # TODO_MANUAL_CONVERSION_INDENT: for x in range(0, 100):
                              # TODO_MANUAL_CONVERSION_INDENT: if sw == SW18AB_6B:
                                # TODO_MANUAL_CONVERSION_INDENT: SW18AB_6B.readTemperature_100thsDegC()
                                # TODO_MANUAL_CONVERSION_INDENT: readResult = analog17.readCounts()
                                # TODO_MANUAL_CONVERSION_INDENT: test("ANALOGIN_COUNTS_17", readResult, ratio, 256, 3)

                              # TODO_MANUAL_CONVERSION_INDENT: if sw == SW4B_6C:
                                # TODO_MANUAL_CONVERSION_INDENT: readResult = analog17SW4B.readCounts()
                                # TODO_MANUAL_CONVERSION_INDENT: test("ANALOGIN_COUNTS_17_4B", readResult, ratio, 256, 3)

                              # TODO_MANUAL_CONVERSION_INDENT: delay(0)
                            # TODO_MANUAL_CONVERSION_INDENT: ratio += 15000
                            # TODO_MANUAL_CONVERSION_INDENT: for x in range(0, 100):
                              # TODO_MANUAL_CONVERSION_INDENT: if sw == SW18AB_6B:
                                # TODO_MANUAL_CONVERSION_INDENT: SW18AB_6B.readTemperature_100thsDegC()
                                # TODO_MANUAL_CONVERSION_INDENT: readResult = analog18.readCounts()
                                # TODO_MANUAL_CONVERSION_INDENT: test("ANALOGIN_COUNTS_18", readResult, ratio, 256, 3)
                              # TODO_MANUAL_CONVERSION_INDENT: if sw == SW4B_6C:
                                # TODO_MANUAL_CONVERSION_INDENT: readResult = analog18SW4B.readCounts()
                                # TODO_MANUAL_CONVERSION_INDENT: test("ANALOGIN_COUNTS_18_4B", readResult, ratio, 256, 3)
                              # TODO_MANUAL_CONVERSION_INDENT: delay(0)



                            # TODO_MANUAL_CONVERSION_INDENT: ratio += 15000
                            # TODO_MANUAL_CONVERSION_INDENT: for x in range(0, 100):
                              # TODO_MANUAL_CONVERSION_INDENT: if sw == SW18AB_6B:
                                # TODO_MANUAL_CONVERSION_INDENT: SW18AB_6B.readTemperature_100thsDegC()
                                # TODO_MANUAL_CONVERSION_INDENT: readResult = analog19.readCounts()
                                # TODO_MANUAL_CONVERSION_INDENT: test("ANALOGIN_COUNTS_19", readResult, ratio, 256, 3)

                              # TODO_MANUAL_CONVERSION_INDENT: if sw == SW4B_6C:
                                # TODO_MANUAL_CONVERSION_INDENT: readResult = analog19SW4B.readCounts()
                                # TODO_MANUAL_CONVERSION_INDENT: test("ANALOGIN_COUNTS_10_4B", readResult, ratio, 256, 3)
                              # TODO_MANUAL_CONVERSION_INDENT: delay(0)
                            # TODO_MANUAL_CONVERSION_INDENT: delay(100)




                        # TODO_MANUAL_CONVERSION_INDENT: def analogInputTest_SW8B():
                          # TODO_MANUAL_CONVERSION_INDENT: for i in range(0, 8):
                            # TODO_MANUAL_CONVERSION_INDENT: SW8BAnalogs[i].begin(i)

                          # TODO_MANUAL_CONVERSION_INDENT: for i in range(0, 65535):
                            # TODO_MANUAL_CONVERSION_INDENT: adc = i

                            # TODO_MANUAL_CONVERSION_INDENT: for i in range(0, 8):
                              # TODO_MANUAL_CONVERSION_INDENT: setAnalogRatio(SW8BPinTo18ABPin(i), adc + 0x1800 * i)
                            # TODO_MANUAL_CONVERSION_INDENT: delay(100)
                            # TODO_MANUAL_CONVERSION_INDENT: for i in range(0, 8):

                              # TODO_MANUAL_CONVERSION_INDENT: readResult = SW8BAnalogs[i].readPublicData()
                              # TODO_MANUAL_CONVERSION_INDENT: test("ANALOGIN_COUNTS_8B", readResult,  adc + 0x1800 * i, 256, 3)
                              # TODO_MANUAL_CONVERSION_INDENT: readResult = SW8BAnalogs[i].readAveragedCounts()
                              # TODO_MANUAL_CONVERSION_INDENT: test("ANALOGIN_COUNTS_8B_AVG", readResult,  adc + 0x1800 * i, 256, 3)


                          #void analogMaxMinTest()
                            # TODO_MANUAL_CONVERSION_INDENT: setAnalogRatio(SW8BPinTo18ABPin(4), 0x8000)
                            # TODO_MANUAL_CONVERSION_INDENT: SW8BAnalogs[4].readMaximumCounts(True)

                            # TODO_MANUAL_CONVERSION_INDENT: setAnalogRatio(SW8BPinTo18ABPin(4), 0x4000)
                            # TODO_MANUAL_CONVERSION_INDENT: delay(100)
                            # TODO_MANUAL_CONVERSION_INDENT: setAnalogRatio(SW8BPinTo18ABPin(4), 0xC000)
                            # TODO_MANUAL_CONVERSION_INDENT: delay(100)
                            # TODO_MANUAL_CONVERSION_INDENT: minimum = SW8BAnalogs[4].readMinimumCounts()
                            # TODO_MANUAL_CONVERSION_INDENT: test("ANALOGIN_MIN_8", minimum, 0x4000, 256, 3)

                            # TODO_MANUAL_CONVERSION_INDENT: maximum = SW8BAnalogs[4].readMaximumCounts()
                            # TODO_MANUAL_CONVERSION_INDENT: test("ANALOGIN_MAX_8", maximum, 0xC000, 256, 3)

                          #void analogAverageTest()
                            # TODO_MANUAL_CONVERSION_INDENT: setAnalogRatio(SW8BPinTo18ABPin(4), 0x0000)
                            # TODO_MANUAL_CONVERSION_INDENT: SW8BAnalogs[4].begin(SW8BPinTo18ABPin(4), 10000)
                            # TODO_MANUAL_CONVERSION_INDENT: for i in range(0, 60):
                              # TODO_MANUAL_CONVERSION_INDENT: setAnalogRatio(SW8BPinTo18ABPin(4), 0x4000)
                              # TODO_MANUAL_CONVERSION_INDENT: delay(100)
                              # TODO_MANUAL_CONVERSION_INDENT: setAnalogRatio(SW8BPinTo18ABPin(4), 0xC000)
                              # TODO_MANUAL_CONVERSION_INDENT: delay(100)

                            # TODO_MANUAL_CONVERSION_INDENT: average = SW8BAnalogs[4].readAveragedCounts()
                            # TODO_MANUAL_CONVERSION_INDENT: test("ANALOGIN_AVG_8", average, 0x4000, 256, 3)


                          #void analogFilterTest()
                            # TODO_MANUAL_CONVERSION_INDENT: setAnalogRatio(SW8BPinTo18ABPin(4), 0xFFFF)
                            # TODO_MANUAL_CONVERSION_INDENT: delay(100)
                            # TODO_MANUAL_CONVERSION_INDENT: SW8BAnalogs[4].begin(SW8BPinTo18ABPin(4), 10000, 65445)
                            # TODO_MANUAL_CONVERSION_INDENT: setAnalogRatio(SW8BPinTo18ABPin(4), 0)
                            # TODO_MANUAL_CONVERSION_INDENT: delay(500)

                            # TODO_MANUAL_CONVERSION_INDENT: result = SW8BAnalogs[4].readFilteredCounts()
                            # TODO_MANUAL_CONVERSION_INDENT: test("ANALOGIN_Filter_8", result, 0x8000, 256, 3)
                            # TODO_MANUAL_CONVERSION_INDENT: delay(500)
                            # TODO_MANUAL_CONVERSION_INDENT: result = SW8BAnalogs[4].readFilteredCounts()
                            # TODO_MANUAL_CONVERSION_INDENT: test("ANALOGIN_Filter_8_2", result, 0x4000, 256, 3)

                        # TODO_MANUAL_CONVERSION_INDENT: def analogInputTest_SW18AB():
                          # TODO_MANUAL_CONVERSION_INDENT: for i in range(16, (19) + 1):
                            # TODO_MANUAL_CONVERSION_INDENT: SW18ABAnalogs[i].begin(i)

                          # TODO_MANUAL_CONVERSION_INDENT: for i in range(0, 65535):
                            # TODO_MANUAL_CONVERSION_INDENT: adc = i

                            # TODO_MANUAL_CONVERSION_INDENT: for i in range(16, (19) + 1):
                              # TODO_MANUAL_CONVERSION_INDENT: setAnalogRatio(i, adc + 0x1800 * i)
                            # TODO_MANUAL_CONVERSION_INDENT: delay(200)
                            # TODO_MANUAL_CONVERSION_INDENT: for i in range(16, (19) + 1):

                              # TODO_MANUAL_CONVERSION_INDENT: readResult = SW18ABAnalogs[i].readPublicData()
                              # TODO_MANUAL_CONVERSION_INDENT: test("ANALOGIN_COUNTS_18AB", readResult,  adc + 0x1800 * i, 256, 3)
                              # TODO_MANUAL_CONVERSION_INDENT: readResult = SW18ABAnalogs[i].readAveragedCounts()
                              # TODO_MANUAL_CONVERSION_INDENT: test("ANALOGIN_COUNTS_18AB_AVG", readResult,  adc + 0x1800 * i, 256, 3)


                          #void analogMaxMinTest()
                            # TODO_MANUAL_CONVERSION_INDENT: setAnalogRatio(16, 0x8000)
                            # TODO_MANUAL_CONVERSION_INDENT: analog16.readMaximumCounts(True)

                            # TODO_MANUAL_CONVERSION_INDENT: setAnalogRatio(16, 0x4000)
                            # TODO_MANUAL_CONVERSION_INDENT: delay(100)
                            # TODO_MANUAL_CONVERSION_INDENT: setAnalogRatio(16, 0xC000)
                            # TODO_MANUAL_CONVERSION_INDENT: delay(100)
                            # TODO_MANUAL_CONVERSION_INDENT: minimum = analog16.readMinimumCounts()
                            # TODO_MANUAL_CONVERSION_INDENT: test("ANALOGIN_MIN_16", minimum, 0x4000, 256, 3)

                            # TODO_MANUAL_CONVERSION_INDENT: maximum = analog16.readMaximumCounts()
                            # TODO_MANUAL_CONVERSION_INDENT: test("ANALOGIN_MAX_16", maximum, 0xC000, 256, 3)

                          #void analogAverageTest()
                            # TODO_MANUAL_CONVERSION_INDENT: setAnalogRatio(16, 0x0000)
                            # TODO_MANUAL_CONVERSION_INDENT: analog16.begin(16, 10000)
                            # TODO_MANUAL_CONVERSION_INDENT: for i in range(0, 60):
                              # TODO_MANUAL_CONVERSION_INDENT: setAnalogRatio(16, 0x4000)
                              # TODO_MANUAL_CONVERSION_INDENT: delay(100)
                              # TODO_MANUAL_CONVERSION_INDENT: setAnalogRatio(16, 0xC000)
                              # TODO_MANUAL_CONVERSION_INDENT: delay(100)

                            # TODO_MANUAL_CONVERSION_INDENT: average = analog16.readAveragedCounts()
                            # TODO_MANUAL_CONVERSION_INDENT: test("ANALOGIN_AVG_16", average, 0x4000, 256, 3)


                          #void analogFilterTest()
                            # TODO_MANUAL_CONVERSION_INDENT: setAnalogRatio(16, 0xFFFF)
                            # TODO_MANUAL_CONVERSION_INDENT: delay(100)
                            # TODO_MANUAL_CONVERSION_INDENT: analog16.begin(16, 10000, 65445)
                            # TODO_MANUAL_CONVERSION_INDENT: setAnalogRatio(16, 0)
                            # TODO_MANUAL_CONVERSION_INDENT: delay(500)

                            # TODO_MANUAL_CONVERSION_INDENT: result = analog16.readFilteredCounts()
                            # TODO_MANUAL_CONVERSION_INDENT: test("ANALOGIN_Filter_16", result, 0x8000, 256, 3)
                            # TODO_MANUAL_CONVERSION_INDENT: delay(500)
                            # TODO_MANUAL_CONVERSION_INDENT: result = analog16.readFilteredCounts()
                            # TODO_MANUAL_CONVERSION_INDENT: test("ANALOGIN_Filter_16_2", result, 0x4000, 256, 3)
