import copy

import tcod

from engine import Engine
import entity_factories
from procgen import generate_dungeon


def main() -> None:
    screen_width = 80  # Setting up the window specs.
    screen_height = 50

    map_width = 80
    map_height = 45

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    max_monsters_per_room = 2

    tileset = tcod.tileset.load_tilesheet(  # Telling TCOD which tileset to use.
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    player = copy.deepcopy(entity_factories.player)  # Initializes the player.

    engine = Engine(player=player)

    engine.game_map = generate_dungeon(
        max_rooms=max_rooms,
        room_min_size=room_min_size,
        room_max_size=room_max_size,
        map_width=map_width,
        map_height=map_height,
        max_monsters_per_room=max_monsters_per_room,
        engine=engine,
    )
    engine.update_fov()

    with tcod.context.new_terminal(  # This part actually creates the screen.
        screen_width,
        screen_height,
        tileset=tileset,
        title="Roguelike Tutorial",
        vsync=True,
    ) as context:
        root_console = tcod.Console(screen_width, screen_height, order="F")  # This creates the "console" that we draw on. Order reverses the x and y in numpy (default is y, x)
        while True:  # Sets the "game loop" that exists until we call system exit
            engine.render(console=root_console, context=context)  # Pulls the needed info from Engine, and renders it on the console.

            engine.event_handler.handle_events()


if __name__ == "__main__":
    main()