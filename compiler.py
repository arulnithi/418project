"""
Compiler class takes the output string from the Formatter class,
and compiles using the appropriate flags.

Gives timing information as well.

Returns result using FFI/output.txt? (TBD)
"""

#Libraries needed
import datetime
import os
import subprocess



#other files needed
from parser import *
from formatter import *

class Compiler:

	def __init__(self, *args):
		#read arguments
		self.option = args[0]
		self.parseOptions = list(args[1:])
		#call the parser
		self.parser = Parser(self.parseOptions)
		#call the formatter
		self.formatted = Formatter(self.parser, self.option)
		#the file name to be compiled
		self.fileName = ""

		#execute the functions needed to compile
		# self.writeToFile()
		# self.buildFile()


	#prints the output string to be written onto file
	def printCodeString(self):
		print self.formatted.returnCodeString()


	#print the AST tree
	def printTree(self):
		self.parser.printTree()

	#prints the body of the function as a list
	def printBodyList(self):
		print self.parser.bodyList


	#write code string to a file (file type based on option)
	def writeToFile(self):
		#get name of file
		now = datetime.datetime.now().strftime("%H%Mhrs_%Y_%m_%d")  
		fileName = "parapy_"+str(self.parser.fileName).split(".py")[0] + "_"+ now
		if "CUDA" in self.option:
			fileName += ".cu"
		else:
			fileName += ".cpp"
		#write to file
		os.system("touch "+fileName)
		f = open(fileName, 'w')
		f.write(self.formatted.returnCodeString())
		f.close()
		self.fileName = fileName


	#depending on the option, compile with the correct flags
	#how to return output?
	def buildFile(self):
		# os.system("touch out.txt")
		#generate the scriptlines
		scriptLine1 = ""
		scriptLine2 = "./output" #  >> out.txt
		if "CUDA" in self.option:
			scriptLine1 += "nvcc " + self.fileName + " -o" + " output" 
		else:
			scriptLine1 += "c++ "  + self.fileName + " -o" + " output"
		#running the scriptlines
		# p = Popen([scriptLine1], stdout=PIPE, stdin=PIPE, stderr=PIPE)
		# stdoutData = p.communicate(scriptLine2)
		# #check for errors
		# if stdoutData[1] != "":
		# 	print "Error in compilation:\n",stdoutData[1]
		# 	return
		# else:
		# 	#get back output somehow
		# 	print stdoutData[0]
		subprocess.call(scriptLine1.split(" "))
		subprocess.call(scriptLine2)




