import curses

class VSplit:
	def __init__(self,mWin,mWidthLeft=1,mWidthRight=1):
		self.xSplit=mWin.getmaxyx()[1]/2
		self.left=mWin.subwin(0,0)
		self.right=mWin.subwin(0,0)
		self.mWin=mWin
		self.mWidthLeft=mWidthLeft
		self.mWidthRight=mWidthRight

		self.refresh()
	def refresh(self):
		if(self.mWin.getmaxyx()[1] < self.mWidthLeft + self.mWidthRight + 1):
			return False
		if(self.xSplit >= self.mWin.getmaxyx()[1]-self.mWidthRight-1):
			self.xSplit=self.mWin.getmaxyx()[1]-self.mWidthRight-1
		if(self.xSplit <= self.mWidthLeft):
			self.xSplit=self.mWidthLeft
		print(self.xSplit)
		self.left.resize(1,1)
		self.right.resize(1,1)
		self.left.mvderwin(0,0)
		self.right.mvderwin(0,self.xSplit+1)
		self.left.resize(self.mWin.getmaxyx()[0],self.xSplit)
		self.right.resize(self.mWin.getmaxyx()[0],self.mWin.getmaxyx()[1]-self.xSplit-1)
		self.mWin.vline(0,self.xSplit,curses.ACS_VLINE,self.mWin.getmaxyx()[0])
		return True
