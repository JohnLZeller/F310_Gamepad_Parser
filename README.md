Logitech F310 Gamepad Controller Parser
========

This software parses the raw binary information coming off of a Logitech F310 Gamepad, makes it useable
by updating state variables kept in a python dictionary and then displays the values through a very simple
Python Tkinter GUI. This serves a good foundation for any project you may want to incorporate a Logitech
F310 GamePad into.

Dependencies include:
* python
* python-tk
* python-pmw
* python-imaging

To add all use the following command in Ubuntu:
* sudo apt-get install python python-tk idle python-pmw python-imaging

More detailed information on the controller used can be found here:
http://www.logitech.com/en-us/product/gamepad-f310