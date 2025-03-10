#!/usr/bin/env python


"""Flexpytester

Usage:
  flexpytester -e <expression> -o <outputfile> -i <inputfile> [-t <type>]
  flexpytester -h | --help

Options:
  -h --help                                         Show this screen.
  -e <expression>                                   The expression to convert.
  -o <outputfile>                                   The output file.
  -i <inputfile>                                    The input file.
  -t <type>                                         The type of the numbers, if not specified it is set to float32.
"""

from docopt import docopt
import sympy as sp

def main():
	arguments = docopt(__doc__, version='Flexpytester 0.0')

	# Create the expression
	exprFile = arguments["-e"]

	# Read the content of the file and parse it
	f = open(exprFile, "r")
	expr = f.read()
	f.close()

	localParams = {'spExpr': None, 'testRanges': None}
	globalParams = {'sp': sp}
	exec(expr, globalParams, localParams)
	spExpr = localParams['spExpr']
	testRanges = localParams['testRanges']

	if spExpr is None:
		print("Error: The expression is not valid")
		return

	# spExpr = sp.parse_expr(expr, evaluate=False)
	# print(srepr(spEXpr))

if __name__ == '__main__':
	main()