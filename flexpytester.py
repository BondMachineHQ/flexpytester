#!/usr/bin/env python


"""Flexpytester

Usage:
  flexpytester --compute -e <expression> -o <outputfile> -i <inputfile> [-t <type>] [--prefix] [--config=<key=value>]...
  flexpytester --generate -e <expression> -s <outputexpression> [-o <outputfile>] [-i <inputfile>] [-r <seed>] [-t <type>] [--prefix] [-d] [--config=<key=value>]...
  flexpytester -h | --help

Options:
  -h --help                                         Show this screen.
  -d                                                Debug mode.
  -c, --compute                                     Compute the expression ranging the inputs over the specified ranges.
  -g, --generate                                    Generate the expression and ranges for the inputs.
  -e <expression>                                   Input expression (when computing), symbols and ranges.
  -o <outputfile>                                   The outputs file name for the generated outputs.
  -i <inputfile>                                    The inputs file name for the generated inputs.
  -s <outputexpression>                             The output expression (when generating).
  -t <type>                                         The type of the numbers, if not specified it is set to float32.
  -r <seed>                                         The seed for the random number generator.
  --prefix                                          Prefix numbers with the prefix type as given by bmnumbers.
  --config=<key=value>                              Configuration options for the generation of the expression.
"""

from docopt import docopt
import sympy as sp
import numpy as np
import sys
import random
import time
import subprocess
import itertools

config_params = {}
config_params["decayFactor"] = float(2.0)
config_params["maxDepth"] = 5
config_params["symNumProp"] = float(0.5)
config_params["numRange"] = float(10.0)
config_params["maxElements"] = 5
config_params["maxRank"] = 3
config_params["evaluateGenerated"] = False
config_params["scalarFreq"] = float(5.0)
config_params["vectorFreq"] = float(1.0)
config_params["matrixFreq"] = float(1.0)
config_params["tensorFreq"] = float(1.0)

def decay(level):
	global config_params
	decayFactor = config_params["decayFactor"]
	return 1.0 / (1.0 + level/decayFactor)

def generate_list(symbols, numElems, level, max):
	list = []
	n = numElems[level]
	if level == max - 1:
		for i in range(n):
			list.append(generator_engine(symbols, level + 1))
	else:
		for i in range(n):
			list.append(generate_list(symbols, numElems, level + 1, max))
	return list

def generator_engine(symbols, level):
	global config_params
	maxElements = config_params["maxElements"]
	symNumProp = config_params["symNumProp"]
	evaluateGenerated = config_params["evaluateGenerated"]
	# print("Level: "+str(level), "Decay: "+str(decay(level, decayFactor)))
	# print(decayFactor)
	# If level is 0, we can potentially generate a Scalar, a Vector, a Matrix or a Tensor
	if level == 0:
		scalarFreq = config_params["scalarFreq"]
		vectorFreq = config_params["vectorFreq"]
		matrixFreq = config_params["matrixFreq"]
		tensorFreq = config_params["tensorFreq"]
		scalarFactor = scalarFreq / (scalarFreq + vectorFreq + matrixFreq + tensorFreq)
		vectorFactor = scalarFactor + vectorFreq / (scalarFreq + vectorFreq + matrixFreq + tensorFreq)
		matrixFactor = vectorFactor + matrixFreq / (scalarFreq + vectorFreq + matrixFreq + tensorFreq)
		# Choose a random number
		randNum = random.random()
		if randNum < scalarFactor:
			# Generate a scalar
			# print("Generating scalar:")
			return generator_engine(symbols, level + 1)
		elif randNum < vectorFactor:
			# Generate a vector
			# print("Generating vector:")
			elemNum = random.randint(1, maxElements)
			list = []
			for i in range(elemNum):
				list.append(generator_engine(symbols, level + 1))
			with sp.evaluate(evaluateGenerated):
				vector = sp.Array(list)
			return vector
			
		elif randNum < matrixFactor:
			# Generate a matrix
			# print("Generating matrix:")
			elemNumN = random.randint(1, maxElements)
			elemNumM = random.randint(1, maxElements)
			listN = []
			for i in range(elemNumN):
				listM = []
				for j in range(elemNumM):
					listM.append(generator_engine(symbols, level + 1))
				listN.append(listM)
			with sp.evaluate(evaluateGenerated):
				matrix = sp.Matrix(listN)
				return matrix

		else:
			# Generate a tensor
			# print("Generating tensor:")
			maxRank = config_params["maxRank"]
			rank = random.randint(3, maxRank)
			elemNumList = []
			for i in range(rank):
				elemNumList.append(random.randint(1, maxElements))
			with sp.evaluate(evaluateGenerated):
				tensor=sp.Array(generate_list(symbols, elemNumList, level, rank))
				return tensor
	else:

		if (level > 2 and random.random() > decay(level)) or level > config_params["maxDepth"]:
		# If the random number is greater than the decay, then we generate a leaf with a symbol or a number
			if random.random() > symNumProp:
				# Generate a random number
				numRange = config_params["numRange"]
				return random.uniform(-numRange, numRange)
			else:
				return random.choice(symbols)
		else:
		# Otherwise we generate a random operator
			# Choose a random operator
			operator = random.choice(["+"])
			# Generate the left and right branches
			left = generator_engine(symbols, level + 1)
			right = generator_engine(symbols, level + 1)
			# Generate the expression
			if operator == "+":
				return left + right
			
			# TODO Add more operators

