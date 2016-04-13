"""
The Formatter class takes in the bodyList from the Parser
and based on the option passed in, outputs a code file.

Possible Options (in string):
CPP
CPP_CUDA
CPP_OpenMp
"""


#Formatter class
class Formatter:


  def __init__(self, parser, option):
    #the list to be parsed
    self.originalBodyList = parser.bodyList
    #the output code in a string
    self.codeString = "" 
    self.indentLevel = 0


  #use this to += a line to the formatter class
  def __iadd__(self, line):
  	self.add(line)
  	return self

  #how the line gets added based on the indent level
  def add(self, line):
  	self.codeString += self.setIndent()
  	self.codeString += line 
  	self.codeString += "\n"


  def setIndent(self):
  	return " " * self.indentLevel * 4


  def indent(self, value):
  	self.indentLevel += value
  	if self.indentLevel <0:
  		raise Exception("Indent level less than zero: level=%s"%(self.indentLevel))


  #/*    */, need to cut at like 80 char every line, optional
  def commentsFromPythonSource(self):
  	return

  
  #check indent level and return strin, not sure if needed
  def returnCodeString(self):
  	return


  #formatter for a cpp file
  def formatCPP(self, codeList):
  	for element in codeList:
  		if type(element) != list:
  			self.add(element)
  		else:
  			self.indent(1)
  			self.formatCPP(element)
  			self.indent(-1)




