from .tetromino import Tetromino

class I(Tetromino):

  def __init__(self):
    super().__init__("I")

  def _build(self):
    self._original = [[0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [6, 6, 6, 6],
                      [0, 0, 0, 0]]

