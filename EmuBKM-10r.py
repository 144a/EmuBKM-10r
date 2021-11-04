import serial
import io

# Sony BKM-10r Serial Protocol
# Link to info: https://pastebin.com/aTUWf33J

# Monitor expects commands in a series of 3 bytes
# Flush after every 3 bytes to ensure each command is accepted

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
PHASE_ENC = [0x44, 0x03, 0x4] # Phase Knob
CHROMA_ENC = [0x44, 0x02, 0x4] # Chroma Knob
BRIGHT_ENC = [0x44, 0x01, 0x04] # Brightness Knob
CONTRAST_ENC = [0x44, 0x00, 0x4] # Contrast Knob


print("Sony BKM-10r Emulated Controller")
print("Type 'help' for Info and 'exit' to Quit")

# Writes bytes for each command
def writeCommandBytes(inp_str):
	#---------------------BANKS-----------------------
	if inp_str == "IEN":
		ser.write(bytearray(IEN))
		return 1
	if inp_str == "ISW":
		ser.write(bytearray(ISW))
		return 1
	if inp_str == "ILE":
		ser.write(bytearray(ILE))
		return 1
	if inp_str == "ICC":
		ser.write(bytearray(ICC))
		return 1
	if inp_str == "IMT":
		ser.write(bytearray(IMT))
		return 1
	#------------------Key Presses--------------------
	# Not Particularly useful, all commands are seperated
	if inp_str == "Shift":
		ser.write(bytearray(SHIFT))
		return 1

	# Shift-based Commands (All keys that involve the shift key)
	if inp_str == "Overscan":
		ser.write(bytearray(OVERSCAN_16_9))
		return 1
	if inp_str == "16:9":
		ser.write(bytearray(SHIFT))
		ser.flush()
		ser.write(bytearray(OVERSCAN_16_9))
		return 1
	if inp_str == "HorizSync":
		ser.write(bytearray(HORIZSYNC_SYNC))
		return 1
	if inp_str == "Sync":
		ser.write(bytearray(SHIFT))
		ser.flush()
		ser.write(bytearray(HORIZSYNC_SYNC))
		return 1
	if inp_str == "VertSync":
		ser.write(bytearray(VERTSYNC_BLUEONLY))
		return 1
	if inp_str == "BlueOnly":
		ser.write(bytearray(SHIFT))
		ser.flush()
		ser.write(bytearray(VERTSYNC_BLUEONLY))
		return 1
	if inp_str == "Mono":
		ser.write(bytearray(MONO_RED))
		return 1
	if inp_str == "Red":
		ser.write(bytearray(SHIFT))
		ser.flush()
		ser.write(bytearray(MONO_RED))
		return 1
	if inp_str == "Aperature":
		ser.write(bytearray(APT_GREEN))
		return 1
	if inp_str == "Green":
		ser.write(bytearray(SHIFT))
		ser.flush()
		ser.write(bytearray(APT_GREEN))
		return 1
	if inp_str == "Comb":
		ser.write(bytearray(COMB_BLUE))
		return 1
	if inp_str == "Blue":
		ser.write(bytearray(SHIFT))
		ser.flush()
		ser.write(bytearray(COMB_BLUE))
		return 1
	if inp_str == "F1":
		ser.write(bytearray(F1_F3))
		return 1
	if inp_str == "F3":
		ser.write(bytearray(SHIFT))
		ser.flush()
		ser.write(bytearray(F1_F3))
		return 1
	if inp_str == "F2":
		ser.write(bytearray(F2_F4))
		return 1
	if inp_str == "F4":
		ser.write(bytearray(SHIFT))
		ser.flush()
		ser.write(bytearray(F2_F4))
		return 1
	if inp_str == "SafeArea":
		ser.write(bytearray(SAFEAREA_ADDR))
		return 1
	if inp_str == "Address":
		ser.write(bytearray(SHIFT))
		ser.flush()
		ser.write(bytearray(SAFEAREA_ADDR))
		return 1

	# Menu Commands
	if inp_str == "Up":
		ser.write(bytearray(UP))
		return 1
	if inp_str == "Down":
		ser.write(bytearray(DOWN))
		return 1
	if inp_str == "Menu":
		ser.write(bytearray(MENU))
		return 1
	if inp_str == "Enter":
		ser.write(bytearray(ENTER))
		return 1

	# Number Commands (used in menus and for selecting channels)
	if inp_str == "Num0":
		ser.write(bytearray(NUM0))
		return 1
	if inp_str == "Num1":
		ser.write(bytearray(NUM1))
		return 1
	if inp_str == "Num2":
		ser.write(bytearray(NUM2))
		return 1
	if inp_str == "Num3":
		ser.write(bytearray(NUM3))
		return 1
	if inp_str == "Num4":
		ser.write(bytearray(NUM4))
		return 1
	if inp_str == "Num5":
		ser.write(bytearray(NUM5))
		return 1
	if inp_str == "Num6":
		ser.write(bytearray(NUM6))
		return 1
	if inp_str == "Num7":
		ser.write(bytearray(NUM7))
		return 1
	if inp_str == "Num8":
		ser.write(bytearray(NUM8))
		return 1
	if inp_str == "Num9":
		ser.write(bytearray(NUM9))
		return 1

	# Power and Degauss Commands
	if inp_str == "Power":
		ser.write(bytearray(POWER))
		ser.flush()
		# Switch Bank to ensure all keys can be pressed
		ser.write(bytearray(ISW))
		return 1

	if inp_str == "Degauss":
		ser.write(bytearray(DEGAUSS))
		return 1


	#--------------------Encoders---------------------

	# Encoder input requires switching banks to IEN
	# After, it accepts an input in the form of
	# <0x44, 'encoder id', 'number of ticks'>


	# When calling an encoder command, it will prompt
	# for user input. The number is a two's compliment byte,
	# and as such you can turn the knob to the right (positive input)
	# by using a number less than 128, while you can turn the knob
	# to the left by using a number greater than 128 but less than 256


	if inp_str == "PhaseInc":
		dif = int(input("Input Wanted Difference:")) # Ask for user input
		bytes = [PHASE_ENC[0], PHASE_ENC[1], dif * 4] # Create array with correct format
		ser.write(bytearray(IEN)) # Switch to encoder bank
		ser.flush()
		ser.write(bytearray(bytes)) # Write byte array
		ser.flush()
		ser.write(bytearray(ISW)) # Switch back to key bank
		return 1
	if inp_str == "ChromaInc":
		dif = int(input("Input Wanted Difference:"))
		bytes = [CHROMA_ENC[0], CHROMA_ENC[1], dif * 4]
		ser.write(bytearray(IEN))
		ser.flush()
		ser.write(bytearray(bytes))
		ser.flush()
		ser.write(bytearray(ISW))
		return 1
	if inp_str == "BrightInc":
		dif = int(input("Input Wanted Difference:"))
		bytes = [BRIGHT_ENC[0], BRIGHT_ENC[1], dif * 4]
		ser.write(bytearray(IEN))
		ser.flush()
		ser.write(bytearray(bytes))
		ser.flush()
		ser.write(bytearray(ISW))
		return 1
	if inp_str == "ContrastInc":
		dif = int(input("Input Wanted Difference:"))
		bytes = [CONTRAST_ENC[0], CONTRAST_ENC[1], dif * 4]
		print(bytes)
		ser.write(bytearray(IEN))
		ser.flush()
		ser.write(bytearray(bytes))
		ser.flush()
		ser.write(bytearray(ISW))
		return 1

	# If the command does not fit any currently supported command, return 0
	return 0


# Open Serial Port
ser = serial.Serial()
ser.baudrate = 38400

ser.port = input("Enter name of device (ex. '/dev/ttyUSB0' for linux or 'COM3' for windows): ")

#'/dev/ttyUSB0'

# Open Port
ser.open()

inp = ""

while inp != "exit":
	inp = input(">") # Take user Input
	if inp == "help":
		# Create help command response
	if inp != "exit":
		ret = writeCommandBytes(inp) # Parse Input and send the proper write() commands
		if ret == 1:
			ser.flush() # Need one final Flush to send last write()
			print("Command Successfully Sent")
		else:
			print("Command Failed")
ser.close()
