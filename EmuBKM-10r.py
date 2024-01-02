import serial
import io
import time

# Sony BKM-10r Serial Protocol
# Link to info: https://pastebin.com/aTUWf33J

# Monitor expects commands in a series of 3 bytes
# Flush after every 3 bytes to ensure each command is accepted

# LIST OF BYTE COMMANDS

# -------BANKS---------
COMMANDS = {
	"IEN":[0x49, 0x45, 0x4E], # Encoders
	"ISW":[0x49, 0x53, 0x57], # Switches
	"ILE":[0x49, 0x4c, 0x45], # Leds
	"ICC":[0x49, 0x43, 0x43], # ??
	"IMT":[0x49, 0x4d, 0x54], # ??
	#-----Key Presses------
	# Format: 0x44 <group> <mask>
	"SHIFT":[0x44, 0x03, 0x01], # Shift Key
	"OVERSCAN_16_9":[0x44, 0x03, 0x02], # Overscan / 16:9
	"HORIZSYNC_SYNC":[0x44, 0x03, 0x04], # Horizontal Sync View / Sync
	"VERTSYNC_BLUEONLY":[0x44, 0x03, 0x08], # Vertical Sync View / Blue Only
	"MONO_RED":[0x44, 0x03, 0x10], # Mono / Red Beam
	"APT_GREEN":[0x44, 0x04, 0x01], # Aperature / Green Beam
	"COMB_BLUE":[0x44, 0x04, 0x02], # Comb / Blue Beam
	"F1_F3":[0x44, 0x04, 0x04], # F1 Key / F3 Key
	"F2_F4":[0x44, 0x04, 0x08], # F2 Key / F4 Key
	"SAFEAREA_ADDR":[0x44, 0x04, 0x10], # Safe Area / Address

	"UP":[0x44, 0x02, 0x40], # Up Key
	"DOWN":[0x44, 0x02, 0x80], # Down Key
	"MENU":[0x44, 0x02, 0x10], # Menu Key
	"ENTER":[0x44, 0x02, 0x20], # Enter Key

	"PHASE_M":[0x44, 0x02, 0x08], # Phase Manual
	"CHROMA_M":[0x44, 0x02, 0x04], # Chroma Manual
	"BRIGHT_M":[0x44, 0x02, 0x02], # Bright Manual
	"CONTRAST_M":[0x44, 0x02, 0x01], # Contrast Manual

	"NUM0":[0x44, 0x00, 0x01], # Number 0
	"NUM1":[0x44, 0x00, 0x02], # Number 1
	"NUM2":[0x44, 0x00, 0x04], # Number 2
	"NUM3":[0x44, 0x00, 0x08], # Number 3
	"NUM4":[0x44, 0x00, 0x10], # Number 4
	"NUM5":[0x44, 0x00, 0x20], # Number 5
	"NUM6":[0x44, 0x00, 0x40], # Number 6
	"NUM7":[0x44, 0x00, 0x80], # Number 7
	"NUM8":[0x44, 0x01, 0x01], # Number 8
	"NUM9":[0x44, 0x01, 0x02], # Number 9
	"DEL":[0x44, 0x01, 0x04], # Delete Key
	"ENT":[0x44, 0x01, 0x08], # Enter Key

	"POWER":[0x44, 0x01, 0x10], # Power On/Off
	"DEGAUSS":[0x44, 0x01, 0x20], # Degauss Button

	#-------Encoders-------
	"PHASE_ENC":[0x44, 0x03, 0x4], # Phase Knob
	"CHROMA_ENC":[0x44, 0x02, 0x4], # Chroma Knob
	"BRIGHT_ENC":[0x44, 0x01, 0x04], # Brightness Knob
	"CONTRAST_ENC":[0x44, 0x00, 0x4], # Contrast Knob
}

