import tcod

from actions import EscapeAction, MovementAction
from input_handlers import EventHandler


def main() -> None:
    screen_width = 80  # Setting up the window specs.
    screen_height = 50

    player_x = int(screen_width / 2)  # This tracks and stores the players x coords.
    player_y = int(screen_height / 2)  # This tracks and stores the players y coords.

    tileset = tcod.tileset.load_tilesheet(  # Telling TCOD which tileset to use.
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    event_handler = EventHandler()  # Receives events and processes them.

    with tcod.context.new_terminal(  # This part actually creates the screen.
        screen_width,
        screen_height,
        tileset=tileset,
        title="Roguelike Tutorial",
        vsync=True,
    ) as context:
        root_console = tcod.Console(screen_width, screen_height, order="F")  # This creates the "console" that we draw on. Order reverses the x and y in numpy (default is y, x)
        while True:  # Sets the "game loop" that exists until we call system exit
            root_console.print(x=player_x, y=player_y, string="@")  # Prints out the @ symbol on the console, calls back to player_x and player_y to get coord info.

            context.present(root_console)  # Nothing would print without this line

            root_console.clear()

            for event in tcod.event.wait():  # Gives us a way to exit the window.
                action = event_handler.dispatch(event)  # Gets the events from event_handler and dispatches them to their proper place.

                if action is None:  # If no key was pressed skip over the rest of the loop.
                    continue

                if isinstance(action, MovementAction):  # Grabs the dx, dy vars from the MovementAction event and adds them to the players current position, moving the player.
                    player_x += action.dx
                    player_y += action.dy

                elif isinstance(action, EscapeAction):  # If the user hits the escape key, the window should close.
                    raise SystemExit()


if __name__ == "__main__":
    main()