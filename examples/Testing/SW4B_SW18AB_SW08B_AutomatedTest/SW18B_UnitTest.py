import time
#import datetime
import sys
"""
Pin Matching:
SW18AB  SW4B  SW8B  DAC
0       D3    -     SWA
1       -     -
2       -     -
3       -     -
4       -     -
5       D2    -
6       D1    8P0   SWD
7       C0    8P5   SWB
8       D0    -
9       C1    8P4   SWC
10      C2    -
11      C3    -
12      E0    -
13      F0    -
14      F3    -
15      F2    -
16      F1    8P2   HWA
17      E3    8P3   HWB
18      E2    8P6   HWC
19      E1    8P7   HWD
"""
#sys.path.append(r'..')
import SW18B_UnitTest_globals
from ArduinoFunctions import delay
from ArduinoFunctions import millis


TEST_SW18AB = True
TEST_SW4B = False
TEST_SW8B = False

UNIT_TEST_QUEUE = False #Updated for 2.2.4
UNIT_TEST_USDSENSOR = False #Updated for 2.2.4
UNIT_TEST_HSCLOCK = False #Updated for 2.2.4
UNIT_TEST_HSCOUNTER = False #Updated for 2.2.4
UNIT_TEST_RESISTANCE_INPUT = True #Updated for 2.2.4
UNIT_TEST_BLINK = False #Updated for 2.2.4
UNIT_TEST_SCALING = False #Updated for 2.2.4
UNIT_TEST_SW_UART = False #Updated for 2.2.4
UNIT_TEST_UART = False #Updated for 2.2.4
UNIT_TEST_HBRIDGE = False #Updated for 2.2.4
UNIT_TEST_ANALOG_INPUT = False #Updated for 2.2.4
UNIT_TEST_FREQUENCY_OUTPUT = False #Updated for 2.2.4
UNIT_TEST_INPUT_PROCESSOR = False #Updated for 2.2.4   
UNIT_TEST_COMMUNICATION_ERROR = False
UNIT_TEST_ECHO = False #Updated for 2.2.4
UNIT_TEST_PWM = False  #Updated for 2.2.4
UNIT_TEST_QUAD_ENC = False #Updated for 2.2.4
UNIT_TEST_SERVO = False #Updated for 2.2.4
UNIT_TEST_PUBLIC_DATA = True #Updated for 2.2.4
UNIT_TEST_DEBOUNCED_INPUT = False #Updated for 2.2.4
UNIT_TEST_PULSE_ON_CHANGE = False #Updated for 2.2.4
UNIT_TEST_PULSE_TIMER = False #Updated for 2.2.4
UNIT_TEST_SEQUENCE_TEST = False
UNIT_TEST_DATALOGGER = False #Updated for 2.2.4
UNIT_TEST_PROTECTED_OUTPUT = False
UNIT_TEST_WATCHDOG = True #Updated for 2.2.4
UNIT_TEST_FRAME_TIMER = False
UNIT_TEST_QUEUED_PULSE_OUTPUT = False
UNIT_TEST_SOURCE_VOLTAGE = False
UNIT_TEST_IR_TX_RX = False #Updated for 2.2.4

SW18B_UnitTest_globals.init()

SW6B = SW18B_UnitTest_globals.SW18AB_6B
SW6C = SW18B_UnitTest_globals.SW4B_6C
SW6D = SW18B_UnitTest_globals.SW4B_6D
SW6E = SW18B_UnitTest_globals.SW4B_6E
SW6F = SW18B_UnitTest_globals.SW4B_6F



print()
print("#############################################################")
print()
print("Serial Wombat 18B Unit Test")
print()
print("#############################################################")
print()

lastPassedTest = -1
SW18B_UnitTest_globals.resetAll()   
SW6B.readVersion()
print(f"SW18AB Version: {SW6B.fwVersion}")


def testPassed(i):
    passCount += 1
    lastPassedTest = i

lastFailedTest = -1

def testFailed(i):
    lastFailedTest = i
    failCount += 1

#import SW18B_UnitTest_Analog


