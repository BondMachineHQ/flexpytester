#!/usr/bin/env python


"""Flexpytester

Usage:
  flexpytester --compute -e <expression> -o <outputfile> -i <inputfile> [-t <type>] [--csv] [--prefix]
  flexpytester --generate -e <expression> -s <outputexpression> [-o <outputfile>] [-i <inputfile>] [-t <type>] [--csv] [--prefix]
  flexpytester -h | --help

Options:
  -h --help                                         Show this screen.
  -c, --compute                                     Compute the expression ranging the inputs over the specified ranges.
  -e <expression>                                   Input expression (when computing), symbols and ranges.
  -o <outputfile>                                   The outputs file name for the generated outputs.
  -i <inputfile>                                    The inputs file name for the generated inputs.
  -s <outputexpression>                             The output expression (when generating).
  -t <type>                                         The type of the numbers, if not specified it is set to float32.
  --csv                                             The output file is in CSV format.
  --prefix                                          Prefix numbers with the prefix type as given by bmnumbers.
"""

from docopt import docopt
import sympy as sp
import sys
import random

DECAY_FACTOR = 3.0
SYM_NUM_PROP = 0.5
NUM_RANGE = 10
MAX_ELEMENTS = 10
MAX_RANK = 4
EVALUATE_GENERATED = False
SCALAR_FACTOR = 1.0
VECTOR_FACTOR = 10.0
MATRIX_FACTOR = 1.0
TENSOR_FACTOR = 1.0

def decay(level):
	return 1.0 / (1.0 + level/DECAY_FACTOR)

def generator_engine(symbols, level):
	# If level is 0, we can potentially generate a Scalar, a Vector, a Matrix or a Tensor
	if level == 0:
		scalarFactor = SCALAR_FACTOR / (SCALAR_FACTOR + VECTOR_FACTOR + MATRIX_FACTOR + TENSOR_FACTOR)
		vectorFactor = scalarFactor + VECTOR_FACTOR / (SCALAR_FACTOR + VECTOR_FACTOR + MATRIX_FACTOR + TENSOR_FACTOR)
		matrixFactor = vectorFactor + MATRIX_FACTOR / (SCALAR_FACTOR + VECTOR_FACTOR + MATRIX_FACTOR + TENSOR_FACTOR)
		# Choose a random number
		randNum = random.random()
		if randNum < scalarFactor:
			# Generate a scalar
			return generator_engine(symbols, level + 1)
		elif randNum < vectorFactor:
			# Generate a vector
			elemNum = random.randint(1, MAX_ELEMENTS)
			list = []
			for i in range(elemNum):
				list.append(generator_engine(symbols, level + 1))
			with sp.evaluate(EVALUATE_GENERATED):
				vector = sp.Array(list)
			return vector
			
		elif randNum < matrixFactor:
			elemNumN = random.randint(1, MAX_ELEMENTS)
			elemNumM = random.randint(1, MAX_ELEMENTS)
			listN = []
			listM = []
			for i in range(elemNumN):
				listN.append(generator_engine(symbols, level + 1))
			for i in range(elemNumM):
				listM.append(generator_engine(symbols, level + 1))
			with sp.evaluate(EVALUATE_GENERATED):
				matrix = sp.Matrix(listN, listM)
			return matrix

		else:
			rank = random.randint(3, MAX_RANK)
			elemNumList = []
			for i in range(rank):
				elemNumList.append(random.randint(1, MAX_ELEMENTS))
			print ("TODO Tensor")
	else:

		if random.random() > decay(level):
		# If the random number is greater than the decay, then we generate a leaf with a symbol or a number
			if random.random() > SYM_NUM_PROP:
				# Generate a random number
				return random.uniform(-NUM_RANGE, NUM_RANGE)
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

def main():
	random.seed()
	arguments = docopt(__doc__, version='Flexpytester 0.0')

	# Create the expression
	exprFile = arguments["-e"]

	# Read the content of the file and parse it
	f = open(exprFile, "r")
	expr = f.read()
	f.close()

	if arguments["--compute"]:
		localParams = {'spExpr': None, 'testRanges': None}
		globalParams = {'sp': sp}
		# exec(expr, globalParams, localParams)
		spExpr = localParams['spExpr']
		testRanges = localParams['testRanges']

		# TODO Generate the test ranges if all the parameters are valid
		if testRanges != None and arguments["-o"] != None and arguments["-i"] != None:
			print ("TODO")


		if spExpr is None:
			print("Error: The expression is not valid")
			sys.exit(1)
		
	elif arguments["--generate"]:
		localParams = {'symbols': None, 'testRanges': None}
		globalParams = {'sp': sp}
		exec(expr, globalParams, localParams)
		symbols = localParams['symbols']
		testRanges = localParams['testRanges']

		if symbols is None:
			print("Error: Symbols not valid")
			sys.exit(1)
	
		# TODO Place here the code to generate the expression
		with sp.evaluate(EVALUATE_GENERATED):
			genExpr=generator_engine(symbols, 0)
			
		# TODO Generate also the test ranges if all the parameters are valid
		if testRanges != None and arguments["-o"] != None and arguments["-i"] != None:
			print ("TODO")

	else:
		print("Error: Invalid arguments")
		sys.exit(1)
	
if __name__ == '__main__':
	main()