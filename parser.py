"""
The Parse class takes in a function and 
returns the breakdown of the function needed to write a CUDA kernel
"""

#Libraries needed
import ast
import inspect


#Parser class
class Parser:


#====================================================================
#initializing class and getting an ast dump by inspecting it
#and checking it for correct function types
#====================================================================

  #Parser initilizer
  def __init__(self, function):
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
    #turn the code into an AST
    self.astTree = ast.parse(self.originalSourceCode)
    #input arguments list
    self.argList = []
    self.argValueList = []
    #list of the complete body
    self.bodyList = []


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
#Parsing the input arguments
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
  	#set the argValueList with None for non default args
  	while (len(self.argValueList)!=len(self.argList)):
  		self.argValueList.append(None)
  	self.argValueList = self.argValueList[::-1]



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
  	returnString += self.bodyHandlerLiterals(body.args[0])[0]
  	returnString += ")"
  	return returnString


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
  	returnList[0] += self.bodyHandlerLiterals(body.value)[0]
  	returnList[0] += ";"
  	return returnList[0]


  def bodyHandlerAssign(self, body):
  	returnList = []
  	#targets (list of target)
  	for target in body.targets:
  		if isinstance(target, ast.BinOp):
  			returnList.append(self.binOpsParser(target))
  		elif isinstance(target, ast.Name) or isinstance(target, ast.Str):
  			returnList.append(self.bodyHandlerLiterals(target)[0])
  		else:
  			raise Exception("Assignment not supported for target: %s"%(target))
  	#equal sign
  	returnList[0] += "="
  	#value (single node, can be Name, Num, BinOp)
  	if isinstance(body.value, ast.BinOp):
  		returnList[0] += self.binOpsParser(body.value)
  	elif isinstance(body.value, ast.Name) or isinstance(body.value, ast.Num) or isinstance(body.value, ast.List):
  		returnList[0] += self.bodyHandlerLiterals(body.value)[0]
  	returnList[0] += ";"
  	return returnList[0]


  def bodyHandlerAugAssign(self, body):
  	returnList = []
  	#target
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


  #only int interator allowed
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

  	# #print
   # 	elif isinstance(body, ast.Print):
  	# 	self.bodyHandlerPrint(body)

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
 

