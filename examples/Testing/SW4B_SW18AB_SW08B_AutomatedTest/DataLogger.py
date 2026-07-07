# Converted from Testing/SW4B_SW18AB_SW08B_AutomatedTest/DataLogger.ino
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
import SerialWombat18ABDataLogger
import SerialWombatPWM
import SerialWombatQueue

swdl = SerialWombat18ABDataLogger.SerialWombat18ABDataLogger(SW18AB_6B)
dlQueue = SerialWombatQueue.SerialWombatQueue(SW18AB_6B)
DLQUEUELENGTH = 512
DLQUEUEADDR = 300
def dataLoggerTest():
  p0 = SerialWombatPWM.SerialWombatPWM(SW18AB_6B)
  p8 = SerialWombatPWM.SerialWombatPWM(SW18AB_6B)
  p10 = SerialWombatPWM.SerialWombatPWM(SW18AB_6B)
  p17 = SerialWombatPWM.SerialWombatPWM(SW18AB_6B)  # Set to PWMs to allow config of public data
  resetAll()
  p0.begin(0)
  p8.begin(8)
  p10.begin(10)
  p17.begin(17)

    # TODO_MANUAL_CONVERSION_INDENT: dlQueue.begin(DLQUEUEADDR,DLQUEUELENGTH)
    # TODO_MANUAL_CONVERSION_INDENT: swdl.begin(DLQUEUEADDR,DLQUEUELENGTH,True,  # Queue Frame Index
    # TODO_MANUAL_CONVERSION_INDENT: False,  # QueueOnChange
    # TODO_MANUAL_CONVERSION_INDENT: PERIOD_128mS)

    # TODO_MANUAL_CONVERSION_INDENT: swdl.configurePin(0,True,True)
    # TODO_MANUAL_CONVERSION_INDENT: swdl.configurePin(8,True,True)
    # TODO_MANUAL_CONVERSION_INDENT: swdl.configurePin(10,True,True)
    # TODO_MANUAL_CONVERSION_INDENT: swdl.configurePin(17,True,True)
    # TODO_MANUAL_CONVERSION_INDENT: swdl.enable(True)
    # TODO_MANUAL_CONVERSION_INDENT: delay(130)
    # TODO_MANUAL_CONVERSION_INDENT: p0.writePublicData(1000)
    # TODO_MANUAL_CONVERSION_INDENT: delay(130)
    # TODO_MANUAL_CONVERSION_INDENT: p8.writePublicData(2000)
    # TODO_MANUAL_CONVERSION_INDENT: delay(130)
    # TODO_MANUAL_CONVERSION_INDENT: p10.writePublicData(3000)
    # TODO_MANUAL_CONVERSION_INDENT: delay(130)
    # TODO_MANUAL_CONVERSION_INDENT: p17.writePublicData(4000)
    # TODO_MANUAL_CONVERSION_INDENT: delay(130)
    # TODO_MANUAL_CONVERSION_INDENT: swdl.enable(False)

    # Should be at least 5 * 2 * 5 = 50 data bytes available, no more than 60
      # TODO_MANUAL_CONVERSION_INDENT: i = dlQueue.available()
      # TODO_MANUAL_CONVERSION_INDENT: if i >= 50  and  i <=60:
        # TODO_MANUAL_CONVERSION_INDENT: i = 50
      # TODO_MANUAL_CONVERSION_INDENT: test("DataLogger_00", i, 50)

    # TODO_MANUAL_CONVERSION_INDENT: d0 = [0] * (5)
    # TODO_MANUAL_CONVERSION_INDENT: d1 = [0] * (5)
      # Test that first entry is all 0's

      # TODO_MANUAL_CONVERSION_INDENT: dlQueue.readUInt16(d0,5)
      # TODO_MANUAL_CONVERSION_INDENT: dlQueue.readUInt16(d1,5)

      # TODO_MANUAL_CONVERSION_INDENT: for i in range(1, 5):
        # TODO_MANUAL_CONVERSION_INDENT: st = [0] * (20)
        # TODO_MANUAL_CONVERSION_INDENT: st = ("Datalogger_01_%d") % (i)
        # TODO_MANUAL_CONVERSION_INDENT: test(st, d0[i], 0)
      # TODO_MANUAL_CONVERSION_INDENT: if d0[1] == d1[1]  and  d0[2] == d1[2]  and  d0[3] == d1[3]  and  d0[4] == d1[4]:
        # TODO_MANUAL_CONVERSION_INDENT: dlQueue.readUInt16(d1,5)
      # TODO_MANUAL_CONVERSION_INDENT: else:
        # TODO_MANUAL_CONVERSION_INDENT: test("Datalogger_02",d1[0]-d0[0],128)
      # TODO_MANUAL_CONVERSION_INDENT: test("Datalogger_03", d1[1], 1000)
      # TODO_MANUAL_CONVERSION_INDENT: test("Datalogger_04", d1[2], 0)
      # TODO_MANUAL_CONVERSION_INDENT: test("Datalogger_05", d1[3], 0)
      # TODO_MANUAL_CONVERSION_INDENT: test("Datalogger_06", d1[4], 0)
      # TODO_MANUAL_CONVERSION_INDENT: memcpy(d0,d1,10)
      # TODO_MANUAL_CONVERSION_INDENT: dlQueue.readUInt16(d1,5)
      # TODO_MANUAL_CONVERSION_INDENT: if d0[1] == d1[1]  and  d0[2] == d1[2]  and  d0[3] == d1[3]  and  d0[4] == d1[4]:
        # TODO_MANUAL_CONVERSION_INDENT: dlQueue.readUInt16(d1,5)
      # TODO_MANUAL_CONVERSION_INDENT: else:
        # TODO_MANUAL_CONVERSION_INDENT: test("Datalogger_07",d1[0]-d0[0],128)
      # TODO_MANUAL_CONVERSION_INDENT: test("Datalogger_08", d1[1], 1000)
      # TODO_MANUAL_CONVERSION_INDENT: test("Datalogger_09", d1[2], 2000)
      # TODO_MANUAL_CONVERSION_INDENT: test("Datalogger_10", d1[3], 0)
      # TODO_MANUAL_CONVERSION_INDENT: test("Datalogger_11", d1[4], 0)
      # TODO_MANUAL_CONVERSION_INDENT: memcpy(d0,d1,10)
      # TODO_MANUAL_CONVERSION_INDENT: dlQueue.readUInt16(d1,5)
      # TODO_MANUAL_CONVERSION_INDENT: if d0[1] == d1[1]  and  d0[2] == d1[2]  and  d0[3] == d1[3]  and  d0[4] == d1[4]:
        # TODO_MANUAL_CONVERSION_INDENT: dlQueue.readUInt16(d1,5)
      # TODO_MANUAL_CONVERSION_INDENT: else:
        # TODO_MANUAL_CONVERSION_INDENT: test("Datalogger_12",d1[0]-d0[0],128)
      # TODO_MANUAL_CONVERSION_INDENT: test("Datalogger_13", d1[1], 1000)
      # TODO_MANUAL_CONVERSION_INDENT: test("Datalogger_14", d1[2], 2000)
      # TODO_MANUAL_CONVERSION_INDENT: test("Datalogger_15", d1[3], 3000)
      # TODO_MANUAL_CONVERSION_INDENT: test("Datalogger_16", d1[4], 0)
      # TODO_MANUAL_CONVERSION_INDENT: memcpy(d0,d1,10)
      # TODO_MANUAL_CONVERSION_INDENT: dlQueue.readUInt16(d1,5)
      # TODO_MANUAL_CONVERSION_INDENT: if d0[1] == d1[1]  and  d0[2] == d1[2]  and  d0[3] == d1[3]  and  d0[4] == d1[4]:
        # TODO_MANUAL_CONVERSION_INDENT: dlQueue.readUInt16(d1,5)
      # TODO_MANUAL_CONVERSION_INDENT: else:
        # TODO_MANUAL_CONVERSION_INDENT: test("Datalogger_17",d1[0]-d0[0],128)
      # TODO_MANUAL_CONVERSION_INDENT: test("Datalogger_18", d1[1], 1000)
      # TODO_MANUAL_CONVERSION_INDENT: test("Datalogger_19", d1[2], 2000)
      # TODO_MANUAL_CONVERSION_INDENT: test("Datalogger_20", d1[3], 3000)
      # TODO_MANUAL_CONVERSION_INDENT: test("Datalogger_21", d1[4], 4000)

    # TODO_MANUAL_CONVERSION_INDENT: swdl.enable(False)
    # TODO_MANUAL_CONVERSION_INDENT: p0.writePublicData(0)
    # TODO_MANUAL_CONVERSION_INDENT: p8.writePublicData(0)
    # TODO_MANUAL_CONVERSION_INDENT: p10.writePublicData(0)
    # TODO_MANUAL_CONVERSION_INDENT: p17.writePublicData(0)
    # TODO_MANUAL_CONVERSION_INDENT: dlQueue.begin(DLQUEUEADDR,DLQUEUELENGTH)
    # TODO_MANUAL_CONVERSION_INDENT: swdl.begin(DLQUEUEADDR,DLQUEUELENGTH,True,  # Queue Frame Index
    # TODO_MANUAL_CONVERSION_INDENT: False,  # QueueOnChange
    # TODO_MANUAL_CONVERSION_INDENT: PERIOD_128mS)

    # TODO_MANUAL_CONVERSION_INDENT: swdl.configurePin(0,True,True)
    # TODO_MANUAL_CONVERSION_INDENT: swdl.configurePin(8,True,True)
    # TODO_MANUAL_CONVERSION_INDENT: swdl.configurePin(10,True,False)
    # TODO_MANUAL_CONVERSION_INDENT: swdl.configurePin(17,False,True)
    # TODO_MANUAL_CONVERSION_INDENT: swdl.enable(True)
    # TODO_MANUAL_CONVERSION_INDENT: delay(130)
    # TODO_MANUAL_CONVERSION_INDENT: p0.writePublicData(1000)
    # TODO_MANUAL_CONVERSION_INDENT: delay(130)
    # TODO_MANUAL_CONVERSION_INDENT: p8.writePublicData(2000)
    # TODO_MANUAL_CONVERSION_INDENT: delay(130)
    # TODO_MANUAL_CONVERSION_INDENT: p10.writePublicData(3000)
    # TODO_MANUAL_CONVERSION_INDENT: delay(130)
    # TODO_MANUAL_CONVERSION_INDENT: p17.writePublicData(4000)
    # TODO_MANUAL_CONVERSION_INDENT: delay(130)
    # TODO_MANUAL_CONVERSION_INDENT: swdl.enable(False)

    # Should be at least 40 data bytes available, no more than 48
      # TODO_MANUAL_CONVERSION_INDENT: i = dlQueue.available()
      # TODO_MANUAL_CONVERSION_INDENT: if i >= 40  and  i <=48:
        # TODO_MANUAL_CONVERSION_INDENT: i = 40
      # TODO_MANUAL_CONVERSION_INDENT: test("DataLogger_22", i, 40)

    # TODO_MANUAL_CONVERSION_INDENT: d0 = [0] * (5)
    # TODO_MANUAL_CONVERSION_INDENT: d1 = [0] * (5)
      # Test that first entry is all 0's

      # TODO_MANUAL_CONVERSION_INDENT: dlQueue.readUInt16(d0,3)
      # TODO_MANUAL_CONVERSION_INDENT: d0[3] = dlQueue.read()
      # TODO_MANUAL_CONVERSION_INDENT: d0[4] = dlQueue.read()
      # TODO_MANUAL_CONVERSION_INDENT: dlQueue.readUInt16(d1,3)
      # TODO_MANUAL_CONVERSION_INDENT: d1[3] = dlQueue.read()
      # TODO_MANUAL_CONVERSION_INDENT: d1[4] = dlQueue.read()

      # TODO_MANUAL_CONVERSION_INDENT: for i in range(1, 5):
        # TODO_MANUAL_CONVERSION_INDENT: st = [0] * (20)
        # TODO_MANUAL_CONVERSION_INDENT: st = ("Datalogger_21_%d") % (i)
        # TODO_MANUAL_CONVERSION_INDENT: test(st, d0[i], 0)
      # TODO_MANUAL_CONVERSION_INDENT: if d0[1] == d1[1]  and  d0[2] == d1[2]  and  d0[3] == d1[3]  and  d0[4] == d1[4]:
        # TODO_MANUAL_CONVERSION_INDENT: dlQueue.readUInt16(d1,3)
        # TODO_MANUAL_CONVERSION_INDENT: d1[3] = dlQueue.read()
        # TODO_MANUAL_CONVERSION_INDENT: d1[4] = dlQueue.read()

      # TODO_MANUAL_CONVERSION_INDENT: else:
        # TODO_MANUAL_CONVERSION_INDENT: test("Datalogger_22",d1[0]-d0[0],128)
      # TODO_MANUAL_CONVERSION_INDENT: test("Datalogger_23", d1[1], 1000)
      # TODO_MANUAL_CONVERSION_INDENT: test("Datalogger_24", d1[2], 0)
      # TODO_MANUAL_CONVERSION_INDENT: test("Datalogger_25", d1[3], 0)
      # TODO_MANUAL_CONVERSION_INDENT: test("Datalogger_26", d1[4], 0)
      # TODO_MANUAL_CONVERSION_INDENT: memcpy(d0,d1,10)
      # TODO_MANUAL_CONVERSION_INDENT: dlQueue.readUInt16(d1,3)
      # TODO_MANUAL_CONVERSION_INDENT: d1[3] = dlQueue.read()
      # TODO_MANUAL_CONVERSION_INDENT: d1[4] = dlQueue.read()
      # TODO_MANUAL_CONVERSION_INDENT: if d0[1] == d1[1]  and  d0[2] == d1[2]  and  d0[3] == d1[3]  and  d0[4] == d1[4]:
        # TODO_MANUAL_CONVERSION_INDENT: dlQueue.readUInt16(d1,3)
        # TODO_MANUAL_CONVERSION_INDENT: d1[3] = dlQueue.read()
        # TODO_MANUAL_CONVERSION_INDENT: d1[4] = dlQueue.read()
      # TODO_MANUAL_CONVERSION_INDENT: else:
        # TODO_MANUAL_CONVERSION_INDENT: test("Datalogger_27",d1[0]-d0[0],128)
      # TODO_MANUAL_CONVERSION_INDENT: test("Datalogger_28", d1[1], 1000)
      # TODO_MANUAL_CONVERSION_INDENT: test("Datalogger_29", d1[2], 2000)
      # TODO_MANUAL_CONVERSION_INDENT: test("Datalogger_30", d1[3], 0)
      # TODO_MANUAL_CONVERSION_INDENT: test("Datalogger_31", d1[4], 0)
      # TODO_MANUAL_CONVERSION_INDENT: memcpy(d0,d1,10)
      # TODO_MANUAL_CONVERSION_INDENT: dlQueue.readUInt16(d1,3)
      # TODO_MANUAL_CONVERSION_INDENT: d1[3] = dlQueue.read()
      # TODO_MANUAL_CONVERSION_INDENT: d1[4] = dlQueue.read()

      # TODO_MANUAL_CONVERSION_INDENT: if d0[1] == d1[1]  and  d0[2] == d1[2]  and  d0[3] == d1[3]  and  d0[4] == d1[4]:
        # TODO_MANUAL_CONVERSION_INDENT: dlQueue.readUInt16(d1,3)
        # TODO_MANUAL_CONVERSION_INDENT: d1[3] = dlQueue.read()
        # TODO_MANUAL_CONVERSION_INDENT: d1[4] = dlQueue.read()

      # TODO_MANUAL_CONVERSION_INDENT: else:
        # TODO_MANUAL_CONVERSION_INDENT: test("Datalogger_32",d1[0]-d0[0],128)
      # TODO_MANUAL_CONVERSION_INDENT: test("Datalogger_33", d1[1], 1000)
      # TODO_MANUAL_CONVERSION_INDENT: test("Datalogger_34", d1[2], 2000)
      # TODO_MANUAL_CONVERSION_INDENT: test("Datalogger_35", d1[3], 3000  0xFF)
      # TODO_MANUAL_CONVERSION_INDENT: test("Datalogger_36", d1[4], 0)
      # TODO_MANUAL_CONVERSION_INDENT: memcpy(d0,d1,10)
      # TODO_MANUAL_CONVERSION_INDENT: dlQueue.readUInt16(d1,3)
      # TODO_MANUAL_CONVERSION_INDENT: d1[3] = dlQueue.read()
      # TODO_MANUAL_CONVERSION_INDENT: d1[4] = dlQueue.read()

      # TODO_MANUAL_CONVERSION_INDENT: if d0[1] == d1[1]  and  d0[2] == d1[2]  and  d0[3] == d1[3]  and  d0[4] == d1[4]:
        # TODO_MANUAL_CONVERSION_INDENT: dlQueue.readUInt16(d1,3)
        # TODO_MANUAL_CONVERSION_INDENT: d1[3] = dlQueue.read()
        # TODO_MANUAL_CONVERSION_INDENT: d1[4] = dlQueue.read()
      # TODO_MANUAL_CONVERSION_INDENT: else:
        # TODO_MANUAL_CONVERSION_INDENT: test("Datalogger_37",d1[0]-d0[0],128)
      # TODO_MANUAL_CONVERSION_INDENT: test("Datalogger_38", d1[1], 1000)
      # TODO_MANUAL_CONVERSION_INDENT: test("Datalogger_39", d1[2], 2000)
      # TODO_MANUAL_CONVERSION_INDENT: test("Datalogger_40", d1[3], 3000  0xFF)
      # TODO_MANUAL_CONVERSION_INDENT: test("Datalogger_41", d1[4], 4000 >>8)

    # TODO_MANUAL_CONVERSION_INDENT: swdl.enable(False)
    # TODO_MANUAL_CONVERSION_INDENT: p0.writePublicData(0)
    # TODO_MANUAL_CONVERSION_INDENT: p8.writePublicData(0)
    # TODO_MANUAL_CONVERSION_INDENT: p10.writePublicData(0)
    # TODO_MANUAL_CONVERSION_INDENT: p17.writePublicData(0)
    # TODO_MANUAL_CONVERSION_INDENT: dlQueue.begin(DLQUEUEADDR,DLQUEUELENGTH)
    # TODO_MANUAL_CONVERSION_INDENT: swdl.begin(DLQUEUEADDR,DLQUEUELENGTH,True,  # Queue Frame Index
    # TODO_MANUAL_CONVERSION_INDENT: True  # QueueOnChange
    # TODO_MANUAL_CONVERSION_INDENT: )

    # TODO_MANUAL_CONVERSION_INDENT: swdl.configurePin(0,True,True)
    # TODO_MANUAL_CONVERSION_INDENT: swdl.configurePin(8,True,True)
    # TODO_MANUAL_CONVERSION_INDENT: swdl.configurePin(10,True,False)
    # TODO_MANUAL_CONVERSION_INDENT: swdl.configurePin(17,False,True)
    # TODO_MANUAL_CONVERSION_INDENT: swdl.enable(True)
    # TODO_MANUAL_CONVERSION_INDENT: delay(100)
    # TODO_MANUAL_CONVERSION_INDENT: p0.writePublicData(1000)
    # TODO_MANUAL_CONVERSION_INDENT: delay(200)
    # TODO_MANUAL_CONVERSION_INDENT: p8.writePublicData(2000)
    # TODO_MANUAL_CONVERSION_INDENT: delay(300)
    # TODO_MANUAL_CONVERSION_INDENT: p10.writePublicData(3000)
    # TODO_MANUAL_CONVERSION_INDENT: delay(400)
    # TODO_MANUAL_CONVERSION_INDENT: p17.writePublicData(4000)
    # TODO_MANUAL_CONVERSION_INDENT: delay(500)
    # TODO_MANUAL_CONVERSION_INDENT: swdl.enable(False)

    # Should be at least 40 data bytes available, no more than 48
      # TODO_MANUAL_CONVERSION_INDENT: i = dlQueue.available()
      # TODO_MANUAL_CONVERSION_INDENT: if i >= 40  and  i <=48:
        # TODO_MANUAL_CONVERSION_INDENT: i = 40
      # TODO_MANUAL_CONVERSION_INDENT: test("DataLogger_42", i, 40)

    # TODO_MANUAL_CONVERSION_INDENT: d0 = [0] * (5)
    # TODO_MANUAL_CONVERSION_INDENT: d1 = [0] * (5)
      # Test that first entry is all 0's

      # TODO_MANUAL_CONVERSION_INDENT: dlQueue.readUInt16(d0,3)
      # TODO_MANUAL_CONVERSION_INDENT: d0[3] = dlQueue.read()
      # TODO_MANUAL_CONVERSION_INDENT: d0[4] = dlQueue.read()
      # TODO_MANUAL_CONVERSION_INDENT: dlQueue.readUInt16(d1,3)
      # TODO_MANUAL_CONVERSION_INDENT: d1[3] = dlQueue.read()
      # TODO_MANUAL_CONVERSION_INDENT: d1[4] = dlQueue.read()

      # TODO_MANUAL_CONVERSION_INDENT: for i in range(1, 5):
        # TODO_MANUAL_CONVERSION_INDENT: st = [0] * (20)
        # TODO_MANUAL_CONVERSION_INDENT: st = ("Datalogger_42_%d") % (i)
        # TODO_MANUAL_CONVERSION_INDENT: test(st, d0[i], 0)
      # TODO_MANUAL_CONVERSION_INDENT: if d0[1] == d1[1]  and  d0[2] == d1[2]  and  d0[3] == d1[3]  and  d0[4] == d1[4]:
        # TODO_MANUAL_CONVERSION_INDENT: dlQueue.readUInt16(d1,3)
        # TODO_MANUAL_CONVERSION_INDENT: d1[3] = dlQueue.read()
        # TODO_MANUAL_CONVERSION_INDENT: d1[4] = dlQueue.read()

      # TODO_MANUAL_CONVERSION_INDENT: else:
        # TODO_MANUAL_CONVERSION_INDENT: if d1[0] < d0[0]:
          # TODO_MANUAL_CONVERSION_INDENT: d1[0] += 65536
        # TODO_MANUAL_CONVERSION_INDENT: test("Datalogger_43",d1[0]-d0[0],100,10)
      # TODO_MANUAL_CONVERSION_INDENT: test("Datalogger_44", d1[1], 1000)
      # TODO_MANUAL_CONVERSION_INDENT: test("Datalogger_45", d1[2], 0)
      # TODO_MANUAL_CONVERSION_INDENT: test("Datalogger_46", d1[3], 0)
      # TODO_MANUAL_CONVERSION_INDENT: test("Datalogger_47", d1[4], 0)
      # TODO_MANUAL_CONVERSION_INDENT: memcpy(d0,d1,10)
      # TODO_MANUAL_CONVERSION_INDENT: dlQueue.readUInt16(d1,3)
      # TODO_MANUAL_CONVERSION_INDENT: d1[3] = dlQueue.read()
      # TODO_MANUAL_CONVERSION_INDENT: d1[4] = dlQueue.read()
      # TODO_MANUAL_CONVERSION_INDENT: if d0[1] == d1[1]  and  d0[2] == d1[2]  and  d0[3] == d1[3]  and  d0[4] == d1[4]:
        # TODO_MANUAL_CONVERSION_INDENT: dlQueue.readUInt16(d1,3)
        # TODO_MANUAL_CONVERSION_INDENT: d1[3] = dlQueue.read()
        # TODO_MANUAL_CONVERSION_INDENT: d1[4] = dlQueue.read()
      # TODO_MANUAL_CONVERSION_INDENT: else:
        # TODO_MANUAL_CONVERSION_INDENT: if d1[0] < d0[0]:
          # TODO_MANUAL_CONVERSION_INDENT: d1[0] += 65536
        # TODO_MANUAL_CONVERSION_INDENT: test("Datalogger_48",d1[0]-d0[0],200,10)
      # TODO_MANUAL_CONVERSION_INDENT: test("Datalogger_49", d1[1], 1000)
      # TODO_MANUAL_CONVERSION_INDENT: test("Datalogger_50", d1[2], 2000)
      # TODO_MANUAL_CONVERSION_INDENT: test("Datalogger_51", d1[3], 0)
      # TODO_MANUAL_CONVERSION_INDENT: test("Datalogger_52", d1[4], 0)
      # TODO_MANUAL_CONVERSION_INDENT: memcpy(d0,d1,10)
      # TODO_MANUAL_CONVERSION_INDENT: dlQueue.readUInt16(d1,3)
      # TODO_MANUAL_CONVERSION_INDENT: d1[3] = dlQueue.read()
      # TODO_MANUAL_CONVERSION_INDENT: d1[4] = dlQueue.read()

      # TODO_MANUAL_CONVERSION_INDENT: if d0[1] == d1[1]  and  d0[2] == d1[2]  and  d0[3] == d1[3]  and  d0[4] == d1[4]:
        # TODO_MANUAL_CONVERSION_INDENT: dlQueue.readUInt16(d1,3)
        # TODO_MANUAL_CONVERSION_INDENT: d1[3] = dlQueue.read()
        # TODO_MANUAL_CONVERSION_INDENT: d1[4] = dlQueue.read()

      # TODO_MANUAL_CONVERSION_INDENT: else:
        # TODO_MANUAL_CONVERSION_INDENT: if d1[0] < d0[0]:
          # TODO_MANUAL_CONVERSION_INDENT: d1[0] += 65536

        # TODO_MANUAL_CONVERSION_INDENT: test("Datalogger_53",d1[0]-d0[0],300,10)
      # TODO_MANUAL_CONVERSION_INDENT: test("Datalogger_54", d1[1], 1000)
      # TODO_MANUAL_CONVERSION_INDENT: test("Datalogger_55", d1[2], 2000)
      # TODO_MANUAL_CONVERSION_INDENT: test("Datalogger_56", d1[3], 3000  0xFF)
      # TODO_MANUAL_CONVERSION_INDENT: test("Datalogger_57", d1[4], 0)
      # TODO_MANUAL_CONVERSION_INDENT: memcpy(d0,d1,10)
      # TODO_MANUAL_CONVERSION_INDENT: dlQueue.readUInt16(d1,3)
      # TODO_MANUAL_CONVERSION_INDENT: d1[3] = dlQueue.read()
      # TODO_MANUAL_CONVERSION_INDENT: d1[4] = dlQueue.read()

      # TODO_MANUAL_CONVERSION_INDENT: if d0[1] == d1[1]  and  d0[2] == d1[2]  and  d0[3] == d1[3]  and  d0[4] == d1[4]:
        # TODO_MANUAL_CONVERSION_INDENT: dlQueue.readUInt16(d1,3)
        # TODO_MANUAL_CONVERSION_INDENT: d1[3] = dlQueue.read()
        # TODO_MANUAL_CONVERSION_INDENT: d1[4] = dlQueue.read()
      # TODO_MANUAL_CONVERSION_INDENT: else:
        # TODO_MANUAL_CONVERSION_INDENT: if d1[0] < d0[0]:
          # TODO_MANUAL_CONVERSION_INDENT: d1[0] += 65536

        # TODO_MANUAL_CONVERSION_INDENT: test("Datalogger_58",d1[0]-d0[0],400,10)
      # TODO_MANUAL_CONVERSION_INDENT: test("Datalogger_59", d1[1], 1000)
      # TODO_MANUAL_CONVERSION_INDENT: test("Datalogger_60", d1[2], 2000)
      # TODO_MANUAL_CONVERSION_INDENT: test("Datalogger_61", d1[3], 3000  0xFF)
      # TODO_MANUAL_CONVERSION_INDENT: test("Datalogger_62", d1[4], 4000 >>8)
