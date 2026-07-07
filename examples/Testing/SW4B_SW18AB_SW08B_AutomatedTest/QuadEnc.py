# Converted from Testing/SW4B_SW18AB_SW08B_AutomatedTest/QuadEnc.ino
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
import SerialWombatPWM
import SerialWombatPin
import SerialWombatQuadEnc
import SerialWombatSimulatedQuadEnc

USEQEA = True

# #ifdef USEQEA
sw18qeA = SerialWombatQuadEnc.SerialWombatQuadEnc_18AB(SW18AB_6B)
sw18qeSimA = SerialWombatSimulatedQuadEnc.SerialWombatSimulatedQuadEnc(SW4B_6D, SW4B_6D, 1, 2, True, False)
# #endif
sw18qeSimB = SerialWombatSimulatedQuadEnc.SerialWombatSimulatedQuadEnc(SW4B_6E, SW4B_6E, 1, 2, True, False)
sw18qeB = SerialWombatQuadEnc.SerialWombatQuadEnc_18AB(SW18AB_6B)


# #ifdef USEQEA
sw8qeA = SerialWombatQuadEnc.SerialWombatQuadEnc_18AB(SW8B_68)
sw8qeSimA = SerialWombatSimulatedQuadEnc.SerialWombatSimulatedQuadEnc(SW4B_6F, SW4B_6E, 1, 3, True, False)
# #endif
sw8qeSimB = SerialWombatSimulatedQuadEnc.SerialWombatSimulatedQuadEnc(SW4B_6E, SW4B_6E, 1, 2, True, False)
sw8qeB = SerialWombatQuadEnc.SerialWombatQuadEnc_18AB(SW8B_68)




