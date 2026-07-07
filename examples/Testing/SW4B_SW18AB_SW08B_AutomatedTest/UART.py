# Converted from Testing/SW4B_SW18AB_SW08B_AutomatedTest/UART.ino
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
import SerialWombatUART

sw18UART1 = SerialWombatUART.SerialWombatUART(SW18AB_6B)
sw18UART2 = SerialWombatUART.SerialWombatUART(SW18AB_6B)
sw8UART1 = SerialWombatUART.SerialWombatUART(SW8B_68)
sw8UART2 = SerialWombatUART.SerialWombatUART(SW8B_68)
UART1Match_6C = SerialWombatUART.SerialWombatUART(SW4B_6C)
UART2Match_6E = SerialWombatUART.SerialWombatUART(SW4B_6E)

SerialWombatUART* hwUART1
SerialWombatUART* hwUART2
SerialWombatUART* UART1Match
SerialWombatUART* UART2Match
uartRx = [0] * (200)
uartTx = [0] * (200)
txSeed = 1
countSeed = 1

# TODO_MANUAL_CONVERSION: baudArray = 
  # TODO_MANUAL_CONVERSION_INDENT: 300,
  # TODO_MANUAL_CONVERSION_INDENT: 1200,
  # TODO_MANUAL_CONVERSION_INDENT: 2400,
  # TODO_MANUAL_CONVERSION_INDENT: 4800,
  # TODO_MANUAL_CONVERSION_INDENT: 9600,
  # TODO_MANUAL_CONVERSION_INDENT: 19200,
  # TODO_MANUAL_CONVERSION_INDENT: 38400,
  # TODO_MANUAL_CONVERSION_INDENT: 57600,
  # TODO_MANUAL_CONVERSION_INDENT: 115200