import SW18B_UnitTest_Analog
import SW18B_UnitTest_Blink
import SW18B_UnitTest_DataLogger
import SW18B_UnitTest_Servo

import SW18B_UnitTest_Scaling
import SW18B_UnitTest_Debounce
import SW18B_UnitTest_HBridge
import SW18B_UnitTest_HSClock
import SW18B_UnitTest_HSCounter
import SW18B_UnitTest_IR_TX_RX
import SW18B_UnitTest_EchoTest

import SW18B_UnitTest_PWM
import SW18B_UnitTest_ProcessedInput
import SW18B_UnitTest_PublicData
import SW18B_UnitTest_PulseOnChange
import SW18B_UnitTest_PulseTimer
import SW18B_UnitTest_ResistanceInput
import SW18B_UnitTest_UART
import SW18B_UnitTest_UART_SW
import SW18B_UnitTest_USDSensor

import SW18B_UnitTest_CommunicationError
import SW18B_UnitTest_Queue
import SW18B_UnitTest_FrequencyOutput
import SW18B_UnitTest_Watchdog




import SW18B_UnitTest_FrameTimer
import SW18B_UnitTest_QuadEnc

def currentTimeString():
    return  f" timestamp {millis()//1000} "

def loop():

    if (UNIT_TEST_ANALOG_INPUT):
        currentTest = "Analog Input Test"
        if(TEST_SW18AB):
             print(f"Starting SW18AB {currentTest} at {currentTimeString()}")
             SW18B_UnitTest_Analog.analogInputTest(sw=SW18B_UnitTest_globals.SW18AB_6B)
             print(f"SW18AB {currentTest} Complete at {currentTimeString()}.  Pass: {SW18B_UnitTest_globals.passCount}, Fail: {SW18B_UnitTest_globals.failCount}")
        if(TEST_SW8B):
             print(f"Starting SW8B {currentTest} at {currentTimeString()}")
             SW18B_UnitTest_Analog.analogInputTest(sw=SW18B_UnitTest_globals.SW8B_68)
             print(f"SW8B {currentTest} Complete at {currentTimeString()}.  Pass: {SW18B_UnitTest_globals.passCount}, Fail: {SW18B_UnitTest_globals.failCount}")
    
    if (UNIT_TEST_COMMUNICATION_ERROR):
        currentTest = "Communication Error Test"
        if (TEST_SW18AB):
             print(f"Starting SW18AB {currentTest} at {currentTimeString()}")
             SW18B_UnitTest_SW18AB.sw18abTest()
             print(f"SW18AB {currentTest} Complete at {currentTimeString()}.  Pass: {SW18B_UnitTest_globals.passCount}, Fail: {SW18B_UnitTest_globals.failCount}")
        if (TEST_SW8B):
                print(f"Starting SW8B {currentTest} at {currentTimeString()}")
                SW18B_UnitTest_SW8B.sw8bTest()
                print(f"SW8B {currentTest} Complete at {currentTimeString()}.  Pass: {SW18B_UnitTest_globals.passCount}, Fail: {SW18B_UnitTest_globals.failCount}")


    if (UNIT_TEST_SOURCE_VOLTAGE):
        currentTest = "Source Voltage Test"
        if(TEST_SW18AB):
             print(f"Starting SW18AB {currentTest} at {currentTimeString()}")
             SW18B_UnitTest_SW18AB.sourceVoltageTest()
             print(f"SW18AB {currentTest} Complete at {currentTimeString()}.  Pass: {SW18B_UnitTest_globals.passCount}, Fail: {SW18B_UnitTest_globals.failCount}")
        if(TEST_SW8B):
             print(f"Starting SW8B {currentTest} at {currentTimeString()}")
             SW18B_UnitTest_SW8B.sourceVoltageTest()
             print(f"SW8B {currentTest} Complete at {currentTimeString()}.  Pass: {SW18B_UnitTest_globals.passCount}, Fail: {SW18B_UnitTest_globals.failCount}")
    
    if(UNIT_TEST_BLINK):
        currentTest = "Blink Test"
        if(TEST_SW18AB):
             print(f"Starting SW18AB {currentTest} at {currentTimeString()}")
             SW18B_UnitTest_Blink.blinkTest(SW18B_UnitTest_globals.SW18AB_6B, blinkPin= 6, sourcePin= 5)
             print(f"SW18AB {currentTest} Complete at {currentTimeString()}.  Pass: {SW18B_UnitTest_globals.passCount}, Fail: {SW18B_UnitTest_globals.failCount}")
        if(TEST_SW8B):
             print(f"Starting SW8B {currentTest} at {currentTimeString()}")
             SW18B_UnitTest_Blink.blinkTest(SW18B_UnitTest_globals.SW8B_68, blinkPin= 6, sourcePin= 5)
             print(f"SW8B {currentTest} Complete at {currentTimeString()}.  Pass: {SW18B_UnitTest_globals.passCount}, Fail: {SW18B_UnitTest_globals.failCount}")

    if (UNIT_TEST_DATALOGGER):
        currentTest = "Data Logger Test"
        if(TEST_SW18AB):
             print(f"Starting SW18AB {currentTest} at {currentTimeString()}")
             SW18B_UnitTest_DataLogger.dataLoggerTest()
             print(f"SW18AB {currentTest} Complete at {currentTimeString()}.  Pass: {SW18B_UnitTest_globals.passCount}, Fail: {SW18B_UnitTest_globals.failCount}")
                
    if (UNIT_TEST_SERVO):
        currentTest = "Servo Test"
        if(TEST_SW18AB):
             print(f"Starting SW18AB {currentTest} at {currentTimeString()}")
             SW18B_UnitTest_Servo.servoTest(sw=SW18B_UnitTest_globals.SW18AB_6B, startPin=0, endPin=19)
             print(f"SW18AB {currentTest} Complete at {currentTimeString()}.  Pass: {SW18B_UnitTest_globals.passCount}, Fail: {SW18B_UnitTest_globals.failCount}")
        if(TEST_SW8B):
             print(f"Starting SW8B {currentTest} at {currentTimeString()}")
             SW18B_UnitTest_Servo.servoTest(sw=SW18B_UnitTest_globals.SW8B_68, startPin=0, endPin=7)
             print(f"SW8B {currentTest} Complete at {currentTimeString()}.  Pass: {SW18B_UnitTest_globals.passCount}, Fail: {SW18B_UnitTest_globals.failCount}")
    if (UNIT_TEST_PWM):
         print(f"Starting PWM Test at {currentTimeString()}")
         if(TEST_SW18AB):
             SW18B_UnitTest_globals.resetAll()
             SW18B_UnitTest_PWM.pwmTest(sw=SW18B_UnitTest_globals.SW18AB_6B, startPin=0, endPin=19)
             print(f"PWM 18AB Test Complete at {currentTimeString()}.  Pass: {SW18B_UnitTest_globals.passCount}, Fail: {SW18B_UnitTest_globals.failCount}")
         if(TEST_SW8B):
                SW18B_UnitTest_globals.resetAll()
                SW18B_UnitTest_PWM.pwmTest(sw=SW18B_UnitTest_globals.SW8B_68, startPin=0, endPin=7)
                print(f"PWM 8B Test Complete at {currentTimeString()}.  Pass: {SW18B_UnitTest_globals.passCount}, Fail: {SW18B_UnitTest_globals.failCount}")
    if (UNIT_TEST_DEBOUNCED_INPUT):
        currentTest = "Debounced Input Test"
        if(TEST_SW18AB):
             print(f"Starting SW18AB {currentTest} at {currentTimeString()}")
             SW18B_UnitTest_Debounce.debounceTest(sw=SW18B_UnitTest_globals.SW18AB_6B)
             print(f"SW18AB {currentTest} Complete at {currentTimeString()}.  Pass: {SW18B_UnitTest_globals.passCount}, Fail: {SW18B_UnitTest_globals.failCount}")
        if(TEST_SW8B):
             print(f"Starting SW8B {currentTest} at {currentTimeString()}")
             SW18B_UnitTest_Debounce.debounceTest(sw=SW18B_UnitTest_globals.SW8B_68)
             print(f"SW8B {currentTest} Complete at {currentTimeString()}.  Pass: {SW18B_UnitTest_globals.passCount}, Fail: {SW18B_UnitTest_globals.failCount}")
    if (UNIT_TEST_HBRIDGE):
        currentTest = "HBridge Test"
        if(TEST_SW18AB):
             print(f"Starting SW18AB {currentTest} at {currentTimeString()}")
             SW18B_UnitTest_HBridge.hBridgeTest(sw=SW18B_UnitTest_globals.SW18AB_6B,hBridgeFirstPin= 5,hBridgeSecondPin=6)
             print(f"SW18AB {currentTest} Complete at {currentTimeString()}.  Pass: {SW18B_UnitTest_globals.passCount}, Fail: {SW18B_UnitTest_globals.failCount}")
        if(TEST_SW8B):
             print(f"Starting SW8B {currentTest} at {currentTimeString()}")
             SW18B_UnitTest_HBridge.hBridgeTest(sw=SW18B_UnitTest_globals.SW8B_68, hBridgeFirstPin= 5,hBridgeSecondPin=6)
             print(f"SW8B {currentTest} Complete at {currentTimeString()}.  Pass: {SW18B_UnitTest_globals.passCount}, Fail: {SW18B_UnitTest_globals.failCount}")    
    if(UNIT_TEST_HSCLOCK):
        currentTest = "HSClock Test"
        if(TEST_SW18AB):
             print(f"Starting SW18AB {currentTest} at {currentTimeString()}")
             SW18B_UnitTest_HSClock.hsClockTest()
             print(f"SW18AB {currentTest} Complete at {currentTimeString()}.  Pass: {SW18B_UnitTest_globals.passCount}, Fail: {SW18B_UnitTest_globals.failCount}")
        
    if (UNIT_TEST_IR_TX_RX):
        currentTest = "IR TX/RX Test"
        if(TEST_SW18AB or TEST_SW8B):
             print(f"Starting SW18AB {currentTest} at {currentTimeString()}")
             SW18B_UnitTest_IR_TX_RX.irTxRxTest()
             print(f"SW18AB {currentTest} Complete at {currentTimeString()}.  Pass: {SW18B_UnitTest_globals.passCount}, Fail: {SW18B_UnitTest_globals.failCount}")
    
    if (UNIT_TEST_PUBLIC_DATA):
            currentTest = "Public Data Test"
            if(TEST_SW18AB ):
                print(f"Starting SW18AB and SW8B {currentTest} at {currentTimeString()}")
                SW18B_UnitTest_PublicData.publicDataTest(SW18B_UnitTest_globals.SW18AB_6B)
                print(f"SW18AB and SW8B {currentTest} Complete at {currentTimeString()}.  Pass: {SW18B_UnitTest_globals.passCount}, Fail: {SW18B_UnitTest_globals.failCount}")
            if(TEST_SW8B ):
                print(f"Starting SW8B {currentTest} at {currentTimeString()}")
                SW18B_UnitTest_PublicData.publicDataTest(SW18B_UnitTest_globals.SW8B_68)
                print(f"SW8B {currentTest} Complete at {currentTimeString()}.  Pass: {SW18B_UnitTest_globals.passCount}, Fail: {SW18B_UnitTest_globals.failCount}")
    
    if (UNIT_TEST_PULSE_TIMER):
        currentTest = "Pulse Timer Test"
        if(TEST_SW18AB):
             print(f"Starting SW18AB {currentTest} at {currentTimeString()}")
             SW18B_UnitTest_PulseTimer.pulseTimerTest(sw=SW18B_UnitTest_globals.SW18AB_6B, startPin=0, endPin=19)
             print(f"SW18AB {currentTest} Complete at {currentTimeString()}.  Pass: {SW18B_UnitTest_globals.passCount}, Fail: {SW18B_UnitTest_globals.failCount}")
        if(TEST_SW8B):
             print(f"Starting SW8B {currentTest} at {currentTimeString()}")
             SW18B_UnitTest_PulseTimer.pulseTimerTest(sw=SW18B_UnitTest_globals.SW8B_68, startPin=0, endPin=7)
             print(f"SW8B {currentTest} Complete at {currentTimeString()}.  Pass: {SW18B_UnitTest_globals.passCount}, Fail: {SW18B_UnitTest_globals.failCount}")

    if(UNIT_TEST_QUEUE):
        currentTest = "Queue Test"
        if(TEST_SW18AB):
             print(f"Starting SW18AB {currentTest} at {currentTimeString()}")
             SW18B_UnitTest_Queue.queueTest(SW18B_UnitTest_globals.SW18AB_6B)
             print(f"SW18AB {currentTest} Complete at {currentTimeString()}.  Pass: {SW18B_UnitTest_globals.passCount}, Fail: {SW18B_UnitTest_globals.failCount}")
        if(TEST_SW8B):
             print(f"Starting SW8B {currentTest} at {currentTimeString()}")
             SW18B_UnitTest_Queue.queueTest(SW18B_UnitTest_globals.SW8B_68)
             print(f"SW8B {currentTest} Complete at {currentTimeString()}.  Pass: {SW18B_UnitTest_globals.passCount}, Fail: {SW18B_UnitTest_globals.failCount}")
    
    if(UNIT_TEST_UART):
        currentTest = "HW UART Test"
        if(TEST_SW18AB):
             print(f"Starting SW18AB {currentTest} at {currentTimeString()}")
             SW18B_UnitTest_UART.uartHWTest(sw=SW18B_UnitTest_globals.SW18AB_6B,txPin0= 7,rxPin0= 9,txPin1= 17,rxPin1= 19)
             print(f"SW18AB {currentTest} Complete at {currentTimeString()}.  Pass: {SW18B_UnitTest_globals.passCount}, Fail: {SW18B_UnitTest_globals.failCount}")
        if(TEST_SW8B):
             print(f"Starting SW8B {currentTest} at {currentTimeString()}")
             SW18B_UnitTest_UART.uartHWTest(sw=SW18B_UnitTest_globals.SW8B_68,txPin0= 4,rxPin0= 5,txPin1= None,rxPin1= None)
             print(f"SW8B {currentTest} Complete at {currentTimeString()}.  Pass: {SW18B_UnitTest_globals.passCount}, Fail: {SW18B_UnitTest_globals.failCount}")

    if (UNIT_TEST_PULSE_ON_CHANGE):
        currentTest = "Pulse On Change Test"
        if(TEST_SW18AB):
             print(f"Starting SW18AB {currentTest} at {currentTimeString()}")
             SW18B_UnitTest_PulseOnChange.pulseOnChangeTest18AB()
             print(f"SW18AB {currentTest} Complete at {currentTimeString()}.  Pass: {SW18B_UnitTest_globals.passCount}, Fail: {SW18B_UnitTest_globals.failCount}")
        if(TEST_SW8B):
             print(f"Starting SW8B {currentTest} at {currentTimeString()}")
             SW18B_UnitTest_PulseOnChange.pulseOnChangeTest8B(SW18B_UnitTest_globals.SW8B_68)
             print(f"SW8B {currentTest} Complete at {currentTimeString()}.  Pass: {SW18B_UnitTest_globals.passCount}, Fail: {SW18B_UnitTest_globals.failCount}")
    
    if (UNIT_TEST_RESISTANCE_INPUT):
        currentTest = "ReistanceInput Test"
        if(TEST_SW18AB):
             print(f"Starting SW18AB and SW8B {currentTest} at {currentTimeString()}")
             SW18B_UnitTest_ResistanceInput.resistanceInputTest()
             print(f"SW18AB and SW8B{currentTest} Complete at {currentTimeString()}.  Pass: {SW18B_UnitTest_globals.passCount}, Fail: {SW18B_UnitTest_globals.failCount}")
 
    if(UNIT_TEST_SW_UART):
        currentTest = "SW UART Test"
        if(TEST_SW18AB or TEST_SW8B):
             print(f"Starting SW18AB and SW8B {currentTest} at {currentTimeString()}")
             SW18B_UnitTest_UART_SW.uartSWTest()
             print(f"SW18AB and SW8B{currentTest} Complete at {currentTimeString()}.  Pass: {SW18B_UnitTest_globals.passCount}, Fail: {SW18B_UnitTest_globals.failCount}")
    if (UNIT_TEST_USDSENSOR):
        currentTest = "USD Sensor Test"
        if(TEST_SW18AB):
             print(f"Starting SW18AB {currentTest} at {currentTimeString()}")
             SW18B_UnitTest_USDSensor.usdSensorTest(10)
             print(f"SW18AB {currentTest} Complete at {currentTimeString()}.  Pass: {SW18B_UnitTest_globals.passCount}, Fail: {SW18B_UnitTest_globals.failCount}")
    
    if (UNIT_TEST_SCALING):
        currentTest = "Output Scaling Test"
        if(TEST_SW18AB):
             print(f"Starting SW18AB {currentTest} at {currentTimeString()}")
             SW18B_UnitTest_Scaling.scalingTest()
             print(f"SW18AB {currentTest} Complete at {currentTimeString()}.  Pass: {SW18B_UnitTest_globals.passCount}, Fail: {SW18B_UnitTest_globals.failCount}")
        if(TEST_SW8B):
             print(f"Starting SW8B {currentTest} at {currentTimeString()}")
             SW18B_UnitTest_Scaling.scalingTest(sw=SW18B_UnitTest_globals.SW8B_68, startPin=0, endPin=7)
             print(f"SW8B {currentTest} Complete at {currentTimeString()}.  Pass: {SW18B_UnitTest_globals.passCount}, Fail: {SW18B_UnitTest_globals.failCount}")
    
    if (UNIT_TEST_HSCOUNTER):
        currentTest = "HS Counter Test"
        if(TEST_SW18AB):
             print(f"Starting SW18AB {currentTest} at {currentTimeString()}")
             SW18B_UnitTest_HSCounter.hsCounterTest()
             print(f"SW18AB {currentTest} Complete at {currentTimeString()}.  Pass: {SW18B_UnitTest_globals.passCount}, Fail: {SW18B_UnitTest_globals.failCount}")
    
    if (UNIT_TEST_QUAD_ENC):
        currentTest = "Quadrature Encoder Test"
        if(TEST_SW18AB):
             print(f"Starting SW18AB {currentTest} at {currentTimeString()}")
             SW18B_UnitTest_QuadEnc.QuadEncTest(SW18B_UnitTest_globals.SW18AB_6B)
             print(f"SW18AB {currentTest} Complete at {currentTimeString()}.  Pass: {SW18B_UnitTest_globals.passCount}, Fail: {SW18B_UnitTest_globals.failCount}")
        if(TEST_SW8B):
             print(f"Starting SW8B {currentTest} at {currentTimeString()}")
             SW18B_UnitTest_QuadEnc.QuadEncTest(sw=SW18B_UnitTest_globals.SW8B_68)
             print(f"SW8B {currentTest} Complete at {currentTimeString()}.  Pass: {SW18B_UnitTest_globals.passCount}, Fail: {SW18B_UnitTest_globals.failCount}")    
    
    
    if (UNIT_TEST_FREQUENCY_OUTPUT):
        currentTest = "Frequency Output Test"
        if(TEST_SW18AB):
             print(f"Starting SW18AB {currentTest} at {currentTimeString()}")
             SW18B_UnitTest_FrequencyOutput.frequencyOutputTest(SW18B_UnitTest_globals.SW18AB_6B, 15)
             print(f"SW18AB {currentTest} Complete at {currentTimeString()}.  Pass: {SW18B_UnitTest_globals.passCount}, Fail: {SW18B_UnitTest_globals.failCount}")
        if(TEST_SW8B):
             print(f"Starting SW8B {currentTest} at {currentTimeString()}")
             SW18B_UnitTest_FrequencyOutput.frequencyOutputTest(SW18B_UnitTest_globals.SW8B_68, 4)
             print(f"SW8B {currentTest} Complete at {currentTimeString()}.  Pass: {SW18B_UnitTest_globals.passCount}, Fail: {SW18B_UnitTest_globals.failCount}")
         
    if (UNIT_TEST_WATCHDOG):
            currentTest = "Watchdog Test"
            if(TEST_SW18AB):
                print(f"Starting SW18AB {currentTest} at {currentTimeString()}")
                SW18B_UnitTest_Watchdog.watchdogTest18AB()
                print(f"SW18AB {currentTest} Complete at {currentTimeString()}.  Pass: {SW18B_UnitTest_globals.passCount}, Fail: {SW18B_UnitTest_globals.failCount}")

    if (UNIT_TEST_ECHO):
        currentTest = "Echo Test"
        if(TEST_SW18AB):
             print(f"Starting SW18AB {currentTest} at {currentTimeString()}")
             SW18B_UnitTest_EchoTest.echoTest(SW18B_UnitTest_globals.SW18AB_6B)
             print(f"SW18AB {currentTest} Complete at {currentTimeString()}.  Pass: {SW18B_UnitTest_globals.passCount}, Fail: {SW18B_UnitTest_globals.failCount}")  
        if(TEST_SW8B):
            print(f"Starting SW8B {currentTest} at {currentTimeString()}")
            SW18B_UnitTest_EchoTest.echoTest(SW18B_UnitTest_globals.SW8B_68)
            print(f"SW8B {currentTest} Complete at {currentTimeString()}.  Pass: {SW18B_UnitTest_globals.passCount}, Fail: {SW18B_UnitTest_globals.failCount}")    
    if(UNIT_TEST_INPUT_PROCESSOR):
        currentTest = "Input Processor Test"
        if(TEST_SW18AB):
             print(f"Starting SW18AB {currentTest} at {currentTimeString()}")
             SW18B_UnitTest_ProcessedInput.inputProcessorTest(SW18B_UnitTest_globals.SW18AB_6B, 19)
             print(f"SW18AB {currentTest} Complete at {currentTimeString()}.  Pass: {SW18B_UnitTest_globals.passCount}, Fail: {SW18B_UnitTest_globals.failCount}")
        if(TEST_SW8B):
             print(f"Starting SW8B {currentTest} at {currentTimeString()}")
             SW18B_UnitTest_ProcessedInput.inputProcessorTest(SW18B_UnitTest_globals.SW8B_68, 4)
             print(f"SW8B {currentTest} Complete at {currentTimeString()}.  Pass: {SW18B_UnitTest_globals.passCount}, Fail: {SW18B_UnitTest_globals.failCount}")
     

     
    
    """
    print(f"Starting Analog Input Test at {currentTimeString()}")
    SW18B_UnitTest_Analog.analogInputTest()
    print(f"Analog Input Test Complete at {currentTimeString()}.  Pass: {SW18B_UnitTest_globals.passCount}, Fail: {SW18B_UnitTest_globals.failCount}")
    
    
    print(f"Starting Resistance Input Test at {currentTimeString()}")
    SW18B_UnitTest_Analog.resistanceInputTest()
    print(f"Resistance Input Test Complete at {currentTimeString()}.  Pass: {SW18B_UnitTest_globals.passCount}, Fail: {SW18B_UnitTest_globals.failCount}")
    
    
    print(f"Starting Pulse Timer Test at {currentTimeString()}")
    SW18B_UnitTest_PulseTimer.pulseTimerTest()
    print(f"PulseTimer Test Complete at {currentTimeString()}.  Pass: {SW18B_UnitTest_globals.passCount}, Fail: {SW18B_UnitTest_globals.failCount}")
 

    print(f"Starting SW UART Test at {currentTimeString()}")
    SW18B_UnitTest_UART_SW.uartSWTest()
    print(f"SW UART Test Complete at {currentTimeString()}.  Pass: {SW18B_UnitTest_globals.passCount}, Fail: {SW18B_UnitTest_globals.failCount}")
   
    print(f"Starting HW UART Test at {currentTimeString()}")
    SW18B_UnitTest_UART.uartHWTest()
    print(f"HW UART Test Complete at {currentTimeString()}.  Pass: {SW18B_UnitTest_globals.passCount}, Fail: {SW18B_UnitTest_globals.failCount}")
    
    print(f"Starting PulseOnChange Test at {currentTimeString()}")
    SW18B_UnitTest_PulseOnChange.pulseOnChangeTest18AB()
    print(f"PulseOnChange Test Complete at {currentTimeString()}.  Pass: {SW18B_UnitTest_globals.passCount}, Fail: {SW18B_UnitTest_globals.failCount}")
    
    print(f"Starting ProcessedInput Test at {currentTimeString()}")
    SW18B_UnitTest_ProcessedInput.inputProcessorTest()
    print(f"ProcessedInput Test Complete at {currentTimeString()}.  Pass: {SW18B_UnitTest_globals.passCount}, Fail: {SW18B_UnitTest_globals.failCount}")
    
    print(f"Starting PWM Test at {currentTimeString()}")
    SW18B_UnitTest_globals.resetAll()
    SW18B_UnitTest_PWM.pwmTest()
    print(f"PWM Test Complete at {currentTimeString()}.  Pass: {SW18B_UnitTest_globals.passCount}, Fail: {SW18B_UnitTest_globals.failCount}")
    
    
    print("Starting ECHO Test.  This test takes about 2 minutes")
    SW18B_UnitTest_EchoTest.echoTest()
    print(f"Echo test complete.  Pass: {SW18B_UnitTest_globals.passCount}  Fail {SW18B_UnitTest_globals.failCount}")

    
    print(f"Starting HSClock Test at {currentTimeString()}")
    SW18B_UnitTest_HSClock.hsClockTest()
    print(f"HSClock Test Complete at {currentTimeString()}.  Pass: {SW18B_UnitTest_globals.passCount}, Fail: {SW18B_UnitTest_globals.failCount}")

    print(f"Starting HSCounter Test at {currentTimeString()}")
    SW18B_UnitTest_HSCounter.hsCounterTest()
    print(f"HSCounter Test Complete at {currentTimeString()}.  Pass: {SW18B_UnitTest_globals.passCount}, Fail: {SW18B_UnitTest_globals.failCount}")

    print(f"Starting Debounce Test at {currentTimeString()}")
    SW18B_UnitTest_Debounce.debounceTest()
    print(f"Debounce Test Complete at {currentTimeString()}.  Pass: {SW18B_UnitTest_globals.passCount}, Fail: {SW18B_UnitTest_globals.failCount}")


    print(f"Starting OutputScaling Test at {currentTimeString()}")
    SW18B_UnitTest_Scaling.scalingTest()
    print(f"OutputScaling Test Complete at {currentTimeString()}.  Pass: {SW18B_UnitTest_globals.passCount}, Fail: {SW18B_UnitTest_globals.failCount}")
   
    print(f"Starting Servo Test at {currentTimeString()}")
    SW18B_UnitTest_globals.resetAll()
    SW18B_UnitTest_Servo.servoTest()
    print(f"Servo Test Complete at {currentTimeString()}.  Pass: {SW18B_UnitTest_globals.passCount}, Fail: {SW18B_UnitTest_globals.failCount}")
    
    
    print(f"Starting Frametimer Test at {currentTimeString()}")
    SW18B_UnitTest_FrameTimer.frameTimerTest()
    print(f"Frametimer Test Complete at {currentTimeString()}.  Pass: {SW18B_UnitTest_globals.passCount}, Fail: {SW18B_UnitTest_globals.failCount}")

   
    print(f"Starting QuadEnc Test at {currentTimeString()}")
    SW18B_UnitTest_QuadEnc.QuadEncTest()
    print(f"QuadEnc Test Complete at {currentTimeString()}.  Pass: {SW18B_UnitTest_globals.passCount}, Fail: {SW18B_UnitTest_globals.failCount}")
    

    SW18B_UnitTest_globals.resetAll()
    print("Starting communication error test.  This test takes less than a minute")
    SW18B_UnitTest_CommunicationError.CommunicationErrorTest()
    """

while (True):
    loop()
