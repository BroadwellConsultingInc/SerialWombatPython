# Converted from Testing/SW4B_SW18AB_SW08B_AutomatedTest/PulseOnChange.ino
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
import SerialWombatPin
import SerialWombatPulseOnChange


POC_IN_PIN2 = 7
POC_IN_PIN1 = 6
POC_OUT_PIN = 0

# TODO_MANUAL_CONVERSION: *pocInput1 = SerialWombatPin.SerialWombatPin()
# TODO_MANUAL_CONVERSION: *pocInput2 = SerialWombatPin.SerialWombatPin()
# TODO_MANUAL_CONVERSION: *pocPointer = SerialWombatPulseOnChange.SerialWombatPulseOnChange()

def pulseOnChangeTest(sw):
  resetAll()

  pocInput1_18 = SerialWombatPin.SerialWombatPin(sw,POC_IN_PIN1)
  pocInput2_18 = SerialWombatPin.SerialWombatPin(sw,POC_IN_PIN2)
  pocPin18 = SerialWombatPulseOnChange.SerialWombatPulseOnChange(sw)
  pocPointer = pocPin18
  pocInput1 = pocInput1_18
  pocInput2 = pocInput2_18
  pocPulseOnChange(sw)
  pocPulseOnIncrease(sw)
  pocPulseOnDecrease(sw)
  pocPulseOnEqualValue(sw)
  pocPulseOnLessThanValue(sw)
  pocPulseOnGreaterThanValue(sw)
  pocPulseOnNotEqualValue(sw)
  pocPulseOnPinsEqual(sw)
  pocPulseOnPinsNotEqual(sw)
  pocInput1.readPublicData()
  pocInput2.readPublicData()
  pocPointer.readPublicData()


def pocPulseOnChange(sw):
  resetAll()
  #pocInput1->begin(POC_IN_PIN1);
  pocInput1.pinMode(1)
  pocInput1.writePublicData(0x8000)
  pocPointer.begin(POC_OUT_PIN)
  initializePulseReaduS(sw,POC_OUT_PIN)
  delay(1000)
  test("POC_POC_01", pulseCounts(sw,POC_OUT_PIN), 0);  # No Pulses So far
  pocPointer.setEntryOnChange(0,POC_IN_PIN1)
  pocInput1.writePublicData(0x8001)
  delay(1000)
  test("POC_POC_02A", pulseCounts(sw,POC_OUT_PIN), 1);  # 1 change
  test("POC_POC_02B", pulseRead(sw,POC_OUT_PIN), 50000,10000);  # Should be a 50 mS pulse

def pocPulseOnIncrease(sw):

  pocPointer.begin(POC_OUT_PIN)
  # pocInput1->begin(POC_IN_PIN1);
  pocInput1.writePublicData(0x8000)
  pocInput1.pinMode(1)
  initializePulseReaduS(sw,POC_OUT_PIN)
  delay(1000)
  test("POC_INC_01", pulseCounts(sw,POC_OUT_PIN), 0);  # No Pulses So far
  pocPointer.setEntryOnIncrease(1,POC_IN_PIN1)
  pocInput1.writePublicData(0x7FFF)
  delay(1000)
  test("POC_INC_02", pulseCounts(sw,POC_OUT_PIN), 0);  # No Pulses So far
  pocInput1.writePublicData(0x8000)
  delay(1000)
  test("POC_INC_03", pulseCounts(sw,POC_OUT_PIN), 1);  # 1 change
  test("POC_INC_04", pulseRead(sw,POC_OUT_PIN), 50000,10000);  # Should be a 50 mS pulse
  pocInput1.writePublicData(0xC000)
  delay(1000)
  test("POC_INC_05", pulseCounts(sw,POC_OUT_PIN), 2);  # 2 changes
  test("POC_INC_06", pulseRead(sw,POC_OUT_PIN), 50000,10000);  # Should be a 50 mS pulse
def pocPulseOnDecrease(sw):

  pocPointer.begin(POC_OUT_PIN,SW_HIGH,SW_LOW,20)
  #pocInput1->begin(POC_IN_PIN1);
  pocInput1.pinMode(1)
  pocInput1.writePublicData(0x8000)
  initializePulseReaduS(sw,POC_OUT_PIN)
  delay(1000)
  test("POC_DEC_01", pulseCounts(sw,POC_OUT_PIN), 0);  # No Pulses So far
  pocPointer.setEntryOnDecrease(1,POC_IN_PIN1)
  pocInput1.writePublicData(0xC000)
  delay(1000)
  test("POC_DEC_02", pulseCounts(sw,POC_OUT_PIN), 0);  # No Pulses So far
  pocInput1.writePublicData(0x8000)
  delay(1000)
  test("POC_DEC_03", pulseCounts(sw,POC_OUT_PIN), 1);  # 1 change
  test("POC_DEC_04", pulseRead(sw,POC_OUT_PIN), 20000,5000);  # Should be a 20 mS pulse
  pocInput1.writePublicData(0x0000)
  delay(1000)
  test("POC_DEC_05", pulseCounts(sw,POC_OUT_PIN), 2);  # 2 changes
  test("POC_DEC_06", pulseRead(sw,POC_OUT_PIN), 20000,5000);  # Should be a 50 mS pulse

