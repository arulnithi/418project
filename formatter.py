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
    #parser class
    self.parser = parser
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
  	return self.codeString


  #formatter function for a cpp file
  def formatCPP(self, codeList):
    #adding code
    for element in codeList:
  		if type(element) != list:
  			self.add(element)
  		else:
  			self.indent(1)
  			self.formatCPP(element)
  			self.indent(-1)


  
  def formatTopLevel(self):
    #add the comments
    self.add("//Function %s parsed from %s"%(self.parser.functionName,self.parser.fileName))
    self.add("")
    #add the libraries
    self.add("#include <stdio.h>")
    self.add("#include <math.h>")
    self.add("")
    #add defines
    self.add("#define PI 3.14159265")
    self.add("")


  def formatBotLevel(self):
    #seperate out the main function
    self.add("") 
    #go through arguments to be passed in
    args = ""
    for x in xrange(len(self.parser.argValueList)):
      if x != 0:
        args += ","
      args += str(self.parser.argValueList[len(self.parser.argValueList)-x-1])
    #add the main function now
    self.add("float main() {")
    self.indent(1)
    self.add('printf("STARTING MAIN FUNCTION\\n");')
    self.add("return %s(%s);"%(self.parser.functionName,args))
    #self.add("return 0;")
    self.indent(-1)
    self.add("}")

