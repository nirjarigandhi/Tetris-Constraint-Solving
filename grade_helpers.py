from tetris.tetrominos import *
from csp import TetrisVariable
from json import load

def pprint(grid):
  for i in range(len(grid)):
    for j in range(len(grid[0])):
      print(grid[i][j], end=",")
    print()

def display(grid, sol):
  for var, val in sol.items():
    pos, rotation = val
    var.rotate(rotation)

    TetrominoUtil.place(grid, var, pos)

  pprint(grid)

def to_variable(name):
  var = None
  
  if name == "i":
    var = TetrisVariable(I())
  elif name == "j":
    var = TetrisVariable(J())
  elif name == "l":
    var = TetrisVariable(L())
  elif name == "o":
    var = TetrisVariable(O())
  elif name == "s":
    var = TetrisVariable(S())
  elif name == "t":
    var = TetrisVariable(T())
  elif name == "z":
    var = TetrisVariable(Z())
  
  return var

def generate_variables(variables):
  return [to_variable(var_name) for var_name in variables]

def load_test(test_name):
  with open("assets/tests/{}.json".format(test_name), "r") as f:
    test = load(f)

  return test["test_name"], test["grid"], \
         [to_variable(var_name) for var_name in test["variables"]], \
         test["solution"], test["expected"]

def assign_variables(csp, variables, assignments):
  for i in range(len(variables)):
    csp.assign(variables[i], (tuple(assignments[i][0]), assignments[i][1]))

def create_solution(variables, assignments):
  solution = {}
  for i in range(len(variables)):
    solution[variables[i]] = (tuple(assignments[i][0]), assignments[i][1])

  return solution
    
def verify_domain(answer, solution):
  if len(answer) != len(solution):
    return False

  for i in range(len(answer)):
    if not [(tuple(val[0]), val[1]) for val in solution[i]] == answer[i]:
      return False

  return True