HUMAN_READABLE_COMMANDS = {
	"IEN":["COMMAND", "IEN"],
	"ISW":["COMMAND", "ISW"],
	"ILE":["COMMAND", "ILE"],
	"ICC":["COMMAND", "ICC"],
	"IMT":["COMMAND", "IMT"],
	"Shift":["COMMAND", "SHIFT"],
	"Overscan":["COMMAND", "OVERSCAN_16_9"],
	"16:9":["COMMAND", "SHIFT", "OVERSCAN_16_9", "SHIFT"],
	"HorizSync":["COMMAND", "HORIZSYNC_SYNC"],
	"Sync":["COMMAND", "SHIFT", "HORIZSYNC_SYNC", "SHIFT"],
	"VertSync":["COMMAND", "VERTSYNC_BLUEONLY"],
	"BlueOnly":["COMMAND", "SHIFT", "VERTSYNC_BLUEONLY", "SHIFT"],
	"Mono":["COMMAND", "MONO_RED"],
	"Red":["COMMAND", "SHIFT", "MONO_RED", "SHIFT"],
	"Aperature":["COMMAND", "APT_GREEN"],
	"Green":["COMMAND", "SHIFT", "APT_GREEN", "SHIFT"],
	"Comb":["COMMAND", "COMB_BLUE"],
	"Blue":["COMMAND", "SHIFT", "COMB_BLUE", "SHIFT"],
	"F1":["COMMAND", "F1_F3"],
	"F3":["COMMAND", "SHIFT", "F1_F3", "SHIFT"],
	"F2":["COMMAND", "F2_F4"],
	"F4":["COMMAND", "SHIFT", "F2_F4", "SHIFT"],
	"SafeArea":["COMMAND", "SAFEAREA_ADDR"],
	"Address":["COMMAND", "SHIFT", "SAFEAREA_ADDR", "SHIFT"],
	"Up":["COMMAND", "UP"],
	"Down":["COMMAND", "DOWN"],
	"Enter":["COMMAND", "ENTER"],
	"Menu":["COMMAND", "ISW", "MENU", "ISW"],
	"Num0":["COMMAND", "NUM0"],
	"Num1":["COMMAND", "NUM1"],
	"Num2":["COMMAND", "NUM2"],
	"Num3":["COMMAND", "NUM3"],
	"Num4":["COMMAND", "NUM4"],
	"Num5":["COMMAND", "NUM5"],
	"Num6":["COMMAND", "NUM6"],
	"Num7":["COMMAND", "NUM7"],
	"Num8":["COMMAND", "NUM8"],
	"Num9":["COMMAND", "NUM9"],
	"Power":["COMMAND", "ISW", "POWER", "ISW"],
	"Degauss":["COMMAND", "DEGAUSS"],
	"PhaseInc":["ENCODER-SUB", "PHASE_ENC"],
	"ChromaInc":["ENCODER-SUB", "CHROMA_ENC"],
	"BrightInc":["ENCODER-SUB", "PHASE_ENC"],
	"ContrastInc":["ENCODER-SUB", "PHASE_ENC"],
	"UpdateChannelName":["SCRIPT", "CHANNEL_NAME"]
}

