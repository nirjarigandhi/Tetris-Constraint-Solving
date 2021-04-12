from .tetromino import Tetromino

class L(Tetromino):

  def __init__(self):
    super().__init__("L")

  def _build(self):
    self._original = [[0, 0, 0, 0],
                      [0, 0, 0, 3],
                      [0, 3, 3, 3],
                      [0, 0, 0, 0]]
