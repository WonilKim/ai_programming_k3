# Numeric problem에만 사용 가능
import random
import math

DELTA = 0.01   # Mutation step size
NumEval = 0    # Total number of evaluations


def main():
    # /Search Tool v1 - program codes/problem/

    # Create an instance of numerical optimization problem
    p = createProblem()   # 'p': (expr, domain)
    # Call the search algorithm
    solution, minimum = gradientDescent(p)
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

    filename = "./Search Tool v1 - program codes/problem/" + input("Enter the file name of function : ")
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


def gradientDescent(p):
    current = randomInit(p) # 'current' is a list of values
    valueC = evaluate(current, p)
    while True:
        successor = p.takeStep(current, valueC)
        valueS = p.evaluate(successor)

        if valueS >= valueC:
            break
        else:
            current = successor
            valueC = valueS
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
    varNames = p[1][0]  # p[1] is domain
    for i in range(len(varNames)):
        assignment = varNames[i] + '=' + str(current[i])    # x1 = 1.23 과 같은 정의문(statement) 코드를 문자열로 생성
        exec(assignment)    # 생성된 문자열 코드를 실행
    return eval(expr)   # 수식(expression)을 실행


def mutants(current, p): ###
    neighbors = []

    for i in range(len(current)):
        mutant = mutate(current, i, DELTA, p)
        neighbors.append(mutant)
        mutant = mutate(current, i, -DELTA, p)
        neighbors.append(mutant)
    
    return neighbors     # Return a set of successors


def mutate(current, i, d, p): ## Mutate i-th of 'current' if legal
    curCopy = current[:]
    domain = p[1]        # [VarNames, low, up]
    l = float(domain[1][i])     # Lower bound of i-th
    u = float(domain[2][i])     # Upper bound of i-th
    if l <= (curCopy[i] + d) <= u:
        curCopy[i] += d
    return curCopy

def bestOf(neighbors, p): ###
    best = neighbors[0]
    bestValue = evaluate(neighbors[0], p)
    for i in range(1, len(neighbors)):
        temp = evaluate(neighbors[i], p)
        if bestValue > temp:
            bestValue = temp
            best = neighbors[i]

    return best, bestValue

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
    print("Search algorithm: Steepest-Ascent Hill Climbing")
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
