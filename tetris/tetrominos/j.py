from .tetromino import Tetromino

class J(Tetromino):

  def __init__(self):
    super().__init__("J")

  def _build(self):
    self._original = [[0, 0, 0, 0],
                      [4, 0, 0, 0],
                      [4, 4, 4, 0],
                      [0, 0, 0, 0]]

