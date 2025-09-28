"""
This file allows downloading of a new hex file to a Serial Wombat 8B
chip over i2c.   The Chip must previously have been loaded with
the SW8B bootloader using a CH Link-E programmer or similar.

The user must set the proper I2C address to target the proper chip.

This file requires the ArduinoFunctions.py , SerialWombat.py files to
be available.   The script will search for the first .hex file it finds
and try to download it.  Only one .hex file should be in the current directory
at a time.

When the script runs it will ask the user to press Y and press enter
in the terminal to confirm intent to bootload.

If the script hangs at Connecting to Serial Wombat chip

then the chip was not found.  Check your connections, verify I2C
address, and I2C pull up resistors.

The download process can be monitored using a Saleae Logic Analyzer
or generic along with Saleae Logic software and Serial Wombat protocol
analzyer plug in.

A demonstration video of this process can be found here

"""
import SerialWombat
from ArduinoFunctions import delay
from ArduinoFunctions import millis


#Comment these lines in if you're connecting to a Serial Wombat Chip's I2C port using Micropython's I2C interface
#Change the values for sclPin, sdaPin, and swI2Caddress to match your configuration
import machine
import SerialWombat_mp_i2c
sclPin = 17  # Pins assume PICO on I2C0
sdaPin = 16
swI2Caddress = 0x6A
i2c = machine.I2C(0,
            scl=machine.Pin(sclPin),
            sda=machine.Pin(sdaPin),
            freq=100000,timeout = 50000)
sw = SerialWombat_mp_i2c.SerialWombatChip_mp_i2c(i2c,swI2Caddress)



#Interface independent code starts here:

import re

import os

def glob(root, wildcard):
  n = wildcard.find("*")
  lst = []
  for file in os.listdir(root):
      if n < 0:
        if file == wildcard:
          lst.append(file)
      elif file.startswith(wildcard[:n]) and file.endswith(wildcard[n+1:]):
        lst.append(file)
  return lst


hexfilelist =  glob(".","*.hex")

if (len(hexfilelist) == 0):
  print("No Hex file found")
  quit()
  


print(f"Bootloading {hexfilelist[0]}")
print("Parsing file takes a few seconds...")
hexfile = open(hexfilelist[0])
addressBase = 0
listAddress = 0


def parseline(l):
  global addressBase
  data = []
  x = re.match(r":(\w\w)(\w\w\w\w)(\w\w)(\w*)(\w\w)",l)
  if not x:
      return([-1,[]]) #  No match
  if (x.group(3) == "04"):
      addressBase = 65536 * int(x.group(4),16)
      return ([addressBase,[]])
  if (x.group(3) == "00"):
    a = addressBase + int(x.group(2),16)
    d = [x.group(4)[i:i+2] for i in range(0, len(x.group(4)), 2)] #split group 4 into chunks of 2 chars
   
    for res in d:
      data.append(int(res,16))
    return ([a,data])
  return([-1,[]])


 
mem = [0xFF] * 16384

l = hexfile.readline()

while (l):
    
    hexaddr, ldata = parseline(l)
    if  hexaddr < 0:
        l = hexfile.readline()
        continue
    offset = 0
    for x in ldata:
        mem[hexaddr + offset] = ldata[offset]
        offset = offset + 1
    l = hexfile.readline()
        
#Set magic values to indicate complete bootload
mem[0x3FFC] = 0x11
mem[0x3FFD] = 0x01
mem[0x3FFE] = 0x25
mem[0x3FFF] = 0x20
sw.begin()
if (True):#sw.isLatestFirmware()):
    print("Firmware is already the latest version.  Update?  Send capital 'Y' to update");
    yesno = input();
    if (yesno != 'Y'):
        print("Non 'Y' character received.  Going into infinite loop.  Reset to try again");
        while(True):
            pass

    print("Jumping to boot");
    sw.hardwareReset();
    for i in range(0,50):
        print("boot");
        sw.jumpToBoot();
        delay(20);

  #WombatFinder();

    sw.begin(False)
    address = 0

    print("Connecting to Serial Wombat chip");
    found = False
    while (not found):
        found = sw.queryVersion()
    print('.');
    if (sw.inBoot):
        print("In Boot Mode.")
    print(f"Found.  Version {chr(sw.fwVersion[0])}.{chr(sw.fwVersion[1])}.{chr(sw.fwVersion[2])}")
    #delay(200);
    print()
    print("Erasing Flash...")
    sw.eraseFlashPage(0)
    delay(5000);

    pageaddress = 0
 

    while (pageaddress < 0x4000):
      data = [0xFF] * 64
      for i in range(0,64):
        data[i] = mem[i + pageaddress]
      print(f"Writing 0x{pageaddress:04x}  / 0x4000");
      sw.writeUserBuffer(0x00,data,64);
      sw.writeFlashRow(pageaddress + 0x08000000);
      
      data = []
      pageaddress = pageaddress + 64
              

    print("Bootload complete.  Calculating CRC...");

       
    print("Setting Jump To App Flag")
    bootflag = [164,4,0,0,0,0,0,0]
    sw.sendPacket(bootflag)
    
    print("Resetting")
    sw.hardwareReset();
    print();



