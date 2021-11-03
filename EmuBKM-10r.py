import serial
import io

# Sony BKM-10r Serial Protocol



# LIST OF BYTE COMMANDS

# -------BANKS---------

IEN = [0x49, 0x45, 0x4E] # Encoders
ISW = [0x49, 0x53, 0x57] # Switches
ILE = [0x49, 0x4c, 0x45] # Leds
ICC = [0x49, 0x43, 0x43] # ??
IMT = [0x49, 0x4d, 0x54] # ??

#-----Key Presses------

# Format: 0x44 <group> <mask>

SHIFT = [0x44, 0x03, 0x01] # Shift Key
OVERSCAN_16_9 = [0x44, 0x03, 0x02] # Overscan / 16:9
HORIZSYNC_SYNC = [0x44, 0x03, 0x04] # Horizontal Sync View / Sync
VERTSYNC_BLUEONLY = [0x44, 0x03, 0x08] # Vertical Sync View / Blue Only
MONO_RED = [0x44, 0x03, 0x10] # Mono / Red Beam
APT_GREEN = [0x44, 0x04, 0x01] # Aperature / Green Beam
COMB_BLUE = [0x44, 0x04, 0x02] # Comb / Blue Beam
F1_F3 = [0x44, 0x04, 0x04] # F1 Key / F3 Key
F2_F4 = [0x44, 0x04, 0x08] # F2 Key / F4 Key
SAFEAREA_ADDR = [0x44, 0x04, 0x10] # Safe Area / Address

UP = [0x44, 0x02, 0x40] # Up Key
DOWN = [0x44, 0x02, 0x80] # Down Key
MENU = [0x44, 0x02, 0x10] # Menu Key
ENTER = [0x44, 0x02, 0x20] # Enter Key

PHASE_M = [0x44, 0x02, 0x08] # Phase Manual
CHROMA_M = [0x44, 0x02, 0x04] # Chroma Manual
BRIGHT_M = [0x44, 0x02, 0x02] # Bright Manual
CONTRAST_M = [0x44, 0x02, 0x01] # Contrast Manual

NUM0 = [0x44, 0x00, 0x01] # Number 0
NUM1 = [0x44, 0x00, 0x02] # Number 1
NUM2 = [0x44, 0x00, 0x04] # Number 2
NUM3 = [0x44, 0x00, 0x08] # Number 3
NUM4 = [0x44, 0x00, 0x10] # Number 4
NUM5 = [0x44, 0x00, 0x20] # Number 5
NUM6 = [0x44, 0x00, 0x40] # Number 6
NUM7 = [0x44, 0x00, 0x80] # Number 7
NUM8 = [0x44, 0x01, 0x01] # Number 8
NUM9 = [0x44, 0x01, 0x02] # Number 9
DEL = [0x44, 0x01, 0x04] # Delete Key
ENT = [0x44, 0x01, 0x08] # Enter Key

POWER = [0x44, 0x01, 0x10] # Power On/Off
DEGAUSS = [0x44, 0x01, 0x20] # Degauss Button

#-------Encoders-------
PHASE_ENC = [0x44, 0x03, 0x4]
CHROMA_ENC = [0x44, 0x02, 0x4]
BRIGHT_ENC = [0x44, 0x01, 0x04]
CONTRAST_ENC = [0x44, 0x00, 0x4]


print("Sony BKM-10r Emulated Controller")
print("Type 'help' for Info and 'exit' to Quit")

# Writes bytes for each command
def writeCommandBytes(inp_str):
	#---------------------BANKS-----------------------
	if inp_str == "IEN":
		ser.write(bytearray(IEN))
	if inp_str == "ISW":
		ser.write(bytearray(ISW))
	if inp_str == "ILE":
		ser.write(bytearray(ILE))
	if inp_str == "ICC":
		ser.write(bytearray(ICC))
	if inp_str == "IMT":
		ser.write(bytearray(IMT))
	#------------------Key Presses--------------------
	if inp_str == "Shift":
		ser.write(bytearray(SHIFT))
	if inp_str == "Up":
		ser.write(bytearray(UP))
	if inp_str == "Down":
		ser.write(bytearray(DOWN))
	if inp_str == "Menu":
		ser.write(bytearray(MENU))
	if inp_str == "Enter":
		ser.write(bytearray(ENTER))
	if inp_str == "Power":
		ser.write(bytearray(POWER))
		ser.flush()
		ser.write(bytearray(ISW))

	#--------------------Encoders---------------------
	if inp_str == "PhaseInc":
		dif = int(input("Input Wanted Difference:"))
		bytes = [PHASE_ENC[0], PHASE_ENC[1], dif * 4]
		ser.write(bytearray(IEN))
		ser.flush()
		ser.write(bytearray(bytes))
		ser.flush()
		ser.write(bytearray(ISW))
	if inp_str == "ChromaInc":
		dif = int(input("Input Wanted Difference:"))
		bytes = [CHROMA_ENC[0], CHROMA_ENC[1], dif * 4]
		ser.write(bytearray(IEN))
		ser.flush()
		ser.write(bytearray(bytes))
		ser.flush()
		ser.write(bytearray(ISW))
	if inp_str == "BrightInc":
		dif = int(input("Input Wanted Difference:"))
		bytes = [BRIGHT_ENC[0], BRIGHT_ENC[1], dif * 4]
		ser.write(bytearray(IEN))
		ser.flush()
		ser.write(bytearray(bytes))
		ser.flush()
		ser.write(bytearray(ISW))
	if inp_str == "ContrastInc":
		dif = int(input("Input Wanted Difference:"))
		bytes = [CONTRAST_ENC[0], CONTRAST_ENC[1], dif * 4]
		print(bytes)
		ser.write(bytearray(IEN))
		ser.flush()
		ser.write(bytearray(bytes))
		ser.flush()
		ser.write(bytearray(ISW))



# Open Serial Port
ser = serial.Serial()
ser.baudrate = 38400
ser.port = '/dev/ttyUSB0'

# Open Port
ser.open()

#bytearr = bytearray([68, 1, 32])

#print(bytearr)

#ser.write(b'\x49\x53\x57')

#ser.write(bytearray(b'\x44\x01\x10'))

inp = ""

while inp != "exit":
	inp = input()
	writeCommandBytes(inp)
	ser.flush()
	#if ret == 1:
	#	print("Command Successfully Sent")
	#else:
	#	print("Command Failed")
#ser.flush()

#ser.write(bytearray(NUM1))
#ser.write(

#ser.flush()

ser.close()
