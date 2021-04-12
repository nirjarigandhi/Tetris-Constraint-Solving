from .tetromino import Tetromino

class S(Tetromino):

  def __init__(self):
    super().__init__("s")

  def _build(self):
    self._original = [[0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [0, 1, 1, 0],
                      [1, 1, 0, 0]]
