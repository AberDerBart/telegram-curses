import curses
import json
import textwrap
from telegramData import *
from VSplit import *
from ContactList import *
from ChatWindow import *

class InputWin:
	def __init__(self,mWin):
		height=5
		width=mWin.getmaxyx()[1]-30
		self.win=mWin.subwin(height,width,mWin.getmaxyx()[0]-5,30)
	def width(self):
		"""return the width of the window (excluding border)"""
		return self.win.getmaxyx()[1]
	def height(self):
		"""return the height of the window (excluding border)"""
		return self.win.getmaxyx()[0]
	def resize(self,h,w):
		"""resizes the input window to height h and width w"""
		self.win.resize(h,w)
		self.redraw()
	def move(self,row,col):
		"""move the window to the coordinates specified by row, col"""
		self.win.mvwin(row,col)
	def redraw(self):
		self.win.border(0,0,0,0,curses.ACS_LTEE,curses.ACS_RTEE,0,0)
		self.win.refresh()
		



mWin=curses.initscr()
curses.noecho()
curses.cbreak()
mWin.keypad(True)
curses.start_color()

curses.init_pair(1,curses.COLOR_CYAN,curses.COLOR_BLACK)
curses.init_pair(2,curses.COLOR_GREEN,curses.COLOR_BLACK)

leftRight=VSplit(mWin,10,10)

cl=ContactList(leftRight.left)
cl.loadList(liste)
cl.redraw()

cw=ChatWindow(leftRight.right)
cw.loadChat(chat)
cw.redraw()


while(True):
	inp=mWin.getch()
	if(inp==curses.KEY_UP):
		cl.prevContact()
		continue
	elif(inp==curses.KEY_DOWN):
		cl.nextContact()
		continue
	elif(inp==curses.KEY_RESIZE):
		if(not leftRight.refresh()):
			break
		cw.redraw()
		cl.redraw()
		continue
	else:
		break

curses.nocbreak()
mWin.keypad(False)
curses.echo()
curses.endwin()
