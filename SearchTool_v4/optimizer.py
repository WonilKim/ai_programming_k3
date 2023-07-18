from setup import Setup
from problem import *

class HillClimbing(Setup):

    def __init__(self):
        Setup.__init__(self)
        self._aType = 0
        self._pType = 0
        self._limitStuck = 0
        self._algorithm = "algorithm"

        self._numExp = 0
        self._numRestart = 0

    def setVariables(self, parameters):
        Setup.setVariables(self, parameters)

        self._pType = parameters['pType']
        self._aType = parameters['aType']
        self._limitStuck = parameters['limitStuck']
        self._numExp = parameters['numExp']
        self._numRestart = parameters['numRestart']

    def setAlgorithm(self, algorithm):
        self._algorithm = algorithm

    def setLimitStock(self, limitStock):
        self._limitStuck = limitStock

    def getNumExp(self):
        return self._numExp
        

    def run(self):
        pass

    def randomRestart(self, p):
        print("  randomRestart", 0)
        self.run(p)
        bestSolution = p.getSolution()
        bestMinimum = p.getValue()
        numEval = p.getNumEval()

        for i in range(1, self._numRestart):
            print("  randomRestart", i)
            self.run(p)
            newSolution = p.getSolution()
            newMinimum = p.getValue()
            numEval += p.getNumEval()

            if newMinimum < bestMinimum:
                bestMinimum = newMinimum
                bestSolution = newSolution

        p.storeResult(bestSolution, bestMinimum)
           
    def displayNumExp(self):
        print()
        print("Number of experiments: ", self._numExp)

    def displaySetting(self):
        print()
        print("Search algorithm: " + self._algorithm)

        if self._pType == 1:
            print()
            if self._aType == 3:
                print("Update rate", self._alpha)
                print("Increment for calculating derivatives", self._dx)
            else:
                print("Mutation step size", self._delta)

class SteepestAscent(HillClimbing):

    def __init__(self):
        super().__init__()

    def run(self, p):
        current = p.randomInit() # 'current' is a list of values
        valueC = p.evaluate(current)
        while True:
            neighbors = p.mutants(current)
            successor, valueS = p.bestOf(neighbors)
            if valueS >= valueC:
                break
            else:
                current = successor
                valueC = valueS

        p._solution = current
        p._value = valueC

    # def displaySetting(self):
    #     print()
    #     print("Search algorithm: " + self._algorithm)

    #     HillClimbing.displaySetting(self)

class FirstChoice(HillClimbing):

    def __init__(self):
        super().__init__()

    def run(self, p):
        current = p.randomInit()   # 'current' is a list of city ids
        valueC = p.evaluate(current)
        i = 0
        while i < p.LIMIT_STUCK:
            successor = p.randomMutant(current)
            valueS = p.evaluate(successor)
            if valueS < valueC:
                current = successor
                valueC = valueS
                i = 0              # Reset stuck counter
            else:
                i += 1

        p._solution = current
        p._value = valueC

class GradientDescent(HillClimbing):

    def __init__(self):
        super().__init__()

    def run(self, p):
        current = p.randomInit() # 'current' is a list of values
        valueC = p.evaluate(current)
        while True:
            successor = p.takeStep(current, valueC)
            valueS = p.evaluate(successor)

            if valueS >= valueC:
                break
            else:
                current = successor
                valueC = valueS

        p._solution = current
        p._value = valueC
