class Action:
    pass


class EscapeAction(Action):  # Used for exiting the game.
    pass


class MovementAction(Action):  # Used to move the player around.
    def __init__(self, dx: int, dy: int):
        super().__init__()

        self.dx = dx
        self.dy = dy