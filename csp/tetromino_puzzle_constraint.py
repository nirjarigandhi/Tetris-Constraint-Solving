from .constraint import Constraint
from utils import MatrixUtil
from tetris.tetrominos import TetrominoUtil
from .csp_algorithms import CSPAlgorithms

class TetrominoPuzzleConstraint(Constraint):
  
  def __init__(self, grid):
    super().__init__()
    self._grid = MatrixUtil.copy(grid)

    # Helpful Functions:
    # MatrixUtil.copy(matrix) --> returns a copy of the matrix
    # MatrixUtil.valid_position(matrix, row, col) --> returns True iff (row, col) is a valid position within the matrix
    # TetrominoUtil.copy(tetromino) --> returns a copy of the tetromino
    # Tetromino.get_pruned_grid() --> returns a condensed version of the block grid representing a tetromino piece.
    #                                 Use this over Tetromino.get_original_grid()!
    # Tetromino.get_pruned_dimensions() --> returns row_count, col_count of the tetromino piece
    # Tetromino.rotate(rotation_amount) --> rotates the tetromino piece rotation_amount times
    
  def check(self, variables, assignments):
    grid_copy = MatrixUtil.copy(self._grid)

    for var in variables:
      move = assignments[var]
      var_copy = TetrominoUtil.copy(var)
      if move is not None:
        pos = move[0]
        var_copy.rotate(move[1])
        rows, cols = var_copy.get_pruned_dimensions()
        pruned_grid = var_copy.get_pruned_grid()

        if not MatrixUtil.valid_position(grid_copy, pos[0] + rows - 1,pos[1]+ cols - 1):
          return False
        for r in range(rows):
          for c in range(cols):
            dr, dc = pos[0]+r, pos[1]+c
            if grid_copy[dr][dc] > 0 and pruned_grid[r][c] > 0:
              return False
            grid_copy[dr][dc] = pruned_grid[r][c]

    return True

  def has_future(self, csp, var, val):
    unassigned_vars = csp.unassigned_variables()
    if len(unassigned_vars) == 0:
      return True
    csp.assign(var,val)
    next_var = csp.extract_unassigned()
    for val in next_var.domain():
      csp.assign(next_var,val)
      constraintOK=True
      for constraint in csp.constraints():
        if not constraint.check(csp.variables(), csp.assignments()):
          constraintOK = False
          break
      if constraintOK:
        return TetrominoPuzzleConstraint.has_future(self, csp, var, val)
    csp.unassign(next_var)
    csp.unassign(var)
    return False