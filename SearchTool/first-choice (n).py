import random
import math

DELTA = 0.01   # Mutation step size
LIMIT_STUCK = 100 # Max number of evaluations enduring no improvement
NumEval = 0    # Total number of evaluations


def main():
    # Create an instance of numerical optimization problem
    p = createProblem()   # 'p': (expr, domain)
    # Call the search algorithm
    solution, minimum = firstChoice(p)
    # Show the problem and algorithm settings
    describeProblem(p)
    displaySetting()
    # Report results
    displayResult(solution, minimum)


def createProblem(): ###
    ## Read in an expression and its domain from a file.
    ## Then, return a problem 'p'.
    ## 'p' is a tuple of 'expression' and 'domain'.
    ## 'expression' is a string.
    ## 'domain' is a list of 'varNames', 'low', and 'up'.
    ## 'varNames' is a list of variable names.
    ## 'low' is a list of lower bounds of the varaibles.
    ## 'up' is a list of upper bounds of the varaibles.
    filename = "./SearchTool/problem/" + input("Enter the file name of function : ")
    infile = open(filename, 'r')

    expression = infile.readline()
    varName = []
    low = []
    up = []
    domain = []
    
    line = infile.readline()
    while line != '':
        temp = line.split(',')
        varName.append(temp[0].strip())
        low.append(temp[1].strip())
        up.append(temp[2].strip())

        # domain.append([temp[0].strip(), temp[1].strip(), temp[2].strip()])
        line = infile.readline()

    infile.close()

    domain = [varName, low, up]

    return expression, domain


def firstChoice(p):
    current = randomInit(p)   # 'current' is a list of values
    valueC = evaluate(current, p)
    i = 0
    while i < LIMIT_STUCK:
        successor = randomMutant(current, p)
        valueS = evaluate(successor, p)
        if valueS < valueC:
            current = successor
            valueC = valueS
            i = 0              # Reset stuck counter
        else:
            i += 1
    return current, valueC


def randomInit(p): ###
    expression, domain = p
    varName, low, up = domain

    init = []
    for i in range(len(low)):
        val = random.uniform(float(low[i]), float(up[i]))
        init.append(val)

    return init    # Return a random initial point
                   # as a list of values

def evaluate(current, p):
    ## Evaluate the expression of 'p' after assigning
    ## the values of 'current' to the variables
    global NumEval
    
    NumEval += 1
    expr = p[0]         # p[0] is function expression
    varNames = p[1][0]  # p[1] is domain: [varNames, low, up]
    for i in range(len(varNames)):
        assignment = varNames[i] + '=' + str(current[i])
        exec(assignment)
    return eval(expr)


def randomMutant(current, p): ###
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

    return mutate(current, i, d, p)


def mutate(current, i, d, p): ## Mutate i-th of 'current' if legal
    curCopy = current[:]
    domain = p[1]        # [VarNames, low, up]
    l = float(domain[1][i])     # Lower bound of i-th
    u = float(domain[2][i])     # Upper bound of i-th
    if l <= (curCopy[i] + d) <= u:
        curCopy[i] += d
    return curCopy

def describeProblem(p):
    print()
    print("Objective function:")
    print(p[0])   # Expression
    print("Search space:")
    varNames = p[1][0] # p[1] is domain: [VarNames, low, up]
    low = p[1][1]
    up = p[1][2]
    for i in range(len(low)):
        print(" " + varNames[i] + ":", (low[i], up[i])) 

def displaySetting():
    print()
    print("Search algorithm: First-Choice Hill Climbing")
    print()
    print("Mutation step size:", DELTA)

def displayResult(solution, minimum):
    print()
    print("Solution found:")
    print(coordinate(solution))  # Convert list to tuple
    print("Minimum value: {0:,.3f}".format(minimum))
    print()
    print("Total number of evaluations: {0:,}".format(NumEval))

def coordinate(solution):
    c = [round(value, 3) for value in solution]
    return tuple(c)  # Convert the list to a tuple

main()
