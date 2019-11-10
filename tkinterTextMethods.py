from tkinter import *
def init(self, text="", color="BLACK"):
	self.tag_config(f"{color}", foreground=color)
	self.config(state=NORMAL)

def close(self):
	self.config(state=DISABLED)
	self.master.update()
	
def setText(self, text, color="BLACK"):
	init(self, text, color)
	self.delete("1.0", END)
	self.insert(END, text, color)
	close(self)


def addLine(self, text, color="BLACK"):
	init(self, text, color)
	self.insert(END, text + '\n', color)
	close(self)


def addWord(self, text, color="BLACK"):
	init(self, text, color)
	self.insert(END, text + ' ', color)
	close(self)


def clear(self):
	init(self)
	self.delete("1.0", END)
	close(self)