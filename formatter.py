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

    #execute formatting based on option
    if option == "CPP":
      self.formatTopLevelCPP()
      self.formatBodyLevelCPP(self.originalBodyList)
      self.formatBotLevelCPP()
    elif option == "CUDA":
      self.formatTopLevelCU()
      self.formatBodyLevelCU(self.originalBodyList)
      self.formatBotLevelCU()
    else:
      raise Exception("Formatting option not available (%s)"%option)


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


#====================================================================
#CPP
#====================================================================

  #formatter function for a cpp file
  def formatBodyLevelCPP(self, codeList):
    #adding code
    for element in codeList:
  		if type(element) != list:
  			self.add(element)
  		else:
  			self.indent(1)
  			self.formatBodyLevelCPP(element)
  			self.indent(-1)


  
  def formatTopLevelCPP(self):
    #add the comments
    self.add("//Function %s parsed from %s"%(self.parser.functionName,self.parser.fileName))
    self.add("")
    #add the libraries
    self.add("#include <stdio.h>")
    self.add("#include <math.h>")
    self.add("")
    #add defines
    self.add("#define pi 3.14159265")
    self.add("")


  def formatBotLevelCPP(self):
    #seperate out the main function
    self.add("") 
    #go through arguments to be passed in
    args = ""
    malloc = []
    free = []
    for x in xrange(len(self.parser.argValueList)):
      if x != 0:
        args += ","
      if (len(str(self.parser.argValueList[x]))>2) and str(self.parser.argValueList[x])[0]=='[' and str(self.parser.argValueList[x])[-1]==']':
        args += str(self.parser.argList[x])
        oldString = str(self.parser.argValueList[x])
        newString = "{" + oldString[1:-1] + "}"
        mallocString = "float %s []=%s;"%(self.parser.argList[x],newString)
        malloc.append(mallocString)
        free.append("free("+str(self.parser.argList[x])+");")
      elif str(self.parser.argValueList[x]) != "[]":
        args += str(self.parser.argValueList[x])
      else:
        args += str(self.parser.argList[x])
        mallocString = "%s=(float*)malloc(%s*sizeof(float));"%(self.parser.argList[x],self.parser.length)
        malloc.append(mallocString)
        free.append("free("+str(self.parser.argList[x])+");")
    #add the main function now
    self.add("float main() {")
    self.indent(1)
    self.add('printf("STARTING MAIN FUNCTION\\n");')
    #allocate memory
    for m in malloc:
      self.add(m)
    #call the function
    self.add("%s(%s);"%(self.parser.functionName,args))
    #free memory
    for f in free:
      self.add(f)
    #return
    self.add("return 0;")
    self.indent(-1)
    self.add("}")


#====================================================================
#CUDA
#====================================================================

#go through string, if [], change the index
#if there are for/while loops, set range to 1 if the iterator is only for []

  #formatter function for a cpp file
  def formatBodyLevelCU(self, codeList):
    #adding code
    for element in codeList:
      if type(element) != list:
        #first line of function
        if (self.parser.functionName in element) and (") {" in element):
          self.add("__global__ " + element)
          #add checker for threadIdx.x
          self.indent(1)
          self.add("if (threadIdx > %s) {"%self.parser.length)
          self.indent(1)
          self.add("return;")
          self.indent(-1)
          self.add("}")
          self.indent(-1)
        #for loop which needs to be manually set to 1
        elif ("for " in element) and ("x=" in element) and ("x+" in element):
          l = element.split(";")
          l[1] = "x<1"
          newElement = ";".join(l)
          self.add(newElement)
        #index x set to threadIdx.x
        elif ("[x]" in element):
          l = element.split("[x]")
          newL = [l[0],"[threadIdx.x]",l[1]]
          self.add("".join(newL))
        #non special case
        else:
          self.add(element)
      else:
        self.indent(1)
        self.formatBodyLevelCU(element)
        self.indent(-1)

  
  def formatTopLevelCU(self):
    #add the comments
    self.add("//Function %s parsed from %s"%(self.parser.functionName,self.parser.fileName))
    self.add("")
    #add the libraries
    self.add("#include <stdio.h>")
    self.add("#include <math.h>")
    self.add("")
    #add defines
    self.add("#define pi 3.14159265")
    self.add("")


  def formatBotLevelCU(self):
    #seperate out the main function
    self.add("") 
    #go through arguments to be passed in
    args = ""
    malloc = []   
    cudaMalloc = []  #to add a character at the end to differentiate the variable from malloc
    free = []
    blockSize = self.parser.length
    for x in xrange(len(self.parser.argValueList)):
      if x != 0:
        args += ","
      if (len(str(self.parser.argValueList[x]))>2) and str(self.parser.argValueList[x])[0]=='[' and str(self.parser.argValueList[x])[-1]==']':
        args += str(self.parser.argList[x]) + "Cuda"
        oldString = str(self.parser.argValueList[x])
        newString = "{" + oldString[1:-1] + "}" #to handle declaration in C++
        mallocString = "float %s []=%s;"%(self.parser.argList[x],newString)
        cudaMalloc.append(self.parser.argList[x]);
        malloc.append(mallocString)
        free.append("free("+str(self.parser.argList[x])+");")
      elif str(self.parser.argValueList[x]) != "[]":
        args += str(self.parser.argValueList[x])
      else:
        args += str(self.parser.argList[x])
        mallocString = "%s=(float*)malloc(%s*sizeof(float));"%(self.parser.argList[x],self.parser.length)
        malloc.append(mallocString)
        free.append("free("+str(self.parser.argList[x])+");")
    #add the main function now
    self.add("int main() {")
    self.indent(1)
    self.add('printf("STARTING MAIN FUNCTION\\n");')
    self.add("")
    self.add("//Define constants to use")
    self.add("const int N = %d;"%blockSize)
    self.add("const int blocksize = %d;"%blockSize)
    self.add("")
    self.add("//Allocate the variables")
    #allocate memory
    for m in malloc:
      self.add(m)
    self.add("")
    self.add("//Declare and allocate the variables and copy it over to device")
    #declare cuda variables
    for name in cudaMalloc:
      self.add("float *%s;"% (name + "Cuda"))
    self.add("const int csize = N*sizeof(float);")

    #cudaMalloc
    for name in cudaMalloc:
      self.add("cudaMalloc( (void**)&%s, csize );"%(name + "Cuda"))

    #cudaMemCpy
    for name in cudaMalloc:
      self.add("cudaMemcpy( %s, %s, csize, cudaMemcpyHostToDevice );"%((name + "Cuda"),name))
    
    self.add("")
    self.add("//Setup variables for cuda block and grid and then call function")
    self.add("dim3 dimBlock( blocksize, 1 );")
    self.add("dim3 dimGrid( 1, 1 );")

    #call the function
    self.add("%s<<<dimGrid, dimBlock>>>(%s);"%(self.parser.functionName,args))
    self.add("")
    self.add("//Free allocated memory")
    #cudaFree
    for name in cudaMalloc:
      self.add("cudaFree( %s );"%(name + "Cuda"))
    #free memory
    for f in free:
      self.add(f)
    #return
    self.add("return 0;")
    self.indent(-1)
    self.add("}")

#====================================================================
#OpenMP
#====================================================================
