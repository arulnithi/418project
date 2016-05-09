import math
import time

#=============================================================
#MandelBrot Example with Timing, using CUDA-MAP
#=============================================================

def mandelbrotPy(c_re,c_im,maxiter=2048):
	z_re = c_re
	z_im = c_im
	for i in xrange(maxiter):
		if (z_re * z_re + z_im * z_im > 4.0):
			return i
		new_re = z_re*z_re - z_im*z_im
		new_im = 2 * z_re * z_im
		z_re = c_re + new_re
		z_im = c_im + new_im
	return maxiter

def mandelDemo(rArray,iArray,maxiter,height,width,output):
	c_re = rArray[index]
	c_im = iArray[index]
	z_re = c_re
	z_im = c_im
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
maxiter = 2048
x0 = -2.0
x1 = 0.5
y0 = -1.25
y1 = 1.25
height = 500
width = 500
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
blocksize = 256
startCuda = time.clock()
c = Compiler("CUDA-MAP",blocksize,mandelDemo,length,rArray,iArray,maxiter,height,width,output)
endCuda = (time.clock()-startCuda)*1000

startPyMap = time.clock()
pyResult = map(mandelbrotPy,rArray,iArray)
endPyMap = (time.clock()-startPyMap)*1000

startPyFor = time.clock()
pyForResult = []
for i in xrange(0,length):
	pyForResult.append(mandelbrotPy(rArray[i],iArray[i],maxiter))
endPyFor = (time.clock()-startPyFor)*1000


print("CUDA:%d, MAP:%d, FOR:%d"%(endCuda,endPyMap,endPyFor))




