# Converted from Testing/SW4B_SW18AB_SW08B_AutomatedTest/ProtectedOutput.ino
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
import SerialWombatProtectedOutput

# TODO_MANUAL_CONVERSION: PO_WRITE_VALUE = (_VALUE) {SW18AB_6B.writePublicData(0,_VALUE);}
# TODO_MANUAL_CONVERSION: PO_READ_VALUE = ) SW18AB_6B.readPublicData(0
swpo = SerialWombatProtectedOutput.SerialWombatProtectedOutput(SW18AB_6B)
def protectedOutputTest18AB():
  pin = 19
  resetAll()

    # Make pin 0 on driving Serial Wombat chip a servo.  We can set the public data here.
    # TODO_MANUAL_CONVERSION_INDENT: tx = [ 200, 0, PIN_MODE_SERVO, 0, 0x55, 0x55, 0x55, 0x55]
    # TODO_MANUAL_CONVERSION_INDENT: SW18AB_6B.sendPacket(tx)
  swpo.begin(pin, 0)
    # TODO_MANUAL_CONVERSION_INDENT: PO_WRITE_VALUE(0)
    # TODO_MANUAL_CONVERSION_INDENT: delay(2)

    # TODO_MANUAL_CONVERSION_INDENT: swpo.configure(PO_FAULT_IF_NOT_EQUAL, 0, 100, SW_LOW, SW_HIGH)
    # TODO_MANUAL_CONVERSION_INDENT: delay(2)
    # TODO_MANUAL_CONVERSION_INDENT: if not SWChipAndPinTo4BChip(SW18AB_6B,pin).digitalRead(SW18ABPinTo4BPin(pin)):
      # TODO_MANUAL_CONVERSION_INDENT: pass(0)
    # TODO_MANUAL_CONVERSION_INDENT: else:
      # TODO_MANUAL_CONVERSION_INDENT: fail(0)
      # #ifdef PRINT_FAILURES
      # TODO_MANUAL_CONVERSION_INDENT: print(("Pin %d: Expected pin read low, got high at test 0\n") % (pin), end="")
      # #endif
    # TODO_MANUAL_CONVERSION_INDENT: PO_WRITE_VALUE(1)
    # TODO_MANUAL_CONVERSION_INDENT: delay(2)
    # TODO_MANUAL_CONVERSION_INDENT: if not SWChipAndPinTo4BChip(SW18AB_6B,pin).digitalRead(SW18ABPinTo4BPin(pin)):
      # Still low until debounce
      # TODO_MANUAL_CONVERSION_INDENT: pass(1)
    # TODO_MANUAL_CONVERSION_INDENT: else:
      # TODO_MANUAL_CONVERSION_INDENT: fail(1)
      # #ifdef PRINT_FAILURES
      # TODO_MANUAL_CONVERSION_INDENT: print(("Pin %d: Expected pin read low, got high at test 1\n") % (pin), end="")
      # #endif
    # TODO_MANUAL_CONVERSION_INDENT: delay(110)

    # TODO_MANUAL_CONVERSION_INDENT: PO_READ_VALUE()
    # TODO_MANUAL_CONVERSION_INDENT: if SWChipAndPinTo4BChip(SW18AB_6B,pin).digitalRead(SW18ABPinTo4BPin(pin)):

      # TODO_MANUAL_CONVERSION_INDENT: pass(2)
    # TODO_MANUAL_CONVERSION_INDENT: else:
      # TODO_MANUAL_CONVERSION_INDENT: fail(2)
      # #ifdef PRINT_FAILURES
      # TODO_MANUAL_CONVERSION_INDENT: print(("Pin %d: Expected pin read High, got low at test 2\n") % (pin), end="")
      # #endif

    # TODO_MANUAL_CONVERSION_INDENT: PO_WRITE_VALUE(0)
    # TODO_MANUAL_CONVERSION_INDENT: delay(2)

    # TODO_MANUAL_CONVERSION_INDENT: swpo.configure(PO_FAULT_IF_NOT_EQUAL, 0, 100, SW_HIGH, SW_LOW)
    # TODO_MANUAL_CONVERSION_INDENT: delay(2)
    # TODO_MANUAL_CONVERSION_INDENT: if SWChipAndPinTo4BChip(SW18AB_6B,pin).digitalRead(SW18ABPinTo4BPin(pin)):
      # TODO_MANUAL_CONVERSION_INDENT: pass(3)
    # TODO_MANUAL_CONVERSION_INDENT: else:
      # TODO_MANUAL_CONVERSION_INDENT: fail(3)
      # #ifdef PRINT_FAILURES
      # TODO_MANUAL_CONVERSION_INDENT: print(("Pin %d: Expected pin read high, got low at test 3\n") % (pin), end="")
      # #endif
    # TODO_MANUAL_CONVERSION_INDENT: PO_WRITE_VALUE(1)
    # TODO_MANUAL_CONVERSION_INDENT: delay(2)
    # TODO_MANUAL_CONVERSION_INDENT: if SWChipAndPinTo4BChip(SW18AB_6B,pin).digitalRead(SW18ABPinTo4BPin(pin)):
      # Still high until debounce
      # TODO_MANUAL_CONVERSION_INDENT: pass(4)
    # TODO_MANUAL_CONVERSION_INDENT: else:
      # TODO_MANUAL_CONVERSION_INDENT: fail(4)
      # #ifdef PRINT_FAILURES
      # TODO_MANUAL_CONVERSION_INDENT: print(("Pin %d: Expected pin read high, got low at test 4\n") % (pin), end="")
      # #endif
    # TODO_MANUAL_CONVERSION_INDENT: delay(110)

    # TODO_MANUAL_CONVERSION_INDENT: PO_READ_VALUE()
    # TODO_MANUAL_CONVERSION_INDENT: if not SWChipAndPinTo4BChip(SW18AB_6B,pin).digitalRead(SW18ABPinTo4BPin(pin)):

      # TODO_MANUAL_CONVERSION_INDENT: pass(5)
    # TODO_MANUAL_CONVERSION_INDENT: else:
      # TODO_MANUAL_CONVERSION_INDENT: fail(5)
      # #ifdef PRINT_FAILURES
      # TODO_MANUAL_CONVERSION_INDENT: print(("Pin %d: Expected pin read High, got low at test 5\n") % (pin), end="")
      # #endif

    # TODO_MANUAL_CONVERSION_INDENT: PO_WRITE_VALUE(0x70FF)
    # TODO_MANUAL_CONVERSION_INDENT: delay(2)

    # TODO_MANUAL_CONVERSION_INDENT: swpo.configure(PO_FAULT_IF_FEEDBACK_GREATER_THAN_EXPECTED, 0x8000, 100, SW_HIGH, SW_LOW)
    # TODO_MANUAL_CONVERSION_INDENT: delay(2)
    # TODO_MANUAL_CONVERSION_INDENT: if SWChipAndPinTo4BChip(SW18AB_6B,pin).digitalRead(SW18ABPinTo4BPin(pin)):
      # TODO_MANUAL_CONVERSION_INDENT: pass(6)
    # TODO_MANUAL_CONVERSION_INDENT: else:
      # TODO_MANUAL_CONVERSION_INDENT: fail(6)
      # #ifdef PRINT_FAILURES
      # TODO_MANUAL_CONVERSION_INDENT: print(("Pin %d: Expected pin read high, got low at test 6\n") % (pin), end="")
      # #endif
    # TODO_MANUAL_CONVERSION_INDENT: PO_WRITE_VALUE(0x9000)
    # TODO_MANUAL_CONVERSION_INDENT: delay(2)
    # TODO_MANUAL_CONVERSION_INDENT: if SWChipAndPinTo4BChip(SW18AB_6B,pin).digitalRead(SW18ABPinTo4BPin(pin)):
      # Still high until debounce
      # TODO_MANUAL_CONVERSION_INDENT: pass(7)
    # TODO_MANUAL_CONVERSION_INDENT: else:
      # TODO_MANUAL_CONVERSION_INDENT: fail(7)
      # #ifdef PRINT_FAILURES
      # TODO_MANUAL_CONVERSION_INDENT: print(("Pin %d: Expected pin read high, got low at test 7\n") % (pin), end="")
      # #endif
    # TODO_MANUAL_CONVERSION_INDENT: delay(110)

    # TODO_MANUAL_CONVERSION_INDENT: PO_READ_VALUE()
    # TODO_MANUAL_CONVERSION_INDENT: if not SWChipAndPinTo4BChip(SW18AB_6B,pin).digitalRead(SW18ABPinTo4BPin(pin)):

      # TODO_MANUAL_CONVERSION_INDENT: pass(8)
    # TODO_MANUAL_CONVERSION_INDENT: else:
      # TODO_MANUAL_CONVERSION_INDENT: fail(8)
      # #ifdef PRINT_FAILURES
      # TODO_MANUAL_CONVERSION_INDENT: print(("Pin %d: Expected pin read High, got low at test 8\n") % (pin), end="")
      # #endif

    # TODO_MANUAL_CONVERSION_INDENT: PO_WRITE_VALUE(0x9000)
    # TODO_MANUAL_CONVERSION_INDENT: delay(2)

    # TODO_MANUAL_CONVERSION_INDENT: swpo.configure(PO_FAULT_IF_FEEDBACK_LESS_THAN_EXPECTED, 0x8000, 100, SW_HIGH, SW_LOW)
    # TODO_MANUAL_CONVERSION_INDENT: delay(2)
    # TODO_MANUAL_CONVERSION_INDENT: if SWChipAndPinTo4BChip(SW18AB_6B,pin).digitalRead(SW18ABPinTo4BPin(pin)):
      # TODO_MANUAL_CONVERSION_INDENT: pass(9)
    # TODO_MANUAL_CONVERSION_INDENT: else:
      # TODO_MANUAL_CONVERSION_INDENT: fail(9)
      # #ifdef PRINT_FAILURES
      # TODO_MANUAL_CONVERSION_INDENT: print(("Pin %d: Expected pin read high, got low at test 9\n") % (pin), end="")
      # #endif
    # TODO_MANUAL_CONVERSION_INDENT: PO_WRITE_VALUE(0x7000)
    # TODO_MANUAL_CONVERSION_INDENT: delay(2)
    # TODO_MANUAL_CONVERSION_INDENT: if SWChipAndPinTo4BChip(SW18AB_6B,pin).digitalRead(SW18ABPinTo4BPin(pin)):
      # Still high until debounce
      # TODO_MANUAL_CONVERSION_INDENT: pass(10)
    # TODO_MANUAL_CONVERSION_INDENT: else:
      # TODO_MANUAL_CONVERSION_INDENT: fail(10)
      # #ifdef PRINT_FAILURES
      # TODO_MANUAL_CONVERSION_INDENT: print(("Pin %d: Expected pin read high, got low at test 10\n") % (pin), end="")
      # #endif
    # TODO_MANUAL_CONVERSION_INDENT: delay(110)

    # TODO_MANUAL_CONVERSION_INDENT: PO_READ_VALUE()
    # TODO_MANUAL_CONVERSION_INDENT: if not SWChipAndPinTo4BChip(SW18AB_6B,pin).digitalRead(SW18ABPinTo4BPin(pin)):

      # TODO_MANUAL_CONVERSION_INDENT: pass(11)
    # TODO_MANUAL_CONVERSION_INDENT: else:
      # TODO_MANUAL_CONVERSION_INDENT: fail(11)
      # #ifdef PRINT_FAILURES
      # TODO_MANUAL_CONVERSION_INDENT: print(("Pin %d: Expected pin read High, got low at test 11\n") % (pin), end="")
      # #endif
