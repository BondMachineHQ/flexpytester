import numpy as np
import sympy as sp
from sympy import *
import itertools
import subprocess
import re 


x = Symbol('x', real=False)
y = Symbol('y', real=False)
z = Symbol('z', real=False)
#t = Symbol('t', real=False)
#k = Symbol('k', real=False)

symbols = [x,y,z]
with evaluate(False):
	#spExpr = Array([[[x, y], [z, x*z]], [[1, x*y], [1/x, x/y]]])
	spExpr = x + y + z + 1
	
# Definiamo una funzione generica
def evaluate_expression(spExpr, variables, lista):

    results = []
    for values in itertools.product(*lista):  # It generates all possible combination of values
        subs_dict = {} #That's the dictionary i have to provide to evalf 
        for var, (val_r, val_i) in zip(variables, zip(*[iter(values)]*2)):
            subs_dict[var] = val_r + val_i * sp.I
        res = spExpr.evalf(subs=subs_dict).as_real_imag()
        results.append(res)
    return results

single_vslue = [y, x, z]
lista = [[-1.0, -0.5, 0.0, 0.5, 1.0], [-2.0, -0.3, 0.1, 3, 5], [4,3,1,1,1], [2,6,8,3,1], [7,7,3,5,3], [-2,3,4,0,5]]

res = evaluate_expression(spExpr, single_vslue, lista)

for i in res:
     print(i)
     input()


