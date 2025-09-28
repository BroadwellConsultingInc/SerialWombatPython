"""
This file is used to update the Serial Wombat 18AB chip to the lastest firmware,
 version 2.1.4 over I2C or UART.  It will connect to a single Serial Wombat 18AB chip at the address
 specified by the I2C_ADDRESS below.  The sketch contains the entire 
 firmware image as a constant.   
 
 Open a serial terminal at 115200 to monitor progress.
 
 Hardware setup is simple.  Connect the SDA and SCL lines, including external pull up
 resistors, and power both boards.   Ensure the Serial Wombat chip has all support
 capacitors and resistors attached, and that the address pin selects the desired
 address, and set that Address in this sketch by changing I2C_ADDRESS below, then
 compile and download this sketch.
 
 This sketch requires a lot of flash space because it contains the entire firmware
 image.  For this reason it cannot be loaded into small-memory boards such as
 the Arduino Uno.  Additionally, storing or accessing large flash arrays often requires
 board specific compiler instructions or functions.  
 
 --- THIS SKETCH HAS ONLY BEEN TESTED ON THE ESP8266, ESP32 and SEEDUINO XIAO AT THIS TIME ---
 
 Other large flash micros will be supported in the future.
 
 The download function requires about 30 seconds.  A CRC is calculated
 on the Serial Wombat Chip at the end of the download and verified against
 a CRC stored in the image.  These should match
 
 A video tutorial on this example is available at:
https://youtu.be/q7ls-lMaL80
"""
https://github.com/ryansturmer/hexfile


import SerialWombat
from ArduinoFunctions import delay

#Comment these lines in if you're connecting directly to a Serial Wombat Chip's UART through cPython serial Module
#Change the paramter of SerialWombatChip_cpy_serial to match the name of your Serial port
#import SerialWombat_cpy_serial
#sw = SerialWombat_cpy_serial.SerialWombatChip_cpy_serial("COM25")


#Comment these lines in if you're connecting to a Serial Wombat Chip's I2C port using Micropython's I2C interface
#Change the values for sclPin, sdaPin, and swI2Caddress to match your configuration
import machine
import SerialWombat_mp_i2c
sclPin = 22
sdaPin = 21
swI2Caddress = 0x6B
i2c = machine.I2C(0,
            scl=machine.Pin(sclPin),
            sda=machine.Pin(sdaPin),
            freq=100000,timeout = 50000)
sw = SerialWombat_mp_i2c.SerialWombatChip_mp_i2c(i2c,swI2Caddress)
sw.adress = 0x6B

#Comment these lines in if you're connecting to a Serial Wombat Chip's UART port using Micropython's UART interface
#Change the values for UARTnum, txPin, and rxPin to match your configuration
#import machine
#import SerialWombat_mp_UART
#txPin = 12
#rxPin = 14
#UARTnum = 2
#uart = machine.UART(UARTnum, baudrate=115200, tx=txPin, rx=rxPin)
#sw = SerialWombat_mp_UART.SerialWombatChipUART(uart)


#Interface independent code starts here:
import SerialWombatTM1637
DISPLAY_CLK_PIN  = 1 # <<<<<<<<<   Set this to the Serial Wombat pin connected to your Display Clock Pin
DISPLAY_DIN_PIN  = 2  # <<<<<<<<<   Set this to the Serial Wombat pin connected to your Display Data Pin
myDisplay = SerialWombatTM1637.SerialWombatTM1637(sw)


def setup():
  # put your setup code here, to run once:
  sw.begin()
  #wombatFinder();