def pocPulseOnEqualValue(sw):

  pocPointer.begin(POC_OUT_PIN)
  #pocInput1->begin(POC_IN_PIN1);
  pocInput1.pinMode(1)
  pocInput1.writePublicData(0x8000)
  initializePulseReaduS(sw,POC_OUT_PIN)
  delay(1000)
  test("POC_EQV_01", pulseCounts(sw,POC_OUT_PIN), 0);  # No Pulses So far
  pocPointer.setEntryOnEqualValue(1,POC_IN_PIN1,0x1234)
  pocInput1.writePublicData(0xC000)
  delay(1000)
  test("POC_EQV_02", pulseCounts(sw,POC_OUT_PIN), 0);  # No Pulses So far
  pocInput1.writePublicData(0x1234)
  delay(1000)
  test("POC_EQV_03", pulseCounts(sw,POC_OUT_PIN), 10,3);  # 1 change
  test("POC_EQV_04", pulseRead(sw,POC_OUT_PIN), 50000,5000);  # Should be a 50 mS pulse
  pocInput1.writePublicData(0x0000)
  delay(1000)
  test("POC_EQV_05", pulseCounts(sw,POC_OUT_PIN), 10,3);  # 1 change
  pocInput1.writePublicData(0x1234)
  delay(1000)
  test("POC_EQV_06", pulseCounts(sw,POC_OUT_PIN), 20,6);  # 2 changes
  test("POC_EQV_07", pulseRead(sw,POC_OUT_PIN), 50000,5000);  # Should be a 50 mS pulse

def pocPulseOnLessThanValue(sw):

  pocPointer.begin(POC_OUT_PIN)
  #pocInput1->begin(POC_IN_PIN1);
  pocInput1.pinMode(1)
  pocInput1.writePublicData(0x8000)
  initializePulseReaduS(sw,POC_OUT_PIN)
  delay(1000)
  test("POC_LTV_01", pulseCounts(sw,POC_OUT_PIN), 0);  # No Pulses So far
  pocPointer.setEntryOnLessThanValue(1,POC_IN_PIN1,0x1234)
  pocInput1.writePublicData(0xC000)
  delay(1000)
  test("POC_LTV_02", pulseCounts(sw,POC_OUT_PIN), 0);  # No Pulses So far
  pocInput1.writePublicData(0x1233)
  delay(1000)
  test("POC_LTV_03", pulseCounts(sw,POC_OUT_PIN), 10,3);  # 1 change
  test("POC_LTV_04", pulseRead(sw,POC_OUT_PIN), 50000,5000);  # Should be a 50 mS pulse
  pocInput1.writePublicData(0x6000)
  delay(1000)
  test("POC_LTV_05", pulseCounts(sw,POC_OUT_PIN), 10,3);  # 1 change
  pocInput1.writePublicData(0x1234)
  delay(1000)
  pocInput1.writePublicData(0x6000)
  delay(1000)
  test("POC_LTV_06", pulseCounts(sw,POC_OUT_PIN), 10,3);  # 1 change
  pocInput1.writePublicData(0x1000)
  delay(1000)
  test("POC_LTV_07", pulseCounts(sw,POC_OUT_PIN), 20,6);  # 2 changes
  test("POC_LTV_08", pulseRead(sw,POC_OUT_PIN), 50000,5000);  # Should be a 50 mS pulse


def pocPulseOnGreaterThanValue(sw):

  pocPointer.begin(POC_OUT_PIN)
  #pocInput1->begin(POC_IN_PIN1);
  pocInput1.pinMode(1)
  pocInput1.writePublicData(0x0000)
  initializePulseReaduS(sw,POC_OUT_PIN)
  delay(1000)
  test("POC_GTV_01", pulseCounts(sw,POC_OUT_PIN), 0);  # No Pulses So far
  pocPointer.setEntryOnGreaterThanValue(1,POC_IN_PIN1,0x1234)
  pocInput1.writePublicData(0x0000)
  delay(1000)
  test("POC_GTV_02", pulseCounts(sw,POC_OUT_PIN), 0);  # No Pulses So far
  pocInput1.writePublicData(0x1235)
  delay(1000)
  test("POC_GTV_03", pulseCounts(sw,POC_OUT_PIN), 10,3);  # 1 change
  test("POC_GTV_04", pulseRead(sw,POC_OUT_PIN), 50000,5000);  # Should be a 50 mS pulse
  pocInput1.writePublicData(0x0500)
  delay(1000)
  test("POC_GTV_05", pulseCounts(sw,POC_OUT_PIN), 10,3);  # 1 change
  pocInput1.writePublicData(0x0500)
  delay(1000)
  test("POC_GTV_06", pulseCounts(sw,POC_OUT_PIN), 10,3);  # 1 change
  pocInput1.writePublicData(0x6000)
  delay(1000)
  test("POC_GTV_07", pulseCounts(sw,POC_OUT_PIN), 20,6);  # 2 changes
  test("POC_GTV_08", pulseRead(sw,POC_OUT_PIN), 50000,5000);  # Should be a 50 mS pulse



