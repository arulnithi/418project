"""
The Parse class takes in a function and 
returns the breakdown of the function needed to write a CUDA kernel
"""

#Libraries needed
import ast
import inspect

#Parser class
class Parser:

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


  #parse the body of the function
  def parseBody(self):
	return   	 

