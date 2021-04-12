from .variable import Variable
from tetris.tetrominos import Tetromino

class TetrisVariable(Variable, Tetromino):

  def __init__(self, tetromino):
    Variable.__init__(self)
    Tetromino.__init__(self, tetromino.__str__(), tetromino)
