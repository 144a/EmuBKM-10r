import serial
import io
import time
import argparse

# Sony BKM-10r Serial Protocol
# Link to info: https://pastebin.com/aTUWf33J

# Monitor expects commands in a series of 3 bytes
# Flush after every 3 bytes to ensure each command is accepted

# LIST OF BYTE COMMANDS

# -------BANKS---------
COMMANDS = {
    "IEN": [0x49, 0x45, 0x4E],  # Encoders
    "ISW": [0x49, 0x53, 0x57],  # Switches
    "ILE": [0x49, 0x4C, 0x45],  # Leds
    "ICC": [0x49, 0x43, 0x43],  # ??
    "IMT": [0x49, 0x4D, 0x54],  # ??
    # -----Key Presses------
    # Format: 0x44 <group> <mask>
    "SHIFT": [0x44, 0x03, 0x01],  # Shift Key
    "OVERSCAN_16_9": [0x44, 0x03, 0x02],  # Overscan / 16:9
    "HORIZSYNC_SYNC": [0x44, 0x03, 0x04],  # Horizontal Sync View / Sync
    "VERTSYNC_BLUEONLY": [0x44, 0x03, 0x08],  # Vertical Sync View / Blue Only
    "MONO_RED": [0x44, 0x03, 0x10],  # Mono / Red Beam
    "APT_GREEN": [0x44, 0x04, 0x01],  # Aperture / Green Beam
    "COMB_BLUE": [0x44, 0x04, 0x02],  # Comb / Blue Beam
    "F1_F3": [0x44, 0x04, 0x04],  # F1 Key / F3 Key
    "F2_F4": [0x44, 0x04, 0x08],  # F2 Key / F4 Key
    "SAFEAREA_ADDR": [0x44, 0x04, 0x10],  # Safe Area / Address

    "UP": [0x44, 0x02, 0x40],  # Up Key
    "DOWN": [0x44, 0x02, 0x80],  # Down Key
    "MENU": [0x44, 0x02, 0x10],  # Menu Key
    "ENTER": [0x44, 0x02, 0x20],  # Enter Key

    "PHASE_M": [0x44, 0x02, 0x08],  # Phase Manual
    "CHROMA_M": [0x44, 0x02, 0x04],  # Chroma Manual
    "BRIGHT_M": [0x44, 0x02, 0x02],  # Bright Manual
    "CONTRAST_M": [0x44, 0x02, 0x01],  # Contrast Manual

    "NUM0": [0x44, 0x00, 0x01],  # Number 0
    "NUM1": [0x44, 0x00, 0x02],  # Number 1
    "NUM2": [0x44, 0x00, 0x04],  # Number 2
    "NUM3": [0x44, 0x00, 0x08],  # Number 3
    "NUM4": [0x44, 0x00, 0x10],  # Number 4
    "NUM5": [0x44, 0x00, 0x20],  # Number 5
    "NUM6": [0x44, 0x00, 0x40],  # Number 6
    "NUM7": [0x44, 0x00, 0x80],  # Number 7
    "NUM8": [0x44, 0x01, 0x01],  # Number 8
    "NUM9": [0x44, 0x01, 0x02],  # Number 9
    "DEL": [0x44, 0x01, 0x04],  # Delete Key
    "ENT": [0x44, 0x01, 0x08],  # Enter Key

    "POWER": [0x44, 0x01, 0x10],  # Power On/Off
    "DEGAUSS": [0x44, 0x01, 0x20],  # Degauss Button

    # -------Encoders-------
    "PHASE_ENC": [0x44, 0x03],  # Phase Knob
    "CHROMA_ENC": [0x44, 0x02], # Chroma Knob
    "BRIGHT_ENC": [0x44, 0x01], # Brightness Knob
    "CONTRAST_ENC": [0x44, 0x00],  # Contrast Knob
}

