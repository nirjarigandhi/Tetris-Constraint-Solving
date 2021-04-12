from .constants import TETROMINO_GRID_SIZE

class MatrixUtil:

  @staticmethod
  def get_column(matrix, n):
    return [row[n] for row in matrix]

  @staticmethod
  def copy(matrix):
    return [row[:] for row in matrix]
  
  @staticmethod
  def rotate(matrix, n=1):
    copy = MatrixUtil.copy(matrix)
    for i in range(n):
      copy = [list(row) for row in zip(*copy[::-1])]
    return copy

  @staticmethod
  def valid_position(grid, r, c):
    return r >= 0 and r < len(grid) and c >= 0 and c < len(grid[0])

  @staticmethod
  def prune(matrix, value):

    new_matrix = []

    wanted_rows = []
    wanted_cols = []

    for i in range(TETROMINO_GRID_SIZE):

      if any(block != value for block in matrix[i]):
        wanted_rows.append(i)

      if any(block != value for block in MatrixUtil.get_column(matrix, i)):
        wanted_cols.append(i)

    for r in wanted_rows:
      row = []
      for c in wanted_cols:
        row.append(matrix[r][c])

      new_matrix.append(row)

    return new_matrix
