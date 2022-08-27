from typing import Set, Iterable, Any

from tcod.context import Context
from tcod.console import Console

from actions import EscapeAction, MovementAction
from entity import Entity
from game_map import GameMap
from input_handlers import EventHandler


class Engine:
    def __init__(self, entities: Set[Entity], event_handler: EventHandler, game_map: GameMap,
                 player: Entity):  # Takes three args, entities enforces uniqueness, event_handler is self-explanatory,  player is the player.
        self.entities = entities
        self.event_handler = event_handler
        self.game_map = game_map
        self.player = player

    def handle_events(self, events: Iterable[Any]) -> None:
        for event in events:
            action = self.event_handler.dispatch(
                event)  # Gets the events from event_handler and dispatches them to their proper place.

            if action is None:  # If no key was pressed skip over the rest of the loop.
                continue

            action.perform(self, self.player)  # Simplifys the event handling

    def render(self, console: Console,context: Context) -> None:  # Handles drawing the screen, iterates through self.entities and prints them in their proper place.
        self.game_map.render(console)

        for entity in self.entities:
            console.print(entity.x, entity.y, entity.char, fg=entity.color)

        context.present(console)

        console.clear()
