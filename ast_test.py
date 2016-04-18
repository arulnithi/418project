import math

#TESTTING ACTUAL
#blah blah
def foo(arg1,arg2):
  a = arg1+2 
  return a


# print foo(1,2) #gives 4

from parser import *
from formatter import *

#should not have default option i guess
#int only
#only can declare ints / cant handle bracket ops
#(handle calls for math)
#lists declared outside
#ATTRIBUTE in handle ltieral
#change all to float? done 
#python to c ffi



#TESTING
parser = Parser(foo,1,2)
code = Formatter(parser, 'CPP')
# print parser.argValueList
#CPP
code.formatTopLevel()
code.formatCPP(code.originalBodyList)
code.formatBotLevel()

print code.returnCodeString()


# parser.printTree()
# print parser.bodyList
# print parser.fileName






