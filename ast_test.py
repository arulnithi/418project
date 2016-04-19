import math

#TESTTING ACTUAL
#blah blah
def foo(brg1,arg2):
  a = brg1[0]+2 + math.cos(0.4)
  return a


from parser import *
from formatter import *


#TESTING
parser = Parser(foo,5,[],2)
code = Formatter(parser, 'CPP')

print parser.argList
print code.returnCodeString()


# parser.printTree()
# print parser.bodyList
# print parser.fileName