HUMAN_READABLE_COMMANDS = {
    "IEN": ["COMMAND", "IEN"],
    "ISW": ["COMMAND", "ISW"],
    "ILE": ["COMMAND", "ILE"],
    "ICC": ["COMMAND", "ICC"],
    "IMT": ["COMMAND", "IMT"],
    "Shift": ["COMMAND", "SHIFT"],
    "Overscan": ["COMMAND", "OVERSCAN_16_9"],
    "16:9": ["COMMAND", "SHIFT", "OVERSCAN_16_9", "SHIFT"],
    "HorizSync": ["COMMAND", "HORIZSYNC_SYNC"],
    "Sync": ["COMMAND", "SHIFT", "HORIZSYNC_SYNC", "SHIFT"],
    "VertSync": ["COMMAND", "VERTSYNC_BLUEONLY"],
    "BlueOnly": ["COMMAND", "SHIFT", "VERTSYNC_BLUEONLY", "SHIFT"],
    "Mono": ["COMMAND", "MONO_RED"],
    "Red": ["COMMAND", "SHIFT", "MONO_RED", "SHIFT"],
    "Aperture": ["COMMAND", "APT_GREEN"],
    "Green": ["COMMAND", "SHIFT", "APT_GREEN", "SHIFT"],
    "Comb": ["COMMAND", "COMB_BLUE"],
    "Blue": ["COMMAND", "SHIFT", "COMB_BLUE", "SHIFT"],
    "F1": ["COMMAND", "F1_F3"],
    "F3": ["COMMAND", "SHIFT", "F1_F3", "SHIFT"],
    "F2": ["COMMAND", "F2_F4"],
    "F4": ["COMMAND", "SHIFT", "F2_F4", "SHIFT"],
    "SafeArea": ["COMMAND", "SAFEAREA_ADDR"],
    "Address": ["COMMAND", "SHIFT", "SAFEAREA_ADDR", "SHIFT"],
    "Up": ["COMMAND", "UP"],
    "Down": ["COMMAND", "DOWN"],
    "Enter": ["COMMAND", "ENTER"],
    "Menu": ["COMMAND", "ISW", "MENU", "ISW"],
    "Num0": ["COMMAND", "NUM0"],
    "Num1": ["COMMAND", "NUM1"],
    "Num2": ["COMMAND", "NUM2"],
    "Num3": ["COMMAND", "NUM3"],
    "Num4": ["COMMAND", "NUM4"],
    "Num5": ["COMMAND", "NUM5"],
    "Num6": ["COMMAND", "NUM6"],
    "Num7": ["COMMAND", "NUM7"],
    "Num8": ["COMMAND", "NUM8"],
    "Num9": ["COMMAND", "NUM9"],
    "Power": ["COMMAND", "ISW", "POWER", "ISW"],
    "Degauss": ["COMMAND", "DEGAUSS"],
    "PhaseInc": ["ENCODER-SUB", "PHASE_ENC"],
    "ChromaInc": ["ENCODER-SUB", "CHROMA_ENC"],
    "BrightInc": ["ENCODER-SUB", "BRIGHT_ENC"],
    "ContrastInc": ["ENCODER-SUB", "CONTRAST_ENC"],
    "UpdateChannelName": ["SCRIPT", "CHANNEL_NAME"]
}

