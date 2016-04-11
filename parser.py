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
#Operations parser
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
  		raise Exception("Operation not supported: %s"%(body))


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
  		for value in body.elts.n:
  			if count != 0:
  				returnString += ','
  			returnString += str(value)
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



#====================================================================
#Handlers for Parsing the body
#each handler should return a list of strings
#which can be appended to the full string
#====================================================================


  def bodyHandlerIf(self, body):
  	returnList = []
  	returnList.append("")
  	returnList[0] += "if "
  	#test
  	if isinstance(body.test, ast.Compare):
  		returnList[0] += (self.bodyHandlerCompare(body.test))
  	elif isinstance(body.test, ast.Num):
  		returnList[0] += ((self.bodyHandlerLiterals(body.test)[0]))
  	elif isinstance(body.test, ast.Name):
  		returnList[0] += ((self.bodyHandlerLiterals(body.test)[0]))
  	else:
  		raise Exception("If test type Unknown: %s"%(body.test))
  	#body
  	#orelse
  	return returnList


  def bodyHandlerReturn(self, body):
  	returnList = []
  	returnList.append("")
  	returnList[0] += "return "
  	returnList[0] += self.bodyHandlerLiterals(body.value)[0]
  	return returnList

#====================================================================
#Main Handler for Parsing the body
#should be a concatnation of lists
#====================================================================


  #Handle the different cases in the body
  def bodyHandler(self,body):
  	#different loop types
  	if isinstance(body, ast.If):
  		return self.bodyHandlerIf(body)
  	# elif isinstance(body, ast.While):
  	# 	self.bodyHandlerWhile(body)
  	# elif isinstance(body, ast.For):
  	# 	self.bodyHandlerFor(body)

  	# #different assign types
  	# elif isinstance(body, ast.Assign):
  	# 	self.bodyHandlerAssign(body)
  	# elif isinstance(body, ast.AugAssign):
  	# 	self.bodyHandlerAugAssign(body)

  	# #return body
   	elif isinstance(body, ast.Return):
  		return self.bodyHandlerReturn(body)

  	# #print
   # 	elif isinstance(body, ast.Print):
  	# 	self.bodyHandlerPrint(body)

  	# #loop modifiers
  	# elif isinstance(body, ast.Break):
  	# 	self.bodyHandlerBreak(body)
   # 	elif isinstance(body, ast.Continue):
  	# 	self.bodyHandlerContinue(body)
  	#not parsable
  	else:
  		raise Exception("Body type not parsable: %s"%(body))

  #parse the body of the function
  def parseBody(self):
  	#go through the main body node
  	for node in ast.iter_child_nodes(self.astTree):
  		#pass it the handler
		for body in node.body:
			self.bodyList.append( self.bodyHandler(body)   )
			#need to recurse outwards/inwards for bodies within bodies 	 