def QuadEncTest(sw):
  testStr = [0] * (40)
  resetAll()

  # TODO_MANUAL_CONVERSION: SerialWombatQuadEnc_18AB* qeA = None
  # TODO_MANUAL_CONVERSION: SerialWombatQuadEnc_18AB* qeB = None
  # TODO_MANUAL_CONVERSION: SerialWombatSimulatedQuadEnc* qeSimA = None
  # TODO_MANUAL_CONVERSION: SerialWombatSimulatedQuadEnc* qeSimB = None

  if sw == SW18AB_6B:
    # #ifdef USEQEA
    qeA = sw18qeA
    qeSimA = sw18qeSimA
    # #endif
    qeB = sw18qeB

    qeSimB = sw18qeSimB
  elif sw == SW8B_68:
    # #ifdef USEQEA
    qeA = sw8qeA
    qeSimA = sw8qeSimA
    # #endif
    qeB = sw8qeB

    qeSimB = sw8qeSimB

  if sw == SW18AB_6B:
      #Test different port error
      print("EXPECTED ERROR HERE - PART OF TEST: ", end="")
      priorErrorCount = sw.errorCount
      qeA.begin(7, 8,10,True,QE_ONBOTH_INT)
      test("Quad Enc Port Mismatch: ",sw.errorCount, priorErrorCount + 1)

    # TODO_MANUAL_CONVERSION_INDENT: for pollType in range(2, 7):

      if sw == SW18AB_6B:
        # #ifdef USEQEA
        qeSimA.initialize()
        # TODO_MANUAL_CONVERSION: qeA.begin(5, 6, 10, True, (QE_READ_MODE_t)pollType)
        # #endif

        qeSimB.initialize()
        # TODO_MANUAL_CONVERSION: qeB.begin(18, 19, 10, True, (QE_READ_MODE_t)pollType)
      elif sw == SW8B_68:
        # #ifdef USEQEA
        qeSimA.initialize()
        # TODO_MANUAL_CONVERSION: qeA.begin(3, 2, 10, True, (QE_READ_MODE_t)pollType)
        # #endif

        qeSimB.initialize()
        # TODO_MANUAL_CONVERSION: qeB.begin(6, 7, 10, True, (QE_READ_MODE_t)pollType)

      else:
        test("Quad Enc invalid Serial Wombat Chip", 0)

      target = 30000

      # #ifdef USEQEA
      qeA.writePublicData(target)
      qeSimA.targetPosition = qeSimA.currentPosition = target
      # #endif

      qeB.writePublicData(target)
      qeSimB.targetPosition = qeSimB.currentPosition = target

      testIteration = 0
      for testIteration in range(0, 20):
        #Serial.print("Test iteration: ");
        #Serial.println(testIteration);

        # #ifdef USEQEA
        qeSimA.targetPosition += testIteration
        #uint16_t lastASample = qeA->readPublicData();
        # #endif

        qeSimB.targetPosition += testIteration

        #uint16_t lastBSample = qeB->readPublicData();
        # TODO_MANUAL_CONVERSION: while :
          # #ifdef USEQEA
           # TODO_MANUAL_CONVERSION_INDENT: or  qeSimA.targetPosition != qeSimA.currentPosition
          # #endif
          # TODO_MANUAL_CONVERSION_INDENT: )

            #Serial.print("B+: T: ");
            #Serial.print(qeSimB->targetPosition);
            #Serial.print ("C: ");
            #Serial.println(qeSimB->currentPosition);

            # #ifdef USEQEA
            # TODO_MANUAL_CONVERSION_INDENT: qeSimA.service()
            # #endif

            # TODO_MANUAL_CONVERSION_INDENT: qeSimB.service()
            #delay(15);
          # TODO_MANUAL_CONVERSION_INDENT: delay(10)

          # #ifdef USEQEA

          # TODO_MANUAL_CONVERSION_INDENT: testStr = ("QuadEnc_00A_I%d") % (testIteration)
          # TODO_MANUAL_CONVERSION_INDENT: test(testStr, qeA.readPublicData(), qeSimA.currentPosition)

          # TODO_MANUAL_CONVERSION_INDENT: qeSimA.targetPosition -= 2 * testIteration
          # #endif

          # TODO_MANUAL_CONVERSION_INDENT: testStr = ("QuadEnc_00B_I%d") % (testIteration)
          # TODO_MANUAL_CONVERSION_INDENT: test(testStr, qeB.readPublicData(), qeSimB.currentPosition)

          # TODO_MANUAL_CONVERSION_INDENT: qeSimB.targetPosition -= 2 * testIteration

          # TODO_MANUAL_CONVERSION_INDENT: while qeSimB.targetPosition != (uint16_t:
            # #ifdef USEQEA
             # TODO_MANUAL_CONVERSION_INDENT: or  qeSimA.targetPosition != qeSimA.currentPosition
            # #endif
            # TODO_MANUAL_CONVERSION_INDENT: )

              # #ifdef USEQEA
              # TODO_MANUAL_CONVERSION_INDENT: qeSimA.service()
              # #endif
              # TODO_MANUAL_CONVERSION_INDENT: qeSimB.service()
              # TODO_MANUAL_CONVERSION_INDENT: delay(1)
              #uint16_t newSample;
              # newSample= qeB->readPublicData();
            # TODO_MANUAL_CONVERSION_INDENT: delay(10)
            # #ifdef USEQEA
            # TODO_MANUAL_CONVERSION_INDENT: testStr = ("QuadEnc_01A_I%d") % (testIteration)
            # TODO_MANUAL_CONVERSION_INDENT: test(testStr, qeA.read(), qeSimA.currentPosition)

            # #endif
            # TODO_MANUAL_CONVERSION_INDENT: testStr = ("QuadEnc_01B_I%d") % (testIteration)
            # TODO_MANUAL_CONVERSION_INDENT: test(testStr, qeB.read(), qeSimB.currentPosition)

          # Increment Increment testing
          # TODO_MANUAL_CONVERSION_INDENT: increment = 10
          # TODO_MANUAL_CONVERSION_INDENT: qeSimB.initialize()
          # TODO_MANUAL_CONVERSION_INDENT: if sw == SW18AB_6B:
            # TODO_MANUAL_CONVERSION_INDENT: qeB.begin(18, 19, 10, True)
          # TODO_MANUAL_CONVERSION_INDENT: elif sw == SW8B_68:
            # TODO_MANUAL_CONVERSION_INDENT: qeB.begin(6, 7, 10, True)
          # TODO_MANUAL_CONVERSION_INDENT: qeB.writeMinMaxIncrementTargetPin(0, 65535, increment)

          # TODO_MANUAL_CONVERSION_INDENT: target = 30000

          # TODO_MANUAL_CONVERSION_INDENT: qeB.writePublicData(target)
          # TODO_MANUAL_CONVERSION_INDENT: qeSimB.targetPosition = qeSimB.currentPosition = target

          # TODO_MANUAL_CONVERSION_INDENT: testIteration = 0
          # TODO_MANUAL_CONVERSION_INDENT: expectedOutput = 30000
          # TODO_MANUAL_CONVERSION_INDENT: for testIteration in range(0, 20):

            # TODO_MANUAL_CONVERSION_INDENT: qeSimB.targetPosition += testIteration
            # TODO_MANUAL_CONVERSION_INDENT: expectedOutput += testIteration * increment
            # TODO_MANUAL_CONVERSION_INDENT: while qeSimB.targetPosition != qeSimB.currentPosition:
              # TODO_MANUAL_CONVERSION_INDENT: qeSimB.service()
              # TODO_MANUAL_CONVERSION_INDENT: delay(1)
            # TODO_MANUAL_CONVERSION_INDENT: delay(10)

            # TODO_MANUAL_CONVERSION_INDENT: test("QUADENC_INC_A", qeB.readPublicData(), expectedOutput)

            # TODO_MANUAL_CONVERSION_INDENT: qeSimB.targetPosition -= 2 * testIteration
            # TODO_MANUAL_CONVERSION_INDENT: expectedOutput -= 2 * testIteration * increment

            # TODO_MANUAL_CONVERSION_INDENT: while qeSimB.targetPosition != qeSimB.currentPosition:
              # TODO_MANUAL_CONVERSION_INDENT: qeSimB.service()
              # TODO_MANUAL_CONVERSION_INDENT: delay(1)
            # TODO_MANUAL_CONVERSION_INDENT: delay(10)
            # TODO_MANUAL_CONVERSION_INDENT: test("QUADENC_INC_B", qeB.readPublicData(), expectedOutput)


          # Minimum testing
          # TODO_MANUAL_CONVERSION_INDENT: increment = 10
          # TODO_MANUAL_CONVERSION_INDENT: qeSimB.initialize()
          # TODO_MANUAL_CONVERSION_INDENT: if sw == SW18AB_6B:
            # TODO_MANUAL_CONVERSION_INDENT: qeB.begin(18, 19, 10, True)
          # TODO_MANUAL_CONVERSION_INDENT: elif sw == SW8B_68:
            # TODO_MANUAL_CONVERSION_INDENT: qeB.begin(6, 7, 10, True)
          # TODO_MANUAL_CONVERSION_INDENT: qeB.writeMinMaxIncrementTargetPin(29999, 65535, increment)

          # TODO_MANUAL_CONVERSION_INDENT: target = 30000

          # TODO_MANUAL_CONVERSION_INDENT: qeB.writePublicData(target)
          # TODO_MANUAL_CONVERSION_INDENT: qeSimB.targetPosition = qeSimB.currentPosition = target





          # TODO_MANUAL_CONVERSION_INDENT: qeSimB.targetPosition = 29500

          # TODO_MANUAL_CONVERSION_INDENT: while qeSimB.targetPosition != qeSimB.currentPosition:
            # TODO_MANUAL_CONVERSION_INDENT: qeSimB.service()
            # TODO_MANUAL_CONVERSION_INDENT: delay(1)
          # TODO_MANUAL_CONVERSION_INDENT: delay(10)
          # TODO_MANUAL_CONVERSION_INDENT: test("QUADENC_MIN_A", qeB.readPublicData(), 29999)


          # Maximum testing
          # TODO_MANUAL_CONVERSION_INDENT: increment = 10
          # TODO_MANUAL_CONVERSION_INDENT: qeSimB.initialize()
          # TODO_MANUAL_CONVERSION_INDENT: if sw == SW18AB_6B:
            # TODO_MANUAL_CONVERSION_INDENT: qeB.begin(18, 19, 10, True)
          # TODO_MANUAL_CONVERSION_INDENT: elif sw == SW8B_68:
            # TODO_MANUAL_CONVERSION_INDENT: qeB.begin(6, 7, 10, True)
          # TODO_MANUAL_CONVERSION_INDENT: qeB.writeMinMaxIncrementTargetPin(0, 30500, increment)

          # TODO_MANUAL_CONVERSION_INDENT: target = 30000

          # TODO_MANUAL_CONVERSION_INDENT: qeB.writePublicData(target)
          # TODO_MANUAL_CONVERSION_INDENT: qeSimB.targetPosition = qeSimB.currentPosition = target





          # TODO_MANUAL_CONVERSION_INDENT: qeSimB.targetPosition = 36000

          # TODO_MANUAL_CONVERSION_INDENT: while qeSimB.targetPosition != qeSimB.currentPosition:
            # TODO_MANUAL_CONVERSION_INDENT: qeSimB.service()
            # TODO_MANUAL_CONVERSION_INDENT: delay(1)
          # TODO_MANUAL_CONVERSION_INDENT: delay(10)
          # TODO_MANUAL_CONVERSION_INDENT: test("QUADENC_MAX_A", qeB.readPublicData(), 30500)


          # Target Pin testing

          # TODO_MANUAL_CONVERSION_INDENT: servo = SerialWombatPin.SerialWombatPin(sw,0)
          # TODO_MANUAL_CONVERSION_INDENT: servo.pinMode(1)
          # TODO_MANUAL_CONVERSION_INDENT: servo.writePublicData(30000)
          # TODO_MANUAL_CONVERSION_INDENT: increment = 10
          # TODO_MANUAL_CONVERSION_INDENT: qeSimB.initialize()
          # TODO_MANUAL_CONVERSION_INDENT: if sw == SW18AB_6B:
            # TODO_MANUAL_CONVERSION_INDENT: qeB.begin(18, 19, 10, True)
          # TODO_MANUAL_CONVERSION_INDENT: elif sw == SW8B_68:
            # TODO_MANUAL_CONVERSION_INDENT: qeB.begin(6, 7, 10, True)
          # TODO_MANUAL_CONVERSION_INDENT: qeB.writeMinMaxIncrementTargetPin(0, 65535, increment, 0)

          # TODO_MANUAL_CONVERSION_INDENT: target = 30000

          # TODO_MANUAL_CONVERSION_INDENT: qeB.writePublicData(target)
          # TODO_MANUAL_CONVERSION_INDENT: qeSimB.targetPosition = qeSimB.currentPosition = target

          # TODO_MANUAL_CONVERSION_INDENT: testIteration = 0
          # TODO_MANUAL_CONVERSION_INDENT: expectedOutput = 30000
          # TODO_MANUAL_CONVERSION_INDENT: for testIteration in range(0, 20):

            # TODO_MANUAL_CONVERSION_INDENT: qeSimB.targetPosition += testIteration
            # TODO_MANUAL_CONVERSION_INDENT: expectedOutput += testIteration * increment
            # TODO_MANUAL_CONVERSION_INDENT: while qeSimB.targetPosition != qeSimB.currentPosition:
              # TODO_MANUAL_CONVERSION_INDENT: qeSimB.service()
              # TODO_MANUAL_CONVERSION_INDENT: delay(1)
            # TODO_MANUAL_CONVERSION_INDENT: delay(10)

            # TODO_MANUAL_CONVERSION_INDENT: test("QUADENC_TARGET_PIN_A", servo.readPublicData(), expectedOutput)

            # TODO_MANUAL_CONVERSION_INDENT: qeSimB.targetPosition -= 2 * testIteration
            # TODO_MANUAL_CONVERSION_INDENT: expectedOutput -= 2 * testIteration * increment

            # TODO_MANUAL_CONVERSION_INDENT: while qeSimB.targetPosition != qeSimB.currentPosition:
              # TODO_MANUAL_CONVERSION_INDENT: qeSimB.service()
              # TODO_MANUAL_CONVERSION_INDENT: delay(1)
            # TODO_MANUAL_CONVERSION_INDENT: delay(10)
            # TODO_MANUAL_CONVERSION_INDENT: test("QUADENC_TARGET_PIN_B", servo.readPublicData(), expectedOutput)





          # Frequency testing

          # TODO_MANUAL_CONVERSION_INDENT: resetAll()
          # TODO_MANUAL_CONVERSION_INDENT: if sw == SW18AB_6B:
            # TODO_MANUAL_CONVERSION_INDENT: qeB.begin(18, 19, 1, True);  # 1mS debounce
          # TODO_MANUAL_CONVERSION_INDENT: elif sw == SW8B_68:
            # TODO_MANUAL_CONVERSION_INDENT: qeB.begin(6, 7, 1, True);  # 1mS debounce

          # TODO_MANUAL_CONVERSION_INDENT: sw4bPin = 0
          # If no SW4B available, continue
          # Initialize the pin mode to pulse timer, uS
          # Set up the PWM to 32Hz (31250 uS) duty cycle to 0x1000 + 0x1000 * pin

          # TODO_MANUAL_CONVERSION_INDENT: SerialWombatChip sw4b = SWChipAndPinTo4BChip(sw, qeB.pin())


          # TODO_MANUAL_CONVERSION_INDENT: sw4bPin = SWChipAndPinTo4BPin(sw,qeB.pin())


          # TODO_MANUAL_CONVERSION_INDENT: if sw4bPin == 0:
            # TODO_MANUAL_CONVERSION_INDENT: test("QuadEnc Test SW4B 0 pin isn't output", 0);  # Pin 0 can't output

          # TODO_MANUAL_CONVERSION_INDENT: pwm4B = SerialWombatPWM.SerialWombatPWM_4AB(sw4b)
          # TODO_MANUAL_CONVERSION_INDENT: pwm4B.begin(sw4bPin)
          # TODO_MANUAL_CONVERSION_INDENT: pwm4B.setFrequency_SW4AB(SW4AB_PWMFrequency_125_Hz)

          # TODO_MANUAL_CONVERSION_INDENT: pwm4B.writePublicData(0x8000)





          # TODO_MANUAL_CONVERSION_INDENT: delay(3000)


          # TODO_MANUAL_CONVERSION_INDENT: test("QUADENC_FREQ_A", qeB.readFrequency(), 125, 10)
          # TODO_MANUAL_CONVERSION_INDENT: test("QUADENC_FREQ_B", sw.readPublicData((qeB.pin() + 1)), 125, 10)