def uartHWTest(sw, rxPin0, txPin0, rxPin1, txPin1):
  if sw == SW18AB_6B:
    hwUART1 = sw18UART1
    hwUART2 = sw18UART2
    UART1Match = UART1Match_6C
    UART2Match = UART2Match_6E
    SW4B_6C.pinMode(1,1)
    SW4B_6C.digitalWrite(1,1)
    SW4B_6E.pinMode(1,1)
    SW4B_6E.digitalWrite(1,1)
  elif sw == SW8B_68:

    hwUART1 = sw8UART1
    hwUART2 = None
    UART1Match = sw18UART1
  else:
    test("HW UART Invalid SW Chip",0,1)





  baudIteration = 0
  if sw == SW8B_68:
    baudIteration = 1
  # TODO_MANUAL_CONVERSION: for (; baudIteration < 9; ++ baudIteration) {
    # TODO return to 0
    #uint32_t rxSeed = txSeed;
    delayMs = 10000/ baudArray[baudIteration]
    txcount = 0
    hwUART1.begin(baudArray[baudIteration], rxPin0, rxPin0, txPin0)

    if sw == SW18AB_6B:

      UART1Match.begin(baudArray[baudIteration], 0, 0, 1)
    elif sw== SW8B_68:

      UART1Match.begin(baudArray[baudIteration], 9, 9, 7)

    if sw == SW18AB_6B:
      hwUART2.begin(baudArray[baudIteration], rxPin1, rxPin1, txPin1, 2)
      UART2Match.begin(baudArray[baudIteration], 3, 3, 1)
    for iteration in range(0, 500):
      txcount = wrandom(countSeed) % 32

      for i in range(0, txcount):
        uartTx[i] = wrandom(txSeed)
      SW18AB_6B.readPublicData(6);  #TODO Remove

      bytesWritten = hwUART1.write(uartTx, txcount)
      test("HWU 0",bytesWritten,txcount)

      delay(delayMs * txcount)
      # TODO_MANUAL_CONVERSION: bytesRead = UART1Match.readBytes((char*)uartRx, txcount)
      test("HWU 1",bytesRead,txcount)
      for i in range(0, txcount):
        c = [0] * (80)
        c = ("HWU 2 Baud: %d, iter: %d, i %d") % (baudIteration, iteration,i)
        test(c,uartRx[i],uartTx[i])
        #
        # #if (uartTx[i] == uartRx[i])
        #{
          #pass(1);
          #}
          # #else
          #{
            #Serial.print("F0: b: ");
            #Serial.print(baudIteration);
            #Serial.print("iter: ");
            #Serial.print(iteration);
            #Serial.print(" i: ");
            #Serial.println(i);
            #fail(1);
            #}
            #

          # TODO_MANUAL_CONVERSION_INDENT: txcount = wrandom(countSeed) % 32

          # TODO_MANUAL_CONVERSION_INDENT: for i in range(0, txcount):
            # TODO_MANUAL_CONVERSION_INDENT: uartTx[i] = wrandom(txSeed)
          # TODO_MANUAL_CONVERSION_INDENT: bytesWritten = UART1Match.write(uartTx, txcount)
          # TODO_MANUAL_CONVERSION_INDENT: test("HWU 4",bytesWritten,txcount)
          # TODO_MANUAL_CONVERSION_INDENT: delay(delayMs * txcount)
          # TODO_MANUAL_CONVERSION_INDENT: bytesRead = hwUART1.readBytes((char*)uartRx, txcount)
          # TODO_MANUAL_CONVERSION_INDENT: test("HWU 5",bytesRead,txcount)
          # TODO_MANUAL_CONVERSION_INDENT: for i in range(0, txcount):
            # TODO_MANUAL_CONVERSION_INDENT: c = [0] * (80)
            # TODO_MANUAL_CONVERSION_INDENT: c = ("HWU 6 Baud: %d, iter: %d, i %d") % (baudIteration, iteration,i)
            # TODO_MANUAL_CONVERSION_INDENT: test(c,uartRx[i],uartTx[i])
            #
            # #if (uartTx[i] == uartRx[i])
            #{
              #pass(1);
              #}
              # #else
              #{
                #Serial.print("F1: b: ");
                #Serial.print(baudIteration);
                #Serial.print(" iter: ");
                #Serial.print(iteration);
                #Serial.print(" i: ");
                #Serial.print(i);
                #Serial.print(" X: ");
                #Serial.print(uartTx[i]);
                #Serial.print(" G: ");
                #Serial.println(uartRx[i]);
                #fail(1);
                #}
                #
              # TODO_MANUAL_CONVERSION_INDENT: if sw == SW18AB_6B:

                # TODO_MANUAL_CONVERSION_INDENT: txcount = wrandom(countSeed) % 32

                # TODO_MANUAL_CONVERSION_INDENT: for i in range(0, txcount):
                  # TODO_MANUAL_CONVERSION_INDENT: uartTx[i] = wrandom(txSeed)

                # TODO_MANUAL_CONVERSION_INDENT: bytesWritten = hwUART2.write(uartTx, txcount)
                # TODO_MANUAL_CONVERSION_INDENT: test("HWU 7",bytesWritten,txcount)
                # TODO_MANUAL_CONVERSION_INDENT: delay(delayMs * txcount)
                # TODO_MANUAL_CONVERSION_INDENT: bytesRead = UART2Match.readBytes((char*)uartRx, txcount)
                # TODO_MANUAL_CONVERSION_INDENT: test("HWU 8",bytesRead,txcount)
                # TODO_MANUAL_CONVERSION_INDENT: for i in range(0, txcount):
                    # TODO_MANUAL_CONVERSION_INDENT: c = [0] * (80)
                    # TODO_MANUAL_CONVERSION_INDENT: c = ("HWU 9 Baud: %d, iter: %d, i %d") % (baudIteration, iteration,i)
                    # TODO_MANUAL_CONVERSION_INDENT: test(c,uartRx[i],uartTx[i])
                    #
                    # #if (uartTx[i] == uartRx[i])
                    #{
                      #pass(1);
                      #}
                      # #else
                      #{
                        #Serial.print("F2: b: ");
                        #Serial.print(baudIteration);
                        #Serial.print("iter: ");
                        #Serial.print(iteration);
                        #Serial.print(" i: ");
                        #Serial.println(i);
                        #fail(1);
                        #}
                        #

                      # TODO_MANUAL_CONVERSION_INDENT: txcount = wrandom(countSeed) % 32

                      # TODO_MANUAL_CONVERSION_INDENT: for i in range(0, txcount):
                        # TODO_MANUAL_CONVERSION_INDENT: uartTx[i] = wrandom(txSeed)
                      # TODO_MANUAL_CONVERSION_INDENT: bytesWritten = UART2Match.write(uartTx, txcount)
                      # TODO_MANUAL_CONVERSION_INDENT: test("HWU 10",bytesWritten,txcount)
                      # TODO_MANUAL_CONVERSION_INDENT: delay(delayMs * txcount)
                      # TODO_MANUAL_CONVERSION_INDENT: bytesRead = hwUART2.readBytes((char*)uartRx, txcount)
                      # TODO_MANUAL_CONVERSION_INDENT: test("HWU 11",bytesRead,txcount)
                      # TODO_MANUAL_CONVERSION_INDENT: for i in range(0, txcount):
                        # TODO_MANUAL_CONVERSION_INDENT: c = [0] * (80)
                        # TODO_MANUAL_CONVERSION_INDENT: c = ("HWU 12 Baud: %d, iter: %d, i %d") % (baudIteration, iteration,i)
                        # TODO_MANUAL_CONVERSION_INDENT: test(c,uartRx[i],uartTx[i])
                        #
                        # #if (uartTx[i] == uartRx[i])
                        #{
                          #pass(1);
                          #}
                          # #else
                          #{
                            #Serial.print("F3: b: ");
                            #Serial.print(baudIteration);
                            #Serial.print("iter: ");
                            #Serial.print(iteration);
                            #Serial.print(" i: ");
                            #Serial.println(i);
                            #fail(1);
                            #}
                            #

                    # TODO_MANUAL_CONVERSION_INDENT: return 0
