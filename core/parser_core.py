############ Logitech F310 Gamepad Controller Parser - parser_core.py ##########
# Original Author: John Zeller
# Description: Parser_Core parses data coming from a Logitech F310 Gamepad Controller and
#	       updates a dictionary of states.

### NOTES ###############################################################################
# 1) LEAVE MODE 'OFF' there is no support in parser_core.py for MODE ON 		#
# 2) This parser was built using this tutorial as a reference:				#
#	http://hackshark.com/?p=147#axzz2BHTVXCFz					#
# 3) Naturally the gamepad sends the following values:					#
# 	LJ/RJ - Down: 0-127								#
# 	LJ/RJ - Up: 255-128								#
# 	LJ/RJ - Left: 255-128								#
# 	LJ/RJ - Right: 0-127								#
#########################################################################################

### Buttons/Joys Represented: ###########################################################
# A, B, X, Y, RB, LB, LJButton, RJButton, Back, Start, Middle				#
# RT, LT, LeftJoy, RightJoy, Left, Right, Up, Down					#
#########################################################################################

### States Dictionary Reference: ########################################################
#	self.states = { 'A':0, 'B':0, 'X':0, 'Y':0,  		   		\	#
#			'Back':0, 'Start':0, 'Middle':0,		   	\	#
#			'Left':0, 'Right':0, 'Up':0, 'Down':0, 			\	#
#			'LB':0, 'RB':0, 'LT':0, 'RT':0,				\	#
#			'LJ/Button':0, 'RJ/Button':0, 				\	#
#			'LJ/Left':0, 'LJ/Right':0, 'LJ/Up':0, 'LJ/Down':0, 	\	#
#			'RJ/Left':0, 'RJ/Right':0, 'RJ/Up':0, 'RJ/Down':0}		#
#########################################################################################

import sys
import threading

class ParserCore(threading.Thread):
	def __init__(self, bus, states):
		# Initializes threading
		threading.Thread.__init__(self)
		# Stores the bus and states objects
		self.bus = bus
		self.states = states
		# Creates lists and dictionaries
		self.templist = []
		# All button raw packet values of data coming from gamepad
		self.buttons = {'\x00':'A', '\x01':'B', '\x02':'X', '\x03':'Y', \
				'\x04':'LB', '\x05':'RB', '\x06':'Back', '\x07':'Start', \
				'\x08':'Middle', '\t':'LJ/Button', '\n':'RJ/Button'}
		# Initializes templist
		for x in range(8):
		        self.templist.append(0)

	def run(self):
		# Start Parser
		while 1:
			# Read 1 byte
			for x in range(8):
				self.templist[x] = self.bus.gamepad.read(1)
				
			# BUTTON is PRESSED
			if self.templist[4]=='\x01' or self.templist[4]=='\xFF':
				self.parse_pressed_button()
				
			# BUTTON is RELEASED
			if self.templist[4]=='\x00':
				self.parse_released_button()
				
			# JOYSTICK is PRESSED
			else:
				self.parse_pressed_joy()

	def parse_pressed_button(self):
		# Updates states of buttons to 1 (on)
		if self.templist[6]=='\x01' and self.templist[5]=='\x00': # Letters, Start/Back or LJ/RJ Buttons
			self.states[self.buttons[self.templist[7]]] = 1
		elif self.templist[6]=='\x02' and self.templist[5]=='\x80': # D-Pad L/U
			if self.templist[7]=='\x06': # Left
				self.states['Left'] = 1
			elif self.templist[7]=='\x07': # Up
				self.states['Up'] = 1
		elif self.templist[6]=='\x02' and self.templist[5]=='\x7F': # D-Pad R/D
			if self.templist[7]=='\x06': # Right
				self.states['Right'] = 1
			elif self.templist[7]=='\x07': # Down
				self.states['Down'] = 1

	def parse_pressed_joy(self):
		# Updates joy states with values 0-255
		if self.templist[7]=='\x02' and self.templist[6]=='\x02': # LT
			if ord(self.templist[5])>=128:
				val = str(ord(self.templist[5]) - 128)
				self.states['LT'] = val
			elif ord(self.templist[5])<=127:
				val = str(ord(self.templist[5]) + 127)
				self.states['LT'] = val
		elif self.templist[7]=='\x05' and self.templist[6]=='\x02': # RT
			if ord(self.templist[5])>=128:
				val = str(ord(self.templist[5]) - 128)
				self.states['RT'] = val
			elif ord(self.templist[5])<=127:
				val = str(ord(self.templist[5]) + 127)
				self.states['RT'] = val
		elif self.templist[7]=='\x00' and self.templist[6]=='\x02': # Left-Joy L/R
			if ord(self.templist[5])<=127: # Right
				val = str(ord(self.templist[5]))
				self.states['LJ/Right'] = val
			elif ord(self.templist[5])>=128: # Left
				val = str(ord(self.templist[5]))
				self.states['LJ/Left'] = val
		elif self.templist[7]=='\x01' and self.templist[6]=='\x02': # Left-Joy U/D
			if ord(self.templist[5])<=127: # Down
				val = str(ord(self.templist[5]))
				self.states['LJ/Down'] = val
			elif ord(self.templist[5])>=128: # Up
				val = str(ord(self.templist[5]) - 255)
				self.states['LJ/Up'] = val
		elif self.templist[7]=='\x03' and self.templist[6]=='\x02': # Right-Joy L/R
			if ord(self.templist[5])<=127: # Right
				val = str(ord(self.templist[5]))
				self.states['RJ/Right'] = val
			elif ord(self.templist[5])>=128: # Left
				val = str(ord(self.templist[5]) - 255)
				self.states['RJ/Left'] = val
		elif self.templist[7]=='\x04' and self.templist[6]=='\x02': # Right-Joy U/D
			if ord(self.templist[5])<=127: # Down
				val = str(ord(self.templist[5]))
				self.states['RJ/Down'] = val
			elif ord(self.templist[5])>=128: # Up
				val = str(ord(self.templist[5]) - 255)
				self.states['RJ/Up'] = val

	def parse_released_button(self):
		# Updates states of buttons to 0(off)
		if self.templist[5]=='\x00' and self.templist[6]=='\x01': # Letters, Start/Stop, or LJ/RJ Buttons
			# Check to see if templist[5] is in button list
			# and if not then see if it is /00 - DPad
			self.states[self.buttons[self.templist[7]]] = 0
		elif self.templist[5]=='\x00' and self.templist[6]=='\x02': # D-Pad
			if self.templist[7]=='\x07': # D-Pad, Up/Down
				if self.states['Up']==1: # Up
					self.states['Up'] = 0
				elif self.states['Down']==1: # Down
					self.states['Down'] = 0
			elif self.templist[7]=='\x06': # D-Pad, Left/Right
				if self.states['Left']==1: # Left
					self.states['Left'] = 0
				elif self.states['Right']==1: # Right
					self.states['Right'] = 0
		# ADD IN JOY RELEASED
