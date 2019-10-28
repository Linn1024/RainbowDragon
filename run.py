import sys
import subprocess
import os
from shutil import copyfile

userName = ""
listOfProbs = []
curProb = None
curProbName = ""

class Problem:
	def __init__(self):
		self.props = {}
	def __getitem__(self, i):
		return self.props[i]
	def __setitem__(self, i, v):
		self.props[i] = v

def parseMeta(fileName):
	p = Problem()
	f = open(fileName, encoding="UTF-8").readlines()
	for i in f:
		i = i.strip()
		a, b = i.split('=')
		p[a] = b
	return p


def findAllProblems():
	global listOfProbs
	listOfProbsFiles = next(os.walk("problems"))[1]
	for prob in listOfProbsFiles:
		exists = os.path.isfile('problems/' + prob + '/meta')
		if exists:
			p = parseMeta('problems/' + prob + '/meta')
			p['path'] = 'problems/' + prob + '/'
			print(p.props)
			listOfProbs.append(p)
	    	


def defineUser():
	global userName
	try:
		userFile = open("user", "r", encoding="UTF-8")
		userName = userFile.readline().strip()
	except:
		print("No user defined")


def changeUserName(nameEntry):
	global userName
	userName = str(nameEntry.get())
	nameEntry.configure(state='readonly')
	userFile = open("user", "w", encoding="UTF-8")
	print(userName, file=userFile)
	userFile.close()
	try:
		makeDir()
	except Exception as e:
		print(e)

def makeDir():
	try:
		os.mkdir('Users/' + userName + '/' + curProbName.get())
	except Exception as e:
		print(e)
def curProbFind():
	global curProb
	for i in listOfProbs:
		if i['name'] == curProbName.get():
			curProb = i

def showStatement():
	global curProbName
	makeDir()
	curProbFind()
	userPathProb = 'Users/' + userName + '/' + curProbName.get() + '/'
	exists = os.path.isfile('"' + userPathProb + 'statement.pdf"')
	print(exists)
	if exists:
		os.system(userPathProb + 'statement.pdf"')
		return
	sys.path.insert(0, curProb['path'])
	import gen
	os.mkdir(userPathProb + 'tests')
	gen.makeTests(userName.strip(), curProb['path'], userPathProb)
	resProb, resState = gen.makeState(userName.strip(), curProb['path'])
	probFile = open(userPathProb + 'problem.tex', 'w', encoding="UTF-8")
	stateFile = open(userPathProb + 'statement.tex', 'w', encoding="UTF-8")
	print(*resProb, file=probFile)
	print(*resState, file=stateFile)
	copyfile("makeStatement/task.sty", userPathProb + 'task.sty')
	probFile.close()
	stateFile.close()
	print('pdflatex "' + userPathProb + 'statement.tex"')
	os.system('cd "' + userPathProb + '" && pdflatex statement.tex')
	os.system('"' + userPathProb + 'statement.pdf"')
	
	

def makeAllFields():
	global master, curProbName
	nameEntry = Entry(master)
	nameEntry.grid(row=0, column=0)
	nameEntry.insert(0, userName)
	if userName != "":
		nameEntry.configure(state='readonly')
	nameOKButton = Button(master, text="OK", command=lambda : changeUserName(nameEntry))
	nameOKButton.grid(row=0, column=1)
	nameChangeButton = Button(master, text="Change", command=lambda : nameEntry.configure(state='normal'))
	nameChangeButton.grid(row=0, column=2)
	curProbName = StringVar(master)
	optionMenuProblems = OptionMenu(master, curProbName, *[x['name'] for x in listOfProbs])
	optionMenuProblems.grid(row=0, column=3)
	showStatementButton = Button(master, text="Show statement", command=showStatement)
	showStatementButton.grid(row=1, column=1)

import os
from tkinter import *
master = Tk()
defineUser()
findAllProblems()
makeAllFields()
mainloop()