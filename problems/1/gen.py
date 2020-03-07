import os
import subprocess
from tkinter import *
rdFirstVarChose = ['int', 'char']
rdSecondVarChose = ['string', 'float']
rdDelimeterChose = [':', ';', '%']
rdFirstVar = ''
rdSecondVar = ''
rdDelimeterOne = ''
rdDelimeterTwo = ''
macroses = {}
upStr = ''
	
def makeButtons(master):
	tmp = StringVar(master)
	langOptionMenu = OptionMenu(master, tmp, *['python', 'c'])
	langOptionMenu.grid(row=5, column=4)
	return tmp

def removeButtons(master):
	langOptionMenu

def makeState(name, curProb, userPathProb, logsText):
	global macroses, upStr
	logsText.setText("Statement is building")
	makeTests(name, curProb, userPathProb)
	makeVars(name)
#	print(f"Name: {name}, Upstr : {upStr}")
	stateTemp = open(f"{curProb['path']}/statements.tex", encoding="UTF-8").readlines()
	probTemp = open(f"{curProb['path']}/problem.tex", encoding="UTF-8").readlines()
	macroses['rdStudent'] = name
	macroses['rdName'] = "Считывание"
	rdFirstVarString = { 'int' : 'целое число n $(1 \\le n \\le 10^{10})$', 'char' : 'символ'}
	rdSecondVarString = { 'string':  'строка', 'float' : 'вещественное число f $(1 \\le f \\le 10^{5}) с двумя знаками после запятой$'}
	macroses['rdFirstVar'] = rdFirstVarString[rdFirstVar]
	macroses['rdSecondVar'] = rdSecondVarString[rdSecondVar]
	macroses['rdDelimeterOne'] = rdDelimeterOne
	macroses['rdDelimeterTwo'] = rdDelimeterTwo
	if rdDelimeterTwo == '%':
		macroses['rdDelimeterTwo'] = '\%'
	macrString = []
	for i in macroses:
		macrString.append('\\newcommand{\\' + i + '}{' + macroses[i] + '}\n')
	
	resProb, resState = probTemp, macrString + stateTemp
	probFile = open(f"{userPathProb}/problem.tex", 'w', encoding="UTF-8")
	stateFile = open(f"{userPathProb}/statement.tex", 'w', encoding="UTF-8")
	print("".join(resProb), file=probFile)
	print("".join(resState), file=stateFile)
	probFile.close()
	stateFile.close()
	os.chdir(f"{userPathProb}")
	logsText.clear()
#	print(" ".join(['cd', f"{userPathProb}", "&&", "pdflatex", "statement.tex"]))
	subprocess.run(["pdflatex", "statement.tex"])
	os.chdir('../../../')
	return True


def makeVars(name):
	global rdFirstVar, rdSecondVar, rdDelimeterOne, rdDelimeterTwo, upStr
	rdFirstVar = rdFirstVarChose[hashStr(upStr, 31, 2)]
	rdSecondVar = rdSecondVarChose[hashStr(upStr, 37, 2)]
	rdDelimeterOne = rdDelimeterChose[hashStr(upStr, 41, 3)]
	rdDelimeterTwo = rdDelimeterChose[hashStr(upStr, 41, 3) - 1]

def replaceSol(matchobj):
	return rdDelimeterOne if matchobj.groups()[0] == 'rdDelimeterOne' else rdDelimeterTwo

def makeSol(name, curProb, pathUser):
	import re
	rep = re.compile("@(.*?)@")
	sol = open(f"{curProb['path']}/sol.py").readlines()
	solution = open(f"{pathUser}/solution.py", 'w')
	for i in sol:
		print(re.sub(rep, replaceSol, i), file=solution)	
		

def hashStr(s, p, MOD):
	h = 0
	for i in s:
		h = ((h * p) + ord(i) - ord('A')) % MOD
#	print(f"String : {s}, Hash : {h}")
	return h


