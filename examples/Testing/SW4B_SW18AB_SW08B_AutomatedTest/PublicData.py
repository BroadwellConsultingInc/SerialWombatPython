# Converted from Testing/SW4B_SW18AB_SW08B_AutomatedTest/PublicData.ino
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
import SerialWombatThroughputConsumer


tc18 = SerialWombatThroughputConsumer.SerialWombatThroughputConsumer(SW18AB_6B)
def publicDataTest(sw):

    number = sw.readPublicData(SW_DATA_SOURCE_INCREMENTING_NUMBER)

    for i in range(1, 500):
      if sw.readPublicData(SW_DATA_SOURCE_INCREMENTING_NUMBER) == number + i:
        pass
        # TODO_MANUAL_CONVERSION: pass(1)
      else:
        fail(1)
  # TODO_MANUAL_CONVERSION_INDENT: print("SW_DATA_SOURCE_1024mvCounts test not implemented")


    framesLSW = sw.readPublicData(SW_DATA_SOURCE_FRAMES_RUN_LSW)
    framesMSW = sw.readPublicData(SW_DATA_SOURCE_FRAMES_RUN_MSW)
    startTime = millis()
    startFrames = framesMSW
    startFrames <<=16
    startFrames += framesLSW

    delay(100000)

    framesLSW = sw.readPublicData(SW_DATA_SOURCE_FRAMES_RUN_LSW)
    framesMSW = sw.readPublicData(SW_DATA_SOURCE_FRAMES_RUN_MSW)
    endTime = millis()

    endFrames = framesMSW
    endFrames <<=16
    endFrames += framesLSW
    netTime = endTime - startTime
    netFrames = endFrames - startFrames

    if netTime < (( netFrames * 21) / 20)   and  netTime > ((netFrames * 19) / 20):
      pass
      # TODO_MANUAL_CONVERSION: pass(1)
    else:
      fail(1)



  # TODO_MANUAL_CONVERSION_INDENT: if sw == SW18AB_6B:
    tc18.begin(17)
    number = sw.readPublicData(SW_DATA_SOURCE_OVERRUN_FRAMES)
    numDroppedFrames = sw.readPublicData(SW_DATA_SOURCE_DROPPED_FRAMES)
    delay(100)
    finalNumber = sw.readPublicData(SW_DATA_SOURCE_OVERRUN_FRAMES)
    if finalNumber == number:
      pass
      # TODO_MANUAL_CONVERSION: pass(1)
    else:
      fail(1)
    tc18.write(0,1200)

    number = sw.readPublicData(SW_DATA_SOURCE_OVERRUN_FRAMES)

    delay(100)
    finalNumber = sw.readPublicData(SW_DATA_SOURCE_OVERRUN_FRAMES)
    if finalNumber >= number + 5:
      pass
      # TODO_MANUAL_CONVERSION: pass(1)
    else:
      fail(1)
    tc18.begin(17)

    finalNumDroppedFrames = sw.readPublicData(SW_DATA_SOURCE_DROPPED_FRAMES)
    if numDroppedFrames == finalNumDroppedFrames:
      pass
      # TODO_MANUAL_CONVERSION: pass(1)
    else:
      fail(1)
    numDroppedFrames = finalNumDroppedFrames
    tc18.write(0,2200)

    delay(100)
    finalNumDroppedFrames = sw.readPublicData(SW_DATA_SOURCE_OVERRUN_FRAMES)
    if finalNumDroppedFrames >= numDroppedFrames + 5:
      pass
      # TODO_MANUAL_CONVERSION: pass(1)
    else:
      fail(1)

    tc18.begin(17)
    delay(1000)
    systemUtilization = sw.readPublicData(SW_DATA_SOURCE_SYSTEM_UTILIZATION)
    tc18.writeAll(200)
    delay(1000)
    systemUtilization2 = sw.readPublicData(SW_DATA_SOURCE_SYSTEM_UTILIZATION)
    tc18.begin(17)
    difference = systemUtilization2 - systemUtilization
    if difference > 10000  and  difference < 16000:
      pass
      # TODO_MANUAL_CONVERSION: pass(1)
    else:
      print("SU: ", end="")
      print(systemUtilization, end="")
      print(" SU2: ", end="")
      print(systemUtilization2)
      fail(1)
  # TODO_MANUAL_CONVERSION_INDENT: print("SW_DATA_SOURCE_TEMPERATURE  test not implemented")
    number = sw.readPublicData(SW_DATA_SOURCE_PACKETS_RECEIVED)

    for i in range(0, 10):
      sw.readPublicData(SW_DATA_SOURCE_INCREMENTING_NUMBER)
    finalNumber = sw.readPublicData(SW_DATA_SOURCE_PACKETS_RECEIVED)
    if finalNumber == number + 11:
      pass
      # TODO_MANUAL_CONVERSION: pass(1)
    else:
      fail(1)

  # TODO_MANUAL_CONVERSION_INDENT: if sw == SW18AB_6B  or  sw == SW8B_68:
    sourceErrorsStart = sw.readPublicData(SW_DATA_SOURCE_ERRORS)

    for i in range(0, 10):
      sw.readPublicData(SW_DATA_SOURCE_INCREMENTING_NUMBER)

    tx = [200, 50,0,0,0,0,0,0];  # 50 is an invalid pin number
    sw.sendPacket(tx)
    sourceErrorsEnd = sw.readPublicData(SW_DATA_SOURCE_ERRORS)
    if sourceErrorsEnd == sourceErrorsStart + 1:
      pass
      # TODO_MANUAL_CONVERSION: pass(1)
    else:
      fail(1)


  # TODO_MANUAL_CONVERSION_INDENT: print("SW_DATA_SOURCE_LFSR  test not implemented")
  # TODO_MANUAL_CONVERSION_INDENT: if sw == SW18AB_6B:
    a = sw.readPublicData(SW_DATA_COM_ADDRESS_LOW)
    test("SW_DATA_COM_ADDRESS_LOW SW18AB ",a,0x6B)

  # TODO_MANUAL_CONVERSION_INDENT: if sw == SW8B_68:
    a = sw.readPublicData(SW_DATA_COM_ADDRESS_LOW)
    test("SW_DATA_COM_ADDRESS_LOW SW18AB ",a,0x68)

  # TODO_MANUAL_CONVERSION_INDENT: print("SW_DATA_SOURCE_1024mvCounts test not implemented")
  # TODO_MANUAL_CONVERSION_INDENT: print("SW_DATA_SOURCE_2HZ_SQUARE and similar  test not implemented")
