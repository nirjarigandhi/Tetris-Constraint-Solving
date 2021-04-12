from .tetromino import Tetromino

class T(Tetromino):

  def __init__(self):
    super().__init__("t")

  def _build(self):
    self._original = [[0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 7, 0],
                      [0, 7, 7, 7]]
