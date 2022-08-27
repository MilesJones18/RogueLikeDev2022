from __future__ import annotations

from typing import Optional, TYPE_CHECKING

import tcod.event

from actions import Action, EscapeAction, BumpAction

if TYPE_CHECKING:
    from engine import Engine


class EventHandler(tcod.event.EventDispatch[Action]):  # Sends events to their proper method based on the event.
    def __init__(self, engine: Engine):
        self.engine = engine

    def handle_events(self) -> None:
        for event in tcod.event.wait():
            action = self.dispatch(event)

            if action is None:
                continue

            action.perform()

            self.engine.handle_enemy_turns()
            self.engine.update_fov()  # Update the FOV before the players next action.

    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:  # Defines a quit event.
        raise SystemExit()

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:  # Receives key presses and either returns an Action or None.
        action: Optional[Action] = None  # action is the variable that will hold whatever subclass of Action we end up assigning to it, defaults to none if no valid key press.

        key = event.sym  # key holds the actual key pressed.

        player = self.engine.player

        if key == tcod.event.K_UP:  # Creates a MovementAction for the key pressed, and defines a direction based off of that key pressed.
            action = BumpAction(player, dx=0, dy=-1)
        elif key == tcod.event.K_DOWN:
            action = BumpAction(player, dx=0, dy=1)
        elif key == tcod.event.K_LEFT:
            action = BumpAction(player, dx=-1, dy=0)
        elif key == tcod.event.K_RIGHT:
            action = BumpAction(player, dx=1, dy=0)

        elif key == tcod.event.K_ESCAPE:  # If the user presses the escape key, will return EscapeAction
            action = EscapeAction(player)

        return action  # Whether action is assigned to an Action subclass or None, we return it.
