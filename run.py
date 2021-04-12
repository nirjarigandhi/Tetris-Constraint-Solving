from tetris import Tetris
from utils import GFrame

if __name__ == "__main__":

  frame = GFrame("Tetris")
  frame.display(Tetris(60, "standard"))
  frame.run() # Runs the Frame + Game 

