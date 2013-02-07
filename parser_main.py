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
import threading
from core.bus import *
from core.parser_core import *
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
				'RJ/Left':0, 'RJ/Right':0, 'RJ/Up':0, 'RJ/Down':0}
		# Launch Parser_Core as a seperate thread to parse the gamepad
		self.parsercore = ParserCore(self.bus, self.states)
		self.parsercore.start()
	
	def run(self):
		# Description: Polls the gamepad states and displays their current values on a simple Tkinter GUI
		
		# Launch simple GUI with Tkinter (Native GUI on Python)
		gui = self.GUI()     # Create GUI object
		gui.mainloop()  # Launch GUI object into the main loop

class GUI():
    def __init__(self, states):
	self.states = states	# Save the states in self.states
	self.root = tk.Tk()
        self.root.title('Logitech F310 Gamepad Controller Output Display')
        self.root.geometry('400x650')
        # Create and Position Title Labels
        self.label_Time = tk.Label(self.root, text="GUI Running for... ").grid(row=0, padx=10, pady=20)
        self.label_Time_s = tk.Label(self.root, text="seconds").grid(row=0, column=2)
        self.label_Buttons_Title = tk.Label(self.root, text="-- Buttons --").grid(columnspan=2, pady=10, sticky="E")
        self.label_A = tk.Label(self.root, text="A").grid(row=2, padx=5, sticky="E")
        self.label_B = tk.Label(self.root, text="B").grid(row=3, padx=5, sticky="E")
        self.label_X = tk.Label(self.root, text="X").grid(row=4, padx=5, sticky="E")
        self.label_Y = tk.Label(self.root, text="Y").grid(row=5, padx=5, sticky="E")
        self.label_Back = tk.Label(self.root, text="Back").grid(row=6, padx=5, sticky="E")
        self.label_Start = tk.Label(self.root, text="Start").grid(row=7, padx=5, sticky="E")
        self.label_Middle = tk.Label(self.root, text="Middle").grid(row=8, padx=5, sticky="E")
        self.label_Left = tk.Label(self.root, text="Left").grid(row=9, padx=5, sticky="E")
        self.label_Right = tk.Label(self.root, text="Right").grid(row=10, padx=5, sticky="E")
        self.label_Up = tk.Label(self.root, text="Up").grid(row=11, padx=5, sticky="E")
        self.label_Down = tk.Label(self.root, text="Down").grid(row=12, padx=5, sticky="E")
        self.label_LJButton = tk.Label(self.root, text="LJ/Button").grid(row=13, padx=5, sticky="E")
        self.label_RJButton = tk.Label(self.root, text="RJ/Button").grid(row=14, padx=5, sticky="E")
        self.label_Joys_Title = tk.Label(self.root, text="-- Joys --").grid(columnspan=2, pady=10, sticky="E")
        self.label_LJLeft = tk.Label(self.root, text="LJ/Left").grid(row=16, padx=5, sticky="E")
        self.label_LJRight = tk.Label(self.root, text="LJ/Right").grid(row=17, padx=5, sticky="E")
        self.label_LJUp = tk.Label(self.root, text="LJ/Up").grid(row=18, padx=5, sticky="E")
        self.label_LJDown = tk.Label(self.root, text="LJ/Down").grid(row=19, padx=5, sticky="E")
        self.label_RJLeft = tk.Label(self.root, text="RJ/Left").grid(row=20, padx=5, sticky="E")
        self.label_RJRight = tk.Label(self.root, text="RJ/Right").grid(row=21, padx=5, sticky="E")
        self.label_RJUp = tk.Label(self.root, text="RJ/Up").grid(row=22, padx=5, sticky="E")
        self.label_RJDown = tk.Label(self.root, text="RJ/Down").grid(row=23, padx=5, sticky="E")
        # Create Dynamic Variable Labels
        self.variable_Time = tk.Label(text="")
        self.variable_Blank = tk.Label(text="")
        self.variable_A = tk.Label(text="")
        self.variable_B = tk.Label(text="")
        self.variable_X = tk.Label(text="")
        self.variable_Y = tk.Label(text="")
        self.variable_Back = tk.Label(text="")
        self.variable_Start = tk.Label(text="")
        self.variable_Middle = tk.Label(text="")
        self.variable_Left = tk.Label(text="")
        self.variable_Right = tk.Label(text="")
        self.variable_Up = tk.Label(text="")
        self.variable_Down = tk.Label(text="")
        self.variable_LJButton = tk.Label(text="")
        self.variable_RJButton = tk.Label(text="")
        self.variable_LJLeft = tk.Label(text="")
        self.variable_LJRight = tk.Label(text="")
        self.variable_LJUp = tk.Label(text="")
        self.variable_LJDown = tk.Label(text="")
        self.variable_RJLeft = tk.Label(text="")
        self.variable_RJRight = tk.Label(text="")
        self.variable_RJUp = tk.Label(text="")
        self.variable_RJDown = tk.Label(text="")
        # Position Dynamic Variable Labels
        self.variable_Time.grid(row=0, column=1)
        self.variable_A.grid(row=2, column=1)
        self.variable_B.grid(row=3, column=1)
        self.variable_X.grid(row=4, column=1)
        self.variable_Y.grid(row=5, column=1)
        self.variable_Back.grid(row=6, column=1)
        self.variable_Start.grid(row=7, column=1)
        self.variable_Middle.grid(row=8, column=1)
        self.variable_Left.grid(row=9, column=1)
        self.variable_Right.grid(row=10, column=1)
        self.variable_Up.grid(row=11, column=1)
        self.variable_Down.grid(row=12, column=1)
        self.variable_LJButton.grid(row=13, column=1)
        self.variable_RJButton.grid(row=14, column=1)
        self.variable_LJLeft.grid(row=16, column=1)
        self.variable_LJRight.grid(row=17, column=1)
        self.variable_LJUp.grid(row=18, column=1)
        self.variable_LJDown.grid(row=19, column=1)
        self.variable_RJLeft.grid(row=20, column=1)
        self.variable_RJRight.grid(row=21, column=1)
        self.variable_RJUp.grid(row=22, column=1)
        self.variable_RJDown.grid(row=23, column=1)
        # Start tracking time
        self.start_time = time.time()
        # Run update_label()
        self.update_labels()
        self.root.mainloop()    # Once here, begin main loop again

    def update_labels(self):
        time_counter = time.time() - self.start_time
        time_counter = round(time_counter, 0)
        # Configure Labels with Updates
        self.variable_Time.configure(text=str(time_counter))
        self.variable_A.configure(text=str(self.states['A']))
        self.variable_B.configure(text=str(self.states['B']))
        self.variable_X.configure(text=str(self.states['X']))
        self.variable_Y.configure(text=str(self.states['Y']))
        self.variable_Back.configure(text=str(self.states['Back']))
        self.variable_Start.configure(text=str(self.states['Start']))
        self.variable_Middle.configure(text=str(self.states['Middle']))
        self.variable_Left.configure(text=str(self.states['Left']))
        self.variable_Right.configure(text=str(self.states['Right']))
        self.variable_Up.configure(text=str(self.states['Up']))
        self.variable_Down.configure(text=str(self.states['Down']))
        self.variable_LJButton.configure(text=str(self.states['LJ/Button']))
        self.variable_RJButton.configure(text=str(self.states['RJ/Button']))
        self.variable_LJLeft.configure(text=str(self.states['LJ/Left']))
        self.variable_LJRight.configure(text=str(self.states['LJ/Right']))
        self.variable_LJUp.configure(text=str(self.states['LJ/Up']))
        self.variable_LJDown.configure(text=str(self.states['LJ/Down']))
        self.variable_RJLeft.configure(text=str(self.states['RJ/Left']))
        self.variable_RJRight.configure(text=str(self.states['RJ/Right']))
        self.variable_RJUp.configure(text=str(self.states['RJ/Up']))
        self.variable_RJDown.configure(text=str(self.states['RJ/Down']))
        self.root.after(10, self.update_labels)
