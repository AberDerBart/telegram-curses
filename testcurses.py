import curses
import json
import textwrap
from telegramData import *
from VSplit import *
from ContactList import *
from ChatWindow import *
from InputWindow import *

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
