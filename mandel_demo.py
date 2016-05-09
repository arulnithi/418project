import math
import time
import numpy as np
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

def mandelbrot_numpy(c, maxiter):
    output = np.zeros(c.shape)
    z = np.zeros(c.shape, np.complex64)
    for it in range(maxiter):
        notdone = np.less(z.real*z.real + z.imag*z.imag, 4.0)
        output[notdone] = it
        z[notdone] = z[notdone]**2 + c[notdone]
    output[output == maxiter-1] = 0
    return output

def mandelbrot_setNumPy(r1,r2,maxiter):
    c = r1 + r2[:,None]*1j
    n3 = mandelbrot_numpy(c,maxiter)
    return (r1,r2,n3.T) 

def mandelCuda(rArray,iArray,maxiter,output):
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
height = 400
width = 400
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
c = Compiler("CUDA-MAP",blocksize,mandelCuda,length,rArray,iArray,maxiter,output)
endCuda = (time.clock()-startCuda)*1000

startPyMap = time.clock()
pyResult = map(mandelbrotPy,rArray,iArray)
endPyMap = (time.clock()-startPyMap)*1000


r1 = np.linspace(x0, x1, width, np.float32)
r2 = np.linspace(y0, y1, height, np.float32)
startNumPy = time.clock()
mandelbrot_setNumPy(r1,r2,2048)
endNumPy = (time.clock()-startNumPy)*1000


print("CUDA:%d, MAP:%d,NUMPY:%d"%(endCuda,endPyMap,endNumPy))




