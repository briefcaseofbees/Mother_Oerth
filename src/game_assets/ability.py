"""
code pertaining to abilities, skills, and proficiencies
"""

import enum
from .dice import DieType, D20Modifier, DifficultyClass
from .progression import LevelAdvancement


class AbilityDeterminationType(enum.Enum):
    random      = enum.auto()
    standard    = enum.auto()
    manual      = enum.auto()


class Ability(enum.Enum):
    str     = {"label": "Strength"}
    dex     = {"label": "Dexterity"}
    con     = {"label": "Constitution"}
    int     = {"label": "Intelligence"}
    wis     = {"label": "Wisdom"}
    cha     = {"label": "Charisma"}

    @property
    def label(self):
        return self.value["label"]

    @property
    def associated_skills(self):
        associated_skills = []
        for skill, ability_type in _SKILL_TO_ABILITY_MAPPING.items():
            if self == ability_type:
                associated_skills.append(skill)
        return associated_skills


class SkillProficiencyRanking(enum.Enum):
    proficiency = 0
    expertise = 1


class Skill(enum.Enum):  # should have a JSON file with the associated skill and description for each skill
    athletics           = {"label": "Athletics"}
    acrobatics          = {"label": "Acrobatics"}
    sleight_of_hand     = {"label": "Sleight of Hand"}
    stealth             = {"label": "Stealth"}
    arcana              = {"label": "Arcana"}
    history             = {"label": "History"}
    investigation       = {"label": "Investigation"}
    nature              = {"label": "Nature"}
    religion            = {"label": "Religion"}
    animal_handling     = {"label": "Animal Handling"}
    insight             = {"label": "Insight"}
    medicine            = {"label": "Medicine"}
    perception          = {"label": "Perception"}
    survival            = {"label": "Survival"}
    deception           = {"label": "Deception"}
    intimidation        = {"label": "Intimidation"}
    performance         = {"label": "Performance"}
    persuasion          = {"label": "Persuasion"}

    @property
    def label(self):
        return self.value["label"]

    @property
    def associated_ability(self):
        return _SKILL_TO_ABILITY_MAPPING[self]


_SKILL_TO_ABILITY_MAPPING = {
    Skill["athletics"]:         Ability.str,
    Skill["acrobatics"]:        Ability.dex,
    Skill["sleight_of_hand"]:   Ability.dex,
    Skill["stealth"]:           Ability.dex,
    Skill["arcana"]:            Ability.int,
    Skill["history"]:           Ability.int,
    Skill["investigation"]:     Ability.int,
    Skill["nature"]:            Ability.int,
    Skill["religion"]:          Ability.int,
    Skill["animal_handling"]:   Ability.wis,
    Skill["insight"]:           Ability.wis,
    Skill["medicine"]:          Ability.wis,
    Skill["perception"]:        Ability.wis,
    Skill["survival"]:          Ability.wis,
    Skill["deception"]:         Ability.cha,
    Skill["intimidation"]:      Ability.cha,
    Skill["performance"]:       Ability.cha,
    Skill["persuasion"]:        Ability.cha
}


class Language(enum.Enum):
    common          = {"label": "Common",       "rarity": "standard"}
    draconic        = {"label": "Draconic",     "rarity": "standard"}
    dwarvish        = {"label": "Dwarvish",     "rarity": "standard"}
    elvish          = {"label": "Elvish",       "rarity": "standard"}
    giant           = {"label": "Giant",        "rarity": "standard"}
    gnomish         = {"label": "Gnomish",      "rarity": "standard"}
    goblin          = {"label": "Goblin",       "rarity": "standard"}
    halfling        = {"label": "Halfling",     "rarity": "standard"}
    orc             = {"label": "Orc",          "rarity": "standard"}
    abyssal         = {"label": "Abyssal",          "rarity": "rare"}
    celestial       = {"label": "Celestial",        "rarity": "rare"}
    deep_speech     = {"label": "Deep Speech",      "rarity": "rare"}
    druidic         = {"label": "Druidic",          "rarity": "rare"}
    infernal        = {"label": "Infernal",         "rarity": "rare"}
    primordial      = {"label": "Primordial",       "rarity": "rare"}
    sylvan          = {"label": "Sylvan",           "rarity": "rare"}
    thieves_cant    = {"label": "Thieves Cant",     "rarity": "rare"}
    undercommon     = {"label": "Undercommon",      "rarity": "rare"}

    @property
    def label(self):
        return self.value["label"]

    @property
    def rarity(self):
        return self.value["rarity"]

    @classmethod
    def by_rarity(cls, rarity):
        return [lang for lang in cls if lang.rarity == rarity]


class SpecialSense(enum.Enum):
    normal = -1  # no special senses
    blind_sight = 0
    dark_vision = 1
    tremor_sense = 2
    true_sight = 3
