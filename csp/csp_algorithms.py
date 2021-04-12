from .csp import CSP
from .csp_util import CSPUtil
from .variable import Variable

class CSPAlgorithms:

  # Here you will implement all the Constraint Solving Algorithms. Below are functions we think
  # will be helpful in your implementations. Please read the handout for specific instructions
  # for each algorithm.
  
  # Helpful Functions:
  # CSP.unassigned_variables() --> returns a list of the unassigned variables left in the CSP 
  # CSP.assignments() --> returns a dictionary which holds variable : value pairs
  # CSP.extract_unassigned() --> returns the next unassigned variable in line
  # CSP.assign(variable, value) --> assigns the given value to the given variable
  # CSP.unassign(variable) --> unassigns the given variable (value = None) 
  # CSP.constraints() --> returns a list of constraints for the CSP
  # CSP.num_unassigned() --> returns the number of unassigned variables
  # Variable.domain() --> returns the domain of the variable instance
  # Constraint.check(variables, assignments) --> returns True iff the given variables and their assignments
  #                                              satisfy the constraint instance
  
  @staticmethod
  def backtracking(csp):
    # Qustion 3, your backtracking algorithm goes here.
    unassigned_vars = csp.unassigned_variables()
    if len(unassigned_vars) == 0:
      #this means all the variables are assigned so there is a solution
      return csp.assignments()
    next_var = csp.extract_unassigned()
    for val in next_var.domain():
      csp.assign(next_var,val)
      constraintOK=True
      for constraint in csp.constraints():
        if csp.num_unassigned() == 0:
          if not constraint.check(csp.variables(), csp.assignments()):
            constraintOK = False
            break
      if constraintOK:
        rest_assignments = CSPAlgorithms.backtracking(csp)
        if rest_assignments is not None:
            return rest_assignments
    csp.unassign(next_var)
    return None


  @staticmethod
  def forward_checking(csp):
    unassigned_vars = csp.unassigned_variables()
    if len(unassigned_vars) == 0:
      #this means all the variables are assigned so there is a solution
      return csp.assignments()
    next_var = csp.extract_unassigned()
    for val in next_var.active_domain():
        csp.assign(next_var, val)
        noDWO=True
        for constraint in csp.constraints():
            if csp.num_unassigned() == 1 and not CSPUtil.forward_check(csp, constraint, next_var):
              noDWO=False
              break
        if noDWO:
          rest_assignments = CSPAlgorithms.forward_checking(csp)
          if rest_assignments is not None:
            return rest_assignments
        CSPUtil.undo_pruning_for(next_var)
    csp.unassign(next_var)
    return None

  @staticmethod
  def gac(csp):
    # Question 6, your gac algorithm goes here.
    unassigned_vars = csp.unassigned_variables()
    if len(unassigned_vars) == 0:
      #this means all the variables are assigned so there is a solution
      return csp.assignments()
    next_var = csp.extract_unassigned()
    for val in next_var.active_domain():
      csp.assign(next_var, val)
      noDWO=True
      if not CSPUtil.gac_enforce(csp, next_var):
          noDWO = False
      if noDWO:
          rest_assignments = CSPAlgorithms.gac(csp)
          if rest_assignments is not None:
              return rest_assignments
      CSPUtil.undo_pruning_for(next_var)
    csp.unassign(next_var)
    return None
