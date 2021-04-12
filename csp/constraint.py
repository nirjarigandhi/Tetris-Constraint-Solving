class Constraint:

  def check(self, variables, assignments):
      
    raise NotImplementedError("check needs to be implemented")

  def has_future(self, csp, var, val):
    raise NotImplementedError("check needs to be implemented")
