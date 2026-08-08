"""


"""
import SerialWombat
from ArduinoFunctions import delay
from ArduinoFunctions import millis

SW_ADDRESS = 0x6B  #Change the address to match your configuration

import SerialWombat_interface
sw = SerialWombat_interface.SerialWombatChipInstance(SW_ADDRESS)


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

hexfile = open(hexfilelist[0])
addressBase = 0
listAddress = 0


def parseline(l):
  global addressBase
  data = []
  x = re.match(r":(\w\w)(\w\w\w\w)(\w\w)(\w*)(\w\w)",l)
  if (x.group(3) == "04"):
      addressBase = 65536 * int(x.group(4),16)
      #print(f"New Base Address: {hex(addressBase)}")
      return ([addressBase,[]])
  if (x.group(3) == "00"):
    a = addressBase + int(x.group(2),16)
    d = [x.group(4)[i:i+2] for i in range(0, len(x.group(4)), 2)] #split group 4 into chunks of 2 chars
   
    for res in d:
      data.append(int(res,16))
    return ([a,data])


def rowIsErased(data):
  # An erased PIC24 program word is 0x00FFFFFF, represented in the
  # 512-byte row buffer as 0xFF, 0xFF, 0xFF, 0x00.
  if (len(data) != 512):
    return False
  for i in range(0, 512, 4):
    if (data[i] != 0xFF or data[i + 1] != 0xFF or
        data[i + 2] != 0xFF or data[i + 3] != 0x00):
      return False
  return True


# Initialize communications before checking whether the installed firmware is current.
sw.begin(False)

if (sw.isLatestFirmware()):
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
    delay(200);
print()

# Erase the final/commit page first.  This intentionally invalidates the
# existing application before the remainder of the update begins.
sw.eraseFlashPage(0x1F800 * 2)
delay(50)

# Erase the complete application range, matching the Arduino updater.
for address in range(0x4000 * 2, (0x1F800 * 2) + 1, 0x800 * 2):
    print(f"Erasing Block address: 0x{address:08x}")
    sw.eraseFlashPage(address); # Datasheet worst case is 40.
    delay(50);


address = 0x4000 * 2;  # Bytes
pageaddress = address;
tableindex = 0;
rlecount = 0;
pagebytecount = 0;
hexaddr = 0
ldata = []


# Write all application rows except the final 512-byte commit row at 0x3F000.
while (address < 0x1F800 * 2):
  data = []

  while (len(data) < 512):
    if (hexaddr >= address and hexaddr < address + 512):
      data = data + ldata
    hexaddr, ldata = parseline(hexfile.readline())

  if (rowIsErased(data)):
    print(f"Skipping erased row 0x{pageaddress:08x}  / 0x3FE00")
  else:
    print(f"Writing Addr: {hex(hexaddr)}             0x{(pageaddress // 256) :03x}  / 0x3FE");
    #print (data)
    sw.writeUserBuffer(0x00,data,512);
    sw.writeFlashRow(pageaddress);
    delay(4);# Datasheet worst case is 1.5
  address = address + 512
  pageaddress = address;


# Load, but do not yet write, the final 512-byte row beginning at 0x3F000.
# This row contains the expected CRC and is only committed after CRC verification.
data = []
while (len(data) < 512):
  if (hexaddr >= address and hexaddr < address + 512):
    data = data + ldata
  hexaddr, ldata = parseline(hexfile.readline())


print("Appload complete.  Calculating CRC...");

expectedCRC = 0
calculatedCrc = 1

# Calculate CRC on the Serial Wombat chip, matching the Arduino updater.
tx = [0xA4, 2, 0x55, 0x55, 0x55, 0x55, 0x55, 0x55]
result = sw.sendPacketNoResponse(tx)

delay(15000)

tx3 = [0xA4, 3, 0x55, 0x55, 0x55, 0x55, 0x55, 0x55]
calculatedCrc = 0
while (calculatedCrc == 0):
    result, rx = sw.sendPacket(tx3)
    calculatedCrc = rx[2] + rx[3] * 256

print("Calculated CRC: ")
print(calculatedCrc)

expectedCRC = data[8] + data[9] * 256
print("Expected CRC: ")
print(expectedCRC)
print()

# Only write the final commit row if the downloaded application CRC is correct.
if (expectedCRC == calculatedCrc):
    if (rowIsErased(data)):
        print(f"Skipping erased row 0x{pageaddress:08x}  / 0x3FE00")
    else:
        print(f"Writing 0x{pageaddress:08x}  / 0x3FE00");
        sw.writeUserBuffer(0x00,data,512);
        sw.writeFlashRow(pageaddress);
        delay(4);# Datasheet worst case is 1.5
    print("Download success")
else:
    print("Download failed")

while (True):
    delay(10)
