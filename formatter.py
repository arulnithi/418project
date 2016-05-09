"""
The Formatter class takes in the bodyList from the Parser
and based on the option passed in, outputs a code file.

Possible Options (in string):
CPP
CUDA
"""


#Formatter class
class Formatter:


  def __init__(self, *args):
    #formatting for a function with inputs
    if len(args) > 0:
      #parser class
      self.parser = args[0]
      #the list to be parsed
      self.originalBodyList = args[0].bodyList
      #specified blockSize
      self.blocksize = args[2]
      #the output code in a string
      self.codeString = "" 
      self.indentLevel = 0

      option = args[1]
      #execute formatting based on option
      if option == "CPP":
        self.formatTopLevelCPP()
        self.formatBodyLevelCPP(self.originalBodyList)
        self.formatBotLevelCPP()
      elif option == "CUDA":
        self.formatTopLevelCU()
        self.formatBodyLevelCU(self.originalBodyList)
        self.formatBotLevelCU()
      elif option == "CUDA-MAP":
        self.formatTopLevelCUMAP()
        self.formatBodyLevelCUMAP(self.originalBodyList)
        self.PPIFunctionCUMAP()
        self.mandelFunctionCUMAP()
        self.formatBotLevelCUMAP()
      else:
        raise Exception("Formatting option not available (%s)"%option)
    #in case of writing a function with no inputs
    else:
      self.codeString = "" 
      self.indentLevel = 0


  #use this to += a line to the formatter class
  def __iadd__(self, line):
    self.add(line)
    return self

  #how the line gets added based on the indent level
  def add(self, line):
    self.codeString += self.setIndent()
    self.codeString += line 
    self.codeString += "\n"


  def setIndent(self):
    return " " * self.indentLevel * 4


  def indent(self, value):
    self.indentLevel += value
    if self.indentLevel <0:
      raise Exception("Indent level less than zero: level=%s"%(self.indentLevel))


  #/*    */, need to cut at like 80 char every line, optional
  def commentsFromPythonSource(self):
    return

  
  #check indent level and return strin, not sure if needed
  def returnCodeString(self):
    return self.codeString


#====================================================================
#CPP
#====================================================================

  #formatter function for a cpp file
  def formatBodyLevelCPP(self, codeList):
    #adding code
    for element in codeList:
      if type(element) != list:
        self.add(element)
      else:
        self.indent(1)
        self.formatBodyLevelCPP(element)
        self.indent(-1)


  
  def formatTopLevelCPP(self):
    #add the comments
    self.add("//Function %s parsed from %s"%(self.parser.functionName,self.parser.fileName))
    self.add("")
    #add the libraries
    self.add("#include <stdio.h>")
    self.add("#include <math.h>")
    self.add("#include <stdlib.h>")
    self.add('#include <iostream>')
    self.add('#include <algorithm>')
    self.add('#include <cstudio>')
    self.add('#include <ctime>')
    self.add("")
    #add defines
    self.add("#define pi 3.14159265")
    self.add("")


  def formatBotLevelCPP(self):
    #seperate out the main function
    self.add("") 
    #go through arguments to be passed in
    args = ""
    malloc = []
    free = []
    for x in xrange(len(self.parser.argValueList)):
      if x != 0:
        args += ","
      if (len(str(self.parser.argValueList[x]))>2) and str(self.parser.argValueList[x])[0]=='[' and str(self.parser.argValueList[x])[-1]==']':
        args += str(self.parser.argList[x])
        oldString = str(self.parser.argValueList[x])
        newString = "{" + oldString[1:-1] + "}"
        mallocString = "float %s [%s]=%s;"%(self.parser.argList[x],self.parser.length,newString)
        malloc.append(mallocString)
        #free.append("free ("+str(self.parser.argList[x])+");")
      elif str(self.parser.argValueList[x]) != "[]":
        args += str(self.parser.argValueList[x])
      else:
        args += str(self.parser.argList[x])
        mallocString = "float* %s=(float*)malloc(%s*sizeof(float));"%(self.parser.argList[x],self.parser.length)
        malloc.append(mallocString)
        free.append("free ("+str(self.parser.argList[x])+");")
    #add the main function now
    self.add("int main() {")
    self.indent(1)
    self.add('printf("STARTING MAIN FUNCTION\\n");')
    #allocate memory
    for m in malloc:
      self.add(m)
    #call the function
    self.add("%s(%s);"%(self.parser.functionName,args))
    #free memory
    for f in free:
      self.add(f)
    #return
    self.add("return 0;")
    self.indent(-1)
    self.add("}")


