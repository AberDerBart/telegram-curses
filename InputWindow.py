import curses
from curses import ascii

class InputWindow:
	def __init__(self,win):
		self.win=win
		self.text=""
	def processInput(self,key):
		if(ascii.isprint(key) or ascii.isspace(key)):
			self.text=self.text + chr(key)
			return True
		if(key==curses.KEY_BACKSPACE):
			self.text=self.text[:-1]
			return True
		return False
	def redraw(self):
		"""redraws the window"""
		self.win.clear()
		self.win.addstr(0,0,self.text)

