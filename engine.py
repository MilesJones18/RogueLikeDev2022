from __future__ import annotations

from typing import TYPE_CHECKING

from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov

from input_handlers import EventHandler

if TYPE_CHECKING:
    from entity import Entity
    from game_map import GameMap


class Engine:
    game_map: GameMap

    def __init__(self, player: Entity):
        self.event_handler: EventHandler = EventHandler(self)
        self.player = player

    def handle_enemy_turns(self) -> None:
        for entity in self.game_map.entities - {self.player}:
            print(f'The {entity.name} wonders when it will take a real turn.')

    def update_fov(self) -> None:  # Recompute the visible area based on the players point of view.
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["transparent"],  # Checks if the tiles are floors or walls.
            (self.player.x, self.player.y),  # The POV, or the players coords.
            radius=8,  # How far the FOV extends.
        )

        self.game_map.explored |= self.game_map.visible  # If the tile is "visible" it should be added to "explored".

    def render(self, console: Console,context: Context) -> None:  # Handles drawing the screen, iterates through self.entities and prints them in their proper place.
        self.game_map.render(console)

        context.present(console)

        console.clear()
