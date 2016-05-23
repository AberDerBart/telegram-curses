import curses
import json
import textwrap
from telegramData import *
from VSplit import *
from HSplit import *
from ContactList import *
from ChatWindow import *
from InputWindow import *
from curses import ascii

mWin=curses.initscr()
curses.noecho()
curses.cbreak()
mWin.keypad(True)
curses.start_color()

curses.init_pair(1,curses.COLOR_CYAN,curses.COLOR_BLACK)
curses.init_pair(2,curses.COLOR_GREEN,curses.COLOR_BLACK)

leftRight=VSplit(mWin,10,10)

topBottom=HSplit(leftRight.right,1,1)

cl=ContactList(leftRight.left)
cl.loadList(liste)
cl.redraw()

cw=ChatWindow(topBottom.top)
cw.loadChat(chat)
cw.redraw()

iw=InputWindow(topBottom.bottom)
iw.redraw()

def close(errorText=""):
	curses.nocbreak()
	mWin.keypad(False)
	curses.echo()
	curses.endwin()
	if(errorText != ""):
		print(errorText)
	exit()

inp=0;

while(True):
	inp=mWin.getch()
	
	if(inp==curses.KEY_UP):
		cl.prevContact()
	elif(inp==curses.KEY_DOWN):
		cl.nextContact()
	elif(inp==curses.KEY_RESIZE):
		if(not leftRight.refresh()):
			close("error: window too small")
		if(not topBottom.refresh()):
			close("error: window to small")
		cw.redraw()
		cl.redraw()
		iw.redraw()
	elif(iw.processInput(inp)):
		iw.redraw()
	else:
		break
	if(not leftRight.refresh()):
		close("error: window too small")
	if(not topBottom.refresh()):
		close("error: window to small")
	mWin.refresh()


close(str(inp))
