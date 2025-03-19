import numpy as np
import sympy as sp
from sympy import *
import itertools
import subprocess
import re
import ast 


dict1 = {'a': 1, 'b': 2, 'c': 3}
dict2 = {'d': 4, 'e': 5, 'f': 6}   

a = np.arange(-1,1.1,0.5)
print(a)
print(type(a))
b = list(a)
print(b)
print(type(b))
c = [-1,1,0.1]
print(c)
print(type(c))





def creation_test_ranges(diz1 , diz2 , text_file):
	ranges = []
	#creation of an array of 0s with the same length of the sum of the input dictionaries dimentions
	for i in range(len(diz1)+len(diz2)):
		ranges.append(0)
	print(ranges)

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
		
l = creation_test_ranges(dict1, dict2, './expression.txt')
print(l)