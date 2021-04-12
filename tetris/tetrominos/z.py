from .tetromino import Tetromino

class Z(Tetromino):

  def __init__(self):
    super().__init__("z")

  def _build(self):
    self._original = [[0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [0, 2, 2, 0],
                      [0, 0, 2, 2]]
