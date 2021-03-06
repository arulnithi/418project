"""
The Parse class takes in a function and 
returns the breakdown of the function needed to write a C function.

The bodyList is given to the Formatter class to generate a C-style code.
"""

#Libraries needed
import ast
import inspect
import symtable

#Parser class
class Parser:


#====================================================================
#initializing class and getting an ast dump by inspecting it
#and checking it for correct function types
#====================================================================

  #Parser initilizer
  def __init__(self, args):
    function = args[0]
    #length of all lists
    self.length = args[1]
  	#Gives the function name
    self.functionName = function.__name__
  	#gives the source code as a string
    self.originalSourceCode = inspect.getsource(function)
  	#gives the source as a list, every line is an element
    self.listSourceCode = inspect.getsourcelines(function)[0]
  	#gives the starting line number of function in file
    self.startingLineNumber = inspect.getsourcelines(function)[1]
  	#gives the description of function which is written as comments on top
    self.description = inspect.getcomments(function)
  	#gives Python source file location of the function
    self.locationOfFolder = inspect.getsourcefile(function)
    self.fileName = self.locationOfFolder.split("/")[-1]
  	#turn the code into an AST
    self.astTree = ast.parse(self.originalSourceCode)
  	#input arguments list
    self.argList = []
    self.argValueList = args[2:]
  	#list of the complete body
    self.bodyList = []
  	#local variables list 
    self.localVariablesList = []
  	#for the first line
    self.firstLineOfFunction = "void " + self.functionName + "("
  	#already type casted variables
    self.typeCastedList = []
    self.returnType = ""

  	#CALLING all functions needed
    self.checkTree()
    self.parseArguments()
    self.typeCastedList = self.argList
    self.parseLocalVariables()
    self.parseBody()
    self.parseFirstLine()
    self.wrapper()

  	#PRINTABLE function call
  	#self.printArgs()
  	#self.printTree()


  #Prints all arguments of the kernel
  def printArgs(self):
  	print "Verbose output of Parser class arguments: "
  	print "\nLocation: ", self.locationOfFolder
  	print "\nFunction name: ", self.functionName, ",   Starting at line: ", self.startingLineNumber
  	print "\nFunction description: \n", self.description.rstrip('\n')
  	print "\nOriginal Source Code: \n", self.originalSourceCode.rstrip('\n')
  	print "\nSource Code in list form: \n", self.listSourceCode


  #Print the complete ast tree
  def printTree(self):
  	print ast.dump(self.astTree,annotate_fields=True, include_attributes=False) 


  #Check if the tree is valid
  # - no function calling function
  # - it is a function
  # - it is a valid module
  # - its name should match in the parsing
  def checkTree(self):
  	#check if it is a valid module at root
  	if not isinstance(self.astTree, ast.Module):
  		raise Exception("Not a valid module, it is a %s"%(root.__class__))
  	#iterate through the tree to check
  	for node in ast.iter_child_nodes(self.astTree):
  		#check if all nodes of tree are FunctionDef 
  		if not isinstance(node, ast.FunctionDef):
  			raise Exception("Not a Function Definition")
  		#check if all nodes have no decorators(function calling other functions)
  		if len(node.decorator_list) > 0:
  			raise Exception("Not a pure function")
  		#check if name is right
		if  node.name != self.functionName:
			raise Exception("Function Name does not match %s != %s"%(node.name,self.functionName))


#====================================================================
#Parsing the input arguments / local variables
#====================================================================

  #parses input arguments to function, 
  #as well as the default values
  def parseArguments(self):
  	for node in ast.iter_child_nodes(self.astTree):
  		#getting names of all arguments as strings
  		for arg in node.args.args:
  			self.argList.append(arg.id)
  		#getting default values of arguments if any
  		for values in node.args.defaults:
  			self.argValueList.append(values.n)



  #call only after parsing arguments
  #not exhaustive
  def parseLocalVariables(self):
  	table = symtable.symtable(self.originalSourceCode, "string", "exec")
  	tupleOfArgs = table.get_children()[0].get_locals()
  	for arg in tupleOfArgs:
  		if arg not in self.argList:
  			self.localVariablesList.append(arg)


