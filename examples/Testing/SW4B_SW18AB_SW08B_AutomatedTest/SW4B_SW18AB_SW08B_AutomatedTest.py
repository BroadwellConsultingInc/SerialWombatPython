# Converted from Testing/SW4B_SW18AB_SW08B_AutomatedTest/SW4B_SW18AB_SW08B_AutomatedTest.ino
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
import SerialWombatPulseTimer

#
#Pin Matching:
#SW18AB  SW4B  SW8B  DAC
#0       D3    -     SWA
#1       -     -
#2       -     -
#3       -     -
#4       -     -
#5       D2    -
#6       D1    8P0   SWD
#7       C0    8P5   SWB
#8       D0    -
#9       C1    8P4   SWC
#10      C2    -
#11      C3    -
#12      E0    -
#13      F0    -
#14      F3    -
#15      F2    -
#16      F1    8P2   HWA
#17      E3    8P3   HWB
#18      E2    8P6   HWC
#19      E1    8P7   HWD
#
NUM_TEST_PINS = 20
FAILUREPIN = 8
##define LOAD_REQUIRED_FIRMWARE

##define TEST_SW18AB
TEST_SW8B = True
##define TEST_SW4B


UNIT_TEST_QUEUE = True
UNIT_TEST_USDSENSOR = True
UNIT_TEST_HSCLOCK = True
UNIT_TEST_HSCOUNTER = True

UNIT_TEST_RESISTANCE_INPUT = True

UNIT_TEST_BLINK = True

UNIT_TEST_SCALING = True
UNIT_TEST_SW_UART = True

UNIT_TEST_HW_UART = True

UNIT_TEST_HBRIDGE = True

UNIT_TEST_ANALOG_INPUT = True

UNIT_TEST_FREQUENCY_OUTPUT = True
UNIT_TEST_INPUT_PROCESSOR = True

UNIT_TEST_COMMUNICATION_ERROR = True
UNIT_TEST_ECHO = True

UNIT_TEST_PWM = True
UNIT_TEST_QUAD_ENC = True

UNIT_TEST_SERVO = True
UNIT_TEST_PUBLIC_DATA = True
UNIT_TEST_DEBOUNCED_INPUT = True


UNIT_TEST_PULSE_ON_CHANGE = True

UNIT_TEST_PULSE_TIMER = True
UNIT_TEST_SEQUENCE_TEST = True
UNIT_TEST_DATALOGGER = True
UNIT_TEST_PROTECTED_OUTPUT = True
UNIT_TEST_WATCHDOG = True
UNIT_TEST_FRAME_TIMER = True
UNIT_TEST_QUEUED_PULSE_OUTPUT = True
UNIT_TEST_SOURCE_VOLTAGE = True
UNIT_TEST_IR_TX_RX = True

SW4B_6C = SerialWombat.SerialWombatChip()
SW4B_6D = SerialWombat.SerialWombatChip()
SW4B_6E = SerialWombat.SerialWombatChip()
SW4B_6F = SerialWombat.SerialWombatChip()
SW8B_68 = SerialWombat.SerialWombatChip()

SW18AB_6B = SerialWombat.SerialWombatChip()

SW_NULL = SerialWombat.SerialWombatChip()

# TODO_MANUAL_CONVERSION: SoftWire softWire(2,3)

# TODO_MANUAL_CONVERSION: void test(const char* designator, uint16_t value, uint16_t expected = 1, uint16_t counts = 0, uint16_t sixtyFourths =  0)


