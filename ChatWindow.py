import curses
import json
import textwrap

class ChatWindow:
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