#====================================================================
#Operations parser(x2) / BinOps parser / UnaryOp parser
#====================================================================


  def opsParser(self, body):
  	if isinstance(body, ast.Eq):
  		return "=="
  	elif isinstance(body, ast.NotEq):
  		return "!="
  	elif isinstance(body, ast.Lt):
  		return "<"
  	elif isinstance(body, ast.LtE):
  		return "<="
  	elif isinstance(body, ast.Gt):
  		return ">"
  	elif isinstance(body, ast.GtE):
  		return ">="
  	else:
  		raise Exception("Operation(ops) not supported: %s"%(body))


  def opParser(self, body):
  	if isinstance(body, ast.Add):
  		return "+"
  	elif isinstance(body, ast.Sub):
  		return "-"
  	elif isinstance(body, ast.Mult):
  		return "*"
  	elif isinstance(body, ast.Div):
  		return "/"
  	elif isinstance(body, ast.Mod):
  		return "%"
  	elif isinstance(body, ast.Pow):
  		return "**"
  	elif isinstance(body, ast.LShift):
  		return "<<"
  	elif isinstance(body, ast.RShift):
  		return ">>"
  	elif isinstance(body, ast.BitOr):
  		return "|"
  	elif isinstance(body, ast.BitXor):
  		return "^"
  	elif isinstance(body, ast.BitAnd):
  		return "&"
  	else:
  		raise Exception("Operation(op) not supported: %s"%(body))


  def binOpsParser(self, body):
  	returnString = ""
  	#left
  	returnString += self.bodyHandlerLiterals(body.left)[0]
  	#op
  	returnString += self.opParser(body.op)
  	#right
  	returnString += self.bodyHandlerLiterals(body.right)[0]
  	return returnString


  def unaryOpParser(self, body):
  	returnString = ""
  	#op
  	if isinstance(body.op, ast.UAdd):
  		returnString += "+"
  	elif isinstance(body.op, ast.USub):
  		returnString += "-"
  	elif isinstance(body.op, ast.Invert):
  		returnString += "~"
  	else:
  		raise Exception("Unary Operation not supported: %s"%(body.op))
  	#operand
  	returnString += self.bodyHandlerLiterals(body.operand)[0]
  	return returnString

#====================================================================
#Helper functions for parsing the body
#each helper should return a string
#which goes into a list
#====================================================================


  #Handles literals including Num, Str, List, Name
  #returns tuple of string of Literal and possible ctx(Name)
  def bodyHandlerLiterals(self, body):
    returnString = ""

  	#Name
    if isinstance(body, ast.Name):
      returnString += body.id
      if isinstance(body.ctx, ast.Load):
        return (returnString, "Load")
      elif isinstance(body.ctx, ast.Store):
        return (returnString, "Store")
      else:
        raise Exception("Literal Name's ctx not supported: %s"%(body.ctx))

  	#Num
    elif isinstance(body, ast.Num):
      returnString += str(body.n)
      return (returnString, None)

  	#Str
    elif isinstance(body, ast.Str):
      returnString += body.s
      return (returnString, None)

  	#List
    elif isinstance(body, ast.List):
      returnString += '['
      count = 0
      if len(body.elts) > 0:
        for value in body.elts:
          if count != 0:
            returnString += ','
          returnString += str(self.bodyHandlerLiterals(value)[0])
          count += 1
      returnString += ']'
      if isinstance(body.ctx, ast.Load):
        return (returnString, "Load")
      elif isinstance(body.ctx, ast.Store):
        return (returnString, "Store")
      else:
        raise Exception("Literal List's ctx not supported: %s"%(body.ctx))

    elif isinstance(body, ast.Subscript):
      returnString += self.bodyHandlerSubscript(body)
      return (returnString, None)
    
    elif isinstance(body, ast.BinOp):
      returnString += self.binOpsParser(body)
      return (returnString, None)

    elif isinstance(body, ast.Call):
      returnString += self.bodyHandlerCall(body)
      return (returnString, None)

    elif isinstance(body, ast.Attribute):
      returnString += self.bodyHandlerAttribute(body)
      return (returnString, None)

    elif isinstance(body, ast.None):
      return (returnString, None)

    #Unknown Literal
    else:
      raise Exception("Literal not supported: %s"%(body))


  #not handling more than 1 comparison
  def bodyHandlerCompare(self,body):
  	returnString = ""
  	#left (Name, Num, Str, List)
  	returnString += ((self.bodyHandlerLiterals(body.left)[0]))
  	#ops 
  	returnString += self.opsParser(body.ops[0])
  	#comparators 
  	returnString += (self.bodyHandlerLiterals(body.comparators[0])[0])
  	return returnString

  
  #only 1 argument allowed for now
  def bodyHandlerCall(self, body):
    returnString = ""
    returnString += self.bodyHandlerLiterals(body.func)[0]
    returnString += "("
    for count in xrange(len(body.args)):
      if count != 0:
        returnString += ","
      returnString += self.bodyHandlerLiterals(body.args[count])[0]
    # returnString += self.bodyHandlerLiterals(body.args[0])[0]
    returnString += ")"
    return returnString


  def bodyHandlerSubscript(self, body):
  	returnString = ""
  	#value (usually a name)
  	if isinstance(body.value, ast.Name):
  		returnString += self.bodyHandlerLiterals(body.value)[0]
  	else:
  		raise Exception("Subscript value not supported: %s"%(body.value))
  	#slice ( Index, Slice, ExtSlice(not supported) )
  	returnString += "["
  	if isinstance(body.slice, ast.Index):
  		returnString += self.bodyHandlerLiterals(body.slice.value)[0]
  	elif isinstance(body.slice, ast.Slice):
  		returnString += self.bodyHandlerLiterals(body.slice.lower)[0]
  		returnString += ":"
  		returnString += self.bodyHandlerLiterals(body.slice.upper)[0]
  		if body.slice.step != None:
  			returnString += ":" + self.bodyHandlerLiterals(body.slice.step)[0]
  	else:
  		raise Exception("Subscript.slice not supported: %s"%(body.slice))
  	returnString += "]"
  	#ctx (not needed for noe)
  	return returnString


  def bodyHandlerAttribute(self,body):
    if body.value.id != 'math':
      raise Exception("Only math library allowed currently, not %s"%(body.value.id))
    else:
      return body.attr

