from .tetromino import Tetromino
from .s import S
from .z import Z
from .l import L
from .j import J
from .o import O
from .i import I
from .t import T
import random
from collections import deque
from utils import MatrixUtil

TETROMINOS = [I(), J(), Z(), S(), L(), T(), O()]

class TetrominoUtil:

  @staticmethod
  def create_line_up(size):
    line_up = deque()
    for i in range(size):
      line_up.append(TetrominoUtil.get_random_tetromino())

    return line_up

  @staticmethod
  def get_random_tetromino():
    return TetrominoUtil.copy(TETROMINOS[random.randint(0, len(TETROMINOS) - 1)])

  @staticmethod
  def rotation_limit(tetromino):
    rotated = MatrixUtil.rotate(MatrixUtil.copy(tetromino.get_pruned_grid()))
    limit = 1
    
    while (rotated != tetromino.get_pruned_grid()):
      limit += 1
      rotated = MatrixUtil.rotate(rotated)

    return limit
  
  @staticmethod
  def copy(tetromino):
    t = Tetromino(tetromino.__str__(), tetromino)
    return t
    
  @staticmethod
  def place(grid, tetromino, pos):
    block_grid = tetromino.get_pruned_grid()
    rows, cols = tetromino.get_pruned_dimensions()
    for r in range(rows):
      for c in range(cols):
        dr, dc = pos[0] + r, pos[1] + c
        if MatrixUtil.valid_position(grid, dr, dc) and block_grid[r][c] > 0:
          grid[dr][dc] = block_grid[r][c]
 
