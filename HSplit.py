import curses

class HSplit:
	def __init__(self,mWin,mHeightTop=1,mHeightBottom=1):
		self.ySplit=mWin.getmaxyx()[0]/2
		self.top=mWin.derwin(0,0)
		self.bottom=mWin.derwin(0,0)
		self.mWin=mWin
		self.mHeightTop=mHeightTop
		self.mHeightBottom=mHeightBottom

		self.refresh()
	def refresh(self):
		if(self.mWin.getmaxyx()[0] < self.mHeightTop + self.mHeightBottom + 1):
			return False
		if(self.ySplit >= self.mWin.getmaxyx()[0]-self.mHeightBottom-1):
			self.ySplit=self.mWin.getmaxyx()[0]-self.mHeightBottom-1
		if(self.ySplit <= self.mHeightTop):
			self.ySplit=self.mHeightTop
		self.top.resize(1,1)
		self.bottom.resize(1,1)
		self.top.mvderwin(0,0)
		self.bottom.mvderwin(self.ySplit+1,0)
		self.top.resize(self.ySplit,self.mWin.getmaxyx()[1])
		self.bottom.resize(self.mWin.getmaxyx()[0]-self.ySplit-1,self.mWin.getmaxyx()[1])
		self.mWin.hline(self.ySplit,0,curses.ACS_HLINE,self.mWin.getmaxyx()[1])
		return True
