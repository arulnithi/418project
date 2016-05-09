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


# #WRITE FUNCTION AS IF IT RUNS ON THE FIRST ELEMENT
# def foo(alpha,x,y,result):
# 	index = 0
# 	result[index]= alpha * x[index] + y[index]
# 	print "hi"
	
# #  #CUDA-MAP

# from compiler import *
# alpha = 2
# x = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
# y = [1,2,3,4,2,4,2,63,4,7,4,8,3,1,2,5,1,5,2,2]
# ret = []
# c = Compiler("CPP",foo,len(x),alpha,x,y,ret)

# c.printCodeString()
# # c.printTree()









def mandelbrot(rArray,iArray,maxiter,height,width,output):
	c_re = rArray[index]
	c_im = iArray[index]
	z_re = c_re
	z_im = c_im
	result = 0
	for i in xrange(maxiter):
		if (z_re * z_re + z_im * z_im > 4.0):
			output[index]= i
			return None
		new_re = z_re*z_re - z_im*z_im
		new_im = 2 * z_re * z_im
		z_re = c_re + new_re
		z_im = c_im + new_im
	output[index]= maxiter
	
#  #CUDA-MAP

from compiler import *
maxiter = 80
x0 = -2.0
x1 = 0.5
y0 = -1.25
y1 = 1.25
height = 100
width = 100
dx = (x1-x0)/height
dy = (y1-y0)/width
rArray = []
iArray = []
length = height * width
for x in xrange(0,height):
	for y in xrange(0,width):
		rArray.append(x0+ dx*x)
		iArray.append(y0 + dy*y)

output = []
c = Compiler("CUDA-MAP",mandelbrot,length,rArray,iArray,maxiter,height,width,output)
c.printCodeString()