#====================================================================
#CUDA
#====================================================================

#go through string, if [], change the index
#if there are for/while loops, set range to 1 if the iterator is only for []

  #formatter function for a cpp file
  def formatBodyLevelCU(self, codeList):
    #adding code
    for element in codeList:
      if type(element) != list:
        #first line of function
        if (self.parser.functionName in element) and (") {" in element):
          self.add("__global__ " + element)
          #add checker for threadIdx.x
          self.indent(1)
          self.add("if (threadIdx.x >= %s) {"%self.parser.length)
          self.indent(1)
          self.add("return;")
          self.indent(-1)
          self.add("}")
          self.indent(-1)
        #for loop which needs to be manually set to 1
        elif ("for " in element) and ("x=" in element) and ("x+" in element):
          l = element.split(";")
          l[1] = "x<1"
          newElement = ";".join(l)
          self.add(newElement)
        #index x set to threadIdx.x
        elif ("[x]" in element):
          l = element.split("[x]")
          newL = ("[threadIdx.x]").join(l)
          self.add("".join(newL))
        #non special case
        else:
          self.add(element)
      else:
        self.indent(1)
        self.formatBodyLevelCU(element)
        self.indent(-1)

  
  def formatTopLevelCU(self):
    #add the comments
    self.add("//Function %s parsed from %s"%(self.parser.functionName,self.parser.fileName))
    self.add("")
    #add the libraries
    self.add("#include <stdio.h>")
    self.add("#include <math.h>")
    self.add("#include <stdlib.h>")
    self.add('#include <iostream>')
    self.add('#include <algorithm>')
    self.add('#include <cstudio>')
    self.add('#include <ctime>')
    self.add("")
    #add defines
    self.add("#define pi 3.14159265")
    self.add("")


  def formatBotLevelCU(self):
    #seperate out the main function
    self.add("") 
    #go through arguments to be passed in
    args = ""
    malloc = []   
    cudaMalloc = []  #to add a character at the end to differentiate the variable from malloc
    free = []
    blockSize = self.parser.length
    for x in xrange(len(self.parser.argValueList)):
      if x != 0:
        args += ","
      if (len(str(self.parser.argValueList[x]))>2) and str(self.parser.argValueList[x])[0]=='[' and str(self.parser.argValueList[x])[-1]==']':
        args += str(self.parser.argList[x]) + "Cuda"
        oldString = str(self.parser.argValueList[x])
        newString = "{" + oldString[1:-1] + "}" #to handle declaration in C++
        mallocString = "float %s [%s]=%s;"%(self.parser.argList[x],self.parser.length,newString)
        cudaMalloc.append(self.parser.argList[x]);
        malloc.append(mallocString)
        #free.append("free ("+str(self.parser.argList[x])+");")
      elif str(self.parser.argValueList[x]) != "[]":
        args += str(self.parser.argValueList[x])
      else:
        args += str(self.parser.argList[x])
        mallocString = "float* %s=(float*)malloc(%s*sizeof(float));"%(self.parser.argList[x],self.parser.length)
        malloc.append(mallocString)
        free.append("free ("+str(self.parser.argList[x])+");")
    #add the main function now
    self.add("int main() {")
    self.indent(1)
    self.add('printf("STARTING MAIN FUNCTION\\n");')
    self.add("")
    self.add("//Define constants to use")
    self.add("const int N = %d;"%blockSize)
    self.add("const int blocksize = %d;"%blockSize)
    self.add("")
    self.add("//Allocate the variables")
    #allocate memory
    for m in malloc:
      self.add(m)
    self.add("")
    self.add("//Declare and allocate the variables and copy it over to device")
    #declare cuda variables
    for name in cudaMalloc:
      self.add("float *%s;"% (name + "Cuda"))
    self.add("const int csize = N*sizeof(float);")

    #cudaMalloc
    for name in cudaMalloc:
      self.add("cudaMalloc( (void**)&%s, csize );"%(name + "Cuda"))

    #cudaMemCpy
    for name in cudaMalloc:
      self.add("cudaMemcpy( %s, %s, csize, cudaMemcpyHostToDevice );"%((name + "Cuda"),name))
    
    self.add("")
    self.add("//Setup variables for cuda block and grid and then call function")
    self.add("dim3 dimBlock( blocksize, 1 );")
    self.add("dim3 dimGrid( 1, 1 );")

    #call the function
    self.add("%s<<<dimGrid, dimBlock>>>(%s);"%(self.parser.functionName,args))
    self.add("")
    self.add("//Free allocated memory")
    #cudaFree
    for name in cudaMalloc:
      self.add("cudaFree( %s );"%(name + "Cuda"))
    #free memory
    for f in free:
      self.add(f)
    #return
    self.add("return 0;")
    self.indent(-1)
    self.add("}")


