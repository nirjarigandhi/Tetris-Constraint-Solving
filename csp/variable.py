class Variable:

  def __init__(self):
    self._domain = []
    self._active_domain = []
    self._pruned_domain = {}
    
  def set_domain(self, domain):
    self._domain = domain
    self._active_domain = self._domain[:]

  def reset_active_domain(self):
    self._active_domain = self._domain[:]

  def domain(self):
    return self._domain

  def active_domain(self):
    return self._active_domain

  def add_to_active(self, val):
    self._active_domain.append(val)

  def remove_from_active(self, val):
    self._active_domain.remove(val)
  
