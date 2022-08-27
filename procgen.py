from __future__ import annotations

import random
from typing import Iterator, List, Tuple, TYPE_CHECKING

import tcod

import entity_factories
from game_map import GameMap
import tile_types

if TYPE_CHECKING:
    from engine import Engine


class RectangularRoom:
    def __init__(self, x: int, y: int, width: int,
                 height: int):  # Takes the x and y coords of the top left corner and computes the bottom right coords.
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height

    @property
    def center(self) -> Tuple[int, int]:  # Describes the x and y coords of the center of the room.
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)

        return center_x, center_y

    @property
    def inner(self) -> Tuple[slice, slice]:  # Returns two slices that represent the inner portion of the room.
        return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)

    def intersects(self, other: RectangularRoom) -> bool:  # Checks if rooms intersect.
        return (
                self.x1 <= other.x2
                and self.x2 >= other.x1
                and self.y1 <= other.y2
                and self.y2 >= other.y1
        )


def place_entities(
        room: RectangularRoom, dungeon: GameMap, maximum_monsters: int,
) -> None:
    number_of_monsters = random.randint(0, maximum_monsters)  # Takes a random number between 0 and max.

    for i in range(number_of_monsters):  # Selects a random x and y to place entity.
        x = random.randint(room.x1 + 1, room.x2 - 1)
        y = random.randint(room.y1 + 1, room.y2 - 1)

        if not any(entity.x == x and entity.y == y for entity in
                   dungeon.entities):  # Does quick check to make sure there is no entity where it is placing the new one.
            if random.random() < 0.8:
                entity_factories.rat.spawn(dungeon, x, y)
            else:
                entity_factories.ghoul.spawn(dungeon, x, y)


def tunnel_between(
        # Takes two args, tuples consisting of two ints. It should return an iterator of a tuple of two ints. ALl x and y coords on the map.
        start: Tuple[int, int], end: Tuple[int, int]
) -> Iterator[Tuple[int, int]]:  # Return an L shaped tunnel between these two points.
    x1, y1 = start  # Grabs the coords out of the tuples.
    x2, y2 = end
    if random.random() < 0.5:  # 50% chance.
        corner_x, corner_y = x2, y1  # Move horizontally, then vertically.

    else:  # Move vertically, then horizontally.
        corner_x, corner_y = x1, y2

    for x, y in tcod.los.bresenham((x1, y1), (corner_x,
                                              corner_y)).tolist():  # Uses bresenham lines to draw an L shaped tunnel, .tolist() converts the points in the line into a list.
        yield x, y  # Allows the function to pick up where it left off instead of starting from the beginning.
    for x, y in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist():
        yield x, y


def generate_dungeon(
        max_rooms: int,  # Max number of rooms allowed in the dungeon.
        room_min_size: int,  # Minimum size of a room.
        room_max_size: int,  # Max size of a room.
        map_width: int,  # The width of the GameMap.
        map_height: int,  # The height of the GameMap.
        max_monsters_per_room: int,
        engine: Engine,  # Player Entity.
) -> GameMap:
    player = engine.player
    dungeon = GameMap(engine, map_width, map_height, entities=[player])  # Generates new GameMap

    rooms: List[RectangularRoom] = []  # List of all rooms.

    for r in range(max_rooms):  # Iterates from 0 to max rooms - 1.
        room_width = random.randint(room_min_size,
                                    room_max_size)  # Uses given parameters to set the rooms width and height.
        room_height = random.randint(room_min_size, room_max_size)

        x = random.randint(0, dungeon.width - room_width - 1)
        y = random.randint(0, dungeon.height - room_height - 1)

        new_room = RectangularRoom(x, y, room_width,
                                   room_height)  # RectangularRoom makes rectangles easier to work with.

        if any(new_room.intersects(other_room) for other_room in
               rooms):  # Runs through the other rooms to see if they intersect with the current room.
            continue  # This room intersects so go to the next attempt.
        # If there are no intersections the room is valid.

        dungeon.tiles[new_room.inner] = tile_types.floor  # Dig out this rooms inner area.

        if len(rooms) == 0:  # The first room the player starts in.
            player.place(*new_room.center, dungeon)


        else:  # All rooms after the first.
            for x, y in tunnel_between(rooms[-1].center,
                                       new_room.center):  # Dig out a tunnel between this room and the previous.
                dungeon.tiles[x, y] = tile_types.floor

        place_entities(new_room, dungeon,
                       max_monsters_per_room)  # Takes three args, the room thats being made, dungeon which holds the entities, and max monsters so it knows how many to make.

        rooms.append(new_room)  # Append the new room to the list.

    return dungeon
