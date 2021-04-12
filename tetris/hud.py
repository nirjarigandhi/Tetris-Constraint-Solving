from state import game_state
from utils import TILESIZE, TETROMINO_GRID_SIZE

class HUD:

  def __init__(self, game_state, block_images):
    self._state = game_state
    self._width = 6 * TILESIZE
    self._height = 20 * TILESIZE + 10
    self._block_images = block_images
    
  def get_width(self):
    return self._width

  def get_height(self):
    return self._height

  def render(self, canvas, x):

    PIXEL_SHIFT = 5

    # Background Rect
    canvas.create_rectangle(x + PIXEL_SHIFT, 0, x + self._width - PIXEL_SHIFT,
                            self._height - PIXEL_SHIFT, width=5, outline="#CD6600", fill="#282525")

    # Score
    canvas.create_text(x + PIXEL_SHIFT * 11, PIXEL_SHIFT + 40, font=("Times", 24),
                       fill="white", text="Score:\n{}".format(self._state.get_score()))

    # Make a line separator
    canvas.create_line(x + PIXEL_SHIFT, PIXEL_SHIFT * 30, x + PIXEL_SHIFT + self._width, PIXEL_SHIFT * 30, width=5,fill="#CD6600")

    # Next
    canvas.create_text(x + PIXEL_SHIFT * 11, PIXEL_SHIFT * 40, font=("Times", 24),
                       fill="white", text="Next:")
    
    images = []
    line_up = self._state.get_line_up()
    for k in range(len(line_up)):
      tetromino_grid = line_up[k].get_pruned_grid()
      rows, cols = line_up[k].get_pruned_dimensions()
      
      for i in range(rows):
        for j in range(cols):
          if (tetromino_grid[i][j] == 0): # Skip empty spots, no need to draw them
            continue
          
          block = self._block_images[tetromino_grid[i][j]]
          images.append(block)
          canvas.create_image(x + PIXEL_SHIFT * 7 + j * TILESIZE,
                              PIXEL_SHIFT * 75 + k * (TETROMINO_GRID_SIZE - 1) * TILESIZE + (i - self._state.get_buffer()) * TILESIZE,
                              image=block, anchor="nw")
   
    return images
