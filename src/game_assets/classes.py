import enum
from .dice import DieType

_CLASS_HIT_DICE_TABLE = {
    "barbarian":    DieType.d12,
    "bard":         DieType.d8,
    "cleric":       DieType.d8,
    "druid":        DieType.d8,
    "fighter":      DieType.d10,
    "monk":         DieType.d8,
    "paladin":      DieType.d10,
    "ranger":       DieType.d10,
    "rogue":        DieType.d8,
    "sorcerer":     DieType.d6,
    "warlock":      DieType.d8,
    "wizard":       DieType.d6
}

_CLASS_STARTING_ARRAY_TABLE = {
    "barbarian":    [15, 13, 14, 10, 12, 8],
    "bard":         [8, 14, 12, 13, 10, 15],
    "cleric":       [14, 8, 13, 10, 15, 12],
    "druid":        [8, 12, 14, 13, 15, 10],
    "fighter":      [15, 14, 13, 8, 10, 12],
    "monk":         [12, 15, 13, 10, 14, 8],
    "paladin":      [15, 10, 13, 8, 12, 14],
    "ranger":       [12, 15, 13, 8, 14, 10],
    "rogue":        [12, 15, 13, 14, 10, 8],
    "sorcerer":     [10, 13, 14, 8, 12, 15],
    "warlock":      [8, 14, 13, 12, 10, 15],
    "wizard":       [8, 12, 13, 15, 14, 10]
}


class CreatureClass(enum.Enum):
    barbarian = {"label": "Barbarian"}
    bard = {"label": "Bard"}
    cleric = {"label": "Cleric"}
    druid = {"label": "Druid"}
    fighter = {"label": "Fighter"}
    monk = {"label": "Monk"}
    paladin = {"label": "Paladin"}
    ranger = {"label": "Ranger"}
    rogue = {"label": "Rogue"}
    sorcerer = {"label": "Sorcerer"}
    warlock = {"label": "Warlock"}
    wizard = {"label": "Wizard"}

    @property
    def label(self):
        return self.value["label"]

    @property
    def hit_dice(self):
        return _CLASS_HIT_DICE_TABLE[self.name]

    @property
    def starting_array(self):
        return _CLASS_STARTING_ARRAY_TABLE[self.name]

