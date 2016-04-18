import curses

class VSplit:
	def __init__(self,mWin):
		self.xSplit=mWin.getmaxyx()[1]/2
		self.left=mWin.subwin(0,0)
		self.right=mWin.subwin(0,0)
		self.mWin=mWin
		self.refresh()
	def refresh(self):
		if(self.xSplit >= self.mWin.getmaxyx()[1]-1):
			self.xSplit=self.mWin.getmaxyx()[1]-2
		if(self.xSplit <= 1):
			self.xSplit=1
		self.left.resize(self.mWin.getmaxyx()[0],self.xSplit)
		self.right.resize(self.mWin.getmaxyx()[0],self.mWin.getmaxyx()[1]-self.xSplit-1)
		self.left.mvderwin(0,0)
		self.right.mvderwin(0,self.xSplit+1)
		self.mWin.vline(0,self.xSplit,curses.ACS_VLINE,self.mWin.getmaxyx()[0])
