class CSPUtil:

  prunes = {}

  @staticmethod
  def prune(var, val, for_var):
    if for_var not in CSPUtil.prunes:
      CSPUtil.prunes[for_var]= []

    CSPUtil.prunes[for_var].append((var, val))
    var.remove_from_active(val)
  
  @staticmethod
  def undo_pruning_for(pvar):
    if pvar in CSPUtil.prunes:
      for (var, val) in CSPUtil.prunes[pvar]:
        var.add_to_active(val)
      del CSPUtil.prunes[pvar]

  @staticmethod
  def forward_check(csp, constraint, for_var):
    var = csp.unassigned_variables()[0]

    active_domain = var.active_domain()[:]
    for val in active_domain:
      csp.assign(var, val)
      if not constraint.check(csp.variables(), csp.assignments()):
        CSPUtil.prune(var, val, for_var)
      csp.unassign(var)

    return len(var.active_domain()) > 0

  @staticmethod
  def gac_enforce(csp, fvar):
    constraints = csp.constraints()[:]
    while constraints:
      con = constraints.pop()
      for var in csp.variables():
        active_domain = var.active_domain()[:]
        for val in active_domain:
          if not con.has_future(csp, var, val):
            CSPUtil.prune(var, val, fvar)

            if len(var.active_domain()) == 0:
              return False

    return True
          
    
