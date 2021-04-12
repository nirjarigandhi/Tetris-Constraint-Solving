from utils import TETROMINO_GRID_SIZE
from utils import MatrixUtil

class Tetromino:

  def __init__(self, name, copy = None):

    if not copy:
      self._build()
      self._pruned = MatrixUtil.prune(self._original, 0)
    else:
      self._original = copy.get_original_grid()[:]
      self._pruned = copy.get_pruned_grid()[:]

    self._name = name
    self._find_bounds()
    
  def _build(self):
    raise NotImplementedError("Must implement the build method")

  def set_original_grid(self, grid):
    self._original = grid
    self._pruned = MatrixUtil.prune(self._original, 0)
    self._find_bounds()

  def get_original_grid(self):
    return self._original

  def get_pruned_grid(self):
    return self._pruned

  def get_pruned_dimensions(self):
    return len(self._pruned), len(self._pruned[0])

  def get_original_dimensions(self):
    return TETROMINO_GRID_SIZE, TETROMINO_GRID_SIZE

  def upper_bound(self):
    return self._upper_bound

  def lower_bound(self):
    return self._lower_bound

  def right_bound(self):
    return self._right_bound

  def left_bound(self):
    return self._left_bound

  def _find_bounds(self):
    pruned_row_count, pruned_col_count = self.get_pruned_dimensions()
    
    # Upper Bound
    for i in range(pruned_row_count):
      if any(block != 0 for block in self._pruned[i]):
        self._upper_bound = i
        break
    
    # Lower Bound
    for i in range(pruned_row_count -1, -1, -1):
      if any(block != 0 for block in self._pruned[i]):
        self._lower_bound = i
        break

    # Left Bound
    for i in range(pruned_col_count):
      if any(block != 0 for block in MatrixUtil.get_column(self._pruned, i)):
        self._left_bound = i
        break

    # Right Bound
    for i in range(pruned_col_count - 1, -1, -1):
      if any(block != 0 for block in MatrixUtil.get_column(self._pruned, i)):
        self._right_bound = i
        break
  
  def rotate(self, n=1):
    self._original = MatrixUtil.rotate(self._original, n)
    self._pruned = MatrixUtil.prune(self._original, 0)
    self._find_bounds()

  def __hash__(self):

    h = 0
    for row in self._pruned:
      h += hash(tuple(row))
    
    return h

  def __str__(self):
    return self._name
