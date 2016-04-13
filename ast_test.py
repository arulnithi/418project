#TESTTING ACTUAL
#blah blah
def foo(arg1,arg2):
  #do something with args
  # if arg2<1:
  # 	a = arg1 + arg2
  # elif arg2 == 2:
  # 	a = 1
  # elif arg2 == 2:
  # 	a = 1
  # else:
  # 	a += 1
  #c = []
  a = 1
  b = 1
  arg1 = 1
  a = 2
  c = []
  return c


from parser import *

#should not have default option i guess
parser = Parser(foo,1,2)
# parser.printArgs()
# parser.printTree()


print parser.bodyList


