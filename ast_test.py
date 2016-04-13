import math

#TESTTING ACTUAL
#blah blah
def foo(arg1,arg2):
  #a = cos(0.5)
  if arg1 > 1:
  	arg2 += 1
  else:
  	arg1 -= 1
  return arg1+arg2


from parser import *
from formatter import *

#should not have default option i guess
#int only
#only can declare ints 
#(handle calls for math)
#lists declared outside

#python to c ffi



#TESTING
parser = Parser(foo,1,2)


# print parser.bodyList
# print parser.fileName


code = Formatter(parser, 'CPP')
code.formatCPP(code.originalBodyList)
print code.codeString