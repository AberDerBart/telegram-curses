import curses
import json
import textwrap
from telegramData import *
from VSplit import *

def contactValid(contact):
	return contact['print_name']!=""

class ContactList:
	"""a curses representation of a telegram contact list"""
	def __init__(self,win):
		"""creates a new subwindow of mWin to display the contactlist"""
		self.selection=0
		self.listShift=0;
		self.win=win
	def loadList(self,listJson):
		"""loads the contact list from listJson"""
		self.contactList=filter(contactValid,json.loads(listJson))
	def width(self):
		"""return the width of the window"""
		return self.win.getmaxyx()[1]
	def height(self):
		"""return the height of the window"""
		return self.win.getmaxyx()[0]
	def redraw(self):
		"""(re)draws the contact list"""
		self.win.clear()
		for i,contact in enumerate(self.contactList[self.listShift:self.listShift+self.height()]):
			displayName=(contact['first_name']+' '+contact['last_name']).ljust(self.width())[:self.width()]
			
			if(i==self.selection-self.listShift):
				self.win.insstr(i,0,displayName,curses.A_REVERSE)
			else:
				self.win.insstr(i,0,displayName)
		self.win.refresh()
	def nextContact(self):
		"""selects the next contact in the list"""
		self.selection+=1
		# don't allow selections outside the list
		if(self.selection>=len(self.contactList)):
			self.selection=len(self.contactList)-1
		# adjust list shift
		if(self.selection-self.listShift>=self.height()):
			self.listShift=self.selection-self.height()+1
		self.redraw()
	def prevContact(self):
		"""selects the previous contact in the list"""
		self.selection-=1
		# don't allow selections outside the list
		if(self.selection<0):
			self.selection=0
		# adjust list shift
		if(self.listShift > self.selection):
			self.listShift=self.selection
		self.redraw()
	def getSelectedContact(self):
		"""returns the selected contact or None, if the list is empty or the selection is invalid"""
		if(0 < self.selection < len(self.contactList)):
			return self.contactList[self.selection]
		return None
class ChatWin:
	"""a curses representation of a telegram chat"""
	def __init__(self,win):
		self.win=win
		self.ownNumber="4915141646942"
		self.msgs=[]
	def width(self):
		"""return the width of the window (excluding border)"""
		return self.win.getmaxyx()[1]
	def height(self):
		"""return the height of the window (excluding border)"""
		return self.win.getmaxyx()[0]
	def redraw(self):
		"""redraws the chat"""
		self.win.clear()
		self.linesPrint=0
		for msg in reversed(self.msgs):
			sender=msg['from']
			senderName=(sender['first_name']+' '+sender['last_name']+':')[:self.width()]
			messageLines=textwrap.wrap(msg['text'],self.width()-4)
			for line in reversed(messageLines):
				if(self.linesPrint < self.height()):
					# make sure we only print in available space
					self.win.insstr(self.height()-self.linesPrint-1,4,line)
					self.linesPrint+=1
			if(self.linesPrint < self.height()):
				# make sure we only print in available space
				if(self.ownNumber==sender['phone']):
					self.win.insstr(self.height()-self.linesPrint-1,0,senderName,curses.color_pair(1))
					self.linesPrint+=1
				else:
					self.win.insstr(self.height()-self.linesPrint-1,0,senderName,curses.color_pair(2))
					self.linesPrint+=1
		self.win.refresh()
	def loadChat(self,chatJson):
		"""loads the chat [chatJson] into the chat window"""
		self.msgs=json.loads(chatJson)
	def appendMessage(self,messageJson):
		"""appends [message] to the end of the chat"""
		self.msgs.append(json.loads(chatJson))
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

cw=ChatWin(leftRight.right)
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
		leftRight.refresh()
		cl.redraw()
		cw.redraw()
		continue
	else:
		break

curses.nocbreak()
mWin.keypad(False)
curses.echo()
curses.endwin()