#function to execute: flexpy -e expression.txt --basm --iomap-only
#output should be: an ordered list of symbols
def symbolExtractor(exprFile):
	command = ["flexpy", "-e", exprFile, "--basm", "--iomap-only"]
	try:
		pos_real = {}
		pos_imag = {}
		result = subprocess.run(command, capture_output=True, text=True, check=True)
		output_lines = result.stdout.strip().split('\n')
		
		if len(output_lines) >=2:
			first_line = output_lines[0]
			localParams = {'first_line_array': None}
			exec("first_line_array = " + first_line, localParams)
			first_line_array = localParams['first_line_array']

			for i in range(len(first_line_array)):
				s = first_line_array[i]
				if s.startswith('real: '):
					s=s[6:]
					pos_real[s] = i
				elif s.startswith('imag: '):
					s=s[6:]
					pos_imag[s] = i

			symbolsNames = []
			for item in first_line_array:
				symbolsNames.append(item)

			return symbolsNames, pos_real, pos_imag	
		else:
			print("Error: No symbols found in the expression")
			sys.exit(1)
	except subprocess.CalledProcessError as e:
		print("Error: flexpy command failed with error code "+str(e.returncode))
		sys.exit(1)
	except FileNotFoundError:
		print("Error: flexpy command not found")
		sys.exit(1)

def generateLists(symbolsNames, testRanges, pos_real, pos_imag):
	lists=[]

	for s in symbolsNames:
		if s in testRanges:
			lists.append(testRanges[s])
		else:
			print("Error: Symbol "+s+" not found in the testRanges")
			sys.exit(1)
	return lists
			
def evaluateExpression(spExpr, symbols, lists, pos_real, pos_imag):
	resultsInputs = []
	resultsOutputs = []
	for values in itertools.product(*lists):  #It generates all possible combination of values
		subs_dict = {} #That is the dictionary i have to provide to evalf
		inputs = []
		outputs = []
		for var in range(len(lists)):
			inputs.append(0.0)

		for s in symbols:
			sName = str(s)
			val_r, val_i = 0,0
			if sName in pos_real:
				val_r = values[pos_real[sName]]
				inputs[pos_real[sName]] = val_r
			if sName in pos_imag:
				val_i = values[pos_imag[sName]]
				inputs[pos_imag[sName]] = val_i

			subs_dict[s] = val_r + val_i * sp.I

		for exp in serializeExpr(spExpr):
			res = exp.evalf(subs=subs_dict).as_real_imag()
		
			outputs.append(res[0])
			outputs.append(res[1])

		resultsInputs.append(inputs)
		resultsOutputs.append(outputs)
	return resultsInputs, resultsOutputs

def generateRanges(spExpr, symbols, exprFile, testRanges, outputfile, inputfile, prefix="0f"):
	symbolsNames, pos_real, pos_imag = symbolExtractor(exprFile)
	# print(symbolsNames, pos_real, pos_imag)
	lists = generateLists(symbolsNames, testRanges, pos_real, pos_imag)
	# print(lists)
	resultsInputs, resultsOutputs = evaluateExpression(spExpr, symbols, lists, pos_real, pos_imag)
	# print(resultsInputs, resultsOutputs)
	with open(inputfile, "w") as f:
		for inputs in resultsInputs:
			for inIdx in range(len(inputs)):
				inp = inputs[inIdx]
				f.write(prefix+"%f" % inp)
				if inIdx != len(inputs) - 1:
					f.write(",")
			f.write('\n')
	with open(outputfile, "w") as f:
		for outputs in resultsOutputs:
			for outIdx in range(len(outputs)):
				out = outputs[outIdx]
				f.write("%f" % out)
				if outIdx != len(outputs) - 1:
					f.write(",")
			f.write('\n')


