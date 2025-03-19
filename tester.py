import numpy as np
import sympy as sp
from sympy import *
import itertools


x = Symbol('x', real=False)
y = Symbol('y', real=False)
z = Symbol('z', real=False)
#t = Symbol('t', real=False)
#k = Symbol('k', real=False)

symbols = [x,y,z]
with evaluate(False):
	#spExpr = Array([[[x, y], [z, x*z]], [[1, x*y], [1/x, x/y]]])
	spExpr = x + y + z + 1
	
#Reading Symbols:
simboli = []
for i in spExpr.atoms(Symbol):
	simboli.append(i)
#simboli.sort()
#Trovare una soluzione al sorting dei simboli

stringhe = []
for i in simboli:
	stringhe.append(str(i))
	
print(stringhe)
stringhe.sort()
print(stringhe)
sorted_symbols = []
for i in stringhe:
	sorted_symbols.append(Symbol(i))

	

print(sorted_symbols)
#Some Checks:
print(simboli)



testRanges = {}

for symbol in sorted_symbols:
	if symbol.is_real:
		testRanges[symbol.name + '_re'] = np.arange(-1,1.1,0.5)
	else:
		testRanges[symbol.name + '_re'] = np.arange(-1,1.1,0.5)
		testRanges[symbol.name + '_im'] = np.arange(-1,1.1,0.5)

#Capire come gestire numeri solo immaginari

print(testRanges)




#Converto dizionario in una lista di arrays:
lista = list(testRanges.values())
#print(lista)

#print(lista[0][1])
results = []
# for t in range(len(lista)):
#     print(lista[t])
#     input()
#     for i in lista[0]:
#         for j in lista[1]:
#             for k in lista[2]:
#                 for l in lista[3]:
#                     for m in lista[4]:
#                         for n in lista[5]:
#                             res = spExpr.evalf(subs={x: m + n*I, y: k + l*I, z: i + j*I}).as_real_imag()
#                             print(res)
#                             results.append(res)
#                             input()


# for t in range(len(lista)-1):
#     for i in range(0, len(lista[t])):
#           for j in range(i, len(lista[i+t])):
#                 for k in range(0, len(lista[i+j+t])):
#                     for l in range(0, len(lista[k+i+j+t])):
#                         for m in range(0, len(lista[k+i+j+t+l])):
#                             for n in range(0, len(lista[k+i+j+t+l+m])):
#                                 res = spExpr.evalf(subs={x: m + n*I, y: k + l*I, z: i + j*I}).as_real_imag()
#                                 print(res)
#                                 results.append(res)
#                                 input()


for values in itertools.product(*lista):  # Genera tutte le combinazioni possibili
    i, j, k, l, m, n = values  # Estrai i valori secondo il numero di liste
    res = spExpr.evalf(subs={x: i + j*I, y: k + l*I, z: m + n*I}).as_real_imag()
    
     for spExptr in serializeExpr(self, expr):
		res = spExptr.evalf(subs={x: i + j*I, y: k + l*I, z: m + n*I}).as_real_imag

    		print(res)
    input()
    results.append(res)
	
#print(results)

          


def serializeExpr(self, expr):
	if expr.is_Matrix:
		for i in range(expr.shape[0]):
			for j in range(expr.shape[1]):
				yield expr[i,j]
	elif type(expr) == sp.tensor.array.dense_ndim_array.ImmutableDenseNDimArray:
		fl = sp.flatten(expr)
		for i in fl:
			yield i
	else:
		yield expr

