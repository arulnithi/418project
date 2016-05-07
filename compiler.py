"""
Compiler class takes the output string from the Formatter class,
and compiles using the appropriate flags.

Gives timing information as well.

Returns result using FFI/output.txt? (TBD)
"""

#Libraries needed


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


	#prints the output string to be written onto file
	def printCodeString(self):
		print self.formatted.returnCodeString()


	#print the AST tree
	def printTree(self):
		self.parser.printTree()

	#prints the body of the function as a list
	def printBodyList(self):
		print self.parser.bodyList


	#writes to file, depending on option, compiles with the correct flags, 
	#how to return output?

