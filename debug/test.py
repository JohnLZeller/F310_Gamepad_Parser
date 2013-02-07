############ Parse to Terminal Test - parse_to_terminal_test.py ##########
# Original Author: John Zeller
# Description: Parse_To_Terminal_Test is a debugging tool to print 8 byte
#	       strings to the terminal, representing each byte as a string
#	       showing the hexadecimal value of the byte.

import sys
import threading
import serial, time

class Bus(object):
        def __init__(self):
                self.gamepad = open('/dev/input/js0', 'r')

        def restart(self):
		self.gamepad.close()
		self.gamepad = open('/dev/input/js0', 'r')
		
class ParserCore(threading.Thread):
	def __init__(self):
		# Stores the bus and states objects
		self.bus = Bus()
		# Create a templist
		self.templist = []
		# Initializes templist
		for x in range(8):
		        self.templist.append(0)

	def run(self):
		# Start Parser
		while 1:
			# Read 1 byte
			for x in range(8):
				self.templist[x] = self.bus.gamepad.read(1)
				
			string = str(ord(self.templist[0])) + "\t" + str(ord(self.templist[1])) + "\t" + \
				 str(ord(self.templist[2])) + "\t" + str(ord(self.templist[3])) + "\t" + \
				 str(ord(self.templist[4])) + "\t" + str(ord(self.templist[5])) + "\t" + \
				 str(ord(self.templist[6])) + "\t" + str(ord(self.templist[7]))
			print string + "\n"

if __name__ == '__main__':
        parser = ParserCore()
        parser.run()