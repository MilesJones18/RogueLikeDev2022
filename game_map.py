import numpy as np
from tcod.console import Console

import tile_types


class GameMap:
    def __init__(self, width: int, height: int):  # Takes width and height ints and assigns them in one line.
        self.width, self.height = width, height
        self.tiles = np.full((width, height), fill_value=tile_types.floor, order="F")  # Creates a 2D array filled with the tile_types.floor.

        self.tiles[30:33, 22] = tile_types.wall  # Creates a small wall.

    def in_bounds(self, x: int, y: int) -> bool:  # This method returns true if the given x and y values are within the maps boundaries.
        return 0 <= x < self.width and 0 <= y < self.height

    def render(self, console: Console) -> None:  # Quickly renders the entire map.
        console.tiles_rgb[0:self.width, 0:self.height] = self.tiles["dark"]