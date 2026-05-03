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


def skill_check(modifiers:list = None,
                dc:DifficultyClass = DifficultyClass.medium,
                roll_type:D20Modifier = D20Modifier.normal):
    """
    Rolling a D20 against a check (DC) to determine if roll passes or not
    :param modifiers: positive or negative influence on outcome of roll
    :param dc: number that needs to be met, or exceeded
    :param roll_type: whether the roll is with advantage, disadvantage, or neither (normal)
    :return: TODO: feel like I need to figure this out more cleanly
    """
    roll_history = [DieType.d20.roll()]
    roll_result = roll_history[0]

    if roll_type == D20Modifier.disadvantage or roll_type == D20Modifier.advantage:
        roll_history.append(DieType.d20.roll())

        if roll_type == D20Modifier.disadvantage:
            roll_result = min(roll_history)
        if roll_type == D20Modifier.advantage:
            roll_result = max(roll_history)

    # need way to catch 20-rolls (critical success, auto-success)

    premod_roll = roll_result

    if modifiers:
        for modifier in modifiers:
            roll_result += int(modifier)


    # make below better formatted...
    return ((f"rolled a {premod_roll}, "
            f"modifiers = {modifiers} "
            f"==> {roll_result}"),
            f"PASSED on DC {f"{dc.label}, ({dc.number})"}" if roll_result >= dc.number
            else f"FAILED on DC {f"{dc.label}, ({dc.number})"}",
            f"roll history = {roll_history}")


class ToolProficiency(enum.Enum):
    alchemist_supplies          = {"label": "Alchemist Supplies"}
    brewer_supplies             = {"label": "Brewer Supplies"}
    calligrapher_supplies       = {"label": "Calligrapher Supplies"}
    carpenter_tools             = {"label": "Carpenter Tools"}
    cartographer_tools          = {"label": "Cartographer Tools"}
    cobbler_tools               = {"label": "Cobbler Tools"}
    cook_utensils               = {"label": "Cook Utensils"}
    glassblower_tools           = {"label": "Glassblower Tools"}
    jeweler_tools               = {"label": "Jeweler Tools"}
    leatherworker_tools         = {"label": "Leatherworker Tools"}
    mason_tools                 = {"label": "Mason Tools"}
    painter_supplies            = {"label": "Painter Supplies"}
    potter_tools                = {"label": "Potter Tools"}
    smith_tools                 = {"label": "Smith Tools"}
    tinker_tools                = {"label": "Tinker Tools"}
    weaver_tools                = {"label": "Weaver Tools"}
    woodcarver_tools            = {"label": "Woodcarver Tools"}
    disguise_kit                = {"label": "Disguise Kit"}
    forgery_kit                 = {"label": "Forgery Kit"}
    gaming_set                  = {"label": "Gaming Set"}
    herbalism_kit               = {"label": "Herbalism Kit"}
    musical_instrument          = {"label": "Musical Instrument"}
    navigator_tools             = {"label": "Navigator Tools"}
    poisoner_kit                = {"label": "Poisoner Kit"}
    thief_tools                 = {"label": "Thief Tools"}

    @property
    def label(self):
        return self.value["label"]


class GamingSetType(enum.Enum):
    dice                = {"label": "Dice"}
    dragonchess         = {"label": "Dragonchess"}
    playing_cards       = {"label": "Playing Cards"}
    threedragon_ante    = {"label": "Three-Dragon Ante"}

    @property
    def label(self):
        return self.value["label"]


class MusicalInstrumentType(enum.Enum):
    bagpipes        = {"label": "Bagpipes"}
    drum            = {"label": "Drum"}
    dulcimer        = {"label": "Dulcimer"}
    flute           = {"label": "Flute"}
    horn            = {"label": "Horn"}
    lute            = {"label": "Lute"}
    lyre            = {"label": "Lyre"}
    pan_flute       = {"label": "Pan Flute"}
    shawm           = {"label": "Shawm"}
    viol            = {"label": "Viol"}

    @property
    def label(self):
        return self.value["label"]


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
