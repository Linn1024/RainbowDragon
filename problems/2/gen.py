from sys import argv
var = int(argv[1])
var = bin(var % 8)[2:]
fileTest = fopen("test", "w")
if var[0] == '0':
	print(randint(1, 100000))
else:
	print(chr(randint(30, 50)))
fopen.close()