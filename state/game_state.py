from utils.utils import load_grid
from tetris.tetrominos import TetrominoUtil
from utils import TETROMINO_GRID_SIZE, MatrixUtil
from collections import deque

class GameState:

  def __init__(self, grid_name):
    self._grid, self._row_count, self._col_count = load_grid(grid_name)
    self._line_up = TetrominoUtil.create_line_up(4)

    self._BUFFER = 4
    self._add_buffer()

    self._curr_tetromino = self.get_next_tetromino()
    self._curr_tetromino_pos = (0, 0) # The position it is currently in ( (0,0) is temp)
    self._score = 0
    
  def _add_buffer(self):
    self._grid = ([[0] * self._col_count] * self._BUFFER) + self._grid
    self._row_count += self._BUFFER

  def _can_drop(self, starting_row):
    for c in range(self._col_count):
      if self._grid[starting_row][c] > 0 and self._grid[starting_row + 1][c] > 0:
        return False

    return True
    
  def get_grid(self):
    return self._grid

  def get_score(self):
    return self._score

  def is_valid_position(self, r, c):
    return MatrixUtil.valid_position(self._grid, r, c)
  
  def get_line_up(self):
    return self._line_up

  def set_line_up(self, line_up):
    self._line_up = line_up
  
  def get_next_tetromino(self):
    tetromino = self._line_up.popleft() # Take the first in the queue
    self._line_up.append(TetrominoUtil.get_random_tetromino()) # Fill the queue back up
    return tetromino

  def merge_tetromino(self):
    TetrominoUtil.place(self._grid, self._curr_tetromino, self._curr_tetromino_pos)
    self._curr_tetromino_pos = (0,0) # Temp (0, 0)
    self._curr_tetromino = self.get_next_tetromino() # Get the next tetromino in the line up
    
  def get_current_tetromino(self):
    return self._curr_tetromino

  def get_current_tetromino_position(self):
    return self._curr_tetromino_pos
  
  def update_tetromino_position(self, pos):
    self._curr_tetromino_pos = pos
    
  def get_row_count(self):
    return self._row_count

  def get_col_count(self):
    return self._col_count

  def get_buffer(self):
    return self._BUFFER

  def is_buffer_reached(self):
    for i in range(self._BUFFER - 1, -1, -1):
      if any(block != 0 for block in self._grid[i]):
        return True

    return False
  
  def check_for_clears(self):
    starting_row = None
    for r in range(self._row_count - 1, self._BUFFER -1, -1):
      if all(block > 0 for block in self._grid[r]):
        self._grid[r] = [0] * self._col_count
        starting_row = r
        self._score += 1000

    if starting_row:
      self.drop(starting_row)

  def drop(self, starting_row):

    if starting_row == self._row_count - 1:
      starting_row -= 1

    while(self._can_drop(starting_row)):
      # Start from self._buffer from the bottom row and move blocks down if you can
      for r in range(starting_row, self._BUFFER - 1, -1):
        for c in range(0, self._col_count):
          # If the spot below you is not blocked, drop down
          if not self._grid[r + 1][c]:
            self._grid[r + 1][c] = self._grid[r][c] # Block above becomes the block below
            self._grid[r][c] = 0 # Now the block left and open space
