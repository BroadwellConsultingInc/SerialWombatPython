# Converted from Testing/SW4B_SW18AB_SW08B_AutomatedTest/IR_TX_RX.ino
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
import SerialWombatIRRx
import SerialWombatIRTx

irRx18 = SerialWombatIRRx.SerialWombatIRRx(SW18AB_6B)
irRx8 = SerialWombatIRRx.SerialWombatIRRx(SW8B_68)
irTx18 = SerialWombatIRTx.SerialWombatIRTx(SW18AB_6B)
irTx8 = SerialWombatIRTx.SerialWombatIRTx(SW8B_68)
def irTxRxTest():
  # Basic test using stream functions
    irRx18.begin(19,
    DATACOUNT,
    0,  #Mode
    True,  #Use Repeat
    SW_HIGH  #Active
    )
    irTx8.begin(SW18ABPinTo8BPin(19), 0x1234)

    irTx18.begin(18,
    0x2345  #Address
    )
    irRx8.begin(SW18ABPinTo8BPin(18),
    DATACOUNT,
    0,  #Mode
    True,  #Use Repeat
    SW_HIGH  #Active
    )

    # Send a stream of commands to each and verify that they were received

    for i in range(0, 9):
      irTx8.write((i + 80))
      irTx18.write((i + 180))
    delay(3000)
    for i in range(0, 9):
      test("irRx8 basic stream", irRx8.read(), i + 180)
      test("irRx18 basic stream", irRx18.read(), i + 80)

  #Test Repeat
    irRx18.begin(19,
    DATACOUNT,
    0,  #Mode
    True,  #Use Repeat
    SW_HIGH  #Active
    )
    irTx8.begin(SW18ABPinTo8BPin(19), 0x1234)

    irTx18.begin(18,
    0x2345  #Address
    )
    irRx8.begin(SW18ABPinTo8BPin(18),
    DATACOUNT,
    0,  #Mode
    True,  #Use Repeat
    SW_HIGH  #Active
    )

    # Send a command and 14 repeat commands.  Verify that the right number (15) are received


    irTx8.sendMessage(80, 0x5678, 14)
    irTx18.sendMessage(180, 0x6789, 14)

    delay(10000)
    for i in range(0, 20):
      if i < 15:
        test("irRx8 repeat", irRx8.read(), 180)
        test("irRx18 repeat", irRx18.read(), 80)
      else:
        test("irRx8 repeat end", irRx8.read(), 65535)
        test("irRx18 repeat end", irRx18.read(), 65535)




  #Test Addressing
    irRx18.begin(19,
    DATACOUNT,
    0,  #Mode
    True,  #Use Repeat
    SW_HIGH,  #Active
    1000,  #Timeout period
    65535,  # timeoutValue
    True,  #Use Address Filter
    0x1234  #Address
    )
    irTx8.begin(SW18ABPinTo8BPin(19), 0x1234)

    irTx18.begin(18,
    0x2345  #Address
    )
    irRx8.begin(SW18ABPinTo8BPin(18),
    DATACOUNT,
    0,  #Mode
    True,  #Use Repeat
    SW_HIGH,  #Active
    1000,  #Timeout period
    65535,  # timeoutValue
    True,  #Use Address Filter
    0x2345  #Address
    )

    # Send a command and 14 repeat commands, and then a message with wrong address.  Verify that the right number (15) are received


    irTx8.sendMessage(80, 0x1234, 14)
    irTx18.sendMessage(180, 0x2345, 14)
    irTx8.sendMessage(80, 0x89AB, 14)
    irTx18.sendMessage(180, 0x89AB, 14)

    delay(10000)
    for i in range(0, 20):
      if i < 15:
        test("irRx8 addressed repeat", irRx8.read(), 180)
        test("irRx18 addressed repeat", irRx18.read(), 80)
      else:
        test("irRx8 addressed repeat end", irRx8.read(), 65535)
        test("irRx18 addressedrepeat end", irRx18.read(), 65535)

    test ("irRx8 addressed repeat public data count",irRx8.readPublicData(),15)
    test ("irRx18 addressed repeat public data count",irRx18.readPublicData(),15)


  #Test  public data Address
    irRx18.begin(19,
    ADDRESS,
    0,  #Mode
    True,  #Use Repeat
    SW_HIGH,  #Active
    1000,  #Timeout period
    65535,  # timeoutValue
    True,  #Use Address Filter
    0x1234  #Address

    )
    irTx8.begin(SW18ABPinTo8BPin(19), 0x1234)

    irTx18.begin(18,
    0x2345  #Address
    )
    irRx8.begin(SW18ABPinTo8BPin(18),
    ADDRESS,
    0,  #Mode
    True,  #Use Repeat
    SW_HIGH,  #Active
    1000,  #Timeout period
    65535,  # timeoutValue
    True,  #Use Address Filter
    0x2345  #Address
    )

    # Send a command and 14 repeat commands, and then a message with wrong address.  Verify that the right number (15) are received


    irTx8.sendMessage(80, 0x1234, 14)
    irTx18.sendMessage(180, 0x2345, 14)
    delay(10000)
    test ("irRx8 addressed repeat public data address A1 ",irRx8.readPublicData(),0x2345)
    test ("irRx18 addressed repeat public data address B1 ",irRx18.readPublicData(), 0x1234)
    irTx8.sendMessage(80, 0x89AB, 14)
    irTx18.sendMessage(180, 0x89AB, 14)

    delay(10000)
    for i in range(0, 20):
      if i < 15:
        test("irRx8 addressed repeat B", irRx8.read(), 180)
        test("irRx18 addressed repeat B", irRx18.read(), 80)
      else:
        test("irRx8 addressed repeat end B", irRx8.read(), 65535)
        test("irRx18 addressedrepeat end B", irRx18.read(), 65535)

    test ("irRx8 addressed repeat public data address A1 ",irRx8.readPublicData(),0x89AB)
    test ("irRx18 addressed repeat public data address B1 ",irRx18.readPublicData(),0x89AB)



  #Test  public data Command
    irRx18.begin(19,
    COMMAND,
    0,  #Mode
    True,  #Use Repeat
    SW_HIGH,  #Active
    1000,  #Timeout period
    65535,  # timeoutValue
    True,  #Use Address Filter
    0x1234  #Address
    )
    irTx8.begin(SW18ABPinTo8BPin(19), 0x1234)

    irTx18.begin(18,
    0x2345  #Address
    )
    irRx8.begin(SW18ABPinTo8BPin(18),
    COMMAND,
    0,  #Mode
    True,  #Use Repeat
    SW_HIGH,  #Active
    1000,  #Timeout period
    65535,  # timeoutValue
    True,  #Use Address Filter
    0x2345  #Address
    )

    # Send a command and 14 repeat commands, and then a message with wrong address.  Verify that the right number (15) are received


    irTx8.sendMessage(80, 0x1234, 14)
    irTx18.sendMessage(180, 0x2345, 14)
    delay(250)
    test ("irRx8 addressed repeat public data addressed C1",irRx8.readPublicData(),180)
    test ("irRx18 addressed repeat public data addressed D1",irRx18.readPublicData(),80)
    irTx8.sendMessage(80, 0x89AB, 14)
    irTx18.sendMessage(180, 0x89AB, 14)

    delay(10000)
    for i in range(0, 20):
      if i < 15:
        test("irRx8 addressed repeat C", irRx8.read(), 180)
        test("irRx18 addressed repeat C", irRx18.read(), 80)
      else:
        test("irRx8 addressed repeat end C", irRx8.read(), 65535)
        test("irRx18 addressedrepeat end C", irRx18.read(), 65535)

    test ("irRx8 addressed repeat public data addressed C",irRx8.readPublicData(),65535);  #Timeout
    test ("irRx18 addressed repeat public data addressed D",irRx18.readPublicData(),65535);  #Timeout
