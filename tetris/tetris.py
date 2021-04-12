from .game import Game
from state import *
from utils import TILESIZE, ASSETS, TETROMINO_GRID_SIZE, MatrixUtil, Direction, direction_to_vector, BORDER
from .tetrominos import Tetromino
from .tetrominos import TetrominoUtil
from .hud import HUD
from tkinter import PhotoImage

class Tetris(Game):

  def __init__(self, fps, grid_name):
    super().__init__(fps)
    self._DROP_DELAY = 100
    self._delay_counter = self._DROP_DELAY
    self._state = GameState(grid_name)
    self._setup()
    self._hud = HUD(self._state, self._BLOCKS)

  def _setup(self):
    # Build Image Blocks here
    self._BLOCKS = []
    for i in range(len(ASSETS)):
      self._BLOCKS.append(PhotoImage(file=ASSETS[i]))

    self._tetromino = self._state.get_current_tetromino()

  def _can_move_down(self, pos):
    pruned_row_count, pruned_col_count = self._tetromino.get_pruned_dimensions()

    if not self._state.is_valid_position(pos[0] + pruned_row_count - 1, pos[1]):
      return False

    for r in range(pruned_row_count):
      row_section = self._state.get_grid()[pos[0] + r][pos[1]:(pos[1] + pruned_col_count)]
      
      # Check if you can drop (needs to be only for the parts which are blocks
      for c in range(pruned_col_count):
        if self._tetromino.get_pruned_grid()[r][c] > 0 and row_section[c] != 0:
          return False

    return True

  def _can_move_left(self, pos):
    pruned_row_count, pruned_col_count = self._tetromino.get_pruned_dimensions()
    
    # Check left bound
    if not self._state.is_valid_position(pos[0], pos[1]):
      return False
    
    for c in range(pruned_col_count):
      column = MatrixUtil.get_column(self._state.get_grid(), pos[1] + c) 
      col_section = column[pos[0]:(pos[0] + pruned_row_count)]

      # Check if you can drop (needs to be only for the parts which are blocks
      for r in range(pruned_row_count):
        if self._tetromino.get_pruned_grid()[r][c] > 0 and col_section[r] != 0:
          return False

    return True
  
  def _can_move_right(self, pos):
    pruned_row_count, pruned_col_count = self._tetromino.get_pruned_dimensions()
    right_bound = self._tetromino.right_bound()

    if not self._state.is_valid_position(pos[0], pos[1] + right_bound):
      return False

    for c in range(pruned_col_count):
      column = MatrixUtil.get_column(self._state.get_grid(), pos[1] + right_bound - c) 
      col_section = column[pos[0]:(pos[0] + pruned_row_count)]

      # Check if you can drop (needs to be only for the parts which are blocks
      for r in range(pruned_row_count):
        if self._tetromino.get_pruned_grid()[r][c] > 0 and col_section[r] != 0:
          return False

    return True
 
  def move_tetromino(self, direction):
    pos = self._state.get_current_tetromino_position()    
    delta = direction_to_vector(direction)
    new_pos = (pos[0] + delta[0], pos[1] + delta[1])

    can_move = False
    
    if direction == Direction.SOUTH:
      can_move = self._can_move_down(new_pos)

    elif direction == Direction.WEST:
      can_move = self._can_move_left(new_pos)

    elif direction == Direction.EAST:
      can_move = self._can_move_right(new_pos)
    
    if not can_move:
      return False
    
    self._state.update_tetromino_position(new_pos) 
    return True

  def _within_bounds(self, copy):
    pos = self._state.get_current_tetromino_position()

    return self._state.is_valid_position(copy.lower_bound() + pos[0], pos[1]) and \
      self._state.is_valid_position(pos[0], pos[1] + copy.right_bound()) and \
      self._state.is_valid_position(copy.upper_bound() + pos[0], pos[1]) and \
      self._state.is_valid_position(pos[0], pos[1] - copy.left_bound())
  
  def _no_collisions(self, copy):
    pos = self._state.get_current_tetromino_position()
    pruned_row_count, pruned_col_count = copy.get_pruned_dimensions()
    pruned_grid = copy.get_pruned_grid()

    for r in range(pruned_row_count):
      for c in range(pruned_col_count):
        if self._state.get_grid()[r + pos[0]][c + pos[1]]:
          return False

    return True
  
  def _rotate_tetromino(self):
    # Make a copy of the tetromino and rotate it
    copy = TetrominoUtil.copy(self._tetromino)

    # Rotate it
    copy.rotate()

    if self._within_bounds(copy) and self._no_collisions(copy):
      self._tetromino.rotate()
    
  def get_dimensions(self):
    return (self._state.get_col_count()) * TILESIZE + self._hud.get_width() - BORDER, \
           (self._state.get_row_count() - self._state.get_buffer()) * TILESIZE + BORDER * 2

  def bind_inputs(self, frame):
    frame.bind('<Left>', lambda event: self.move_tetromino(Direction.WEST))
    frame.bind('<Right>', lambda event: self.move_tetromino(Direction.EAST))
    frame.bind('<Down>', lambda event: self.move_tetromino(Direction.SOUTH))
    frame.bind('<space>', lambda event: self._rotate_tetromino())

  def _update(self):

    self._delay_counter -= 1
    if self._delay_counter <= 0:
      was_moved = self.move_tetromino(Direction.SOUTH)
      
      if not was_moved:
        self._state.merge_tetromino()
        self._state.check_for_clears()
        self._tetromino = self._state.get_current_tetromino()
        
      self._delay_counter = self._DROP_DELAY
      
    self._canvas.update()
    
  def _render(self):

    try:
      self._canvas.delete("all")
      self._master.images = []
      
      # Draw the grid
      for i in range(self._state.get_row_count() - self._state.get_buffer()):
        for j in range(self._state.get_col_count()):
          block = self._BLOCKS[self._state.get_grid()[i + self._state.get_buffer()][j]]
          self._master.images.append(block)
          self._canvas.create_image(j * TILESIZE + BORDER, i * TILESIZE + BORDER, image=block, anchor="nw")

      # Draw the HUD
      self._master.images.extend(self._hud.render(self._canvas, TILESIZE * self._state.get_col_count()))
      
      # Draw the tetromino
      left_corner = self._state.get_current_tetromino_position()
      tetromino_grid = self._tetromino.get_pruned_grid()
      rows, cols = self._tetromino.get_pruned_dimensions()
      
      for i in range(rows):
        for j in range(cols):
          if (tetromino_grid[i][j] == 0): # Skip empty spots, no need to draw them
            continue
          
          block = self._BLOCKS[tetromino_grid[i][j]]
          self._master.images.append(block)
          self._canvas.create_image((left_corner[1] + j) * TILESIZE + BORDER,
                                    (left_corner[0] + i - self._state.get_buffer()) * TILESIZE + BORDER,
                                    image=block, anchor="nw")
            
      # Draw a Border
      width, height = self.get_dimensions()
      self._canvas.create_rectangle(0, 0, width, height, width=BORDER*2, outline="#CD6600")
            
    except Exception as e:
      return

  def _check_finished(self):
    game_over = self._state.is_buffer_reached()
    
    if game_over:
      print("Game Over:\n\tYou got a score of {}".format(self._state.get_score()))
      self.set_done(True)
