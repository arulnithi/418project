import ast
import inspect   # print inspect.cleandoc(foo)
import dis
#from dill.source import getsource    #not downloaded    # print dis.dis(foo)

##AST EXAMPLE 1
# code = "a=1"
# tree = ast.parse(code)  # turn the code into an AST
# print ast.dump(tree)  # view it as a string

##AST EXAMPLE 2
# fib_src = "def fib(n):"
# fib_src += "return n if n< 2 else fib(n-1) + fib(n-2)"
# tree = ast.parse(fib_src)
# print ast.dump(tree)

#TESTTING INSPECT
def foo(arg1,arg2):
    #do something with args
    a = arg1 + arg2
    return a
# print inspect.getsourcelines(foo)
# print inspect.getdoc(foo)
# print inspect.getcomments(foo)
# print inspect.getfile(foo)
# print inspect.getmodule(foo)
# print inspect.getsourcefile(foo)
# print inspect.getsource(foo)


#TESTTING ACTUAL
#blah blah
def foo(arg1=2,arg2=1):
    #do something with args
    if 1:
    	a = arg1 + arg2
    return a


from parser import *

parser = Parser(foo)
#parser.printArgs()
code = parser.originalSourceCode
parser.checkTree()
# parser.printTree()
parser.parseArguments()


print parser.argValueList, parser.argList

# for node in ast.iter_child_nodes(parser.astTree):
# 	# print ast.iter_fields(node)
# 	# print node._fields
# 	for arg in node.args.args:
# 		print "J",arg.id, type(arg.id)
# 		print arg.ctx
# 	for gg in node.args.defaults:
# 		print gg.n
# 	# for stmt in node.body:
# 	# 	print stmt