#====================================================================
#Handlers for Parsing the body
#each handler should return a list of strings
#which can be appended to the full string
#====================================================================


  def bodyHandlerIf(self, body, num):
  	returnList = []
  	returnList.append("")
  	if num==0:
  		returnList[0] += "if ("
  	else:
  		returnList[0] += "else if ("
  	#test
  	if isinstance(body.test, ast.Compare):
  		returnList[0] += (self.bodyHandlerCompare(body.test))
  	elif isinstance(body.test, ast.Num):
  		returnList[0] += ((self.bodyHandlerLiterals(body.test)[0]))
  	elif isinstance(body.test, ast.Name):
  		returnList[0] += ((self.bodyHandlerLiterals(body.test)[0]))
  	else:
  		raise Exception("If test type Unknown: %s"%(body.test))
  	returnList[0] += ") {"
  	#body*
  	for bodies in body.body:
  		if isinstance(bodies, ast.If):
  			returnList.append(self.bodyHandler(bodies))
  		else:
	  		tempList = []
	  		tempList.append(self.bodyHandler(bodies))
	  		returnList.append(tempList)
  	returnList.append("}")
  	#orelse*
  	if len(body.orelse) > 0:
  		#else if case
  		if isinstance(body.orelse[0], ast.If):
  			tempList = self.bodyHandlerIf(body.orelse[0],1)
  		#last case
  		else:
  			tempList = ["else {"]
  			tempList2 = []
  			tempList2.append(self.bodyHandler(body.orelse[0]))
  			tempList.append(tempList2)
  			tempList.append("}")
  		returnList = returnList + tempList
  	return returnList




  def bodyHandlerReturn(self, body):
    returnList = []
    returnList.append("")
    returnList[0] += "return "
    if isinstance(body.value, ast.BinOp):
      returnList[0] += self.binOpsParser(body.value)
    else:
      returnList[0] += self.bodyHandlerLiterals(body.value)[0]
      if self.bodyHandlerLiterals(body.value)[0] == 'None':
        returnList[0] = 'return '
  	returnList[0] += ";"
  	#for the firstLine
  	if self.returnType == "":
	  	if (isinstance(body.value, ast.Name) and body.value.id != 'None') or isinstance(body.value, ast.Num):
	  		self.returnType += "float "
	  	elif isinstance(body.value, ast.List):
	  		self.returnType += "float* "
	  	elif isinstance(body.value, ast.Str):
	  		self.returnType += "char"
	  	else:
	  		self.returnType += "void "
	  		#raise Exception("Return type not supported %s"%(body.value))
  	return returnList[0]


  def bodyHandlerAssign(self, body):
    returnList = []
  	#targets (list of target)
    for target in body.targets:
      if isinstance(target, ast.BinOp):
        if isinstance(body.value, ast.Name) or isinstance(body.value, ast.Num):
          if self.binOpsParser(target) not in self.typeCastedList:
            returnList.append("float ")
            returnList[0] += (self.binOpsParser(target))
            self.typeCastedList.append(self.binOpsParser(target))
          else:
            returnList.append(self.binOpsParser(target))
        else:
          returnList.append(self.binOpsParser(target))

      elif isinstance(target, ast.Name):
        if isinstance(body.value, ast.Name) or isinstance(body.value, ast.Num) or isinstance(body.value, ast.BinOp) or isinstance(body.value, ast.Subscript):
          if self.bodyHandlerLiterals(target)[0] not in self.typeCastedList:
            returnList.append("float ")
            returnList[0] += (self.bodyHandlerLiterals(target)[0])
            self.typeCastedList.append(self.bodyHandlerLiterals(target)[0])
          else:
            returnList.append(self.bodyHandlerLiterals(target)[0])
        else:
         returnList.append(self.bodyHandlerLiterals(target)[0])

      elif isinstance(target, ast.Str):
        returnList.append(self.bodyHandlerLiterals(target)[0])

      elif isinstance(target, ast.Subscript):
        returnList.append(self.bodyHandlerSubscript(target))
      
      else:
        raise Exception("Assignment not supported for target: %s"%(target))

  	#equal sign
    returnList[0] += "="

  	#value (single node, can be Name, Num, BinOp)
    if isinstance(body.value, ast.BinOp):
      returnList[0] += self.binOpsParser(body.value)

    elif isinstance(body.value, ast.Name) or isinstance(body.value, ast.Num) or isinstance(body.value, ast.List):
      returnList[0] += self.bodyHandlerLiterals(body.value)[0]

    elif isinstance(body.value, ast.Subscript):
      returnList[0] += self.bodyHandlerSubscript(body.value)
    
    elif isinstance(body.value, ast.Call):
      returnList[0] += self.bodyHandlerCall(body.value)
    else:
      raise Exception("Assign.value not supported %s"%(body.value))


    returnList[0] += ";"
    return returnList[0]


  def bodyHandlerAugAssign(self, body):
  	returnList = []
  	#target
  	if isinstance(body.target, ast.Subscript):
  		returnList.append(self.bodyHandlerSubscript(body.target))
  	else:
  		returnList.append(self.bodyHandlerLiterals(body.target)[0])
  	#op + equals sign
  	returnList[0] += self.opParser(body.op)+"="
  	#value
  	returnList[0] += (self.bodyHandlerLiterals(body.value)[0])
  	returnList[0] += ";"
  	return returnList[0]




  def bodyHandlerWhile(self, body):
  	returnList = []
  	returnList.append("")
  	returnList[0] += "while ("
  	#test
  	if isinstance(body.test, ast.Compare):
  		returnList[0] += (self.bodyHandlerCompare(body.test))
  	elif isinstance(body.test, ast.Num):
  		returnList[0] += ((self.bodyHandlerLiterals(body.test)[0]))
  	elif isinstance(body.test, ast.Name):
  		returnList[0] += ((self.bodyHandlerLiterals(body.test)[0]))
  	else:
  		raise Exception("While test type Unknown: %s"%(body.test))
  	returnList[0] += ") {"
  	#body*
  	for bodies in body.body:
  		if isinstance(bodies, ast.If):
  			returnList.append(self.bodyHandler(bodies))
  		else:
	  		tempList = []
	  		tempList.append(self.bodyHandler(bodies))
	  		returnList.append(tempList)
  	returnList.append("}")
  	#orelse* (ignore)
  	return returnList


  #only float interator allowed
  #assuming always xrange(actually range doesnt make a difference)
  def bodyHandlerFor(self,body):
  	returnList = [""]
  	returnList[0] += "for (int "
  	#target (only name)
  	returnList[0] += (self.bodyHandlerLiterals(body.target)[0])
  	returnList[0] += "="
  	#iter (1/2/3 arguments)
  	argumentList = []
  	for arg in body.iter.args:
  		if isinstance(arg, ast.Num):
  			argumentList.append(self.bodyHandlerLiterals(arg)[0])
  		elif isinstance(arg, ast.Name):
  			argumentList.append("("+self.bodyHandlerLiterals(arg)[0]+")")
  		elif isinstance(arg, ast.Call):
  			argumentList.append(self.bodyHandlerCall(arg))
  		else:
  			raise Exception("For loop iter not supported: %s"%(arg))
  	if len(argumentList) == 2:
  		argumentList.append('1')
  	elif len(argumentList) == 1:
  		argumentList.append('1')
  		argumentList = ["0"] + argumentList
  	elif len(argumentList) == 3:
  		pass
  	else:
  		raise Exception("For loop without correct number arguments: Length=%s"%(len(argumentList)))
  	returnList[0] += argumentList[0]
  	returnList[0] += "; "
  	returnList[0] += (self.bodyHandlerLiterals(body.target)[0])
  	returnList[0] += "<" + argumentList[1] + "; "
  	returnList[0] += (self.bodyHandlerLiterals(body.target)[0])
  	returnList[0] += "+= " + argumentList[2]
  	returnList[0] += ") {"
  	#body*
  	for bodies in body.body:
  		if isinstance(bodies, ast.If):
  			returnList.append(self.bodyHandler(bodies))
  		else:
	  		tempList = []
	  		tempList.append(self.bodyHandler(bodies))
	  		returnList.append(tempList)
  	#orelse* (ignore)
  	returnList.append("}")
  	return returnList



  def bodyHandlerBreak(self, body):
  	return "break;"


  def bodyHandlerContinue(self, body):
  	return "continue;"


  def bodyHandlerPrint(self, body):
    returnString = "std::cout"
    for value in body.values:
      returnString += " << "
      if isinstance(value, ast.Num):
        returnString += str(value.n) + ' << " " '
      elif isinstance(value, ast.Str):
        returnString += '"' + value.s + ' "' 
      elif isinstance(value, ast.Name):
        returnString += str(value.id) + ' << " " '
      elif isinstance(value, ast.Subscript):
        returnString += self.bodyHandlerSubscript(value) + ' << " " '
      else:
        raise Exception("Print type unsupported (%s)"%value)
    returnString += " << std::endl;"
    return returnString