def SW18ABPinTo8BPin(pin):
  # TODO_MANUAL_CONVERSION: switch (pin) {
    # TODO_MANUAL_CONVERSION: case 0:
      return 1
      # TODO_MANUAL_CONVERSION: case 6:
        # TODO_MANUAL_CONVERSION_INDENT: return 0
        # TODO_MANUAL_CONVERSION_INDENT: case 7:
          # TODO_MANUAL_CONVERSION_INDENT: return 5
          # TODO_MANUAL_CONVERSION_INDENT: case 9:
            # TODO_MANUAL_CONVERSION_INDENT: return 4
            # TODO_MANUAL_CONVERSION_INDENT: case 16:
              # TODO_MANUAL_CONVERSION_INDENT: return 2
              # TODO_MANUAL_CONVERSION_INDENT: case 17:
                # TODO_MANUAL_CONVERSION_INDENT: return 3
                # TODO_MANUAL_CONVERSION_INDENT: case 18:
                  # TODO_MANUAL_CONVERSION_INDENT: return 6
                  # TODO_MANUAL_CONVERSION_INDENT: case 19:
                    # TODO_MANUAL_CONVERSION_INDENT: return 7
                    # TODO_MANUAL_CONVERSION_INDENT: default:
                      # TODO_MANUAL_CONVERSION_INDENT: test("Invalid SW18AB pin to 4B pin",0)
                      # TODO_MANUAL_CONVERSION_INDENT: return 255

                  # TODO_MANUAL_CONVERSION_INDENT: def SW18ABPinTo4BPin(pin):
                    # TODO_MANUAL_CONVERSION_INDENT: switch(pin) {
                      # TODO_MANUAL_CONVERSION_INDENT: case 0:
                        # TODO_MANUAL_CONVERSION_INDENT: return 3
                        # TODO_MANUAL_CONVERSION_INDENT: case 5:
                          # TODO_MANUAL_CONVERSION_INDENT: return 2
                          # TODO_MANUAL_CONVERSION_INDENT: case 6:
                            # TODO_MANUAL_CONVERSION_INDENT: return 1
                            # TODO_MANUAL_CONVERSION_INDENT: case 7:
                              # TODO_MANUAL_CONVERSION_INDENT: return 0
                              # TODO_MANUAL_CONVERSION_INDENT: case 8:
                                # TODO_MANUAL_CONVERSION_INDENT: return 0
                                # TODO_MANUAL_CONVERSION_INDENT: case 9:
                                  # TODO_MANUAL_CONVERSION_INDENT: return 1
                                  # TODO_MANUAL_CONVERSION_INDENT: case 10:
                                    # TODO_MANUAL_CONVERSION_INDENT: return 2
                                    # TODO_MANUAL_CONVERSION_INDENT: case 11:
                                      # TODO_MANUAL_CONVERSION_INDENT: return 3
                                      # TODO_MANUAL_CONVERSION_INDENT: case 12:
                                        # TODO_MANUAL_CONVERSION_INDENT: return 0
                                        # TODO_MANUAL_CONVERSION_INDENT: case 13:
                                          # TODO_MANUAL_CONVERSION_INDENT: return 0
                                          # TODO_MANUAL_CONVERSION_INDENT: case 14:
                                            # TODO_MANUAL_CONVERSION_INDENT: return 3
                                            # TODO_MANUAL_CONVERSION_INDENT: case 15:
                                              # TODO_MANUAL_CONVERSION_INDENT: return 2
                                              # TODO_MANUAL_CONVERSION_INDENT: case 16:
                                                # TODO_MANUAL_CONVERSION_INDENT: return 1
                                                # TODO_MANUAL_CONVERSION_INDENT: case 17:
                                                  # TODO_MANUAL_CONVERSION_INDENT: return 3
                                                  # TODO_MANUAL_CONVERSION_INDENT: case 18:
                                                    # TODO_MANUAL_CONVERSION_INDENT: return 2
                                                    # TODO_MANUAL_CONVERSION_INDENT: case 19:
                                                      # TODO_MANUAL_CONVERSION_INDENT: return 1
                                                    # TODO_MANUAL_CONVERSION_INDENT: s = [0] * (50)
                                                    # TODO_MANUAL_CONVERSION_INDENT: s = ("Invalid SW18B pin %d to 4B pin") % (pin)
                                                    # TODO_MANUAL_CONVERSION_INDENT: test(s,0)
                                                    # TODO_MANUAL_CONVERSION_INDENT: return 255

                                                  # TODO_MANUAL_CONVERSION_INDENT: def SW8BPinTo18ABPin(pin):
                                                    # TODO_MANUAL_CONVERSION_INDENT: switch (pin) {
                                                      # TODO_MANUAL_CONVERSION_INDENT: case 0:
                                                        # TODO_MANUAL_CONVERSION_INDENT: return 6
                                                        # TODO_MANUAL_CONVERSION_INDENT: case 1:
                                                          # TODO_MANUAL_CONVERSION_INDENT: return 0
                                                          # TODO_MANUAL_CONVERSION_INDENT: case 2:
                                                            # TODO_MANUAL_CONVERSION_INDENT: return 16
                                                            # TODO_MANUAL_CONVERSION_INDENT: case 3:
                                                              # TODO_MANUAL_CONVERSION_INDENT: return 17
                                                              # TODO_MANUAL_CONVERSION_INDENT: case 4:
                                                                # TODO_MANUAL_CONVERSION_INDENT: return 9
                                                                # TODO_MANUAL_CONVERSION_INDENT: case 5:
                                                                  # TODO_MANUAL_CONVERSION_INDENT: return 7
                                                                  # TODO_MANUAL_CONVERSION_INDENT: case 6:
                                                                    # TODO_MANUAL_CONVERSION_INDENT: return 18
                                                                    # TODO_MANUAL_CONVERSION_INDENT: case 7:
                                                                      # TODO_MANUAL_CONVERSION_INDENT: return 19
                                                                    # TODO_MANUAL_CONVERSION_INDENT: test("Invalid 8B pin to 18AB pin",0)

                                                                    # TODO_MANUAL_CONVERSION_INDENT: return 255;  # Should never happen

                                                                  # TODO_MANUAL_CONVERSION_INDENT: def SW8BPinTo4BPin(pin):
                                                                    # TODO_MANUAL_CONVERSION_INDENT: return SW18ABPinTo4BPin(SW8BPinTo18ABPin(pin))

                                                                  # TODO_MANUAL_CONVERSION_INDENT: SerialWombatChip SWChipAndPinTo4BChip(SerialWombatChip sw, uint8_t pin)
                                                                    # TODO_MANUAL_CONVERSION_INDENT: if sw == SW18AB_6B:
                                                                      # TODO_MANUAL_CONVERSION_INDENT: return SW18ABPinTo4BChip( pin)
                                                                    # TODO_MANUAL_CONVERSION_INDENT: elif sw == SW8B_68:
                                                                      # TODO_MANUAL_CONVERSION_INDENT: return SW8BPinTo4BChip( pin)
                                                                    # TODO_MANUAL_CONVERSION_INDENT: else:
                                                                      # TODO_MANUAL_CONVERSION_INDENT: return SW_NULL

                                                                  # TODO_MANUAL_CONVERSION_INDENT: def SWChipAndPinTo4BPin(sw, pin):
                                                                    # TODO_MANUAL_CONVERSION_INDENT: if sw == SW18AB_6B:
                                                                      # TODO_MANUAL_CONVERSION_INDENT: return SW18ABPinTo4BPin( pin)
                                                                    # TODO_MANUAL_CONVERSION_INDENT: elif sw == SW8B_68:
                                                                      # TODO_MANUAL_CONVERSION_INDENT: return SW8BPinTo4BPin( pin)
                                                                    # TODO_MANUAL_CONVERSION_INDENT: else:
                                                                      # TODO_MANUAL_CONVERSION_INDENT: return 0
                                                                  # TODO_MANUAL_CONVERSION_INDENT: SerialWombatChip SW8BPinTo4BChip(int pin)
                                                                    # TODO_MANUAL_CONVERSION_INDENT: return SW18ABPinTo4BChip(SW8BPinTo18ABPin(pin))
                                                                  # TODO_MANUAL_CONVERSION_INDENT: SerialWombatChip SW18ABPinTo4BChip(int pin)
                                                                    # TODO_MANUAL_CONVERSION_INDENT: switch (pin) {
                                                                      # TODO_MANUAL_CONVERSION_INDENT: case 0:
                                                                        # TODO_MANUAL_CONVERSION_INDENT: return SW4B_6D
                                                                        # TODO_MANUAL_CONVERSION_INDENT: case 5:
                                                                          # TODO_MANUAL_CONVERSION_INDENT: return SW4B_6D
                                                                          # TODO_MANUAL_CONVERSION_INDENT: case 6:
                                                                            # TODO_MANUAL_CONVERSION_INDENT: return SW4B_6D
                                                                            # TODO_MANUAL_CONVERSION_INDENT: case 7:
                                                                              # TODO_MANUAL_CONVERSION_INDENT: return SW4B_6C
                                                                              # TODO_MANUAL_CONVERSION_INDENT: case 8:
                                                                                # TODO_MANUAL_CONVERSION_INDENT: return SW4B_6D
                                                                                # TODO_MANUAL_CONVERSION_INDENT: case 9:
                                                                                  # TODO_MANUAL_CONVERSION_INDENT: return SW4B_6C
                                                                                  # TODO_MANUAL_CONVERSION_INDENT: case 10:
                                                                                    # TODO_MANUAL_CONVERSION_INDENT: return SW4B_6C
                                                                                    # TODO_MANUAL_CONVERSION_INDENT: case 11:
                                                                                      # TODO_MANUAL_CONVERSION_INDENT: return SW4B_6C
                                                                                      # TODO_MANUAL_CONVERSION_INDENT: case 12:
                                                                                        # TODO_MANUAL_CONVERSION_INDENT: return SW4B_6E
                                                                                        # TODO_MANUAL_CONVERSION_INDENT: case 13:
                                                                                          # TODO_MANUAL_CONVERSION_INDENT: return SW4B_6F
                                                                                          # TODO_MANUAL_CONVERSION_INDENT: case 14:
                                                                                            # TODO_MANUAL_CONVERSION_INDENT: return SW4B_6F
                                                                                            # TODO_MANUAL_CONVERSION_INDENT: case 15:
                                                                                              # TODO_MANUAL_CONVERSION_INDENT: return SW4B_6F
                                                                                              # TODO_MANUAL_CONVERSION_INDENT: case 16:
                                                                                                # TODO_MANUAL_CONVERSION_INDENT: return SW4B_6F
                                                                                                # TODO_MANUAL_CONVERSION_INDENT: case 17:
                                                                                                  # TODO_MANUAL_CONVERSION_INDENT: return SW4B_6E
                                                                                                  # TODO_MANUAL_CONVERSION_INDENT: case 18:
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: return SW4B_6E
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: case 19:
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: return SW4B_6E


                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: return SW_NULL;  # Pin has no associated SW4B



                                                                                                  # TODO_MANUAL_CONVERSION_INDENT: def test_pinCanBeOutput(sw, pin):
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: if sw == SW18AB_6B:
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: if pin >=1  and  pin <=4:
                                                                                                        # TODO_MANUAL_CONVERSION_INDENT: return False
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: if pin > 19:
                                                                                                        # TODO_MANUAL_CONVERSION_INDENT: return False

                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: elif sw == SW8B_68:
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: if pin > 7:
                                                                                                        # TODO_MANUAL_CONVERSION_INDENT: return False
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: elif sw == SW4B_6C  or  sw == SW4B_6D  or  sw == SW4B_6E  or  sw == SW4B_6F:
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: if pin == 0  or  pin > 3:
                                                                                                        # TODO_MANUAL_CONVERSION_INDENT: return False
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: else:
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: test("TEST ERROR:  Invalid SW Chip in test_pinCanBeOutput",0)
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: return False

                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: return True

                                                                                                  # #if 0
                                                                                                  # TODO_MANUAL_CONVERSION_INDENT: SWMatchPin = 
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: SW18B_0_MATCH_PIN ,  #0
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: SW18B_1_MATCH_PIN ,  # 1
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: SW18B_2_MATCH_PIN ,  #2
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: SW18B_3_MATCH_PIN ,  #3
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: SW18B_4_MATCH_PIN ,  #4
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: SW18B_5_MATCH_PIN ,  #5
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: SW18B_6_MATCH_PIN ,  #6
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: SW18B_7_MATCH_PIN ,  #7
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: SW18B_8_MATCH_PIN ,  #8
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: SW18B_9_MATCH_PIN ,  #9
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: SW18B_10_MATCH_PIN,  #10
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: SW18B_11_MATCH_PIN,  #11
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: SW18B_12_MATCH_PIN,  #12
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: SW18B_13_MATCH_PIN,  #13
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: SW18B_14_MATCH_PIN,  #14
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: SW18B_15_MATCH_PIN,  #15
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: SW18B_16_MATCH_PIN,  #16
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: SW18B_17_MATCH_PIN,  #17
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: SW18B_18_MATCH_PIN,  #18
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: SW18B_19_MATCH_PIN  #19

                                                                                                  # #endif


                                                                                                  # TODO_MANUAL_CONVERSION_INDENT: passCount = 0
                                                                                                  # TODO_MANUAL_CONVERSION_INDENT: failCount = 0
                                                                                                  # TODO_MANUAL_CONVERSION_INDENT: softWireTxBuffer = [0] * (16)
                                                                                                  # TODO_MANUAL_CONVERSION_INDENT: softWireRxBuffer = [0] * (16)

                                                                                                  # TODO_MANUAL_CONVERSION_INDENT: def setup():
                                                                                                    # put your setup code here, to run once:
                                                                                                    # Wire.begin() is handled by the selected Python interface block
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: softWire.setTxBuffer(softWireTxBuffer, len(softWireTxBuffer))
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: softWire.setRxBuffer(softWireRxBuffer, len(softWireTxBuffer))
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: softWire.setDelay_us(5)
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: softWire.setTimeout(1000)
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: softWire.begin()
                                                                                                    #Turn off pull ups
                                                                                                    #digitalWrite(SCL,LOW);
                                                                                                    #digitalWrite(SDA,LOW);
                                                                                                    #pinMode(SCL,OUTPUT);
                                                                                                    #pinMode(SDA,OUTPUT);

                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: analogShutdown()


                                                                                                    # Serial.begin() is not used in this Python example
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: delay(100)
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: resetAll()
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: print()
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: print("#############################################################")
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: print()
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: print("Serial Wombat 18B Unit Test")
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: print()
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: print("#############################################################")
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: print()

                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: delay(1000)
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: print("Setting Failure Line")

                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: delay(1000)

                                                                                                    # #ifdef FAILUREPIN
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: pinMode(FAILUREPIN, 1)
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: digitalWrite(FAILUREPIN, 0)
                                                                                                    # #endif

                                                                                                    #
                                                                                                    #pinMode(0,OUTPUT); // Set the switch ICS to open
                                                                                                    #digitalWrite(0,LOW);
                                                                                                    #

                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: print("Setting Wire Clock")
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: delay(1000)
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: Wire.setClock(100000)

                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: SW18AB_6B.registerErrorHandler(SerialWombatSerialErrorHandlerBrief)


                                                                                                  # TODO_MANUAL_CONVERSION_INDENT: def updateDisplay():
                                                                                                    # #ifdef USE_DISPLAY
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: display.clearDisplay()
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: display.setTextSize(2)
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: display.setTextColor(WHITE)
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: display.setCursor(0, 0)

                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: display.print("Pass: ")
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: display.println(passCount)
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: display.print("Fail: ")
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: display.println(failCount)

                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: display.setTextSize(1)
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: display.print("Run time (s): ")
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: display.println(millis() / 1000)
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: display.display()
                                                                                                    # #endif

                                                                                                  # TODO_MANUAL_CONVERSION_INDENT: lastDisplayUpdate = 0
                                                                                                  # TODO_MANUAL_CONVERSION_INDENT: lastPassedTest = -1
                                                                                                  # TODO_MANUAL_CONVERSION_INDENT: def pass(i):
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: ++passCount
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: lastPassedTest = i
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: if lastDisplayUpdate + 2000 < millis():
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: yield()
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: lastDisplayUpdate = millis()

                                                                                                  # TODO_MANUAL_CONVERSION_INDENT: lastFailedTest = -1
                                                                                                  # TODO_MANUAL_CONVERSION_INDENT: def fail(i):
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: lastFailedTest = i
                                                                                                    # Serial.print("Fail at iteration "); Serial.println(i);
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: ++failCount
                                                                                                    # #ifdef FAILUREPIN
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: digitalWrite(FAILUREPIN, 1);  #Wiggle a line for triggering by Logic Analyzer
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: delay(1)
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: digitalWrite(FAILUREPIN, 0)
                                                                                                    # #endif
                                                                                                    #delay(500);
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: if lastDisplayUpdate + 250 < millis():
                                                                                                      #Yield periodically in case in tight loop
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: lastDisplayUpdate = millis()
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: yield()

                                                                                                  # TODO_MANUAL_CONVERSION_INDENT: def loop():
                                                                                                    #
                                                                                                    #Serial.println ("Starting Digital IO Test.  This test takes less than a minute");
                                                                                                    #dioTest();
                                                                                                    #Serial.print(millis() / 1000); Serial.print (": Digital I/O test complete.  Pass: "); Serial.print(passCount); Serial.print(" Fail: "); Serial.println(failCount);
                                                                                                    #
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: print("****************************************************")
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: print("TOP OF TEST LOOP")
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: print("****************************************************")
                                                                                                    # #ifdef UNIT_TEST_COMMUNICATION_ERROR
                                                                                                    # #ifdef TEST_SW18AB
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: print("Starting SW18AB communication error test.  This test takes less than a minute")
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: resetAll()
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: CommunicationErrorTest(SW18AB_6B)
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: print("Communication error test complete.  Pass: "); Serial.print(passCount); Serial.print(" Fail: "); Serial.println(failCount, end="")
                                                                                                    # #endif

                                                                                                    # #ifdef TEST_SW8B
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: print("Starting SW8B communication error test.  This test takes less than a minute")
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: resetAll()
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: CommunicationErrorTest(SW8B_68)
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: print("Communication error test complete.  Pass: "); Serial.print(passCount); Serial.print(" Fail: "); Serial.println(failCount, end="")
                                                                                                    # #endif

                                                                                                    # #endif
                                                                                                    # #ifdef UNIT_TEST_SOURCE_VOLTAGE
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: print("Starting supply voltage test.  This test takes less than a minute")
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: resetAll()
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: vSupplyTest()
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: print("vSupply test complete.  Pass: "); Serial.print(passCount); Serial.print(" Fail: "); Serial.println(failCount, end="")
                                                                                                    # #endif

                                                                                                    # #ifdef UNIT_TEST_ECHO
                                                                                                    # put your main code here, to run repeatedly:

                                                                                                    # #ifdef TEST_SW18AB
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: print("Starting SW18AB ECHO Test.  This test takes about 2 minutes")
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: echoTest(SW18AB_6B)
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: print("Echo test complete.  Pass: "); Serial.print(passCount); Serial.print(" Fail: "); Serial.println(failCount, end="")
                                                                                                    # #endif
                                                                                                    # #ifdef TEST_SW8B
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: print("Starting SW8B ECHO Test.  This test takes about 2 minutes")
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: echoTest(SW8B_68)
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: print("Echo test complete.  Pass: "); Serial.print(passCount); Serial.print(" Fail: "); Serial.println(failCount, end="")
                                                                                                    # #endif
                                                                                                    # #ifdef TEST_SW4B
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: print("Starting SW4B ECHO Test.  This test takes about 2 minutes")
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: echoTest(SW4B_6C)
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: print("Echo test complete.  Pass: "); Serial.print(passCount); Serial.print(" Fail: "); Serial.println(failCount, end="")
                                                                                                    # #endif

                                                                                                    # #endif

                                                                                                    # #ifdef UNIT_TEST_SERVO
                                                                                                    # #ifdef TEST_SW18AB
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: print("Starting SW18AB Servo Test.  This test takes about 1 hour 15 minutes.")
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: resetAll()
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: servoTest(SW18AB_6B,0,19)
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: print("Servo test complete.  Pass: "); Serial.print(passCount); Serial.print(" Fail: "); Serial.println(failCount, end="")
                                                                                                    # #endif
                                                                                                    # #ifdef TEST_SW8B
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: if SW8B_68.isPinModeSupported(PIN_MODE_SERVO):
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: print("Starting SW8B Servo Test.  This test takes about 1 hour 15 minutes.")
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: resetAll()
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: servoTest(SW8B_68,0,7)
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: print("Servo test complete.  Pass: "); Serial.print(passCount); Serial.print(" Fail: "); Serial.println(failCount, end="")
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: else:
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: print("Servo not supported on this SW8B Build")
                                                                                                    # #endif
                                                                                                    # #endif

                                                                                                    # #ifdef UNIT_TEST_QUEUE
                                                                                                    # #ifdef TEST_SW18AB
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: print("Starting SW18AB Queue Test.  This test takes about 50 minutes.")
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: resetAll()
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: queueTest(SW18AB_6B)
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: print("Queue test complete.  Pass: "); Serial.print(passCount); Serial.print(" Fail: "); Serial.println(failCount, end="")
                                                                                                    # #endif

                                                                                                    # #ifdef TEST_SW8B
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: if SW8B_68.isPinModeSupported(PIN_MODE_SW_UART):
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: print("Starting SW8B Queue Test.  This test takes about 6 minutes.")
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: resetAll()
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: queueTest(SW8B_68)
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: print("Queue test complete.  Pass: "); Serial.print(passCount); Serial.print(" Fail: "); Serial.println(failCount, end="")
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: else:
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: print("Queues not tested unless SW UART is present on SW8B")
                                                                                                    # #endif
                                                                                                    # #endif

                                                                                                    # #ifdef UNIT_TEST_PWM
                                                                                                    # #ifdef TEST_SW18AB
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: print("Starting SW18AB Pwm Test.  This test takes about 2 minutes.")
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: resetAll()
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: pwmTest(SW18AB_6B,18,19);  #TODO try without TRM, expand pin range
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: print("PWM test complete.  Pass: "); Serial.print(passCount); Serial.print(" Fail: "); Serial.println(failCount, end="")
                                                                                                    # #endif
                                                                                                    # #ifdef TEST_SW8B
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: if SW8B_68.isPinModeSupported(PIN_MODE_PWM):
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: print("Starting SW8B PWM Test.  This test takes about 2 minutes.")
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: resetAll()
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: pwmTest(SW8B_68,6,6);  #TODO expand pin range
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: print("PWM test complete.  Pass: "); Serial.print(passCount); Serial.print(" Fail: "); Serial.println(failCount, end="")
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: else:
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: print("PWM Pin Mode Not Available in this build of SW8B")
                                                                                                    # #endif
                                                                                                    # #endif

                                                                                                    # #ifdef UNIT_TEST_QUAD_ENC
                                                                                                    # #ifdef TEST_SW18AB
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: print("Starting SW18AB Quadrature Encoder Test.  This test takes about 7 minutes.")
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: resetAll()
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: QuadEncTest(SW18AB_6B)
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: print("Quadrature Encoder test complete.  Pass: "); Serial.print(passCount); Serial.print(" Fail: "); Serial.println(failCount, end="")
                                                                                                    # #endif

                                                                                                    # #ifdef TEST_SW8B
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: if SW8B_68.isPinModeSupported(PIN_MODE_QUADRATUREENCODER):
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: print("Starting SW8B Quadrature Encoder Test.  This test takes about 7 minutes.")
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: resetAll()
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: QuadEncTest(SW8B_68)
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: print("Quadrature Encoder test complete.  Pass: "); Serial.print(passCount); Serial.print(" Fail: "); Serial.println(failCount, end="")
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: else:
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: print("Quadrature Encoder Pin Mode Not Available in SW8B")
                                                                                                    # #endif
                                                                                                    # #endif

                                                                                                    # #ifdef UNIT_TEST_IR_TX_RX
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: if SW8B_68.isPinModeSupported(PIN_MODE_IRRX):
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: print("Starting IR RX TX Test.  This test takes about 7 minutes.")
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: resetAll()
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: irTxRxTest()
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: print("IR RX TX test complete.  Pass: "); Serial.print(passCount); Serial.print(" Fail: "); Serial.println(failCount, end="")
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: else:
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: print("IR RX Pin Mode Not Available in SW8B")

                                                                                                    # #endif

                                                                                                    # #ifdef UNIT_TEST_HW_UART
                                                                                                    # #ifdef TEST_SW18AB
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: print("Starting 18AB HW UART Test.  This test takes about 31 minutes.")
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: resetAll()
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: uartHWTest(SW18AB_6B,9,7,19,17)
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: print("UART test complete.  Pass: "); Serial.print(passCount); Serial.print(" Fail: "); Serial.println(failCount, end="")
                                                                                                    # #endif
                                                                                                    # #ifdef TEST_SW8B
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: if SW8B_68.isPinModeSupported(PIN_MODE_UART_RX_TX):
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: print("Starting SW8B HW UART Encoder Test.  This test takes about 31 minutes.")
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: resetAll()
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: SW18AB_6B.readPublicData(0);  #TODO remove
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: uartHWTest(SW8B_68,5,4,255,255)
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: print("UART test complete.  Pass: "); Serial.print(passCount); Serial.print(" Fail: "); Serial.println(failCount, end="")
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: else:
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: print("HW UART Pin Mode Not Available in SW8B")
                                                                                                    # #endif
                                                                                                    # #endif

                                                                                                    # #ifdef UNIT_TEST_SW_UART
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: if SW8B_68.isPinModeSupported(PIN_MODE_SW_UART):
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: print("Starting SW UART Test.  This test takes about 25 minutes.")
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: resetAll()
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: uartSWTest()
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: print("UART SW test complete.  Pass: "); Serial.print(passCount); Serial.print(" Fail: "); Serial.println(failCount, end="")
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: else:
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: print("SW UART not avaialble on SW8B.  Skipped on both platforms")
                                                                                                    # #endif

                                                                                                    # #ifdef UNIT_TEST_DEBOUNCED_INPUT
                                                                                                    # #ifdef TEST_SW18AB
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: print("Starting 18AB Debounced Input Test.  This test takes less than a minute")
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: resetAll()
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: debounceTest(SW18AB_6B)
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: print(": Debounce test complete.  Pass: "); Serial.print(passCount); Serial.print(" Fail: "); Serial.println(failCount, end="")
                                                                                                    # #endif
                                                                                                    # #ifdef TEST_SW8B
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: if SW8B_68.isPinModeSupported(PIN_MODE_DEBOUNCE):
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: print("Starting 8B Debounced Input Test.  This test takes less than a minute")
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: resetAll()
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: debounceTest(SW8B_68)
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: print("Debounce test complete.  Pass: "); Serial.print(passCount); Serial.print(" Fail: "); Serial.println(failCount, end="")
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: else:
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: print("Debounced Input not supported on SW8B")
                                                                                                    # #endif
                                                                                                    # #ifdef TEST_SW4B
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: print("Starting 4B Debounced Input Test.  This test takes less than a minute")
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: resetAll()
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: debounceTest(SW4B_6C)
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: print(": Debounce test complete.  Pass: "); Serial.print(passCount); Serial.print(" Fail: "); Serial.println(failCount, end="")
                                                                                                    # #endif
                                                                                                    # #endif
                                                                                                    # #ifdef UNIT_TEST_RESISTANCE_INPUT
                                                                                                    # #ifdef TEST_SW18AB
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: print("Starting ResistanceInput Test.  This test takes less than a minute")
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: resetAll()
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: resistanceInputTest()
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: print(": ResistanceInput test complete.  Pass: "); Serial.print(passCount); Serial.print(" Fail: "); Serial.println(failCount, end="")
                                                                                                    # #endif
                                                                                                    # #endif
                                                                                                    #
                                                                                                    #Serial.println ("Starting Watchdog Test.  This test takes less than a minute");
                                                                                                    #watchdogTest();
                                                                                                    #Serial.print(millis() / 1000); Serial.print (": Watchdog test complete.  Pass: "); Serial.print(passCount); Serial.print(" Fail: "); Serial.println(failCount);
                                                                                                    #
                                                                                                    #
                                                                                                    # #ifdef UNIT_TEST_PULSE_TIMER
                                                                                                    # #ifdef TEST_SW18AB
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: print("Starting 18AB PulseTimer Test.  This test takes about 3 minutes")
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: resetAll()
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: pulseTimerTest(SW18AB_6B,0,19)
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: print("Pulse Timer test complete.  Pass: "); Serial.print(passCount); Serial.print(" Fail: "); Serial.println(failCount, end="")
                                                                                                    # #endif
                                                                                                    # #ifdef TEST_SW8B
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: if SW8B_68.isPinModeSupported(PIN_MODE_PULSETIMER):
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: print("Starting 8B PulseTimer Test.  This test takes about 3 minutes")
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: resetAll()
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: pulseTimerTest(SW8B_68,0,7)
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: print("Pulse Timer test complete.  Pass: "); Serial.print(passCount); Serial.print(" Fail: "); Serial.println(failCount, end="")
                                                                                                    # #endif
                                                                                                    # #endif

                                                                                                    # #ifdef UNIT_TEST_PROTECTED_OUTPUT
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: print("Starting Protected Output Test.  This test takes about 1 minute")
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: resetAll()
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: protectedOutputTest18AB()
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: print("Protected Output test complete.  Pass: "); Serial.print(passCount); Serial.print(" Fail: "); Serial.println(failCount, end="")
                                                                                                    # #endif

                                                                                                    # #ifdef UNIT_TEST_PULSE_ON_CHANGE
                                                                                                    # #ifdef TEST_SW8B
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: if SW8B_68.isPinModeSupported(PIN_MODE_PULSE_ON_CHANGE):
                                                                                                        # TODO_MANUAL_CONVERSION_INDENT: print("Starting Pulse On Change Test SW8B.  This test takes about 1 minute")
                                                                                                        # TODO_MANUAL_CONVERSION_INDENT: resetAll()
                                                                                                        # TODO_MANUAL_CONVERSION_INDENT: pulseOnChangeTest(SW8B_68)
                                                                                                        # TODO_MANUAL_CONVERSION_INDENT: print("Pulse On Change test complete.  Pass: "); Serial.print(passCount); Serial.print(" Fail: "); Serial.println(failCount, end="")
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: else:
                                                                                                        # TODO_MANUAL_CONVERSION_INDENT: print("Pulse On Change not supported in this build of SW8B")
                                                                                                      # #endif
                                                                                                      # #ifdef TEST_SW18AB
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: print("Starting Pulse On Change Test SW18AB.  This test takes about 1 minute")
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: resetAll()
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: pulseOnChangeTest(SW18AB_6B)
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: print("Pulse On Change test complete.  Pass: "); Serial.print(passCount); Serial.print(" Fail: "); Serial.println(failCount, end="")
                                                                                                      # #endif
                                                                                                      # #endif

                                                                                                      # #ifdef UNIT_TEST_WATCHDOG
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: print("Starting WATCHDOG Test.  This test takes about 1 minute")
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: resetAll()
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: watchdogTest18AB()
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: print("WATCHDOG test complete.  Pass: "); Serial.print(passCount); Serial.print(" Fail: "); Serial.println(failCount, end="")
                                                                                                      # #endif

                                                                                                      # #ifdef UNIT_TEST_SEQUENCE_TEST
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: print("Starting Sequence Test.  This test takes less than a minute")
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: resetAll()
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: SequenceTest()
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: print("Sequence test complete.  Pass: "); Serial.print(passCount); Serial.print(" Fail: "); Serial.println(failCount, end="")
                                                                                                      # #endif
                                                                                                      # #ifdef UNIT_TEST_PUBLIC_DATA
                                                                                                      # #ifdef TEST_SW4B
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: print("Starting 4B Public Data Test.  This test takes less than 2 minutes")
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: resetAll()
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: publicDataTest(SW4B_6C )
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: print(millis() / 1000); Serial.print (": Public Data test complete.  Pass: "); Serial.print(passCount); Serial.print(" Fail: "); Serial.println(failCount, end="")
                                                                                                      # #endif
                                                                                                      # #ifdef TEST_SW8B
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: print("Starting 8B Public Data Test.  This test takes less than 2 minutes")
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: resetAll()
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: publicDataTest(SW8B_68 )
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: print(millis() / 1000); Serial.print (": Public Data test complete.  Pass: "); Serial.print(passCount); Serial.print(" Fail: "); Serial.println(failCount, end="")
                                                                                                      # #endif
                                                                                                      # #ifdef TEST_SW18AB
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: print("Starting 18AB Public Data Test.  This test takes less than 2 minutes")
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: resetAll()
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: publicDataTest(SW18AB_6B )
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: print(millis() / 1000); Serial.print (": Public Data test complete.  Pass: "); Serial.print(passCount); Serial.print(" Fail: "); Serial.println(failCount, end="")
                                                                                                      # #endif
                                                                                                      # #endif
                                                                                                      # #ifdef UNIT_TEST_ANALOG_INPUT
                                                                                                      # #ifdef TEST_SW18AB
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: print("Starting 18AB Analog Input Test.  This test takes less than 2 minutes")
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: resetAll()
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: analogInputTest(SW18AB_6B)
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: print("18AB Analog Input test complete.  Pass: "); Serial.print(passCount); Serial.print(" Fail: "); Serial.println(failCount, end="")
                                                                                                      # #endif
                                                                                                      # #ifdef TEST_SW4B
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: print("Starting 4B Analog Input Test.  This test takes less than 2 minutes")
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: resetAll()
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: analogInputTest(SW4B_6C)
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: print("4B Analog Input test complete.  Pass: "); Serial.print(passCount); Serial.print(" Fail: "); Serial.println(failCount, end="")
                                                                                                      # #endif
                                                                                                      # #ifdef TEST_SW8B

                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: if SW8B_68.isPinModeSupported(PIN_MODE_ANALOGINPUT):
                                                                                                        # TODO_MANUAL_CONVERSION_INDENT: print("Starting 8B Analog Input Test.  This test takes less than 2 minutes")
                                                                                                        # TODO_MANUAL_CONVERSION_INDENT: resetAll()
                                                                                                        # TODO_MANUAL_CONVERSION_INDENT: analogInputTest(SW8B_68)
                                                                                                        # TODO_MANUAL_CONVERSION_INDENT: print("8B Analog Input test complete.  Pass: "); Serial.print(passCount); Serial.print(" Fail: "); Serial.println(failCount, end="")
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: else:
                                                                                                        # TODO_MANUAL_CONVERSION_INDENT: print("Analog Pin Mode Not Available in SW8B")
                                                                                                      # #endif

                                                                                                      # #endif

                                                                                                      # #ifdef UNIT_TEST_BLINK
                                                                                                      # #ifdef TEST_SW18AB
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: print("Starting 18AB Blink Test.  This test takes less than 2 minutes")
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: resetAll()
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: blinkTest(SW18AB_6B,6,5)
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: print("18AB Blink  test complete.  Pass: "); Serial.print(passCount); Serial.print(" Fail: "); Serial.println(failCount, end="")
                                                                                                      # #endif
                                                                                                      # #ifdef TEST_SW8B
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: print("Starting 8B Blink  Test.  This test takes less than 2 minutes")
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: resetAll()
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: blinkTest(SW8B_68,6,5)
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: print("8B Blink test complete.  Pass: "); Serial.print(passCount); Serial.print(" Fail: "); Serial.println(failCount, end="")
                                                                                                      # #endif

                                                                                                      # #endif


                                                                                                      # #ifdef UNIT_TEST_SCALING
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: print("Starting Scaling Test.  This test takes less than 10 minutes")
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: resetAll()
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: scalingTest()
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: print("Scaling complete.  Pass: "); Serial.print(passCount); Serial.print(" Fail: "); Serial.println(failCount, end="")
                                                                                                      # #endif

                                                                                                      # #ifdef UNIT_TEST_INPUT_PROCESSOR
                                                                                                      # #ifdef TEST_SW18AB
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: print("Starting 18AB Input Processor Test.  This test takes less than 5 minutes")
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: resetAll()
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: inputProcessorTest(SW18AB_6B, 19)
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: print("Input Processor Test complete.  Pass: "); Serial.print(passCount); Serial.print(" Fail: "); Serial.println(failCount, end="")
                                                                                                      # #endif
                                                                                                      # #ifdef TEST_SW8B
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: if SW8B_68.isPinModeSupported(PIN_MODE_INPUT_PROCESSOR):

                                                                                                        # TODO_MANUAL_CONVERSION_INDENT: print("Starting 8B Input Processor Test.  This test takes less than 5 minutes")
                                                                                                        # TODO_MANUAL_CONVERSION_INDENT: resetAll()
                                                                                                        # TODO_MANUAL_CONVERSION_INDENT: inputProcessorTest(SW8B_68,4)
                                                                                                        # TODO_MANUAL_CONVERSION_INDENT: print("Input Processor Test complete.  Pass: "); Serial.print(passCount); Serial.print(" Fail: "); Serial.println(failCount, end="")
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: else:
                                                                                                        # TODO_MANUAL_CONVERSION_INDENT: print("Input Processor Pin Mode Not Available in SW8B")
                                                                                                      # #endif


                                                                                                      # #endif

                                                                                                      # #ifdef UNIT_TEST_HSCLOCK
                                                                                                      # #ifdef TEST_SW18AB
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: print("Starting High Speed Clock Test 18AB.  This test takes less than 1 minute")
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: resetAll()
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: hsClockTest()
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: print("HSClock complete.  Pass: "); Serial.print(passCount); Serial.print(" Fail: "); Serial.println(failCount, end="")
                                                                                                      # #endif
                                                                                                      # #endif

                                                                                                      # #ifdef UNIT_TEST_HSCOUNTER
                                                                                                      # #ifdef TEST_SW18AB
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: print("Starting High Speed Counter Test 18AB.  This test takes less than 2 minutes")
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: resetAll()
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: hsCounterTest()
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: print("HSCounter complete.  Pass: "); Serial.print(passCount); Serial.print(" Fail: "); Serial.println(failCount, end="")
                                                                                                      # #endif
                                                                                                      # #endif

                                                                                                      # #ifdef UNIT_TEST_FRAME_TIMER
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: print("Starting Frame Timer Test.  This test takes less than 1 minute")
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: resetAll()
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: frameTimerTest()
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: print("FrameTimer complete.  Pass: "); Serial.print(passCount); Serial.print(" Fail: "); Serial.println(failCount, end="")
                                                                                                      # #endif

                                                                                                      # #ifdef UNIT_TEST_USDSENSOR
                                                                                                      # #ifdef TEST_SW18AB
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: print("Starting Ultrasonic Distance Sensor 18AB Test.  This test takes less than 1 minute")
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: usdSensorTest(10)
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: print("Ultrasonic Distance Sensor Test   complete.  Pass: "); Serial.print(passCount); Serial.print(" Fail: "); Serial.println(failCount, end="")
                                                                                                      # #endif
                                                                                                      # #endif

                                                                                                      # #ifdef UNIT_TEST_FREQUENCY_OUTPUT
                                                                                                      # #ifdef TEST_SW18AB
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: print("Starting 18AB Frequency Output Test.  This test takes less than 1 minute")
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: frequencyOutputTest(SW18AB_6B,15);  #TODO add non TRM pin
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: print("Frequency Output   complete.  Pass: "); Serial.print(passCount); Serial.print(" Fail: "); Serial.println(failCount, end="")
                                                                                                      # #endif

                                                                                                      # #ifdef TEST_SW8B
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: if SW8B_68.isPinModeSupported(PIN_MODE_FREQUENCY_OUTPUT):
                                                                                                        # TODO_MANUAL_CONVERSION_INDENT: print("Starting 8B Frequency Output Test.  This test takes less than 1 minute")
                                                                                                        # TODO_MANUAL_CONVERSION_INDENT: frequencyOutputTest(SW8B_68,4)
                                                                                                        # TODO_MANUAL_CONVERSION_INDENT: print("Frequency Output   complete.  Pass: "); Serial.print(passCount); Serial.print(" Fail: "); Serial.println(failCount, end="")
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: else:
                                                                                                        # TODO_MANUAL_CONVERSION_INDENT: print("Frequency Output Not Available in SW8B")
                                                                                                      # #endif
                                                                                                      # #endif

                                                                                                      # #ifdef UNIT_TEST_HBRIDGE
                                                                                                      # #ifdef TEST_SW18AB
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: print("Starting 18AB H Bridge  Test.  This test takes less than 13 minutes")
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: hBridgeTest(SW18AB_6B,5,6)
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: print("H Bridge Test   complete.  Pass: "); Serial.print(passCount); Serial.print(" Fail: "); Serial.println(failCount, end="")
                                                                                                      # #endif
                                                                                                      # #ifdef TEST_SW8B
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: if SW8B_68.isPinModeSupported(PIN_MODE_HBRIDGE):
                                                                                                        # TODO_MANUAL_CONVERSION_INDENT: print("Starting 8B H Bridge  Test.  This test takes less than 13 minutes")
                                                                                                        # TODO_MANUAL_CONVERSION_INDENT: hBridgeTest(SW8B_68,5,6)
                                                                                                        # TODO_MANUAL_CONVERSION_INDENT: print("H Bridge Test   complete.  Pass: "); Serial.print(passCount); Serial.print(" Fail: "); Serial.println(failCount, end="")
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: else:
                                                                                                        # TODO_MANUAL_CONVERSION_INDENT: print("H Bridge not supported in this build of SW8B")
                                                                                                      # #endif

                                                                                                      # #endif

                                                                                                      # #ifdef UNIT_TEST_QUEUED_PULSE_OUTPUT
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: print("Starting Queued Pulse Output  Test.  This test takes less than XX minutes")
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: queuedPulseOutputTest()
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: print("Queued Pulse Output Test   complete.  Pass: "); Serial.print(passCount); Serial.print(" Fail: "); Serial.println(failCount, end="")

                                                                                                      # #endif

                                                                                                      # #ifdef UNIT_TEST_DATALOGGER
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: print("Starting DataLogger  Test.  This test takes less than XX minutes")
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: dataLoggerTest()
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: print("Queued DataLogger Test   complete.  Pass: "); Serial.print(passCount); Serial.print(" Fail: "); Serial.println(failCount, end="")

                                                                                                      # #endif


                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: def disablePPS(sw):
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: b = [219, 1, 16, 0x55, 0x55, 0x55, 0x55, 0x55]
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: sw.sendPacket(b)
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: b[1] = 2
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: sw.sendPacket(b)
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: b[1] = 3
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: sw.sendPacket(b)

                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: sw.pinMode(1, 0)
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: sw.pinMode(2, 0)
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: sw.pinMode(3, 0)

                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: def resetAll():
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: versionChecked = False
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: analogShutdown()

                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: SW8B_68.registerErrorHandler(None)
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: SW8B_68.begin()  # Python interface was configured above
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: while not SW8B_68.queryVersion():
                                                                                                        # TODO_MANUAL_CONVERSION_INDENT: print("Serial Wombat chip at 0x68 did not respond to version query")
                                                                                                        # TODO_MANUAL_CONVERSION_INDENT: SW8B_68.begin()  # Python interface was configured above
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: if not versionChecked  and  not SW8B_68.isLatestFirmware():
                                                                                                        # TODO_MANUAL_CONVERSION_INDENT: print("Serial Wombat chip at 0x68 is not latest firmware")



                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: SW18AB_6B.registerErrorHandler(None)
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: SW18AB_6B.begin()  # Python interface was configured above
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: while not SW18AB_6B.queryVersion():
                                                                                                        # TODO_MANUAL_CONVERSION_INDENT: print("Serial Wombat chip at 0x6B did not respond to version query")
                                                                                                        # TODO_MANUAL_CONVERSION_INDENT: SW18AB_6B.begin()  # Python interface was configured above
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: if not versionChecked  and  not SW18AB_6B.isLatestFirmware():
                                                                                                        # TODO_MANUAL_CONVERSION_INDENT: print("Serial Wombat chip at 0x6B is not latest firmware")


                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: SW4B_6C.begin()  # Python interface was configured above
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: while not SW4B_6C.queryVersion():
                                                                                                        # TODO_MANUAL_CONVERSION_INDENT: print("Serial Wombat chip at 0x6C did not respond to version query")
                                                                                                        # TODO_MANUAL_CONVERSION_INDENT: SW4B_6C.begin()  # Python interface was configured above
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: disablePPS(SW4B_6C)

                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: SW4B_6D.begin()  # Python interface was configured above
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: while not SW4B_6D.queryVersion():
                                                                                                        # TODO_MANUAL_CONVERSION_INDENT: print("Serial Wombat chip at 0x6D did not respond to version query")
                                                                                                        # TODO_MANUAL_CONVERSION_INDENT: SW4B_6D.begin()  # Python interface was configured above
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: disablePPS(SW4B_6D)

                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: SW4B_6E.begin()  # Python interface was configured above
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: while not SW4B_6E.queryVersion():
                                                                                                        # TODO_MANUAL_CONVERSION_INDENT: print("Serial Wombat chip at 0x6E did not respond to version query")
                                                                                                        # TODO_MANUAL_CONVERSION_INDENT: SW4B_6E.begin()  # Python interface was configured above
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: disablePPS(SW4B_6E)

                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: SW4B_6F.begin()  # Python interface was configured above
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: while not SW4B_6F.queryVersion():
                                                                                                        # TODO_MANUAL_CONVERSION_INDENT: print("Serial Wombat chip at 0x6F did not respond to version query")
                                                                                                        # TODO_MANUAL_CONVERSION_INDENT: SW4B_6F.begin()  # Python interface was configured above
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: disablePPS(SW4B_6F)

                                                                                                      # #ifdef TEST_SW18AB
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: SW18AB_6B.registerErrorHandler(SerialWombatSerialErrorHandlerBrief)
                                                                                                      # #endif
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: versionChecked = True




                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: SW18AB_PT00 = SerialWombatPulseTimer.SerialWombatPulseTimer(SW4B_6D)
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: SW18AB_PT05 = SerialWombatPulseTimer.SerialWombatPulseTimer(SW4B_6D)
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: SW18AB_PT06 = SerialWombatPulseTimer.SerialWombatPulseTimer(SW4B_6D)
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: SW18AB_PT07 = SerialWombatPulseTimer.SerialWombatPulseTimer(SW4B_6C)
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: SW18AB_PT08 = SerialWombatPulseTimer.SerialWombatPulseTimer(SW4B_6D)
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: SW18AB_PT09 = SerialWombatPulseTimer.SerialWombatPulseTimer(SW4B_6C)
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: SW18AB_PT10 = SerialWombatPulseTimer.SerialWombatPulseTimer(SW4B_6C)
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: SW18AB_PT11 = SerialWombatPulseTimer.SerialWombatPulseTimer(SW4B_6C)
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: SW18AB_PT12 = SerialWombatPulseTimer.SerialWombatPulseTimer(SW4B_6E)
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: SW18AB_PT13 = SerialWombatPulseTimer.SerialWombatPulseTimer(SW4B_6F)
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: SW18AB_PT14 = SerialWombatPulseTimer.SerialWombatPulseTimer(SW4B_6F)
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: SW18AB_PT15 = SerialWombatPulseTimer.SerialWombatPulseTimer(SW4B_6F)
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: SW18AB_PT16 = SerialWombatPulseTimer.SerialWombatPulseTimer(SW4B_6F)
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: SW18AB_PT17 = SerialWombatPulseTimer.SerialWombatPulseTimer(SW4B_6E)
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: SW18AB_PT18 = SerialWombatPulseTimer.SerialWombatPulseTimer(SW4B_6E)
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: SW18AB_PT19 = SerialWombatPulseTimer.SerialWombatPulseTimer(SW4B_6E)

                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: SW8B_PT00 = SW18AB_PT06 = SerialWombatPulseTimer.SerialWombatPulseTimer()
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: SW8B_PT01 = SW18AB_PT00 = SerialWombatPulseTimer.SerialWombatPulseTimer()
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: SW8B_PT02 = SW18AB_PT16 = SerialWombatPulseTimer.SerialWombatPulseTimer()
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: SW8B_PT03 = SW18AB_PT17 = SerialWombatPulseTimer.SerialWombatPulseTimer()
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: SW8B_PT04 = SW18AB_PT09 = SerialWombatPulseTimer.SerialWombatPulseTimer()
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: SW8B_PT05 = SW18AB_PT07 = SerialWombatPulseTimer.SerialWombatPulseTimer()
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: SW8B_PT06 = SW18AB_PT18 = SerialWombatPulseTimer.SerialWombatPulseTimer()
                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: SW8B_PT07 = SW18AB_PT19 = SerialWombatPulseTimer.SerialWombatPulseTimer()




                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: SerialWombatPulseTimer* PulseTimerArray18AB[NUM_TEST_PINS] =
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: SW18AB_PT00,  #0
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: None,  # 1
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: None,  #2
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: None,  #3
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: None,  #4
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: SW18AB_PT05,  #5
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: SW18AB_PT06,  #6
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: SW18AB_PT07,  #7
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: SW18AB_PT08,  #8
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: SW18AB_PT09,  #9
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: SW18AB_PT10,  #10
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: SW18AB_PT11,  #11
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: SW18AB_PT12,  #12
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: SW18AB_PT13,  #13
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: SW18AB_PT14,  #14
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: SW18AB_PT15,  #15
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: SW18AB_PT16,  #16
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: SW18AB_PT17,  #17
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: SW18AB_PT18,  #18
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: SW18AB_PT19  #19


                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: SerialWombatPulseTimer* PulseTimerArray08B[NUM_TEST_PINS] =
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: SW8B_PT00,  #0
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: SW8B_PT01,  # 1
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: SW8B_PT02,  #2
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: SW8B_PT03,  #3
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: SW8B_PT04,  #4
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: SW8B_PT05,  #5
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: SW8B_PT06,  #6
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: SW8B_PT07,  #7
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: None,  #8
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: None,  #9
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: None,  #10
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: None,  #11
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: None,  #12
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: None,  #13
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: None,  #14
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: None,  #15
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: None,  #16
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: None,  #17
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: None,  #18
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: None  #19



                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: def initializePulseReaduS(sw, pin):
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: if sw == SW18AB_6B:
                                                                                                        # TODO_MANUAL_CONVERSION_INDENT: if pin < NUM_TEST_PINS:
                                                                                                          # TODO_MANUAL_CONVERSION_INDENT: if PulseTimerArray18AB[pin] != NULL:
                                                                                                            # TODO_MANUAL_CONVERSION_INDENT: PulseTimerArray18AB[pin].begin(SW18ABPinTo4BPin(pin))

                                                                                                          # TODO_MANUAL_CONVERSION_INDENT: else:
                                                                                                            # TODO_MANUAL_CONVERSION_INDENT: test("TEST ERROR:  None PIN in initializePulseReaduS",0)
                                                                                                        # TODO_MANUAL_CONVERSION_INDENT: else:
                                                                                                          # TODO_MANUAL_CONVERSION_INDENT: test("TEST ERROR:  INVALID PIN in initializePulseReaduS",0)
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: elif sw == SW8B_68:
                                                                                                        # TODO_MANUAL_CONVERSION_INDENT: if pin < NUM_TEST_PINS:
                                                                                                          # TODO_MANUAL_CONVERSION_INDENT: if PulseTimerArray08B[pin] != NULL:
                                                                                                            # TODO_MANUAL_CONVERSION_INDENT: PulseTimerArray08B[pin].begin(SW8BPinTo4BPin(pin))
                                                                                                          # TODO_MANUAL_CONVERSION_INDENT: else:
                                                                                                            # TODO_MANUAL_CONVERSION_INDENT: test("TEST ERROR:  None PIN in initializePulseReaduS",0)
                                                                                                        # TODO_MANUAL_CONVERSION_INDENT: else:
                                                                                                          # TODO_MANUAL_CONVERSION_INDENT: test("TEST ERROR:  INVALID PIN in initializePulseReaduS",0)
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: else:
                                                                                                        # TODO_MANUAL_CONVERSION_INDENT: test("TEST ERROR:  INVALID CHIP in initializePulseReaduS",0)


                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: def dutyCycleRead(sw, pin):
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: if sw == SW18AB_6B:
                                                                                                        # TODO_MANUAL_CONVERSION_INDENT: if pin < NUM_TEST_PINS:
                                                                                                          # TODO_MANUAL_CONVERSION_INDENT: if PulseTimerArray18AB[pin] != NULL:


                                                                                                            # TODO_MANUAL_CONVERSION_INDENT: PulseTimerArray18AB[pin].refreshHighCountsLowCounts()
                                                                                                            # TODO_MANUAL_CONVERSION_INDENT: result = 65536*PulseTimerArray18AB[pin].HighCounts
                                                                                                            # TODO_MANUAL_CONVERSION_INDENT: result /= (PulseTimerArray18AB[pin].HighCounts + PulseTimerArray18AB[pin].LowCounts)
                                                                                                            # TODO_MANUAL_CONVERSION_INDENT: return result
                                                                                                          # TODO_MANUAL_CONVERSION_INDENT: else:
                                                                                                            # TODO_MANUAL_CONVERSION_INDENT: test("TEST ERROR:  None PIN in pulseRead",0)
                                                                                                            # TODO_MANUAL_CONVERSION_INDENT: return 0
                                                                                                        # TODO_MANUAL_CONVERSION_INDENT: else:
                                                                                                          # TODO_MANUAL_CONVERSION_INDENT: test("TEST ERROR:  INVALID PIN in pulseRead",0)
                                                                                                          # TODO_MANUAL_CONVERSION_INDENT: return 0
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: elif sw == SW8B_68:
                                                                                                        # TODO_MANUAL_CONVERSION_INDENT: if pin < NUM_TEST_PINS:
                                                                                                          # TODO_MANUAL_CONVERSION_INDENT: if PulseTimerArray08B[pin] != NULL:

                                                                                                            # TODO_MANUAL_CONVERSION_INDENT: PulseTimerArray08B[pin].refreshHighCountsLowCounts()
                                                                                                            # TODO_MANUAL_CONVERSION_INDENT: result = 65536*PulseTimerArray08B[pin].HighCounts
                                                                                                            # TODO_MANUAL_CONVERSION_INDENT: result /= (PulseTimerArray08B[pin].HighCounts + PulseTimerArray08B[pin].LowCounts)
                                                                                                            # TODO_MANUAL_CONVERSION_INDENT: return result

                                                                                                          # TODO_MANUAL_CONVERSION_INDENT: else:
                                                                                                            # TODO_MANUAL_CONVERSION_INDENT: test("TEST ERROR:  None PIN in pulseRead",0)
                                                                                                            # TODO_MANUAL_CONVERSION_INDENT: return 0
                                                                                                        # TODO_MANUAL_CONVERSION_INDENT: else:
                                                                                                          # TODO_MANUAL_CONVERSION_INDENT: test("TEST ERROR:  INVALID PIN in pulseRead",0)
                                                                                                          # TODO_MANUAL_CONVERSION_INDENT: return 0
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: else:
                                                                                                        # TODO_MANUAL_CONVERSION_INDENT: test("TEST ERROR:  INVALID CHIP in pulseRead",0)
                                                                                                        # TODO_MANUAL_CONVERSION_INDENT: return 0


                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: def pulseRead(sw, pin):
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: if sw == SW18AB_6B:
                                                                                                        # TODO_MANUAL_CONVERSION_INDENT: if pin < NUM_TEST_PINS:
                                                                                                          # TODO_MANUAL_CONVERSION_INDENT: if PulseTimerArray18AB[pin] != NULL:
                                                                                                            # TODO_MANUAL_CONVERSION_INDENT: return PulseTimerArray18AB[pin].readHighCounts()
                                                                                                          # TODO_MANUAL_CONVERSION_INDENT: else:
                                                                                                            # TODO_MANUAL_CONVERSION_INDENT: test("TEST ERROR:  None PIN in pulseRead",0)
                                                                                                            # TODO_MANUAL_CONVERSION_INDENT: return 0
                                                                                                        # TODO_MANUAL_CONVERSION_INDENT: else:
                                                                                                          # TODO_MANUAL_CONVERSION_INDENT: test("TEST ERROR:  INVALID PIN in pulseRead",0)
                                                                                                          # TODO_MANUAL_CONVERSION_INDENT: return 0
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: elif sw == SW8B_68:
                                                                                                        # TODO_MANUAL_CONVERSION_INDENT: if pin < NUM_TEST_PINS:
                                                                                                          # TODO_MANUAL_CONVERSION_INDENT: if PulseTimerArray08B[pin] != NULL:
                                                                                                            # TODO_MANUAL_CONVERSION_INDENT: return PulseTimerArray08B[pin].readHighCounts()
                                                                                                          # TODO_MANUAL_CONVERSION_INDENT: else:
                                                                                                            # TODO_MANUAL_CONVERSION_INDENT: test("TEST ERROR:  None PIN in pulseRead",0)
                                                                                                            # TODO_MANUAL_CONVERSION_INDENT: return 0
                                                                                                        # TODO_MANUAL_CONVERSION_INDENT: else:
                                                                                                          # TODO_MANUAL_CONVERSION_INDENT: test("TEST ERROR:  INVALID PIN in pulseRead",0)
                                                                                                          # TODO_MANUAL_CONVERSION_INDENT: return 0
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: else:
                                                                                                        # TODO_MANUAL_CONVERSION_INDENT: test("TEST ERROR:  INVALID CHIP in pulseRead",0)
                                                                                                        # TODO_MANUAL_CONVERSION_INDENT: return 0
                                                                                                      # #if 0
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: if pin < NUM_TEST_PINS:
                                                                                                        # TODO_MANUAL_CONVERSION_INDENT: if PulseTimerArray[pin] != NULL:
                                                                                                          # TODO_MANUAL_CONVERSION_INDENT: return PulseTimerArray[pin].readHighCounts()
                                                                                                        # TODO_MANUAL_CONVERSION_INDENT: else:
                                                                                                          # TODO_MANUAL_CONVERSION_INDENT: print("TEST ERROR:  None PIN in pulseRead")
                                                                                                          # TODO_MANUAL_CONVERSION_INDENT: return 0
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: else:
                                                                                                        # TODO_MANUAL_CONVERSION_INDENT: print("TEST ERROR:  INVALID PIN in pulseRead")
                                                                                                        # TODO_MANUAL_CONVERSION_INDENT: return 0
                                                                                                      # #endif




                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: def pulseCounts(sw, pin):
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: if sw == SW18AB_6B:
                                                                                                        # TODO_MANUAL_CONVERSION_INDENT: if pin < NUM_TEST_PINS:
                                                                                                          # TODO_MANUAL_CONVERSION_INDENT: if PulseTimerArray18AB[pin] != NULL:
                                                                                                            # TODO_MANUAL_CONVERSION_INDENT: return PulseTimerArray18AB[pin].readPulses()
                                                                                                          # TODO_MANUAL_CONVERSION_INDENT: else:
                                                                                                            # TODO_MANUAL_CONVERSION_INDENT: test("TEST ERROR:  None PIN in pulseCounts",0)
                                                                                                            # TODO_MANUAL_CONVERSION_INDENT: return 0
                                                                                                        # TODO_MANUAL_CONVERSION_INDENT: else:
                                                                                                          # TODO_MANUAL_CONVERSION_INDENT: test("TEST ERROR:  INVALID PIN in pulseCounts",0)
                                                                                                          # TODO_MANUAL_CONVERSION_INDENT: return 0
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: elif sw == SW8B_68:
                                                                                                        # TODO_MANUAL_CONVERSION_INDENT: if pin < NUM_TEST_PINS:
                                                                                                          # TODO_MANUAL_CONVERSION_INDENT: if PulseTimerArray08B[pin] != NULL:
                                                                                                            # TODO_MANUAL_CONVERSION_INDENT: return PulseTimerArray08B[pin].readPulses()
                                                                                                          # TODO_MANUAL_CONVERSION_INDENT: else:
                                                                                                            # TODO_MANUAL_CONVERSION_INDENT: test("TEST ERROR:  None PIN in pulseCounts",0)
                                                                                                            # TODO_MANUAL_CONVERSION_INDENT: return 0
                                                                                                        # TODO_MANUAL_CONVERSION_INDENT: else:
                                                                                                          # TODO_MANUAL_CONVERSION_INDENT: test("TEST ERROR:  INVALID PIN in pulseCounts",0)
                                                                                                          # TODO_MANUAL_CONVERSION_INDENT: return 0
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: else:
                                                                                                        # TODO_MANUAL_CONVERSION_INDENT: test("TEST ERROR:  INVALID CHIP in pulseCounts",0)
                                                                                                        # TODO_MANUAL_CONVERSION_INDENT: return 0

                                                                                                      # #if 0
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: if pin < NUM_TEST_PINS:
                                                                                                        # TODO_MANUAL_CONVERSION_INDENT: if PulseTimerArray[pin] != NULL:
                                                                                                          # TODO_MANUAL_CONVERSION_INDENT: return PulseTimerArray[pin].readPulses()
                                                                                                        # TODO_MANUAL_CONVERSION_INDENT: else:
                                                                                                          # TODO_MANUAL_CONVERSION_INDENT: print("TEST ERROR:  None PIN in pulseCounts")
                                                                                                          # TODO_MANUAL_CONVERSION_INDENT: return 0
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: else:
                                                                                                        # TODO_MANUAL_CONVERSION_INDENT: print("TEST ERROR:  INVALID PIN in pulseCounts")
                                                                                                        # TODO_MANUAL_CONVERSION_INDENT: return 0
                                                                                                      # #endif

                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: def withinRange(value, expected, sixtyFourths, counts):
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: x32 = expected
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: if (value > x32 + counts)  and  (value > x32 * (64 + sixtyFourths) / 64):
                                                                                                        # TODO_MANUAL_CONVERSION_INDENT: return False
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: if (value < x32 - counts)  and  (value < x32 * (64 - sixtyFourths) / 64):
                                                                                                        # TODO_MANUAL_CONVERSION_INDENT: return False
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: return True

                                                                                                    # TODO_MANUAL_CONVERSION_INDENT: def test(designator, value, expected, counts, sixtyFourths):
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: if withinRange(value, expected, sixtyFourths, counts):
                                                                                                        # TODO_MANUAL_CONVERSION_INDENT: pass(1)
                                                                                                      # TODO_MANUAL_CONVERSION_INDENT: else:
                                                                                                        # TODO_MANUAL_CONVERSION_INDENT: fail(1)
                                                                                                        # TODO_MANUAL_CONVERSION_INDENT: failPacket = [0x40,0,SW_LE16(expected) , SW_LE16(value),0x55,0x55]
                                                                                                        # TODO_MANUAL_CONVERSION_INDENT: SW18AB_6B.sendPacket(failPacket)
                                                                                                        # TODO_MANUAL_CONVERSION_INDENT: print(designator);  Serial.print(" V: "); Serial.print(value); Serial.print(" X:"); Serial.println(expected, end="")


setup()
while True:
    loop()
