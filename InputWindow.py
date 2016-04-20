import curses
from curses import ascii

class InputWindow:
	def __init__(self,win):
		self.win=win
		self.text=""
	def processInput(self,key):
		if(ascii.isascii(key)):
			self.text=self.text + chr(key)
			return True
		return False
	def redraw(self):
		"""redraws the window"""
		self.win.clear()
		self.win.addstr(0,0,self.text)

