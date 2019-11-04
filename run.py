import sys
import subprocess
import os
from shutil import copyfile, rmtree

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
		os.mkdir('Users/' + userName)
	except Exception as e:
		print(e)
	try:
		os.mkdir('Users/' + userName + '/' + curProbName.get())
	except Exception as e:
		print(e)

def curProbFind():
	global curProb
	for i in listOfProbs:
		if i['name'] == curProbName.get():
			curProb = i

def makeTests():
	global curProbName
	makeDir()
	curProbFind()
	userPathProb = 'Users/' + userName + '/' + curProbName.get() + '/'	
	sys.path.insert(0, curProb['path'])
	import gen
	try:
		os.mkdir(userPathProb + 'tests')
		gen.makeTests(userName.strip(), curProb['path'], userPathProb)
	except Exception as e:
		print(e)

def showStatement():
	global curProbName
	makeDir()
	curProbFind()
	userPathProb = 'Users/' + userName + '/' + curProbName.get() + '/'
	exists = os.path.isfile('' + userPathProb + 'statement.pdf')
	print(exists)
	if exists:
		os.system('"' + userPathProb + 'statement.pdf"')
		return
	makeTests()
	import gen
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
	
def defineSubmitFileName(name, entry):
	entry.delete(0, END)
	entry.insert(0, askopenfilename())

def checkSol(sol, logsText):
	makeDir()
	curProbFind()
	makeTests()
	userPathProb = 'Users/' + userName + '/' + curProbName.get()
	os.mkdir(f"{userPathProb}/files")	
	for i in curProb['files'].split(','):
		copyfile(f"{curProb['path']}{i}", f"{userPathProb}/files/{i}")
	copyfile(sol, f"{userPathProb}/files/solution")
	import gen
	logsText.config(state=NORMAL)
	logsText.delete("1.0", END)
	logsText.insert(END, gen.checkSol(curProb['path'], userPathProb))
	logsText.config(state=DISABLED)
	rmtree(f'{userPathProb}/files')
		

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