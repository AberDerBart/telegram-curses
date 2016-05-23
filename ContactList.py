import curses
import json

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
		self.contactList=list(filter(contactValid,json.loads(listJson)))
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
