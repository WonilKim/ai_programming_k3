from problem import *
from optimizer import *

dictProblem = {1: "NumericProblem()", 2: "TspProblem()"}
dictOptimizer = {1: "SteepestAscent()", 2: "FirstChoice()", 3: "GradientDescent()"}

def selectProblem():
    print("Select the problem type:")
    print(" 1. Numeric")
    print(" 2. Tsp")
    pType = int(input("Enter the numbe "))

    # p = Problem()
    # if (pType == 1):
    #     p = NumericProblem()
    # elif (pType == 2):
    #     p = TspProblem()

    p = eval(dictProblem.get(pType))

    p.setVariables()

    return p, pType    

def selectAlgorithm(pType):
    print("Select the algorithm type:")
    print(" 1. Steepest ascent")
    print(" 2. First choice")
    if(pType == 1):
        print(" 3. Gradient descent")

    algType = int(input("Enter the number: "))

    alg = eval(dictOptimizer.get(algType))

    alg.setAlgorithm(dictOptimizer.get(algType).replace("()", ""))

    alg.setVariables(pType, algType)

    return alg, algType


def main():
    p, pType = selectProblem()
    alg, algType = selectAlgorithm(pType)

    alg.run(p)

    p.describe()
    alg.displaySetting()

    p.report()

main()