num = 0
def makeTests(name, curProb, pathUser):
	global num, upStr
	try:
		os.mkdir(f"{pathUser}/tests")
	except Exception as e:
		num = len(os.listdir(f"{pathUser}/tests")) // 2
		print(f"NUM :::::::::::: num")
		print(e)
		return
	upStr = name.upper()
	num = 0
	makeVars(name)
	makeSol(name, curProb, pathUser)
	from random import randint, random, seed
#	print(f"Upstr : {upStr}")
	seed(hashStr(upStr, 31, 20))
	def printTest(test):
		global num
		testFile = open(pathUser + '/tests/' + str(num), 'w')
		print(test, file=testFile)
		testFile.close()
		print('python' + ' "' + pathUser + '/solution.py" <"' + pathUser + '/tests/' + str(num) + '">"' + pathUser + '/tests/' + str(num) + '.a"')
		subprocess.run(["python", f"{pathUser}/solution.py"], stdin=open(f"{pathUser}/tests/{num}"), stdout=open(f"{pathUser}/tests/{num}.a", "w"))
		num += 1
	def randStr(n):
		ls = []
		for i in range(n):
			ls.append(chr(randint(0, 25) + ord('a')))
		return "".join(ls)
	def randChar():
		return str(chr(60 + randint(0, 60)))
	def randDouble():
		d = str(int(random() * 10 ** 7) / 10 ** 2)
		d += '0' * (3 - len(d) + d.find('.'))
		return d
	if rdFirstVar == 'int':
		rdTestOne = lambda : str(randint(1, 10 ** 10))
	else:
		rdTestOne = randChar
	if rdSecondVar == 'string':
		rdTestTwo = lambda : randStr(randint(1, 10))
	else:
		rdTestTwo = randDouble
	for i in range(10):
		#print(rdTestOne, rdDelimeterOne, rdTestTwo)
		printTest(rdTestOne() + rdDelimeterOne + rdTestTwo())

def compileCode(tools, config):
	if tools.get() == "python":
		pass
	elif tools.get() == "c":
		p = subprocess.run([config['c'], '-x', 'c', 'solution.send', '-o', 'sol'], capture_output=True)
		if p.returncode != 0:
			return p.stderr.decode("utf-8")
	else:
		return "Choose your programming language"
	return None

def runCode(tools, config, inputData):
	if tools.get() == "python":
		return subprocess.run([config["python"], "solution.send"], input=inputData, capture_output=True)	
	elif tools.get() == "c":
		return subprocess.run("sol", input=inputData, capture_output=True)	


def checkSol(name, curProb, pathUser, logsText, tools, config):
	retString = ""
	global num
	print(tools)
	logsText.clear()
	makeTests(name, curProb, pathUser)
	os.chdir(f"{pathUser}/files")
	compileErr = compileCode(tools, config)
	if compileCode(tools, config) is not None:
		logsText.setText(compileErr, color="RED")
		os.chdir('../../../../')			
		return "Compilation error"
#	os.system("g++ check.cpp -o check")
	subprocess.run(['g++', 'check.cpp', '-o', 'check'])
#	subprocess.run(['gcc', '-x', 'c++', 'solution.send', '-o', 'sol'])
	print(f"NUM :       {num}")
	for i in range(num):
#		subprocess.run(["echo", "%cd%"], shell=True)
#		inputFile = open(f"../tests/{i}")
		output = runCode(tools, config, open(f"../tests/{i}", "rb").read())
		if output.returncode != 0:
			logsText.addLine(f'Return code {output.returncode}: {output.stderr.decode("utf-8")}', color="RED")
			retString = "Runtime Error"
			break
		outFile = open("out", "wb")
		outFile.write(output.stdout)
		outFile.close()
		logsText.addLine(f"Checking test {i}...")
		res = subprocess.run(['check', f'../tests/{i}', f'out', f'../tests/{i}.a'], capture_output=True)
		if res.returncode != 0:
			logsText.addLine(res.stderr.decode("utf-8"), color="RED")
			retString = "Failed"
			break
		logsText.addLine("OK", color="GREEN")
	else:
		retString = "OK, all tests passed"
	os.chdir('../../../../')
	return retString
