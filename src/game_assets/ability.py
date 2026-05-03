import enum
from .dice import DieType, D20Modifier, DifficultyClass
from .progression import LevelAdvancement


class AbilityDeterminationType(enum.Enum):
    random = 1
    standard = 2
    manual = 3


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
