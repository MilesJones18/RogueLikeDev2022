from typing import Iterable, Any

from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov

from entity import Entity
from game_map import GameMap
from input_handlers import EventHandler


class Engine:
    def __init__(self, event_handler: EventHandler, game_map: GameMap, player: Entity):  # Takes three args, entities enforces uniqueness, event_handler is self-explanatory,  player is the player.
        self.event_handler = event_handler
        self.game_map = game_map
        self.player = player
        self.update_fov()

    def handle_enemy_turns(self) -> None:
        for entity in self.game_map.entities - {self.player}:
            print(f'The {entity.name} wonders when it will take a real turn.')

    def handle_events(self, events: Iterable[Any]) -> None:
        for event in events:
            action = self.event_handler.dispatch(
                event)  # Gets the events from event_handler and dispatches them to their proper place.

            if action is None:  # If no key was pressed skip over the rest of the loop.
                continue

            action.perform(self, self.player)  # Simplifys the event handling
            self.handle_enemy_turns()
            self.update_fov()  # Update the FOV before the players next action.

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
