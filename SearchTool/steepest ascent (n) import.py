import random
import math
import numeric_prob
 
DELTA = 0.01   # Mutation step size
NumEval = 0    # Total number of evaluations


def main():
    # /Search Tool v1 - program codes/problem/

    algorithm = "Steepest-Ascent Hill Climbing"

    nprob = numeric_prob(algorithm)

    # Create an instance of numerical optimization problem
    p = nprob.createProblem()   # 'p': (expr, domain)
    # Call the search algorithm
    solution, minimum = steepestAscent(nprob, p)
    # Show the problem and algorithm settings
    nprob.describeProblem(p)
    nprob.displaySetting()
    # Report results
    nprob.displayResult(solution, minimum)


def steepestAscent(prob, p):
    current = prob.randomInit(p) # 'current' is a list of values
    valueC = prob.evaluate(current, p)
    while True:
        neighbors = mutants(prob, current, p)
        successor, valueS = bestOf(prob, neighbors, p)
        if valueS >= valueC:
            break
        else:
            current = successor
            valueC = valueS
    return current, valueC


def mutants(prob, current, p): ###
    neighbors = []

    for i in range(len(current)):
        mutant = prob.mutate(current, i, DELTA, p)
        neighbors.append(mutant)
        mutant = prob.mutate(current, i, -DELTA, p)
        neighbors.append(mutant)
    
    return neighbors     # Return a set of successors


def bestOf(prob, neighbors, p): ###
    best = neighbors[0]
    bestValue = prob.evaluate(neighbors[0], p)
    for i in range(1, len(neighbors)):
        temp = prob.evaluate(neighbors[i], p)
        if bestValue > temp:
            bestValue = temp
            best = neighbors[i]

    return best, bestValue