class EmuBKM10r:
	ser = None
	def __init__(self, serial_port, baudrate = 38400):
		# Open Serial Port
		self.ser = serial.Serial()
		self.ser.baudrate = baudrate
		self.ser.port = serial_port

	def connect(self):
		try:
			self.ser.open()
		except:
			print ("Error connecting to Monitor")
	
	def close(self):
		"""Closes serial connection to Monitor"""
		self.ser.close()
	
	def flush(self):
		"""Flushes all current serial data"""
		self.ser.flush()

	def writeCommand(self, command, skipISW=False):
		""" Sends correct byte array for corresponding command """
		if skipISW:
			self.ser.write(bytearray(COMMANDS["ISW"]))
		self.ser.write(bytearray(COMMANDS[command]))
		self.ser.flush()
		if command == "MENU" or command == "POWER":	
			time.sleep(0.50)
		elif command == "SHIFT":
			self.ser.write(bytearray(COMMANDS["ISW"]))
			time.sleep(0.2)
			self.ser.flush()
			self.ser.write(bytearray(COMMANDS["ISW"]))
		else:
			time.sleep(0.025)
		#print(command)

	def repeatCommand(self, command, reps, skipISW=False):
		""" Repeats COMMANDS N times with a 0.05 delay between """
		for i in range(reps):
			self.writeCommand(command, skipISW)

	#--------------------Custom Functions---------------------
	# These are made using the byte commands implemented above
	# These are NOT standard to the BKM series of controllers


	# Function to enter text whenever applicable
	def writeText(self):
		dif = input("Input Text: ")
		for s in dif:
			dir = 1
			charstr = "abcdefghijklmnopqrstuvwxyz0123456789():;.-+/& "
			n = charstr.index(s.lower()) + 1
			
			if n > len(charstr) // 2:
				dir = -1
				n = len(charstr) - (n - 1)
			print(n)
			for i in range(n):
				if dir == 1:
					self.writeCommand("UP")
				else:
					self.writeCommand("DOWN")
			self.writeCommand("ENTER")
			time.sleep(.1)
			self.ser.flush()
		self.writeCommand("ENTER")
		self.ser.flush()

	def updateChannelName(self):
		# Call for Menu
		self.writeCommand("MENU")
		time.sleep(0.1)

		# Select Channel Input
		# Move to Name function
		self.repeatCommand("DOWN", 2, skipISW=True)
		self.writeCommand("ENTER")
		time.sleep(0.1)

		# Get channel to change name
		num = int(input("Channel Number to Update: "))
		channel_num = "NUM" + str(num)

		self.writeCommand(channel_num)
		time.sleep(3)

		# Move to Name function
		self.repeatCommand("DOWN", 6, skipISW=True)

		self.writeCommand("ENTER")
		time.sleep(0.12)

		self.writeCommand("UP")

		self.writeCommand("ENTER")
		time.sleep(0.1)

		self.writeText()

	# Writes bytes for each command
	def sendCommand(self, inp_str):
		try:
			command_list = HUMAN_READABLE_COMMANDS[inp_str].copy()
		except:
			print("Not a Valid Command")
			return 0

		command_type = command_list.pop(0)
		if command_type == "COMMAND":
			for command in command_list:
				self.writeCommand(command)
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


		#if inp_str == "PhaseInc":
		#	dif = int(input("Input Wanted Difference:")) # Ask for user input
		#	bytes = [PHASE_ENC[0], PHASE_ENC[1], dif * 4] # Create array with correct format
		#	ser.write(bytearray(IEN)) # Switch to encoder bank
		#	ser.flush()
		#	ser.write(bytearray(bytes)) # Write byte array
		#	ser.flush()
		#	ser.write(bytearray(ISW)) # Switch back to key bank
		#	return 1
		if command_type == "SCRIPT":
			if command_list[0] == "CHANNEL_NAME":
				self.updateChannelName()
				return 1

		# If the command does not fit any currently supported command, return 0
		return 0


if __name__ == "__main__":
	print("Sony BKM-10r Emulated Controller")
	print("Type 'help' for Info and 'exit' to Quit")

	#ser.port = input("Enter name of device (ex. '/dev/ttyUSB0' for linux or 'COM3' for windows): ")

	bkm = EmuBKM10r('COM9')

	bkm.connect() # opens serial port and connects to monitor

	inp = ""

	while inp != "exit":
		inp = input(">") # Take user Input
		if inp == "help":
			# Create help command response
			break
		if inp != "exit":
			ret = bkm.sendCommand(inp) # Parse Input and send the proper write() commands
			if ret == 1:
				bkm.flush() # Need one final Flush to send last write()
				print("Command Successfully Sent")
			else:
				print("Command Failed")
		#print(ser.read(3))
	bkm.close()
