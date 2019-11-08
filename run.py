﻿import sys
import subprocess
import os
from shutil import copyfile, rmtree, copy

userName = ""
listOfProbs = []
curProb = None
curProbName = ""        
submitFileName = ""

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
		exists = os.path.isfile(f'problems/{prob}/meta')
		if exists:
			p = parseMeta(f'problems/{prob}/meta')
			p['path'] = f'problems/{prob}'
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
		os.mkdir(f'Users/{userName}')
	except Exception as e:
		print(e)
	try:
		os.mkdir(f'Users/{userName}/{curProbName.get()}')
	except Exception as e:
		print(e)

def curProbFind():
	global curProb
	for i in listOfProbs:
		if i['name'] == curProbName.get():
			curProb = i

def makeTests():
	global curProbName
	userPathProb = initDir()
	try:
		gen.makeTests(userName.strip(), curProb, userPathProb)
	except Exception as e:
		print(e)

def copyInitFiles(userPathProb):
	src_files = os.listdir("commonFiles")
	for file_name in src_files:
		full_file_name = os.path.join("commonFiles", file_name)
		copy(full_file_name, userPathProb)

def initDir():
	makeDir()
	curProbFind()
	userPathProb = f'Users/{userName}/{curProbName.get()}'
	sys.path.insert(0, curProb['path'])
	import gen
	copyInitFiles(userPathProb)
	return userPathProb

def showStatement():
	global curProbName
	userPathProb = initDir()
	exists = os.path.isfile(f'{userPathProb}/statement.pdf')
	print(f"Statement is exists : {exists}")
	if exists:
		os.system(f'"{userPathProb}/statement.pdf"')
		return
	import gen
	if gen.makeState(userName.strip(), curProb, userPathProb):	
		os.system(f'"{userPathProb}/statement.pdf"')

def defineSubmitFileName(name, entry):
	entry.delete(0, END)
	entry.insert(0, askopenfilename())

def checkSol(sol, logsText):
	import time 
	logsText.config(state=NORMAL)
	logsText.delete("1.0", END)
	logsText.insert(END, "Solution is checking...")
	logsText.config(state=DISABLED)
	master.update()
	userPathProb = initDir()
	os.mkdir(f"{userPathProb}/files")	
	for i in curProb['files'].split(','):
		copyfile(f"{curProb['path']}/{i}", f"{userPathProb}/files/{i}")
	copyfile(sol, f"{userPathProb}/files/solution")
	import gen
	logsText.config(state=NORMAL)
	logsText.delete("1.0", END)
	logsText.insert(END, gen.checkSol(userName, curProb, userPathProb))
	logsText.config(state=DISABLED)
	rmtree(f'{userPathProb}/files')

def delProbFiles():
	curProbFind()
	userPathProb = f'Users/{userName}/{curProbName.get()}'
	rmtree(f"{userPathProb}")	

def makeAllFields():
	global master, curProbName, submitFileName
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
	deleteFilesButton = Button(master, text="Delete prob files", command=delProbFiles)
	deleteFilesButton.grid(row=1, column=3)


	chooseFileButton = Button(master, text="Choose File", command=lambda : defineSubmitFileName(submitFileName, chooseFileEntry))
	chooseFileButton.grid(row=2, column=0)
	chooseFileEntry = Entry(master, width=50)
	chooseFileEntry.grid(row=2, column=1)
	submitFileButton = Button(master, text="Submit", command=lambda : checkSol(chooseFileEntry.get(), logsText))
	submitFileButton.grid(row=3, column=1)
	logsText = Text(master, height=30, width=50, state=DISABLED)
	logsText.grid(row=4, column=1)



import os
from tkinter import *
from tkinter.filedialog import askopenfilename
master = Tk()
master.title("Rainbow Dragon alpha 0.1")
defineUser()
findAllProblems()
makeAllFields()
mainloop()