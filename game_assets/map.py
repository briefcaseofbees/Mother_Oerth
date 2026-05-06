"""

"""


class MapSquare:
    def __init__(self):
        self.fog_of_war = True          # whether the square is currently visible by the player
        self.difficult_terrain = False  # whether the square is classified as "Difficult Terrain"
        pass


class Map:
    def __init__(self):
        """
        per-user object where the MapSquare objects live
        """
        pass