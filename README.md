# 418project
CMU 15-418 Final Project

## Project Link to Github
http://ramverma92.github.io/418project/

## Current limitations of Python functions
1) Can't handle parantheses as higher priority math operation

2) Only works with floats currently, all ints converted to float, which is bad due to more space needed

3) All lists are float*

4) No support for list of lists, only basic element type


## Usage
To use the ParaPy module:

1) Add 'from compiler import *' to import the module

2) Write your Python function:

	def foo(arg1, arg2):
	    return

3) Call the Compiler class:

	arg1 = 1
	arg2 = 2
	c = Compiler('CUDA',foo,5,arg1,arg2)

	The inputs to the Compiler class are:

	Compiler(option, fn name, array max length, argument1, argument2,...)

## Options
### 'CPP'
	- standard conversion of Python code to C++ code
### 'CUDA'
	- will take any for loop with variable name == 'x'
	- will parallelize that for loop within the function
	- blocksize is set to *array max length*
### 'CUDA-MAP'
	-will translate the Python function to a CUDA function
	-will run the CUDA function on the collection of elements passed in as a list in *argument1*
