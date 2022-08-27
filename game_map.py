from __future__ import annotations

from typing import Iterable, Optional, TYPE_CHECKING

import numpy as np
from tcod.console import Console

import tile_types

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity


class GameMap:
    def __init__(self, engine: Engine, width: int, height: int,
                 entities: Iterable[Entity] = ()):  # Takes width and height ints and assigns them in one line.
        self.engine = engine
        self.width, self.height = width, height
        self.entities = set(entities)
        self.tiles = np.full((width, height), fill_value=tile_types.wall,
                             order="F")  # Creates a 2D array filled with the tile_types.floor.

        self.visible = np.full((width, height), fill_value=False, order="F")  # Tiles that the player can see currently.
        self.explored = np.full((width, height), fill_value=False, order="F")  # Tiles that the player has seen.

    def get_blocking_entity_at_location(self, location_x: int, location_y: int) -> Optional[
        Entity]:  # Checks if an entity is in the way.
        for entity in self.entities:
            if entity.blocks_movement and entity.x == location_x and entity.y == location_y:
                return entity

        return None

    def in_bounds(self, x: int,
                  y: int) -> bool:  # This method returns true if the given x and y values are within the maps boundaries.
        return 0 <= x < self.width and 0 <= y < self.height

    def render(self, console: Console) -> None:  # Quickly renders the entire map.
        console.tiles_rgb[0: self.width, 0: self.height] = np.select(
            # Allows us to conditionally place tiles based on the condlist.
            condlist=[self.visible, self.explored],
            choicelist=[self.tiles["light"], self.tiles["dark"]],
            default=tile_types.SHROUD,  # Default
        )

        for entity in self.entities:
            if self.visible[entity.x, entity.y]:  # Only print entities that are in FOV.
                console.print(entity.x, entity.y, entity.char, fg=entity.color)
