import math
import time
#=============================================================
#MandelBrot Example with Timing, using CUDA-MAP
#=============================================================

def saxpyCuda(x,y,alpha,output):
	output[index]=alpha * x[index] + y[index]

def saxpyPython(x,y,alpha=4):
	return alpha*x+y
	
#  #CUDA-MAP

from compiler import *

alpha = 4
x = range(1000012)
y = range(1000012)
output = []
blocksize = 256
startCuda = time.clock()
c = Compiler("CUDA-MAP",blocksize,saxpyCuda,len(x),x,y,alpha,output)
endCuda = (time.clock()-startCuda)*1000

startPyMap = time.clock()
pyResult = map(saxpyPython,x,y)
endPyMap = (time.clock()-startPyMap)*1000


print("CUDA:%d, MAP:%d"%(endCuda,endPyMap))




