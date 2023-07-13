from setup import Setup
from problem import *

class HillClimbing(Setup):

    def __init__(self):
        Setup.__init__(self)
        self._pType = 0
        self._limitStock = 100
        self._algorithm = "algorithm"

    def setAlgorithm(self, algorithm):
        self._algorithm = algorithm
        

    def run(self):
        pass

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

    def setVariables(self, pType, aType):
        self._pType = pType
        self._aType = aType

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
