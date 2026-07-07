# Converted from Testing/SW4B_SW18AB_SW08B_AutomatedTest/Scaling.ino
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
import SerialWombatAbstractScaledOutput
import SerialWombatPWM

scalingInput18AB = SerialWombatPWM.SerialWombatPWM_18AB(SW18AB_6B)
scalingOutput18AB = SerialWombatPWM.SerialWombatPWM_18AB(SW18AB_6B)

SCALING_INPUT_PIN = 5  #18
SCALING_OUTPUT_PIN = 6  #19

# TODO_MANUAL_CONVERSION: *scalingInput = SerialWombatPWM.SerialWombatPWM_18AB()
# TODO_MANUAL_CONVERSION: *scalingOutput = SerialWombatPWM.SerialWombatPWM_18AB()
def scalingTest():
  scalingInput = scalingInput18AB
  scalingOutput = scalingOutput18AB
  scalingTimeoutTest()

  scalingInputScalingTest()
  scalingInvertScalingTest()
  scalingOutputScalingTest()

  scalingRateControl16HzTest()
  scaling1stOrderTest()
  scalingHysteresisTest()

  scalingSOLinearInterpolationTest()

  if 0:
      #PID
      scalingInput.begin(SCALING_INPUT_PIN)
      scalingOutput.begin(SCALING_OUTPUT_PIN)
      scalingOutput.writeScalingEnabled(False, SCALING_INPUT_PIN)

      kp = 0x100  #256.00
      ki = 0x0  #0
      kd = 0
      target = 10000
      processOutput = 8000

      scalingOutput.writePID(kp, ki, kd, target, PERIOD_128mS)
      scalingInput.writePublicData(processOutput)
      scalingOutput.writeScalingEnabled(True, SCALING_INPUT_PIN)

      test("SCALE_PID_01", scalingOutput.readPublicData(), (target - processOutput) * kp >> 8)

      kp = 200
      ki = 300
      scalingOutput.writePID(kp, ki, kd, target, PERIOD_128mS)
      result = 0
      while result < 65535:
        result = scalingOutput.readPublicData()
        process = result - 16000
        if process < 0:
          process = 0

        scalingInput.writePublicData(process)
        print(result, end="")
        print(' ', end="")
        print(process)

  def scalingTimeoutTest():
    #Timeout Test
    resetAll()

    scalingInput.begin(SCALING_INPUT_PIN)
    scalingOutput.begin(SCALING_OUTPUT_PIN)
    scalingOutput.writeScalingEnabled(False, SCALING_INPUT_PIN)
    scalingOutput.writeScalingEnabled(False, SCALING_OUTPUT_PIN)
    scalingOutput.writeScalingEnabled(True, SCALING_OUTPUT_PIN)
    SW18AB_6B.writePublicData(SCALING_OUTPUT_PIN, 0x0000)
    scalingOutput.writeTimeout(1000, 0x8000)
    startTime = millis()
    while millis() < startTime + 900:
      if scalingOutput.readLastOutputValue() == 0:
        pass
        # TODO_MANUAL_CONVERSION: pass(0)
      else:
        fail(1)
        print("F0")
      delay(100)
    delay(200)
    v = scalingOutput.readLastOutputValue()
    x = 0x8000
    if v == x:
      pass
      # TODO_MANUAL_CONVERSION: pass(0)
    else:
      fail(2)
      print("F0. ");  Serial.print(" V: "); Serial.print(v); Serial.print(" X:"); Serial.println(x, end="")



  def scalingInputScalingTest():
      #Input Scaling Test
      resetAll()

      scalingInput.begin(SCALING_INPUT_PIN)
      scalingOutput.begin(SCALING_OUTPUT_PIN)
      lowLimit = 3000
      highLimit = 50000

      scalingOutput.writeScalingEnabled(False, SCALING_INPUT_PIN)
      scalingOutput.writeScalingEnabled(True, SCALING_INPUT_PIN)

      for i in range(0, 65536):

        SW18AB_6B.writePublicData(SCALING_INPUT_PIN, i)
        scalingOutput.writeInputScaling(lowLimit, highLimit)
        delay(10)
        expected = 0
        if i > lowLimit:
          if i > highLimit:
            expected = 65535
          else:
            expected =  (((i - lowLimit) / (float)(highLimit - lowLimit)) * 65535)
        value = scalingOutput.readPublicData()

        if withinRange(value, expected, 0, 1):
          pass
          # TODO_MANUAL_CONVERSION: pass(1)
        else:
          fail(1)
          print("F1. i: "); Serial.print(i); Serial.print(" V: "); Serial.print(value); Serial.print(" X:"); Serial.println(expected, end="")


    # TODO_MANUAL_CONVERSION_INDENT: def scalingInvertScalingTest():
        #Invert Scaling Test
        scalingInput.begin(SCALING_INPUT_PIN)
        scalingOutput.begin(SCALING_OUTPUT_PIN)
        lowLimit = 3000
        highLimit = 50000
        scalingOutput.writeScalingEnabled(False, SCALING_INPUT_PIN)
        scalingOutput.writeScalingEnabled(True, SCALING_INPUT_PIN)
        scalingOutput.writeScalingInvertedInput(True)

        for i in range(0, 65536):

          SW18AB_6B.writePublicData(SCALING_INPUT_PIN, i)
          scalingOutput.writeOutputScaling(lowLimit, highLimit)
          delay(10)
          expected = 0


          expected =  ((highLimit - lowLimit) * (float)(65535 - i) / 65535 + lowLimit)

          value = scalingOutput.readPublicData()

          if withinRange(value, expected, 0, 1):
            pass
            # TODO_MANUAL_CONVERSION: pass(1)
          else:
            fail(1)
            print("F2. i: "); Serial.print(i); Serial.print(" V: "); Serial.print(value); Serial.print(" X:"); Serial.println(expected, end="")

      def scalingOutputScalingTest():
          #Output Scaling Test
          scalingInput.begin(SCALING_INPUT_PIN)
          scalingOutput.begin(SCALING_OUTPUT_PIN)
          lowLimit = 3000
          highLimit = 50000
          scalingOutput.writeScalingEnabled(False, SCALING_INPUT_PIN)
          scalingOutput.writeScalingEnabled(True, SCALING_INPUT_PIN)

          for i in range(0, 65536):

            SW18AB_6B.writePublicData(SCALING_INPUT_PIN, i)
            scalingOutput.writeOutputScaling(lowLimit, highLimit)
            delay(10)
            expected = 0


            expected =  ((highLimit - lowLimit) * (float)(i) / 65535 + lowLimit)

            value = scalingOutput.readPublicData()

            if withinRange(value, expected, 0, 1):
              pass
              # TODO_MANUAL_CONVERSION: pass(1)
            else:
              fail(1)
              print("F3. i: "); Serial.print(i); Serial.print(" V: "); Serial.print(value); Serial.print(" X:"); Serial.println(expected, end="")

        # TODO_MANUAL_CONVERSION_INDENT: def scalingRateControl16HzTest():
            #Rate Control Test 16 Hz, dual pin
            scalingInput.begin(SCALING_INPUT_PIN)
            scalingOutput.begin(SCALING_OUTPUT_PIN)
            SW18AB_6B.writePublicData(SCALING_OUTPUT_PIN, 0)

            scalingOutput.writeScalingEnabled(False, SCALING_INPUT_PIN)

            scalingOutput.writeRateControl(PERIOD_64mS, 100)
            scalingOutput.writeScalingEnabled(True, SCALING_INPUT_PIN)
            SW18AB_6B.writePublicData(SCALING_INPUT_PIN, 1000)
            while scalingOutput.readPublicData() == 0:

              for i in range(1, 10):
                value = scalingOutput.readPublicData()

                if withinRange(value, i * 100, 0, 0):
                  pass
                  # TODO_MANUAL_CONVERSION: pass(1)
                else:
                  fail(1)
                  print("F8. i: "); Serial.print(i); Serial.print(" V: "); Serial.print(value); Serial.print(" X:"); Serial.println(i * 100, end="")
                delay(64)

              for i in range(1, 10):
                value = scalingOutput.readPublicData()

                if withinRange(value, 1000, 0, 0):
                  pass
                  # TODO_MANUAL_CONVERSION: pass(1)
                else:
                  fail(1)
                  print("F9. i: "); Serial.print(i); Serial.print(" V: "); Serial.print(value); Serial.print(" X:"); Serial.println(1000, end="")
                delay(64)
              SW18AB_6B.writePublicData(SCALING_INPUT_PIN, 500)
              expected = 1000
              for i in range(0, 5):
                value = scalingOutput.readPublicData()

                if withinRange(value, expected, 0, 0):
                  pass
                  # TODO_MANUAL_CONVERSION: pass(1)
                else:
                  fail(1)
                  print("F10. i: "); Serial.print(i); Serial.print(" V: "); Serial.print(value); Serial.print(" X:"); Serial.println(expected, end="")

                expected -= 100
                delay(64)
              for i in range(1, 10):
                value = scalingOutput.readPublicData()

                if withinRange(value, 500, 0, 0):
                  pass
                  # TODO_MANUAL_CONVERSION: pass(1)
                else:
                  fail(1)
                  print("F11. i: "); Serial.print(i); Serial.print(" V: "); Serial.print(value); Serial.print(" X:"); Serial.println(500, end="")
                delay(64)

            def scaling1stOrderTest():
                #1stOrderFiltering, different pins
                scalingInput.begin(SCALING_INPUT_PIN)
                scalingOutput.begin(SCALING_OUTPUT_PIN)
                SW18AB_6B.writePublicData(SCALING_OUTPUT_PIN, 0)

                scalingOutput.writeScalingEnabled(False, SCALING_INPUT_PIN)
                scalingOutput.write1stOrderFiltering(PERIOD_8mS, 65000)
                scalingOutput.writeScalingEnabled(True, SCALING_INPUT_PIN)
                SW18AB_6B.writePublicData(SCALING_INPUT_PIN, 10000)


                value = scalingOutput.readPublicData()
                startTime = millis()
                while value < 9700:
                  #Serial.println(value);
                  value = scalingOutput.readPublicData()
                  delay(0)
                endTime = millis()
                elapsed = endTime - startTime  # Should take about 3400mS


                if withinRange(elapsed, 3400, 0, 200):
                  pass
                  # TODO_MANUAL_CONVERSION: pass(1)
                else:
                  fail(1)
                  print("F12.  Criticalnot ");  Serial.print(" V: "); Serial.print(elapsed); Serial.print(" X:"); Serial.println(3400, end="")


              # TODO_MANUAL_CONVERSION_INDENT: def scalingHysteresisTest():
                  #Hysteresis
                  resetAll()
                  scalingInput.begin(SCALING_INPUT_PIN)
                  scalingOutput.begin(SCALING_OUTPUT_PIN)
                  scalingOutput.writeScalingEnabled(False, SCALING_INPUT_PIN)

                  lowLimit = 0x5000
                  highLimit = 0xA000
                  lowValue = 500
                  highValue = 1000
                  startValue = 750
                  midValue = lowLimit + (highLimit - lowLimit) / 2

                  scalingInput.writePublicData(midValue)
                  scalingOutput.writeScalingEnabled(True, SCALING_INPUT_PIN)
                  scalingOutput.writeHysteresis(lowLimit, lowValue, highLimit, highValue, startValue)

                  test("SCALE_HYS_01", scalingOutput.readPublicData(), startValue)

                  scalingInput.writePublicData(highLimit)
                  test("SCALE_HYS_02", scalingOutput.readPublicData(), highValue)

                  scalingInput.writePublicData(lowLimit)
                  test("SCALE_HYS_03", scalingOutput.readPublicData(), lowValue)

                  scalingInput.writePublicData(65535)
                  test("SCALE_HYS_04", scalingOutput.readPublicData(), highValue)

                  scalingInput.writePublicData(midValue)
                  test("SCALE_HYS_05", scalingOutput.readPublicData(), highValue)

                  scalingInput.writePublicData(0)
                  test("SCALE_HYS_06", scalingOutput.readPublicData(), lowValue)

                  scalingInput.writePublicData(midValue)
                  test("SCALE_HYS_07", scalingOutput.readPublicData(), lowValue)


                def scalingSOLinearInterpolationTest():
                  resetAll()
                  # Linear scaling test.  Table is:
                  table = [
                  0, 0x1000,
                  10000, 0x0000,
                  20000, 0x8000,
                  30000, 0xC000,
                  40000, 0xC000,
                  0xFFFF, 0
                  ]
                  #TODO SW18AB_6B.writeUserBuffer(0x220, (uint8_t*)table, sizeof(table));

                  bufferAddr = 0x20  # Was 220 on 6B test
                  # TODO_MANUAL_CONVERSION: SW18AB_6B.writeUserBuffer(bufferAddr, (uint8_t*)table, len(table))

                  scalingInput.begin(SCALING_INPUT_PIN)
                  scalingOutput.begin(SCALING_OUTPUT_PIN)
                  scalingOutput.writeScalingEnabled(False, SCALING_INPUT_PIN)
                  scalingOutput.Enable2DLookupOutputScaling(bufferAddr)
                  scalingOutput.writeScalingEnabled(True, SCALING_INPUT_PIN)
                  i = 0

                  for i in range(0, (65535) + 1):
                    scalingInput.writePublicData(i)
                    if i == 0:
                      test("SCALE_LI_00", scalingOutput.readPublicData(), 0x1000)
                    elif i <= 10000:
                      test("SCALE_LI_01", scalingOutput.readPublicData(), (10000 - i) * 0x1000 / 10000, 2, 3  )
                    elif i <= 20000:
                      test("SCALE_LI_02", scalingOutput.readPublicData(), (i - 10000) * 0x8000 / 10000, 2, 3  )
                    elif i <= 30000:
                      test("SCALE_LI_03", scalingOutput.readPublicData(), (i - 20000) * 0x4000 / (10000) + 0x8000, 2, 3  )
                    elif i <= 40000:
                      test("SCALE_LI_04", scalingOutput.readPublicData(), 0xC000 )
                    else:
                      test("SCALE_LI_05", scalingOutput.readPublicData(),0xC000- (i - 40000) * 0xC000 / (0xFFFF-40000) , 2, 3  )
                    yield()
