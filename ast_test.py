import math

#TESTTING ACTUAL
#blah blah
def foo(brg1,arg2):
  a = brg1[0]+2 + math.cos(0.4)
  return a


# print foo(1,2) #gives 4

from parser import *
from formatter import *

#should not have default option i guess
#int only (made all float)
#only can declare ints / cant handle bracket ops
#(handle calls for math) (think PI not supported)
#lists declared outside
#ATTRIBUTE in handle ltieral done
#change all to float? done 
#python to c ffi



#TESTING
parser = Parser(foo,5,[],2)
code = Formatter(parser, 'CPP')

print parser.argList
print code.returnCodeString()


# parser.printTree()
# print parser.bodyList
# print parser.fileName






