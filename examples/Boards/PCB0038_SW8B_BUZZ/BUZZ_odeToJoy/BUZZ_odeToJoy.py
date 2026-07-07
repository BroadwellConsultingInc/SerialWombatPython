# Converted from Boards/PCB0038_SW8B_BUZZ/BUZZ_odeToJoy/BUZZ_odeToJoy.ino
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
import SerialWombatFrequencyOutput




# sw is provided by the selected interface block above
buzz4 = SerialWombatFrequencyOutput.SerialWombatFrequencyOutput_18AB(sw)
buzz5 = SerialWombatFrequencyOutput.SerialWombatFrequencyOutput_18AB(sw)
buzz6 = SerialWombatFrequencyOutput.SerialWombatFrequencyOutput_18AB(sw)
buzz7 = SerialWombatFrequencyOutput.SerialWombatFrequencyOutput_18AB(sw)

NUMBER_OF_BUZZERS = 4
NUMBER_OF_NOTES_MAX = 65

# TODO_MANUAL_CONVERSION: extern uint16_t otj [NUMBER_OF_BUZZERS][NUMBER_OF_NOTES_MAX][2];  # otj = OdeToJoy






TIME_MULTIPLIER = 200
NOTE_CUTTOFF = 25

noteEndMillis = [0] * (NUMBER_OF_BUZZERS)
noteCurrentEntry = [0] * (NUMBER_OF_BUZZERS)


def setup():
  # #ifdef ARDUINO_ESP8266_GENERIC
  # Wire.begin() is handled by the selected Python interface block
  # #else
  # Wire.begin() is handled by the selected Python interface block
  # #endif

  # Serial.begin() is not used in this Python example

  delay(100)

  sw.begin()  # Python interface was configured above
  buzz4.begin(4)
  buzz5.begin(5)
  buzz6.begin(6)
  buzz7.begin(7)

    # TODO_MANUAL_CONVERSION_INDENT: i = 0
    # TODO_MANUAL_CONVERSION_INDENT: starttime = millis()
    # TODO_MANUAL_CONVERSION_INDENT: for i in range(0, NUMBER_OF_BUZZERS):
      # TODO_MANUAL_CONVERSION_INDENT: noteEndMillis[i] = starttime + otj[i][0][1] * TIME_MULTIPLIER
      # TODO_MANUAL_CONVERSION_INDENT: noteCurrentEntry[i] = 0
      # TODO_MANUAL_CONVERSION_INDENT: sw.writePublicData(i+ 4, otj[i][0][0]);  # Start first note


def loop():

  for i in range(0, NUMBER_OF_BUZZERS):
    if millis() > noteEndMillis[i]     and  otj[i][noteCurrentEntry[i]][1] != 0:

      ++noteCurrentEntry[i]
      sw.writePublicData(i+4,otj[i][noteCurrentEntry[i]][0])
      noteEndMillis[i] += otj[i][noteCurrentEntry[i]][1] * TIME_MULTIPLIER


    elif millis()  + NOTE_CUTTOFF > noteEndMillis[i]   and  otj[i][noteCurrentEntry[i]][1] != 0:
      sw.writePublicData(i+4,0)
  #
  #{
    # #if (millis() > note1StartMillis + otj_1[note1CurrentEntry][1]* TIME_MULTIPLIER   && otj_1[note1CurrentEntry][1] != 0)
    #{
      #
      #++note1CurrentEntry;
      #buzz5.writePublicData(otj_1[note1CurrentEntry][0]);
      #note1StartMillis = millis();
      #
      #}
      # #else if (millis() > note1StartMillis + otj_1[note1CurrentEntry][1]* TIME_MULTIPLIER  - NOTE_CUTTOFF  && otj_1[note1CurrentEntry][1] != 0)
      #{
        #buzz5.writePublicData(0);
        #}
        #}
        #
        #{
          # #if (millis() > note2StartMillis + otj_2[note2CurrentEntry][1]* TIME_MULTIPLIER   && otj_2[note2CurrentEntry][1] != 0)
          #{
            #char s[50];
            #sprintf(s, "%u %u %u", note2CurrentEntry, otj_2[note2CurrentEntry][0], otj_2[note2CurrentEntry][1]);
            #Serial.println(s);
            #++note2CurrentEntry;
            #buzz6.writePublicData(otj_2[note2CurrentEntry][0]);
            #note2StartMillis = millis();
            #
            #}
            # #else if (millis() > note2StartMillis + otj_2[note2CurrentEntry][1]* TIME_MULTIPLIER  - NOTE_CUTTOFF  && otj_2[note2CurrentEntry][1] != 0)
            #{
              #buzz6.writePublicData(0);
              #}
              #}
              #
              #{
                # #if (millis() > note3StartMillis + otj_3[note3CurrentEntry][1]* TIME_MULTIPLIER   && otj_3[note3CurrentEntry][1] != 0)
                #{
                  #char s[50];
                  #sprintf(s, "%u %u %u", note3CurrentEntry, otj_3[note3CurrentEntry][0], otj_2[note3CurrentEntry][1]);
                  #Serial.println(s);
                  #++note3CurrentEntry;
                  #buzz7.writePublicData(otj_3[note3CurrentEntry][0]);
                  #note3StartMillis = millis();
                  #
                  #}
                  # #else if (millis() > note3StartMillis + otj_3[note3CurrentEntry][1]* TIME_MULTIPLIER  - NOTE_CUTTOFF  && otj_3[note3CurrentEntry][1] != 0)
                  #{
                    #buzz7.writePublicData(0);
                    #}
                    #}
                    #


setup()
while True:
    loop()
