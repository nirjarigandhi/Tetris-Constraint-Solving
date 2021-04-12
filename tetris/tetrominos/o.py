from .tetromino import Tetromino

class O(Tetromino):

  def __init__(self):
    super().__init__("o")

  def _build(self):
    self._original = [[0, 0, 0, 0],
                      [0, 5, 5, 0],
                      [0, 5, 5, 0],
                      [0, 0, 0, 0]]