while(Serial.available()):
    char t= Serial.read();
    if (sw.isLatestFirmware()):
            print("Firmware is already the latest version.  Update?  Send 'Y' to update");
            yesno = input();
            if (i != 'Y'):
                print("Non 'Y' character received.  Going into infinite loop.  Reset to try again");
                while(1):
                    pass()
  print("Jumping to boot");
  sw.hardwareReset();
  for i in range(0,50):
      sw.jumpToBoot();
      delay(20);

  #WombatFinder();

  sw.begin(False)
  address = 0

  print("Connecting to Serial Wombat chip");
  found = False
  while (!found):
    found = sw.queryVersion()
    print('.');
    delay(200);
  print()
  for address in range(0x4000*2,(0x1F800-0x4000) * 2, 0x800*2):
    print(f"Erasing Block address: 0x{address:08x}")
    sw.eraseFlashPage(address); # Datasheet worst case is 40.
    delay(50);


  address = 0x4000 * 2;  # Bytes
  pageaddress = address;
  tableindex = 0;
  rlecount = 0;
  pagebytecount = 0;
  data;

 
  while (address < 0x20000 * 2):
      if (rlecount == 0):
          data = appImage[tableindex] & 0xFFFFFF;
          rlecount = (appImage[tableindex] >>24) + 1;

          ++tableindex;
          #char str[200];
          #sprintf(str,"Processing rle entry 0x%X count: %X  address: 0x%X",data,rlecount, address);
          #print(str);
    --rlecount;
    pagebuffer[pagebytecount] = data & 0xFF;
    ++pagebytecount;
    pagebuffer[pagebytecount] = (data >>8) & 0xFF;
    ++pagebytecount;
    pagebuffer[pagebytecount] = (data >>16) & 0xFF;
    ++pagebytecount;
    pagebuffer[pagebytecount] = 0;
    ++pagebytecount;
    address += 4;
    if (pagebytecount == 512):
      print(f"Writing 0x{pageaddress:08x}  / 0x3FE00");
 
      pagebytecount = 0;
      sw.writeUserBuffer(0x00,pagebuffer,512);
      sw.writeFlashRow(pageaddress);
      pageaddress = address;
      delay(4);// Datasheet worst case is 1.5
    
 
  print("Bootload complete.  Calculating CRC...");

  #Calculate CRC
  uint8_t tx[8] = {0xA4,2,0x55,0x55,0x55,0x55,0x55,0x55};
  uint8_t rx[8];
  sw.sendPacket(tx,rx);

    delay(15000);
    uint8_t tx3[8] = {0xA4,3,0x55,0x55,0x55,0x55,0x55,0x55};

  sw.sendPacket(tx3,rx);
    print("Calculated CRC: ");
    print(rx[2] + rx[3] * 256);
    print("Expected CRC: ");
    print(rx[4] + rx[5] * 256);
    print();
    

  
def loop():
  pass

setup()
while(True):
    loop()

  print("Jumping to boot");
  sw.hardwareReset();
  for i in range(0,50):
      sw.jumpToBoot();
      delay(20);

  #WombatFinder();

  sw.begin(False)
  address = 0

  print("Connecting to Serial Wombat chip");
  found = False
  while (!found):
    found = sw.queryVersion()
    print('.');
    delay(200);
  print()
  for address in range(0x4000*2,(0x1F800-0x4000) * 2, 0x800*2):
    print(f"Erasing Block address: 0x{address:08x}")
    sw.eraseFlashPage(address); # Datasheet worst case is 40.
    delay(50);


  address = 0x4000 * 2;  # Bytes
  pageaddress = address;
  tableindex = 0;
  rlecount = 0;
  pagebytecount = 0;
  data;

 
  while (address < 0x20000 * 2):
      if (rlecount == 0):
          data = appImage[tableindex] & 0xFFFFFF;
          rlecount = (appImage[tableindex] >>24) + 1;

          ++tableindex;
          #char str[200];
          #sprintf(str,"Processing rle entry 0x%X count: %X  address: 0x%X",data,rlecount, address);
          #print(str);
    --rlecount;
    pagebuffer[pagebytecount] = data & 0xFF;
    ++pagebytecount;
    pagebuffer[pagebytecount] = (data >>8) & 0xFF;
    ++pagebytecount;
    pagebuffer[pagebytecount] = (data >>16) & 0xFF;
    ++pagebytecount;
    pagebuffer[pagebytecount] = 0;
    ++pagebytecount;
    address += 4;
    if (pagebytecount == 512):
      print(f"Writing 0x{pageaddress:08x}  / 0x3FE00");
 
      pagebytecount = 0;
      sw.writeUserBuffer(0x00,pagebuffer,512);
      sw.writeFlashRow(pageaddress);
      pageaddress = address;
      delay(4);// Datasheet worst case is 1.5
    
 
  print("Bootload complete.  Calculating CRC...");

  #Calculate CRC
  uint8_t tx[8] = {0xA4,2,0x55,0x55,0x55,0x55,0x55,0x55};
  uint8_t rx[8];
  sw.sendPacket(tx,rx);

    delay(15000);
    uint8_t tx3[8] = {0xA4,3,0x55,0x55,0x55,0x55,0x55,0x55};

  sw.sendPacket(tx3,rx);
    print("Calculated CRC: ");
    print(rx[2] + rx[3] * 256);
    print("Expected CRC: ");
    print(rx[4] + rx[5] * 256);
    print();
    


