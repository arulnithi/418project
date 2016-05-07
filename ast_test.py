import math

#TESTTING ACTUAL
#blah blah
def foo(brg1,arg2):
	for x in xrange(5):
		for y in xrange(100):
			brg1[x] = arg2[x] +1
	


# from parser import *
# from formatter import *


# #only use x to distribute across wraps
# length of list (not always neccessary?)

# #TESTING
# parser = Parser(foo,5,[1,2,3,4,5],2)
# #print parser.bodyList
# code = Formatter(parser, 'CUDA')

# # print parser.argList
# print code.returnCodeString()


# parser.printTree()
# print parser.bodyList
# print parser.fileName

from compiler import *
lol = [1,2,3,4,5]
c = Compiler("CUDA", foo, 5,lol,[])

# c.printCodeString()
# c.printBodyList()