def serializeExpr(expr):
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

def main():
	global config_params

	random.seed()
	arguments = docopt(__doc__, version='Flexpytester 0.0')

	# Create the expression
	exprFile = arguments["-e"]

	# Get the config dictionary
	configParams = arguments["--config"]

	configDict = {}
	if configParams:
		configDict = dict(param.split("=") for param in configParams)
		for key, value in configDict.items():
			if key in config_params:
				if key == "decayFactor" or key == "numRange":
					config_params[key] = float(value)
				elif key == "symNumProp" or key == "scalarFreq" or key == "vectorFreq" or key == "matrixFreq" or key == "tensorFreq":
					config_params[key] = float(value)
				elif key == "maxElements" or key == "maxRank" or key == "maxDepth":
					config_params[key] = int(value)
				elif key == "evaluateGenerated":
					if value == "True" or value == "true":
						config_params[key] = True
					elif value == "False" or value == "false":
						config_params[key] = False
					else:
						print("Error: Invalid config parameter "+key)
						sys.exit(1)
				else:
					print("Error: Invalid config parameter "+key)
					sys.exit(1)

	evaluateGenerated = config_params["evaluateGenerated"]

	# Read the content of the file and parse it
	f = open(exprFile, "r")
	expr = f.read()
	f.close()

	if arguments["--compute"]:
		localParams = {'spExpr': None, 'testRanges': None, 'symbols': None}
		globalParams = {'sp': sp, 'np': np}
		exec(expr, globalParams, localParams)
		spExpr = localParams['spExpr']
		testRanges = localParams['testRanges']
		symbols = localParams['symbols']

		if testRanges != None and arguments["-o"] != None and arguments["-i"] != None:
			generateRanges(spExpr, symbols, exprFile, testRanges, arguments["-o"], arguments["-i"])

		if spExpr is None:
			print("Error: The expression is not valid")
			sys.exit(1)
		
	elif arguments["--generate"]:
		if arguments["-r"] != None:
			random.seed(int(arguments["-r"]))
			if arguments["-d"]: print("Seed set to: "+arguments["-r"])
		else:
			seed=int(time.time())
			random.seed(seed)
			if arguments["-d"]: print("Seed set to: "+str(seed))

		localParams = {'symbols': None, 'testRanges': None}
		globalParams = {'sp': sp, 'np': np}
		exec(expr, globalParams, localParams)
		symbols = localParams['symbols']
		testRanges = localParams['testRanges']

		if symbols is None:
			print("Error: Symbols not valid")
			sys.exit(1)
	
		spExpr = None
		# Generate the expression
		with sp.evaluate(evaluateGenerated):
			genExpr=generator_engine(symbols, 0)
			spExpr = genExpr
			# Print the generated expression
			# print("---")
			# print(sp.python(genExpr))
			# print("---")

			if arguments["-s"] != None:
				# Save the generated expression
				f = open(arguments["-s"], "w")
				f.write("from sympy import *\n")
				f.write("import numpy as np\n")
				f.write("import sympy as sp\n")
				f.write("with sp.evaluate(False):\n")
				for line in sp.python(genExpr).split('\n'):
					f.write("\t"+line+"\n")
				f.write("\nspExpr = e\n")
				f.write("symbols = ["+",".join([str(s) for s in spExpr.free_symbols])+"]\n")
				f.write("testRanges = "+str(testRanges)+"\n")
				f.close	
				f.flush()

				if testRanges != None and arguments["-o"] != None and arguments["-i"] != None:
					subprocess.run(["flexpytester", "--compute", "-e", arguments["-s"], "-i", arguments["-i"], "-o", arguments["-o"]])
					# generateRanges(spExpr, symbols, arguments["-s"], testRanges, arguments["-o"], arguments["-i"])

	else:
		print("Error: Invalid arguments")
		sys.exit(1)
	
if __name__ == '__main__':
	main()
