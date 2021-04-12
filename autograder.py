from csp import TetrisCSP, CSPAlgorithms, CSPUtil
from grade_helpers import load_test, verify_domain, assign_variables, create_solution

def test_domain(csp, solution):
  return verify_domain([var.domain() for var in csp.variables()], solution)

def test_constraint(csp, solution):
  assign_variables(csp, csp.variables(), solution)

  for constraint in csp.constraints():
    if not constraint.check(csp.variables(), csp.assignments()):
      return False
  
  return True

def test_algorithm(algo, csp, solution):
  sol = algo(csp)
  return sol == create_solution(csp.variables(), solution) 

def test_future_check(csp, solution):
  var, val = csp.variables()[solution[0]], solution[1]
  
  for constraint in csp.constraints():
    if not constraint.has_future(csp, var, val):
      return False

  return True

def test(tests, tester):
  total_marks, earned_marks = 0, 0
  
  for test in tests:
    name, grid, variables, solution, pass_expected = load_test(test)
    csp = TetrisCSP(grid)

    total_marks += 1

    try:
      # Run the test
      csp.initialize_variables(variables)
      result = tester(csp, solution) if pass_expected else not tester(csp, solution)
      earned = int(result) 
      print("Testing: {}\t [{}/{}]".format(name, earned, 1))

      earned_marks += earned
      
    except NotImplementedError as e:
      print("Testing {}\t [{}]\t [0/1]".format(name, e))

  return earned_marks, total_marks

if __name__ == "__main__":
  total_marks, earned_marks = 0, 0
  
  print("------ Question 1 ------")
  e, t = test(["q1/simple"], test_domain)
  total_marks += t
  earned_marks += e
  
  print("\n------ Question 2 ------")
  e, t = test(["q2/simple", "q2/incorrect"], test_constraint)
  total_marks += t
  earned_marks += e
  
  print("\n------ Question 3 ------")
  e, t = test(["algorithms/multiple_var"], lambda csp,solution : test_algorithm(CSPAlgorithms.backtracking, csp, solution)) # 324 coming in handy
  total_marks += t
  earned_marks += e
  
  print("\n------ Question 4 ------")
  e, t = test(["algorithms/multiple_var"], lambda csp,solution : test_algorithm(CSPAlgorithms.forward_checking, csp, solution)) # 324 coming in handy
  total_marks += t
  earned_marks += e

  print("\n------ Question 5 ------")
  e, t = test(["q5/future_check"], test_future_check) 
  total_marks += t
  earned_marks += e

  print("\n------ Question 6 ------")
  e, t = test(["algorithms/multiple_var"], lambda csp,solution : test_algorithm(CSPAlgorithms.gac, csp, solution)) # 324 coming in handy
  total_marks += t
  earned_marks += e

  print("\n\nTotal Grade: {}/{}".format(earned_marks, total_marks))
  
