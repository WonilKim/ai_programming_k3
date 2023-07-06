
from problem import NumericProblem


def testSteepestAscent():
    prob = NumericProblem()

    # Create an instance of numerical optimization problem
    prob.setVariables()
    # Call the search algorithm
    prob.steepestAscent()
    # Show the problem and algorithm settings
    prob.describe()
    prob.displaySetting()
    # Report results
    prob.report()

def testFirstChoice():
    prob = NumericProblem()

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
# testSteepestAscent()
testFirstChoice()