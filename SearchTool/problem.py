import math
import random

class Problem:

    LIMIT_STUCK = 100

    def __init__(self):
        self._solution = []
        self._value = 0.
        self._numEval = 0
        self._algorithm = 'algorithm'

    def setAlgorithm(self, algorithm):
        self._algorithm = algorithm

    def setVariables(self): # create problem
        pass
    
    def evaluate(self):
        pass

    def mutants(self):
        pass

    def randomMutant(self):
        pass

    def describe(self, p):
        pass

    def storeResult(self, solution, value):
        self._solution = solution
        self._value = value


    def report(self):
        print()
        print("Total number of evaluations: {0:,}".format(self._numEval))

class NumericProblem(Problem):

    def __init__(self):
        Problem.__init__(self)
        self._expression = ''
        self._domain = []
        self._delta = 0.01

    def setVariables(self):
        filename = "./SearchTool/problem/" + input("Enter the file name of function : ")
        infile = open(filename, 'r')

        self._expression = infile.readline()
        varName = []
        low = []
        up = []
        
        line = infile.readline()
        while line != '':
            temp = line.split(',')
            varName.append(temp[0].strip())
            low.append(temp[1].strip())
            up.append(temp[2].strip())

            # domain.append([temp[0].strip(), temp[1].strip(), temp[2].strip()])
            line = infile.readline()

        infile.close()

        self._domain = [varName, low, up]


    def randomInit(self): ###
        varName, low, up = self._domain

        init = []
        for i in range(len(low)):
            val = random.uniform(float(low[i]), float(up[i]))
            init.append(val)

        return init    # Return a random initial point
                    # as a list of values

    def evaluate(self, current):
        ## Evaluate the expression of 'p' after assigning
        ## the values of 'current' to the variables
        
        self._numEval += 1
        varNames = self._domain[0]  # p[1] is domain
        for i in range(len(varNames)):
            assignment = varNames[i] + '=' + str(current[i])    # x1 = 1.23 과 같은 정의문(statement) 코드를 문자열로 생성
            exec(assignment)    # 생성된 문자열 코드를 실행
        return eval(self._expression)   # 수식(expression)을 실행


    def mutate(self, current, i, d): ## Mutate i-th of 'current' if legal
        curCopy = current[:]

        l = float(self._domain[1][i])     # Lower bound of i-th
        u = float(self._domain[2][i])     # Upper bound of i-th
        if l <= (curCopy[i] + d) <= u:
            curCopy[i] += d
        return curCopy
    
    def mutants(self, current): ###
        neighbors = []

        for i in range(len(current)):
            mutant = self.mutate(current, i, self._delta)
            neighbors.append(mutant)
            mutant = self.mutate(current, i, -self._delta)
            neighbors.append(mutant)
        
        return neighbors     # Return a set of successors

    def firstChoice(self):
        current = self.randomInit()   # 'current' is a list of values
        valueC = self.evaluate(current)
        i = 0
        while i < self.LIMIT_STUCK:
            successor = self.randomMutant(current)
            valueS = self.evaluate(successor)
            if valueS < valueC:
                current = successor
                valueC = valueS
                i = 0              # Reset stuck counter
            else:
                i += 1

        self._solution = current
        self._value = valueC

    def randomMutant(self, current): ###

        i = random.randint(0, len(current) - 1)
        if(random.uniform(0, 1) > 0.5):
            d = self._delta
        else:
            d = -self._delta

        return self.mutate(current, i, d)

    def steepestAscent(self):
        current = self.randomInit() # 'current' is a list of values
        valueC = self.evaluate(current)
        while True:
            neighbors = self.mutants(current)
            successor, valueS = self.bestOf(neighbors)
            if valueS >= valueC:
                break
            else:
                current = successor
                valueC = valueS

        self._solution = current
        self._value = valueC

    def bestOf(self, neighbors): ###
        best = neighbors[0]
        bestValue = self.evaluate(neighbors[0])
        for i in range(1, len(neighbors)):
            temp = self.evaluate(neighbors[i])
            if bestValue > temp:
                bestValue = temp
                best = neighbors[i]

        return best, bestValue


    def describe(self):
        print()
        print("Objective function:")
        print(self._expression)   # Expression
        print("Search space:")
        varNames = self._domain[0]
        low = self._domain[1]
        up = self._domain[2]
        for i in range(len(low)):
            print(" " + varNames[i] + ":", (low[i], up[i])) 


    def report(self):
        print()
        print("Solution found:")
        print(self.coordinate())  # Convert list to tuple
        print("Minimum value: {0:,.5f}".format(self._value))
        
        Problem.report(self)    # super().report(self) 와 같은 내용
        

    def coordinate(self):
        c = [round(value, 3) for value in self._solution]
        return tuple(c)  # Convert the list to a tuple


    def displaySetting(self):
        print()
        print("Search algorithm: " + self._algorithm)
        print()
        print("Mutation step size:", self._delta)
    


