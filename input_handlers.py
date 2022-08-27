from typing import Optional

import tcod.event

from actions import Action, EscapeAction, MovementAction


class EventHandler(tcod.event.EventDispatch[Action]):  # Sends events to their proper method based on the event.
    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:  # Defines a quit event.
        raise SystemExit()

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:  # Receives key presses and either returns an Action or None.
        action: Optional[Action] = None  # action is the variable that will hold whatever subclass of Action we end up assigning to it, defaults to none if no valid key press.

        key = event.sym  # key holds the actual key pressed.

        if key == tcod.event.K_UP:  # Creates a MovementAction for the key pressed, and defines a direction based off of that key pressed.
            action = MovementAction(dx=0, dy=-1)
        elif key == tcod.event.K_DOWN:
            action = MovementAction(dx=0, dy=1)
        elif key == tcod.event.K_LEFT:
            action = MovementAction(dx=-1, dy=0)
        elif key == tcod.event.K_RIGHT:
            action = MovementAction(dx=1, dy=0)

        elif key == tcod.event.K_ESCAPE:  # If the user presses the escape key, will return EscapeAction
            action = EscapeAction()

        return action  # Whether action is assigned to an Action subclass or None, we return it.
