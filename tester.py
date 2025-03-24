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

#function to execute: flexpy -e expression.txt --basm --iomap-only
#output should be: an ordered list of symbols
def Symbol_extractor(text_file):

	command = ["flexpy", "-e", text_file, "--basm", "--iomap-only"]
	try:
		pos_real = {}
		pos_imag = {}
		result = subprocess.run(command, capture_output=True, text=True, check=True)
		output_lines = result.stdout.strip().split('\n')

		if len(output_lines) >=2:
			first_line = output_lines[0]
			exec("first_line_array = " + first_line)
			
			for i in range(len(first_line_array)):
				s = first_line_array[i]
				if s.startswith('real: '):
					s=s[6:]
					pos_real[s] = i
				elif s.startswith('imag: '):
					s=s[6:]
					pos_imag[s] = i

			values = []

			for item in first_line_array:
				values.append(item.split(': ')[1])

			single_values = list(set(values))
			return single_values, pos_real, pos_imag	
		else:
			return "Error: Unexpected output format."
	except subprocess.CalledProcessError as e:
		return f"Error executing command: {e.stderr}"
	except FileNotFoundError:
		return "Error: 'flexpy' command not found. Ensure it is installed and in your PATH."
	

def creation_test_ranges(diz1 , diz2 , text_file):
	ranges = []
	#creation of an array of 0s with the same length of the sum of the input dictionaries dimentions
	for i in range(len(diz1)+len(diz2)):
		ranges.append(0)

	with open(text_file, 'r', encoding='utf-8') as f:
		content = f.read()

		#finding testRanges block:
		pattern = r"""testRanges\s*=\s*\{(?:[^{}]|\n|\s)*\}"""
		print(pattern)
		match = re.search(pattern, content, re.MULTILINE)
		print(match)
		match = match.group(0)
		print(match)
		clean_match = match.split("=")[1].strip()
		print(clean_match)
		

		if clean_match:
			dizionario = eval(clean_match) #DANGEROUS
			print(dizionario)
			print(type(dizionario))
			ranges = list(dizionario.values())
			print(ranges)
			print(type(ranges))
			return ranges
		else:
			return None
		
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


'''for values in itertools.product(*lista):  # Genera tutte le combinazioni possibili
    i, j, k, l, m, n = values  # Estrai i valori secondo il numero di liste
    res = spExpr.evalf(subs={x: i + j*I, y: k + l*I, z: m + n*I}).as_real_imag()
    
for spExptr in serializeExpr(self, expr):
	res = spExptr.evalf(subs={x: i + j*I, y: k + l*I, z: m + n*I}).as_real_imag 
		#print(res)
	print(res)
		
	print(res)
results.append(res)'''


def evaluate_expression(spExpr, variables, lista):
	

    results = []
    for values in itertools.product(*lista):  #It generates all possible combination of values
        subs_dict = {} #That is the dictionary i have to provide to evalf
        for var, (val_r, val_i) in zip(variables, zip(*[iter(values)]*2)):
            subs_dict[var] = val_r + val_i * sp.I
        res = spExpr.evalf(subs=subs_dict).as_real_imag()
        results.append(res)
    return results
          


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

