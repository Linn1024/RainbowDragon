import os
import subprocess
rdFirstVarChose = ['int', 'char']
rdSecondVarChose = ['string', 'float']
rdDelimeterChose = [':', ';', '%']
rdFirstVar = ''
rdSecondVar = ''
rdDelimeterOne = ''
rdDelimeterTwo = ''
macroses = {}
upStr = ''
	
def makeState(name, filetex):
	global macroses, upStr
	makeVars(name)
#	print(f"Name: {name}, Upstr : {upStr}")
	stateTemp = open(filetex + '/statements.tex', encoding="UTF-8").readlines()
	probTemp = open(filetex + '/problem.tex', encoding="UTF-8").readlines()


	macroses['rdStudent'] = name
	macroses['rdName'] = "Считывание"
	rdFirstVarString = { 'int' : 'целое число n $(1 \\le n \\le 10^{10})$', 'char' : 'символ'}
	rdSecondVarString = { 'string':  'строка', 'float' : 'вещественное число f $(1 \\le f \\le 10^{10})$'}
	macroses['rdFirstVar'] = rdFirstVarString[rdFirstVar]
	macroses['rdSecondVar'] = rdSecondVarString[rdSecondVar]
	macroses['rdDelimeterOne'] = rdDelimeterOne
	macroses['rdDelimeterTwo'] = rdDelimeterTwo
	if rdDelimeterTwo == '%':
		macroses['rdDelimeterTwo'] = '\%'
	macrString = []
	for i in macroses:
		macrString.append('\\newcommand{\\' + i + '}{' + macroses[i] + '}\n')
	return [probTemp, macrString + stateTemp]

def makeVars(name):	
	global rdFirstVar, rdSecondVar, rdDelimeterOne, rdDelimeterTwo, upStr
	print(f"Upstr : {upStr}")
	rdFirstVar = rdFirstVarChose[hashStr(upStr, 31, 2)]         
	rdSecondVar = rdSecondVarChose[hashStr(upStr, 37, 2)]       
	rdDelimeterOne = rdDelimeterChose[hashStr(upStr, 41, 3)]    
	rdDelimeterTwo = rdDelimeterChose[hashStr(upStr, 41, 3) - 1]

def replaceSol(matchobj):
	return rdDelimeterOne if matchobj.groups()[0] == 'rdDelimeterOne' else rdDelimeterTwo

def makeSol(name, pathProb, pathUser):
	import re
	rep = re.compile("@(.*?)@")
	sol = open(pathProb + 'sol.py').readlines()
	solution = open(pathUser + 'solution.py', 'w')
	for i in sol:
		print(re.sub(rep, replaceSol, i), file=solution)	
		

def hashStr(s, p, MOD):
	h = 0
	for i in s:
		h = ((h * p) + ord(i) - ord('A')) % MOD
#	print(f"String : {s}, Hash : {h}")
	return h


num = 1
def makeTests(name, pathProb, pathUser):
	global num, upStr
	upStr = name.upper()
	num = 1
	makeVars(name)
	makeSol(name, pathProb, pathUser)
	from random import randint, random, seed
#	print(f"Upstr : {upStr}")
	seed(hashStr(upStr, 31, 20))
	def printTest(test):
		global num
		testFile = open(pathUser + 'tests/' + str(num), 'w')
		print(test, file=testFile)
		testFile.close()
		print('python' + ' "' + pathUser + 'solution.py" <"' + pathUser + 'tests/' + str(num) + '">"' + pathUser + 'tests/' + str(num) + '.a"')
		os.system('python' + ' "' + pathUser + 'solution.py" <"' + pathUser + 'tests/' + str(num) + '">"' + pathUser + 'tests/' + str(num) + '.a"')
		num += 1
	def randStr(n):
		ls = []
		for i in range(n):
			ls.append(chr(randint(0, 25) + ord('a')))
		return "".join(ls)
	def randChar():
		return str(chr(60 + randint(0, 60)))
	def randDouble():
		return str(random() * 10 ** 10)
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

def clearSol(name, pathProb, pathUser):
	os.remove(f"{pathUser}/check.cpp")
	os.remove(f"{pathUser}/check")
	os.remove(f"{pathUser}/sol.cpp")
	os.remove(f"{pathUser}/sol")
	os.remove(f"{pathUser}/out")





def checkSol(name, pathProb, pathUser):
	global num
	os.system(f"g++ {pathUser}/check.cpp")
	os.system(f"gcc {pathUser}/sol.c -O sol")
	for i in range(1, num + 1):
		os.system(f"{pathUser}/sol < tests/{i} > out")
		code, out, err = subprocess.run(["check", f"{pathUser}/tests/{i}", f"{pathUser}/out", f"{pathUser}/tests/{i}.a"])
		if code != 0:
			return f"You failed: {err}"
	return "OK, all tests passed"
