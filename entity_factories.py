from entity import Entity

player = Entity(char="@", color=(255, 255, 255), name="Player", blocks_movement=True)

rat = Entity(char="r", color=(0, 100, 20), name="Rat", blocks_movement=True)
ghoul = Entity(char="G", color=(0, 127, 0), name="Ghoul", blocks_movement=True)