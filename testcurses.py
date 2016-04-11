import curses
import json
liste='[{"id": "$010000007947b3031e511c99da788099", "first_name": "Kristina", "last_name": "Schaab", "peer_type": "user", "peer_id": 62080889, "print_name": "Kristina_Schaab", "when": "2016-04-07 09:07:46", "flags": 196609, "phone": "4917630753680"}, {"id": "$01000000af6f0f020000000000000000", "peer_type": "user", "print_name": "", "peer_id": 34566063, "flags": 5}, {"id": "$01000000a4e8af021a6e8b7a018383ec", "first_name": "Robin", "last_name": "V.", "peer_type": "user", "peer_id": 45082788, "print_name": "Robin_V.", "when": "2016-04-07 13:52:26", "flags": 196609, "phone": "4915151157011"}, {"id": "$010000005f90e301970999266bd9091b", "first_name": "Dion", "last_name": "", "peer_type": "user", "peer_id": 31690847, "print_name": "Dion", "when": "2016-04-07 12:53:22", "flags": 196609, "phone": "491628808949"}, {"first_name": "Phillipp", "id": "$010000000fbea8009fe73f15478e9676", "last_name": "Mevenkamp", "peer_type": "user", "print_name": "Phillipp_Mevenkamp", "peer_id": 11058703, "flags": 196609, "phone": "4915788900332"}, {"id": "$01000000f764c403a0cd980570408a1b", "first_name": "Jonas", "last_name": "G.-H.", "peer_type": "user", "peer_id": 63202551, "print_name": "Jonas_G.-H.", "when": "2016-04-07 13:25:15", "flags": 524289, "phone": "4915141646942"}, {"first_name": "Talkingbot", "id": "$01000000250dbd06b01cfded3833ba9c", "last_name": "", "peer_type": "user", "print_name": "Talkingbot", "peer_id": 113052965, "username": "Boatbot", "flags": 1}, {"first_name": "Birgit", "id": "$0100000007004805565c87cf34892c77", "last_name": "Saalfeld", "peer_type": "user", "print_name": "Birgit_Saalfeld", "peer_id": 88604679, "flags": 1}, {"first_name": "Doodle bot", "id": "$01000000365c320745a27c27e979ea8b", "last_name": "", "peer_type": "user", "print_name": "Doodle_bot", "peer_id": 120740918, "username": "DoodleBot", "flags": 1}, {"first_name": "Stickers", "id": "$01000000c88b0600ed28ca1df1194c0f", "last_name": "", "peer_type": "user", "print_name": "Stickers", "peer_id": 429000, "username": "Stickers", "flags": 1}, {"first_name": "D", "id": "$01000000a5fed0043b30d83a57c40d86", "last_name": "", "peer_type": "user", "print_name": "D", "peer_id": 80805541, "username": "stickersbot", "flags": 1}, {"id": "$010000009c886005de848d7cc3e737a9", "first_name": "Steffen", "last_name": "Brahtz", "peer_type": "user", "peer_id": 90212508, "print_name": "Steffen_Brahtz", "when": "2016-03-22 14:01:27", "flags": 196609, "phone": "4917683732601"}, {"id": "$010000009197c3000000000000000000", "peer_type": "user", "print_name": "", "peer_id": 12818321, "flags": 5}, {"id": "$01000000974e2709537f12940573c3a6", "first_name": "Robin", "last_name": "W.", "peer_type": "user", "peer_id": 153570967, "print_name": "Robin_W.", "when": "2016-03-28 12:18:04", "flags": 196609, "phone": "4917655356439"}]'
chat='[{"text": "Oder halt einfach aalib", "event": "message", "id": "01000000ceed4e009d6200000000000040e003cf14ac450e", "service": false, "flags": 256, "to": {"last_name": "G.-H.", "id": "$01000000f764c403a0cd980570408a1b", "print_name": "Jonas_G.-H.", "when": "2016-04-10 18:29:42", "peer_type": "user", "peer_id": 63202551, "phone": "4915141646942", "first_name": "Jonas", "flags": 524289}, "from": {"last_name": "K.", "id": "$01000000ceed4e0040e003cf14ac450e", "print_name": "Nils_K.", "when": "2016-04-10 18:32:20", "peer_type": "user", "peer_id": 5172686, "phone": "491631631898", "first_name": "Nils", "flags": 196609}, "out": false, "unread": false, "date": 1459957371}, {"text": "naja ein schritt nach dem anderen - ich bin froh, wenn wir erstmal ne kontaktliste und nen chat daneben haben", "event": "message", "id": "01000000ceed4e009e6200000000000040e003cf14ac450e", "service": false, "flags": 258, "to": {"last_name": "K.", "id": "$01000000ceed4e0040e003cf14ac450e", "print_name": "Nils_K.", "when": "2016-04-10 18:32:20", "peer_type": "user", "peer_id": 5172686, "phone": "491631631898", "first_name": "Nils", "flags": 196609}, "from": {"last_name": "G.-H.", "id": "$01000000f764c403a0cd980570408a1b", "print_name": "Jonas_G.-H.", "when": "2016-04-10 18:29:42", "peer_type": "user", "peer_id": 63202551, "phone": "4915141646942", "first_name": "Jonas", "flags": 524289}, "out": true, "unread": false, "date": 1459957563}]'

