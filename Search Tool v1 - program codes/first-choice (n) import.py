import random
import math
from numeric_prob import numeric_prob

LIMIT_STUCK = 100 # Max number of evaluations enduring no improvement

def main():
    algorithm = "First-Choice Hill Climbing"
    delta = 0.01   # Mutation step size
    
    nprob = numeric_prob(algorithm, delta)

    # Create an instance of numerical optimization problem
    p = nprob.createProblem()   # 'p': (expr, domain)
    # Call the search algorithm
    solution, minimum = firstChoice(nprob, p)
    # Show the problem and algorithm settings
    nprob.describeProblem(p)
    nprob.displaySetting()
    # Report results
    nprob.displayResult(solution, minimum)


def firstChoice(prob, p):
    current = prob.randomInit(p)   # 'current' is a list of values
    valueC = prob.evaluate(current, p)
    i = 0
    while i < LIMIT_STUCK:
        successor = randomMutant(prob, current, p)
        valueS = prob.evaluate(successor, p)
        if valueS < valueC:
            current = successor
            valueC = valueS
            i = 0              # Reset stuck counter
        else:
            i += 1
    return current, valueC


def randomMutant(prob, current, p): ###
    # neighbors = []

    # for i in range(len(current)):
    #     mutant = mutate(current, i, DELTA, p)
    #     neighbors.append(mutant)
    #     mutant = mutate(current, i, -DELTA, p)
    #     neighbors.append(mutant)

    # rand_idx = int(random.uniform(0, 10))

    # return neighbors[rand_idx]

    i = random.randint(0, len(current) - 1)
    if(random.uniform(0, 1) > 0.5):
        d = DELTA
    else:
        d = -DELTA

    return prob.mutate(current, i, d, p)

main()
