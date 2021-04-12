from .constraint import Constraint

class CSP:

  def __init__(self):
    self._constraints = []
    self._variables = []
    self._assignments = {}
    self._unassigned_variables = []
    
  def _build_domain(self, var):
    raise NotImplementedError("build domain must be implemented by a csp")

  def initialize_variables(self, variables):
    for var in variables:
      self._variables.append(var)
      self._assignments[var] = None
      var.set_domain(self._build_domain(var))
      
    self._unassigned_variables = self._variables[:]
    
  def add_constraint(self, constraint):
    self._constraints.append(constraint)

  def remove_constraint(self, constraint):
    self._constraints.remove(constraint)

  def constraints(self):
    return self._constraints
  
  def unassign(self, var):
    self._assignments[var] = None
    if var not in self._unassigned_variables:
      self._unassigned_variables.append(var)

  def extract_unassigned(self):
    var = self._unassigned_variables[0]
    self._unassigned_variables.remove(var)
    return var
    
  def is_assigned(self, var):
    return self._assignments[var] != None

  def variables(self):
    return self._variables

  def unassigned_variables(self):
    return self._unassigned_variables

  def assignments(self):
    return self._assignments

  def num_unassigned(self):
    return len(self._unassigned_variables)
  
  def value_of(self, var):
    return self._assignments[var]

  def assign(self, var, val):
    self._assignments[var] = val
