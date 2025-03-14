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

def main():
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
		# exec(expr, globalParams, localParams)
		symbols = localParams['symbols']
		testRanges = localParams['testRanges']

		if symbols is None:
			print("Error: Symbols not valid")
			sys.exit(1)
	
		# TODO Place here the code to generate the expression

		# TODO Generate also the test ranges if all the parameters are valid
		if testRanges != None and arguments["-o"] != None and arguments["-i"] != None:
			print ("TODO")

	else:
		print("Error: Invalid arguments")
		sys.exit(1)
	
	print (arguments)


if __name__ == '__main__':
	main()