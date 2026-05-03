"""

"""

import enum


class CoverType(enum.Enum):
    # TODO: convert to a dictionary, so that the bonuses can be part of the cover type as well

    exposed = 0             # no bonuses
    half = 1                # +2 AC, adv DEX saving throws
    three_quarters = 2      # +5 AC, adv DEX saving throws
    total = 3               # can't be targeted directly


class EnvironmentEffect(enum.Enum):
    deep_water = enum.auto()
    extreme_cold = enum.auto()
    extreme_heat = enum.auto()
    frigid_water = enum.auto()
    heavy_precipitation = enum.auto()
    high_altitude = enum.auto()
    slippery_ice = enum.auto()
    strong_wind = enum.auto()
    thin_ice = enum.auto()


class EnvironmentLightLevel(enum.Enum):
    magical_light = 0
    bright_light = 1
    dim_light = 2
    darkness = 3
    magical_darkness = 4


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