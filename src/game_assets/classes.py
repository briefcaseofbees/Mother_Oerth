"""

"""

import enum

if __name__ == "__main__":
    from dice import DieType
else:
    from .dice import DieType


class CreatureClass(enum.Enum):
    artificer       = {"label": "Artificer"}
    barbarian       = {"label": "Barbarian"}
    bard            = {"label": "Bard"}
    cleric          = {"label": "Cleric"}
    druid           = {"label": "Druid"}
    fighter         = {"label": "Fighter"}
    monk            = {"label": "Monk"}
    paladin         = {"label": "Paladin"}
    ranger          = {"label": "Ranger"}
    rogue           = {"label": "Rogue"}
    sorcerer        = {"label": "Sorcerer"}
    warlock         = {"label": "Warlock"}
    wizard          = {"label": "Wizard"}

    @property
    def label(self):
        return self.value["label"]

    @property
    def hit_dice(self):
        return _CLASS_HIT_DICE_TABLE[self.name]

    @property
    def starting_array(self):
        return _CLASS_STARTING_ABILITY_ARRAY_TABLE[self.name]

_CLASS_HIT_DICE_TABLE = {
    CreatureClass.artificer:    DieType.d8,
    CreatureClass.barbarian:    DieType.d12,
    CreatureClass.bard:         DieType.d8,
    CreatureClass.cleric:       DieType.d8,
    CreatureClass.druid:        DieType.d8,
    CreatureClass.fighter:      DieType.d10,
    CreatureClass.monk:         DieType.d8,
    CreatureClass.paladin:      DieType.d10,
    CreatureClass.ranger:       DieType.d10,
    CreatureClass.rogue:        DieType.d8,
    CreatureClass.sorcerer:     DieType.d6,
    CreatureClass.warlock:      DieType.d8,
    CreatureClass.wizard:       DieType.d6
}

_CLASS_STARTING_ABILITY_ARRAY_TABLE = {
    CreatureClass.artificer:    [10, 14, 14, 16, 10, 10],
    CreatureClass.barbarian:    [15, 13, 14, 10, 12, 8],
    CreatureClass.bard:         [8, 14, 12, 13, 10, 15],
    CreatureClass.cleric:       [14, 8, 13, 10, 15, 12],
    CreatureClass.druid:        [8, 12, 14, 13, 15, 10],
    CreatureClass.fighter:      [15, 14, 13, 8, 10, 12],
    CreatureClass.monk:         [12, 15, 13, 10, 14, 8],
    CreatureClass.paladin:      [15, 10, 13, 8, 12, 14],
    CreatureClass.ranger:       [12, 15, 13, 8, 14, 10],
    CreatureClass.rogue:        [12, 15, 13, 14, 10, 8],
    CreatureClass.sorcerer:     [10, 13, 14, 8, 12, 15],
    CreatureClass.warlock:      [8, 14, 13, 12, 10, 15],
    CreatureClass.wizard:       [8, 12, 13, 15, 14, 10]
}




