#!/usr/bin/env python

import sys, random
import math
import random


def walksat(clauses, nvars, max_tries, max_flips):    
     
    formula = clauses
    for i in range(1, max_tries):
        interpretation = RandomSolution(nvars)
        for j in range(1, max_flips):
            result, clause = checkSatisfiability(interpretation,formula)
            if result == True:
                return interpretation
            #a clause of F not satisfied by I
            C = clause
            S = get_variables(C)
            b, num = broken(S, formula, interpretation)

            if b > 0 and random.random() < 0.2:
                #S[0]
                interpretation[0] = interpretation[0]*-1
            else:
                #S[num]
                interpretation[num%nvars] = interpretation[num%nvars]*-1
                interpretation = RandomSolution(nvars)
                interpretation*-1
        #endfor
    #endfor
    return "No solution found"
    
def broken(S, F, sol):

    broke = [0] * (2*len(sol)+1)
    for clause in F:
        for literal in clause:
            lit = abs(literal)   
            if lit in S and literal != sol[lit-1]:           
                broke[literal] += 1
    return max(broke), broke.index(max(broke))

def get_variables( clause ) :
    counter = {}

    for literal in clause:
        if literal in counter :
            counter[ literal ] += 1 		
        else :
            counter[ literal ] = 0
    return counter

def checkSatisfiability(possibleSolution, cnfFormulaParsed):

    for clause in cnfFormulaParsed:
        if isSatisfiable(possibleSolution, clause) is False:
            return False, clause
    return True, clause


def isSatisfiable(solution, clause):
    for literal in clause:
        if literal == solution[abs(literal) - 1]:
            return True
    return False

def RandomSolution(n_var):
    sol = range(1, n_var+1)
    for i in xrange(len(sol)):
        if random.random() < 0.5:
            sol[i] *= -1
    return sol

def parse( filename ) :
	clauses = []
	for line in open( filename ) :
		if line.startswith( 'c' ) : continue
		if line.startswith( 'p' ) :
			nvars, nclauses = line.split()[2:4]
			continue
		clause = [ int(x) for x in line[:-2].split() ]
		clauses.append( clause )
	return clauses, int( nvars )

def main() :
    clauses, nvars = parse( sys.argv[1])

    solution = walksat(clauses, nvars, 10000, nvars*4)    
    print "s SATISFIABLE"
    print "v " + ' '.join(map(str,solution)) + ' 0'

if __name__ == '__main__':
	main()


