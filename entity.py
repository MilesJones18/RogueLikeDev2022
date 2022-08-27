from typing import Tuple

class Entity:
    def __init__(self,  x: int, y: int, char: str, color: Tuple[int, int, int]):  # Takes four args, x and y coords, char is the the character that represents the entity, color is a tuple for RGB values.
        self.x = x
        self.y = y
        self.char = char
        self.color = color

    def move(self, dx: int, dy: int) -> None:  # Kinda the same as the MovementAction in main.
        self.x += dx
        self.y += dy