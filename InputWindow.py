import curses

class InputWindow:
	def __init__(self,win):
		self.win=win
	def redraw(self):
		"""redraws the window"""
		self.win.clear()
		self.win.border()
		self.win.refresh()