#====================================================================
#CUDA-MAP
#====================================================================

 
  #formatter function for a cpp file
  def formatBodyLevelCUMAP(self, codeList):
    #adding code
    for element in codeList:
      if type(element) != list:
        #first line of function
        if (self.parser.functionName in element) and (") {" in element):
          self.add("__global__ " + element)
          #add checker for threadIdx.x
          self.indent(1)
          newElement = "int index = blockIdx.x * blockDim.x + threadIdx.x;"
          self.add(newElement)
          self.add("if (index >= %s) {"%self.parser.length)
          self.indent(1)
          self.add("return;")
          self.indent(-1)
          self.add("}")
          self.indent(-1)
          
        #index x set to threadIdx.x
        elif ("float index" in element) and ('=' in element) and ('0' in element):
          pass
        else:
          # if element == 'float index=0;':
          self.add(element)
      else:
        self.indent(1)
        self.formatBodyLevelCUMAP(element)
        self.indent(-1)

  
  def formatTopLevelCUMAP(self):
    #add the comments
    self.add("//Function %s parsed from %s"%(self.parser.functionName,self.parser.fileName))
    self.add("")
    #add the libraries
    self.add("#include <stdio.h>")
    self.add("#include <math.h>")
    self.add("#include <stdlib.h>")
    self.add('#include <iostream>')
    self.add('#include <algorithm>')
    self.add('#include <cstudio>')
    self.add('#include <ctime>')
    self.add("")
    #add defines
    self.add("#define pi 3.14159265")
    self.add("")


  def formatBotLevelCUMAP(self):
    #seperate out the main function
    self.add("") 
    #go through arguments to be passed in
    args = ""
    malloc = []   
    cudaMalloc = []  #to add a character at the end to differentiate the variable from malloc
    free = []
    N = self.parser.length
    blocksize = self.blockSize
    for x in xrange(len(self.parser.argValueList)):
      if x != 0:
        args += ","
      if (len(str(self.parser.argValueList[x]))>2) and str(self.parser.argValueList[x])[0]=='[' and str(self.parser.argValueList[x])[-1]==']':
        args += str(self.parser.argList[x]) + "Cuda"
        oldString = str(self.parser.argValueList[x])
        newString = "{" + oldString[1:-1] + "}" #to handle declaration in C++
        mallocString = "float %s [%s]=%s;"%(self.parser.argList[x],self.parser.length,newString)
        cudaMalloc.append(self.parser.argList[x]);
        malloc.append(mallocString)
        #free.append("free ("+str(self.parser.argList[x])+");")
      elif str(self.parser.argValueList[x]) != "[]":
        args += str(self.parser.argValueList[x])
      else:
        args += str(self.parser.argList[x]) + "Cuda"
        cudaMalloc.append(self.parser.argList[x]);
        mallocString = "float* %s=(float*)malloc(%s*sizeof(float));"%(self.parser.argList[x],self.parser.length)
        malloc.append(mallocString)
        free.append("free ("+str(self.parser.argList[x])+");")
    #add the main function now
    self.add("int main() {")
    self.indent(1)
    self.add('printf("STARTING CUDA FUNCTION\\n");')
    self.add("")
    self.add("//Define constants to use")
    self.add("const int N = %d;"%N)
    self.add("const int blocksize = %d;"%blocksize)
    self.add("")
    self.add("//Allocate the variables")
    #allocate memory
    for m in malloc:
      self.add(m)
    self.add("")
    self.add("//Declare and allocate the variables and copy it over to device")
    #declare cuda variables
    for name in cudaMalloc:
      self.add("float *%s;"% (name + "Cuda"))
    self.add("const int csize = N*sizeof(float);")
    #cudaMalloc
    for name in cudaMalloc:
      self.add("cudaMalloc( (void**)&%s, csize );"%(name + "Cuda"))
    #cudaMemCpy
    for i in xrange(0,len(cudaMalloc)-1):
      name = cudaMalloc[i]
      self.add("cudaMemcpy( %s, %s, csize, cudaMemcpyHostToDevice );"%((name + "Cuda"),name))
    
    self.add("")
    self.add("//Setup variables for cuda block and grid and then call function")
    self.add("dim3 dimBlock( blocksize, 1 );")
    #INCLUDE MAX NO THREADS  >>> dim3 numBlocks((MAX_NO_OF_THREADS-1+numCircles)/MAX_NO_OF_THREADS);
    self.add("dim3 dimGrid( ((N + blocksize - 1) / blocksize), 1 );")

    #timer
    self.add('std::clock_t start;')
    self.add('double duration;')
    self.add('start = std::clock();')
    #call the function
    self.add("%s<<<dimGrid, dimBlock>>>(%s);"%(self.parser.functionName,args))
    self.add('duration = ( std::clock() - start ) / (double) CLOCKS_PER_SEC;')
    self.add("")
    self.add("//Copy back result data")
    self.add("cudaMemcpy(%s, %s, N * sizeof(float), cudaMemcpyDeviceToHost);"%(str(self.parser.argList[len(self.parser.argValueList)-1]),str(self.parser.argList[len(self.parser.argValueList)-1])+"Cuda"))
    self.add("")

    #for mandelbrot
    tempName = self.parser.functionName.lower()
    if 'mandelbrot' in tempName:
      self.add('//Print out mandel image')
      self.add('mandel(output);')
      self.add('')

    self.add("")
    self.add("//Free allocated memory")
    #cudaFree
    for name in cudaMalloc:
      self.add("cudaFree( %s );"%(name + "Cuda"))
    #free memory  
    for f in free:
      self.add(f)
    self.add('printf("ENDING CUDA FUNCTION\\n");')
    std::cout<<"printf: "<< duration <<'\n';
    #return
    self.add("return 0;")
    self.indent(-1)
    self.add("}")


  #for mandel print image
  def PPIFunctionCUMAP(self):
    #space
    self.add('')
    self.add('')
    #body
    self.add('//Function taken from assignment 1, 15-418, CMU')
    self.add('void writePPMImage(float* data, int width, int height, const char *filename, int maxIterations) {')
    self.indent(1)
    self.add('FILE *fp = fopen(filename, "wb");')
    self.add('fprintf(fp, "P6\\n");')
    self.add('fprintf(fp, "%d %d\\n", width, height);')
    self.add('fprintf(fp, "255\\n");')
    self.add('for (int i = 0; i < width*height; ++i) {')
    self.indent(1)
    self.add('float mapped = pow( std::min(static_cast<float>(maxIterations),static_cast<float>(data[i])) / 256.f, .5f);')
    self.add('unsigned char result = static_cast<unsigned char>(255.f * mapped);')
    self.add('for (int j = 0; j < 3; ++j)')
    self.indent(1)
    self.add('fputc(result, fp);')
    self.indent(-1)
    self.indent(-1)
    self.add('}')
    self.add('fclose(fp);')
    self.add('printf("Wrote image file %s\\n", filename);')
    self.indent(-1)
    self.add('}')
    #space
    self.add('')
    self.add('')


  #for mandel call functions
  def mandelFunctionCUMAP(self):
    self.add('')
    self.add('//Call the PPIF function if needed') #Explain function
    self.add('void mandel(float* output) {') #Start of function
    self.indent(1)
    #maxiter,height,width
    w = '0'
    h = '0'
    m = '0'
    if 'width' in self.parser.argList:
      w = str(self.parser.argValueList[self.parser.argList.index('width')])
    if 'height' in self.parser.argList:
      h = str(self.parser.argValueList[self.parser.argList.index('height')])
    if 'maxiter' in self.parser.argList:
      m = str(self.parser.argValueList[self.parser.argList.index('maxiter')])
    self.add('int width = %s;'%w)
    self.add('int height = %s;'%h)
    self.add('int maxiter = %s;'%m)
    #call the function
    self.add('writePPMImage(output, width, height, "mandel.ppm", maxiter);')
    self.indent(-1)
    self.add('}') #End of function
    self.add('')

#====================================================================
#OpenMP
#====================================================================