#====================================================================
#Main Handler for Parsing the body
#should be a concatnation of lists
#====================================================================


  #Handle the different cases in the body
  def bodyHandler(self,body):
  	#different loop types
  	if isinstance(body, ast.If):
  		return self.bodyHandlerIf(body,0)
  	elif isinstance(body, ast.While):
  		return self.bodyHandlerWhile(body)
  	elif isinstance(body, ast.For):
  		return self.bodyHandlerFor(body)

  	#different assign types
  	elif isinstance(body, ast.Assign):
  		return self.bodyHandlerAssign(body)
  	elif isinstance(body, ast.AugAssign):
  		return self.bodyHandlerAugAssign(body)

  	#return body
   	elif isinstance(body, ast.Return):
  		return self.bodyHandlerReturn(body)

  	#print (hard to support, need typechecker somehow)
   	elif isinstance(body, ast.Print):
  		return self.bodyHandlerPrint(body)

  	# #loop modifiers
  	elif isinstance(body, ast.Break):
  		return self.bodyHandlerBreak(body)
   	elif isinstance(body, ast.Continue):
  		return self.bodyHandlerContinue(body)
  	#not parsable
  	else:
  		raise Exception("Body type not parsable: %s"%(body))

  #parse the body of the function
  def parseBody(self):
  	#go through the main body node
  	for node in ast.iter_child_nodes(self.astTree):
  		#pass it the handler
			for body in node.body:
				#unpack if If_
				if isinstance(body, ast.If) or isinstance(body, ast.For) or isinstance(body, ast.While):
					for l in self.bodyHandler(body):
						self.bodyList.append(l)
				else:
					self.bodyList.append(self.bodyHandler(body))
 


#====================================================================
#Handler for first+last line of function
#====================================================================

  def parseFirstLine(self):
  	for x in xrange(len(self.argValueList)):
  		if x != 0:
  			self.firstLineOfFunction += ","
  		if type(self.argValueList[x]).__name__ == "list":
  			self.firstLineOfFunction += "float*" + " " + self.argList[x]
  		else:
  			self.firstLineOfFunction += type(self.argValueList[x]).__name__ + " " + self.argList[x] #type(self.argValueList[x]).__name__
  	self.firstLineOfFunction += ") {"



#====================================================================
#Wrapper
#====================================================================

  def wrapper(self):
  	#changing return type
  	if self.returnType != "":
  		self.firstLineOfFunction = self.returnType + self.firstLineOfFunction[5:]
  	#adding new and last line
  	newList = [self.firstLineOfFunction]
  	newList.append(self.bodyList)
  	newList.append("}")
  	self.bodyList = newList




