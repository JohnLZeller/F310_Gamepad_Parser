############ Logitech F310 Gamepad Controller Main - parser_main.py ##########
# Original Author: John Zeller
# Description: Parser_Main polls the data in a python dictionary to check the states of
# 	       several buttons coming from parser_core.py. Once it reads these states, it
#	       will display them for reference on the terminal it was launched in

### NOTES ###############################################################################
# 1) LEAVE MODE 'OFF' there is no support in parser_main.py for MODE ON 		#
# 2) Naturally the gamepad sends the following values:					#
# 	LJ/RJ - Down: 0-127								#
# 	LJ/RJ - Up: 255-128								#
# 	LJ/RJ - Left: 255-128								#
# 	LJ/RJ - Right: 0-127								#
#########################################################################################

### Buttons/Joys Represented: ###########################################################
# A, B, X, Y, RB, LB, LJButton, RJButton, Back, Start, Middle				#
# RT, LT, LeftJoy, RightJoy, Left, Right, Up, Down					#
#########################################################################################

import sys
sys.path.append("./core")
import threading
from bus import *
from parser_core import *
from gui_main import *
import Tkinter as tk	# Native Python GUI Framework
import time

class ParserMain(threading.Thread):
	def __init__(self):
		# Create bus object
		self.bus = Bus()
		# Create a dictionary to be used to keep states from joy_core
		self.states = { 'A':0, 'B':0, 'X':0, 'Y':0,  		   		\
				'Back':0, 'Start':0, 'Middle':0,		   	\
				'Left':0, 'Right':0, 'Up':0, 'Down':0, 			\
				'LB':0, 'RB':0, 'LT':0, 'RT':0,				\
				'LJ/Button':0, 'RJ/Button':0, 				\
				'LJ/Left':0, 'LJ/Right':0, 'LJ/Up':0, 'LJ/Down':0, 	\
				'RJ/Left':0, 'RJ/Right':0, 'RJ/Up':0, 'RJ/Down':0,	\
				'Byte0':0, 'Byte1':0, 'Byte2':0, 'Byte3':0,		\
				'Byte4':0, 'Byte5':0, 'Byte6':0, 'Byte7':0}
		# Launch Parser_Core as a seperate thread to parse the gamepad
		self.parsercore = ParserCore(self.bus, self.states)
		self.parsercore.start()
	
	def run(self):
		# Description: Polls the gamepad states and displays their current values on a simple Tkinter GUI
		
		# Launch simple GUI with Tkinter (Native GUI on Python)
		gui = GUI(self.states)     # Create GUI object
		gui.mainloop()  # Launch GUI object into the main loop

if __name__ == '__main__':
        parser = ParserMain()
        parser.run()