def pocPulseOnNotEqualValue(sw):

  pocPointer.begin(POC_OUT_PIN)
  pocInput1.pinMode(1)
  #pocInput1->begin(POC_IN_PIN1);
  pocInput1.writePublicData(0x1234)
  initializePulseReaduS(sw,POC_OUT_PIN)
  delay(1000)
  test("POC_NEV_01", pulseCounts(sw,POC_OUT_PIN), 0);  # No Pulses So far
  pocPointer.setEntryOnNotEqualValue(1,POC_IN_PIN1,0x1234)

  pocInput1.writePublicData(0x1233)
  delay(1000)
  test("POC_NEV_03", pulseCounts(sw,POC_OUT_PIN), 10,3);  # 1 change
  test("POC_NEV_04", pulseRead(sw,POC_OUT_PIN), 50000,5000);  # Should be a 50 mS pulse
  pocInput1.writePublicData(0x1234)
  delay(1000)
  test("POC_NEV_05", pulseCounts(sw,POC_OUT_PIN), 10,3);  # 1 change
  pocInput1.writePublicData(0x1235)
  delay(1000)
  test("POC_NEV_06", pulseCounts(sw,POC_OUT_PIN), 20,6);  # 2 changes
  test("POC_NEV_07", pulseRead(sw,POC_OUT_PIN), 50000,5000);  # Should be a 50 mS pulse


def pocPulseOnPinsEqual(sw):

  pocPointer.begin(POC_OUT_PIN)
  #pocInput1->begin(POC_IN_PIN1);
  pocInput1.pinMode(1)
  #pocInput2->begin(POC_IN_PIN2);
  pocInput2.pinMode(1)

  pocInput1.writePublicData(0x1234)
  pocInput2.writePublicData(0x1235)
  initializePulseReaduS(sw,POC_OUT_PIN)
  delay(1000)
  test("POC_EQP_01", pulseCounts(sw,POC_OUT_PIN), 0);  # No Pulses So far
  pocPointer.setEntryOnPinsEqual(1,POC_IN_PIN1,POC_IN_PIN2)

  pocInput1.writePublicData(0x1235)
  delay(1000)
  test("POC_EQP_03", pulseCounts(sw,POC_OUT_PIN), 10,3);  # 1 change
  test("POC_EQP_04", pulseRead(sw,POC_OUT_PIN), 50000,5000);  # Should be a 50 mS pulse
  pocInput1.writePublicData(0x1234)
  delay(1000)
  test("POC_EQP_05", pulseCounts(sw,POC_OUT_PIN), 10,3);  # 1 change
  pocInput2.writePublicData(0x1234)
  delay(1000)
  test("POC_EQP_06", pulseCounts(sw,POC_OUT_PIN), 20,6);  # 2 changes
  test("POC_EQP_07", pulseRead(sw,POC_OUT_PIN), 50000,5000);  # Should be a 50 mS pulse


def pocPulseOnPinsNotEqual(sw):

  pocPointer.begin(POC_OUT_PIN)
  pocInput1.pinMode(1)
  pocInput2.pinMode(1)
  #pocInput1->begin(POC_IN_PIN1);
  #pocInput2->begin(POC_IN_PIN2);

  pocInput1.writePublicData(0x1234)
  pocInput2.writePublicData(0x1234)
  initializePulseReaduS(sw,POC_OUT_PIN)
  delay(1000)
  test("POC_EQP_01", pulseCounts(sw,POC_OUT_PIN), 0);  # No Pulses So far
  pocPointer.setEntryOnPinsNotEqual(1,POC_IN_PIN1,POC_IN_PIN2)

  pocInput1.writePublicData(0x1235)
  delay(1000)
  test("POC_EQP_03", pulseCounts(sw,POC_OUT_PIN), 10,3);  # 1 change
  test("POC_EQP_04", pulseRead(sw,POC_OUT_PIN), 50000,5000);  # Should be a 50 mS pulse
  pocInput1.writePublicData(0x1234)
  delay(1000)
  test("POC_EQP_05", pulseCounts(sw,POC_OUT_PIN), 10,3);  # 1 change
  pocInput2.writePublicData(0x1200)
  delay(1000)
  test("POC_EQP_06", pulseCounts(sw,POC_OUT_PIN), 20,6);  # 2 changes
  test("POC_EQP_07", pulseRead(sw,POC_OUT_PIN), 50000,5000);  # Should be a 50 mS pulse
