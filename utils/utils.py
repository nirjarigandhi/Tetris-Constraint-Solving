import json

def load_grid(grid_name):

  with open("assets/grids/{}.json".format(grid_name), "r") as f:
    info = json.load(f)

    grid = info["grid"]
    row_count = info["rows"]
    col_count = info["cols"]

  return grid, row_count, col_count