class TspProblem(Problem):
    def __init__(self):
        Problem.__init__(self)
        self._numCities = 0
        self._locations = []
        self._distanceTable = []


    def setVariables(self):
        ## Read in a TSP (# of cities, locatioins) from a file.
        ## Then, create a problem instance and return it.
        fileName = "./SearchTool/problem/" + input("Enter the file name of a TSP: ")
        infile = open(fileName, 'r')
        # First line is number of cities
        self._numCities = int(infile.readline())
        self._locations = []
        line = infile.readline()  # The rest of the lines are locations
        while line != '':
            self._locations.append(eval(line)) # Make a tuple and append
            line = infile.readline()
        infile.close()
        
        self.calcDistanceTable()
        # print(self._distanceTable)


    def calcDistanceTable(self): ###
        for i in range(len(self._locations)):
            x1, y1 = self._locations[i]

            dist = []
            for j in range(len(self._locations)):
                x2, y2 = self._locations[j]

                dist.append(math.sqrt(math.pow((x2 - x1), 2) + math.pow((y2 - y1), 2)))

            self._distanceTable.append(dist)

    def randomInit(self):   # Return a random initial tour
        # p = numCities, locations, table
        n = self._numCities
        init = list(range(n))
        random.shuffle(init)
        return init


    def evaluate(self, current): ###
        ## Calculate the tour cost of 'current'
        ## 'current' is a list of city ids
        
        self._numEval += 1

        cost = 0
        for i in range(len(current)):
            cost += self._distanceTable[current[i]][current[(i + 1) % len(current)]]

        return cost

    def mutants(self, current): # Apply inversion
        # p = numCities, locations, table
        n = self._numCities
        neighbors = []
        count = 0
        triedPairs = []
        while count <= n:  # Pick two random loci for inversion
            i, j = sorted([random.randrange(n) for _ in range(2)])
            if i < j and [i, j] not in triedPairs:
                triedPairs.append([i, j])
                curCopy = self.inversion(current, i, j)
                count += 1
                neighbors.append(curCopy)
        return neighbors

    def randomMutant(self, current): # Apply inversion
        while True:
            i, j = sorted([random.randrange(self._numCities)
                        for _ in range(2)])
            if i < j:
                curCopy = self.inversion(current, i, j)
                break
        return curCopy

    def inversion(self, current, i, j):  ## Perform inversion
        curCopy = current[:]
        while i < j:
            curCopy[i], curCopy[j] = curCopy[j], curCopy[i]
            i += 1
            j -= 1
        return curCopy
    
    def steepestAscent(self):
        current = self.randomInit()   # 'current' is a list of city ids
        valueC = self.evaluate(current)
        while True:
            neighbors = self.mutants(current)
            (successor, valueS) = self.bestOf(neighbors)
            if valueS >= valueC:
                break
            else:
                current = successor
                valueC = valueS
 
        self._solution = current
        self._value = valueC


    def firstChoice(self):
        current = self.randomInit()   # 'current' is a list of city ids
        valueC = self.evaluate(current)
        i = 0
        while i < self.LIMIT_STUCK:
            successor = self.randomMutant(current)
            valueS = self.evaluate(successor)
            if valueS < valueC:
                current = successor
                valueC = valueS
                i = 0              # Reset stuck counter
            else:
                i += 1

        self._solution = current
        self._value = valueC


    def bestOf(self, neighbors): ###
        best = neighbors[0]
        bestValue = self.evaluate(neighbors[0])
        for i in range(1, len(neighbors)):
            temp = self.evaluate(neighbors[i])
            if bestValue > temp:
                bestValue = temp
                best = neighbors[i]

        return best, bestValue

    def describe(self):
        print()
        n = self._numCities
        print("Number of cities:", n)
        print("City locations:")
        locations = self._locations
        for i in range(n):
            print("{0:>12}".format(str(locations[i])), end = '')
            if i % 5 == 4:
                print()

    def displaySetting(self):
        print()
        print("Search algorithm: " + self._algorithm)

    def report(self):
        print()
        print("Best order of visits:")
        self.tenPerRow()       # Print 10 cities per row
        print("Minimum tour cost: {0:,}".format(round(self._value)))
        
        Problem.report(self)

    def tenPerRow(self):
        for i in range(len(self._solution)):
            print("{0:>5}".format(self._solution[i]), end='')
            if i % 10 == 9:
                print()



##
def testNumericSteepestAscent():
    prob = NumericProblem()

    algorithm = "Steepest-Ascent Hill Climbing"
    prob.setAlgorithm(algorithm)

   # Create an instance of numerical optimization problem
    prob.setVariables()
    # Call the search algorithm
    prob.steepestAscent()
    # Show the problem and algorithm settings
    prob.describe()
    prob.displaySetting()
    # Report results
    prob.report()

def testNumericFirstChoice():
    prob = NumericProblem()

    algorithm = "First-Choice Hill Climbing"
    prob.setAlgorithm(algorithm)

    # Create an instance of numerical optimization problem
    prob.setVariables()
    # Call the search algorithm
    prob.firstChoice()
    # Show the problem and algorithm settings
    prob.describe()
    prob.displaySetting()
    # Report results
    prob.report()

def testTspSteepestAscent():
    prob = TspProblem()

    algorithm = "Steepest-Ascent Hill Climbing"
    prob.setAlgorithm(algorithm)

    # Create an instance of numerical optimization problem
    prob.setVariables()
    # Call the search algorithm
    prob.steepestAscent()
    # Show the problem and algorithm settings
    prob.describe()
    prob.displaySetting()
    # Report results
    prob.report()

def testTspFirstChoice():
    prob = TspProblem()

    algorithm = "First-Choice Hill Climbing"
    prob.setAlgorithm(algorithm)

    # Create an instance of numerical optimization problem
    prob.setVariables()
    # Call the search algorithm
    prob.firstChoice()
    # Show the problem and algorithm settings
    prob.describe()
    prob.displaySetting()
    # Report results
    prob.report()


#
if __name__ == '__main__':

    # testNumericSteepestAscent()
    # testNumericFirstChoice()
    testTspSteepestAscent()
    # testTspFirstChoice()
    
    pass