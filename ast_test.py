import ast
import inspect   # print inspect.cleandoc(foo)
import dis
#from dill.source import getsource    #not downloaded    # print dis.dis(foo)

##AST EXAMPLE 1
# code = "a=1"
# tree = ast.parse(code)  # turn the code into an AST
# print ast.dump(tree)  # view it as a string

##AST EXAMPLE 2
# fib_src = "def fib(n):"
# fib_src += "return n if n< 2 else fib(n-1) + fib(n-2)"
# tree = ast.parse(fib_src)
# print ast.dump(tree)

#TESTTING INSPECT
# def foo(arg1,arg2):
#     #do something with args
#     a = arg1 + arg2
#     return a
# print inspect.getsourcelines(foo)
# print inspect.getdoc(foo)
# print inspect.getcomments(foo)
# print inspect.getfile(foo)
# print inspect.getmodule(foo)
# print inspect.getsourcefile(foo)
# print inspect.getsource(foo)