class EmuBKM10r:
    ser = None

    def __init__(self, serial_port, baudrate=38400):
        # Open Serial Port
        self.ser = serial.Serial()
        self.ser.baudrate = baudrate
        self.ser.port = serial_port

    def connect(self):
        try:
            if not self.ser.is_open:
                self.ser.open()
        except Exception as e:
            print(f"Error connecting to Monitor: {e}")
            raise

    def close(self):
        """Closes serial connection to Monitor"""
        if self.ser.is_open:
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

    def repeatCommand(self, command, reps, skipISW=False):
        """ Repeats COMMANDS N times with a 0.05 delay between """
        for i in range(reps):
            self.writeCommand(command, skipISW)

    # --------------------Custom Functions---------------------
    # These are made using the byte commands implemented above
    # These are NOT standard to the BKM series of controllers

    # Function to enter text whenever applicable
    def writeText(self):
        dif = input("Input Text: ")
        for s in dif:
            dir = 1
            charstr = "abcdefghijklmnopqrstuvwxyz0123456789():;.-+/& "
            try:
                n = charstr.index(s.lower()) + 1
            except ValueError:
                print(f"Character '{s}' not supported.")
                continue

            if n > len(charstr) // 2:
                dir = -1
                n = len(charstr) - (n - 1)
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

        # Move to Channel Settings
        self.repeatCommand("DOWN", 2, skipISW=True)
        self.writeCommand("ENTER")
        time.sleep(0.1)

        # Get channel to change name
        num = int(input("Channel Number to Update (0-9): "))
        if 0 <= num <= 9:
            channel_num = "NUM" + str(num)
        else:
            print("Invalid channel number.")
            return

        self.writeCommand(channel_num)
        time.sleep(0.5)

        # Move to Name function
        self.repeatCommand("DOWN", 6, skipISW=True)
        self.writeCommand("ENTER")
        time.sleep(0.1)

        self.writeCommand("UP")
        self.writeCommand("ENTER")
        time.sleep(0.1)

        self.writeText()

    # Writes bytes for each command
    def sendCommand(self, inp_str):
        try:
            command_list = HUMAN_READABLE_COMMANDS[inp_str].copy()
            print(f"Current command: {command_list}")
        except KeyError:
            print("Not a Valid Command")
            return 0

        command_type = command_list.pop(0)
        if command_type == "COMMAND":
            for command in command_list:
                self.writeCommand(command)
            return 1
        elif command_type == "ENCODER-SUB":
            encoder_name = command_list[0]
            # Ask for user input
            try:
                dif = int(input("Input Wanted Difference (positive for increase, negative for decrease, between -32 and 31): "))
                if not -32 <= dif <= 31:
                    print("Value must be between -32 and 31")
                    return 0
            except ValueError:
                print("Invalid input, please enter an integer between -32 and 31")
                return 0
            # Multiply dif by 4 as per protocol
            dif_byte = (dif * 4) & 0xFF
            bytes_to_send = COMMANDS[encoder_name] + [dif_byte]
            try:
                # Switch to encoder bank (IEN)
                self.ser.write(bytearray(COMMANDS["IEN"]))
                self.ser.flush()
                # Send the encoder command
                self.ser.write(bytearray(bytes_to_send))
                self.ser.flush()
                # Switch back to key bank (ISW)
                self.ser.write(bytearray(COMMANDS["ISW"]))
                self.ser.flush()
                # Brief pause to ensure the command is processed
                time.sleep(0.1)
            except Exception as e:
                print(f"Error sending encoder command: {e}")
                return 0
            return 1
        elif command_type == "SCRIPT":
            if command_list[0] == "CHANNEL_NAME":
                self.updateChannelName()
                return 1
        else:
            print("Command type not recognized.")
            return 0

if __name__ == "__main__":
    argParser = argparse.ArgumentParser()
    argParser.add_argument("-p", "--port", help="Port of USB serial device")
    argParser.add_argument("-c", "--command", help="Single Command to run")

    args = argParser.parse_args()

    try:
        if args.port is not None:
            bkm = EmuBKM10r(args.port)
        else:
            bkm = EmuBKM10r('COM9')  # Default port, change as needed
        bkm.connect()  # Opens serial port and connects to monitor

        # Single command option
        if args.command is not None:
            ret = bkm.sendCommand(args.command)
            if ret == 1:
                bkm.flush()
                print("Command Successfully Sent")
            else:
                print("Command Failed")
        else:
            print("Sony BKM-10r Emulated Controller")
            print("Type 'help' for Info and 'exit' to Quit")

            # CLI Loop
            inp = ""
            while inp.lower() != "exit":
                inp = input(">")
                if inp.lower() == "help":
                    print("Available commands:")
                    for cmd in sorted(HUMAN_READABLE_COMMANDS.keys()):
                        print(cmd)
                    continue
                if inp.lower() != "exit" and inp.strip() != "":
                    ret = bkm.sendCommand(inp)
                    if ret == 1:
                        bkm.flush()
                        print("Command Successfully Sent")
                    else:
                        print("Command Failed")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        bkm.close()