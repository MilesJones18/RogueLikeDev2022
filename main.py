import tcod

from engine import Engine
from entity import Entity
from game_map import GameMap
from input_handlers import EventHandler


def main() -> None:
    screen_width = 80  # Setting up the window specs.
    screen_height = 50

    map_width = 80
    map_height = 45

    tileset = tcod.tileset.load_tilesheet(  # Telling TCOD which tileset to use.
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    event_handler = EventHandler()  # Receives events and processes them.

    player = Entity(int(screen_width / 2), int(screen_height / 2), "@", (255, 255, 255))  # initializes the player.
    npc = Entity(int(screen_width / 2 - 5), int(screen_height / 2), "@", (255, 255, 0))  # initializes a new npc.
    entities = {npc, player}

    game_map = GameMap(map_width, map_height)

    engine = Engine(entities=entities, event_handler=event_handler, game_map=game_map, player=player)

    with tcod.context.new_terminal(  # This part actually creates the screen.
        screen_width,
        screen_height,
        tileset=tileset,
        title="Roguelike Tutorial",
        vsync=True,
    ) as context:
        root_console = tcod.Console(screen_width, screen_height, order="F")  # This creates the "console" that we draw on. Order reverses the x and y in numpy (default is y, x)
        while True:  # Sets the "game loop" that exists until we call system exit
            engine.render(console=root_console, context=context)  # Pulls the need info from Engine, and renders it on the console.

            events = tcod.event.wait()

            engine.handle_events(events)


if __name__ == "__main__":
    main()