import math

#TESTTING ACTUAL
#blah blah
# def foo(brg1,arg2):
# 	for x in xrange(5):
# 		for y in xrange(100):
# 			brg1[x] = arg2[x] +1
	


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

# from compiler import *
# lol = [1,2,3,4,5]
# c = Compiler("CUDA", foo, 5,lol,[])

# c.printCodeString()
# c.printBodyList()


#WRITE FUNCTION AS IF IT RUNS ON THE FIRST ELEMENT
def foo(alpha,x,y,result):
	index = 0
	result[index]= alpha * x[index] + y[index]
	
#  #CUDA-MAP

from compiler import *
alpha = 2
x = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
y = [1,2,3,4,2,4,2,63,4,7,4,8,3,1,2,5,1,5,2,2]
ret = []
c = Compiler("CUDA-MAP",foo,20,alpha,x,y,ret)