def contactValid(contact):
	return contact['print_name']!=""

class ContactList:
	"""a curses representation of a telegram contact list"""
	def __init__(self,mWin):
		"""creates a new subwindow of mWin to display the contactlist"""
		height=mWin.getmaxyx()[0]
		self.win=mWin.subwin(height,30,0,0)
		self.win.border()
		self.win.refresh()
		self.selection=0
		self.listShift=0;
	def loadList(self,listJson):
		"""loads the contact list from listJson"""
		self.contactList=filter(contactValid,json.loads(listJson))
		self.redrawList()
	def width(self):
		"""return the width of the window (excluding border)"""
		return self.win.getmaxyx()[1]-2
	def height(self):
		"""return the height of the window (excluding border)"""
		return self.win.getmaxyx()[0]-2
	def redrawList(self):
		"""(re)draws the contact list"""
		for i,contact in enumerate(self.contactList[self.listShift:self.listShift+self.height()]):
			displayName=(contact['first_name']+' '+contact['last_name'])[:self.width()].ljust(self.width())
			
			if(i==self.selection-self.listShift):
				self.win.addstr(i+1,1,displayName,curses.A_REVERSE)
			else:
				self.win.addstr(i+1,1,displayName)
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
		self.redrawList()
	def prevContact(self):
		"""selects the previous contact in the list"""
		self.selection-=1
		# don't allow selections outside the list
		if(self.selection<0):
			self.selection=0
		# adjust list shift
		if(self.listShift > self.selection):
			self.listShift=self.selection
		self.redrawList()
	def getSelectedContact(self):
		"""returns the selected contact or None, if the list is empty or the selection is invalid"""
		if(0 < self.selection < len(self.contactList)):
			return self.contactList[self.selection]
		return None
class ChatWin:
	"""a curses representation of a telegram chat"""
	def __init__(self,mWin):
		height=mWin.getmaxyx()[0]
		width=mWin.getmaxyx()[1]-30
		self.win=mWin.subwin(height,width,0,30)
		self.win.border()
		self.win.refresh();
		self.ownNumber="4915141646942"
		self.linesPrint=0
	def width(self):
		"""return the width of the window (excluding border)"""
		return self.win.getmaxyx()[1]-2
	def height(self):
		"""return the height of the window (excluding border)"""
		return self.win.getmaxyx()[0]-2
	def redraw(self):
		"""redraws the chat"""
		for msg in reversed(self.msgs):
			sender=msg['from']
			senderName=(sender['first_name']+' '+sender['last_name']+':')[:self.width()]
			if(self.linesPrint < self.height()):
				# make sure we only print in available space
				self.win.addstr(self.height()-self.linesPrint,1,'    '+msg['text'])
				self.linesPrint+=1
			if(self.linesPrint < self.height()):
				# make sure we only print in available space
				if(self.ownNumber==sender['phone']):
					self.win.addstr(self.height()-self.linesPrint,1,senderName,curses.color_pair(1))
					self.linesPrint+=1
				else:
					self.win.addstr(self.height()-self.linesPrint,1,senderName,curses.color_pair(2))
					self.linesPrint+=1
		self.win.refresh()
	def loadChat(self,chatJson):
		"""loads the chat [chatJson] into the chat window"""
		self.msgs=json.loads(chatJson)
	def appendMessage(self,messageJson):
		"""appends [message] to the end of the chat"""
		self.msgs.append(json.loads(chatJson))
mWin=curses.initscr()
curses.noecho()
curses.cbreak()
mWin.keypad(True)
curses.start_color()

curses.init_pair(1,curses.COLOR_CYAN,curses.COLOR_BLACK)
curses.init_pair(2,curses.COLOR_GREEN,curses.COLOR_BLACK)



cl=ContactList(mWin)
cl.loadList(liste);

cw=ChatWin(mWin)
cw.loadChat(chat)
cw.redraw()

inp=mWin.getch()

while(inp == curses.KEY_UP or inp == curses.KEY_DOWN):
	if(inp==curses.KEY_UP):
		cl.prevContact()
	if(inp==curses.KEY_DOWN):
		cl.nextContact()
	inp=mWin.getch()

curses.nocbreak()
mWin.keypad(False)
curses.echo()
curses.endwin()

cl.getSelectedContact()
