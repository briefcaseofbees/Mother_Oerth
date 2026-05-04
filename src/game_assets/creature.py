"""
houses code pertaining to the mechanical aspects of creatures-- includes creature-size, creature-conditions,
creature-classes, creature-metadata, etc.
"""

import enum, math
import json

from .ability import Ability, Skill
from .alignment import Alignment
from .dice import DieType
from .progression import LevelAdvancement, _CR_XP_TABLE

_CREATURE_JSON_FILENAME = "./resources/creatures.json"


class CreatureAttitude(enum.Enum):
    # overall sentiment towards another creature
    hostile = 0  # disadvantage on ability check to influence creature
    indifferent = 1  # no desire to help or hinder (normal/default)
    friendly = 2  # advantage on ability check to influence creature


class CreatureSentiment(enum.Enum):
    # creature sentiment towards a specific action that it's being asked to do
    unwilling = 0  # no ability checks needed, it doesn't comply
    hesitant = 1  # ability check whose outcome is dependent on CreatureAttitude
    willing = 2  # no ability checks needed, it will fulfill your request in the way it prefers


class CreatureType(enum.Enum):
    beast           = {"label": "Beast"}
    humanoid        = {"label": "Humanoid"}
    monstrosity     = {"label": "Monstrosity"}
    dragon          = {"label": "Dragon"}
    fiend           = {"label": "Fiend"}
    celestial       = {"label": "Celestial"}
    undead          = {"label": "Undead"}
    elemental       = {"label": "Elemental"}
    fey             = {"label": "Fey"}
    ooze            = {"label": "Ooze"}
    construct       = {"label": "Construct"}
    plant           = {"label": "Plant"}
    giant           = {"label": "Giant"}
    aberration      = {"label": "Aberration"}

    @property
    def label(self):
        return self.value["label"]


class CreatureSize(enum.Enum):
    tiny            = {"label": "Tiny"}
    small           = {"label": "Small"}
    medium          = {"label": "Medium"}
    large           = {"label": "Large"}
    huge            = {"label": "Huge"}
    gargantuan      = {"label": "Gargantuan"}

    @property
    def label(self):
        return self.value["label"]

    @property
    def hit_dice(self):
        return _CREATURE_SIZE_HIT_DICE_TABLE[self]

    @classmethod
    def creature_size(cls, given_height, given_weight):
        # based on given height and weight, it will fall into one of the CreatureSize categories
        # priority is given to height over weight-- reason:
        #   a sentient cloud is likely large/huge, but weight-wise, is likely typed as small...

        creature_size_based_on_height = int
        creature_size_based_on_weight = int
        resultant_creature_size = None

        for creature_size, height_range in _CREATURE_SIZE_HEIGHT_TABLE.items():
            if height_range[1] is None:
                creature_size_based_on_height = CreatureSize.gargantuan
                break

            if height_range[0] <= given_height <= height_range[1]:
                creature_size_based_on_height = creature_size
                break

        for creature_size, weight_range in _CREATURE_SIZE_WEIGHT_TABLE.items():
            if weight_range[1] is None:
                creature_size_based_on_weight = CreatureSize.gargantuan
                break

            if weight_range[0] <= given_weight <= weight_range[1]:
                creature_size_based_on_weight = creature_size
                break

        if creature_size_based_on_height.value > creature_size_based_on_weight.value:
            resultant_creature_size = creature_size_based_on_height

        return resultant_creature_size

_CREATURE_SIZE_HIT_DICE_TABLE = {
    CreatureSize.tiny:          DieType.d4,
    CreatureSize.small:         DieType.d6,
    CreatureSize.medium:        DieType.d8,
    CreatureSize.large:         DieType.d10,
    CreatureSize.huge:          DieType.d12,
    CreatureSize.gargantuan:    DieType.d20
}

_CREATURE_SIZE_HEIGHT_TABLE = {
    # creature size to height range (ft)
    CreatureSize.tiny:          [0, 2.5],       # unbound lower value
    CreatureSize.small:         [2.5, 4.5],
    CreatureSize.medium:        [4.5, 7.5],
    CreatureSize.large:         [7.5, 12],
    CreatureSize.huge:          [12, 20],
    CreatureSize.gargantuan:    [20, None]      # unbound upper value
}

_CREATURE_SIZE_WEIGHT_TABLE = {
    # creature size to weight range (lbs)
    CreatureSize.tiny:          [0, 30],        # unbound lower value
    CreatureSize.small:         [30, 60],
    CreatureSize.medium:        [60, 250],
    CreatureSize.large:         [250, 1000],
    CreatureSize.huge:          [1000, 4000],
    CreatureSize.gargantuan:    [4000, None]    # unbound upper value
}

_CREATURE_SIZE_CARRY_WEIGHT_TABLE = {
    # creature size to carry weight (equation: str * values-below)
    CreatureSize.tiny:          7.5,
    CreatureSize.small:         15,
    CreatureSize.medium:        15,
    CreatureSize.large:         30,
    CreatureSize.huge:          60,
    CreatureSize.gargantuan:    120
}

_CREATURE_SIZE_DRAG_LIFT_PUSH_TABLE = {
    # creature size to capacity to drag, lift, and push (equation: str * values-below) (values are 2x their carry weight)
    CreatureSize.tiny:          _CREATURE_SIZE_CARRY_WEIGHT_TABLE[CreatureSize.tiny] * 2,
    CreatureSize.small:         _CREATURE_SIZE_CARRY_WEIGHT_TABLE[CreatureSize.small] * 2,
    CreatureSize.medium:        _CREATURE_SIZE_CARRY_WEIGHT_TABLE[CreatureSize.medium] * 2,
    CreatureSize.large:         _CREATURE_SIZE_CARRY_WEIGHT_TABLE[CreatureSize.large] * 2,
    CreatureSize.huge:          _CREATURE_SIZE_CARRY_WEIGHT_TABLE[CreatureSize.huge] * 2,
    CreatureSize.gargantuan:    _CREATURE_SIZE_CARRY_WEIGHT_TABLE[CreatureSize.gargantuan] * 2,
}


class ConditionType(enum.Enum):
    # https://bg3.wiki/wiki/Conditions  <-- use to borrow some conditions that are not listed (some may fit into Trigger)
    # page 1: https://bg3.wiki/wiki/Conditions/List_(1-500)
    # page 2: https://bg3.wiki/wiki/Conditions/List_(501-1000)
    # page 3: https://bg3.wiki/wiki/Conditions/List_(1001-1500)

    """
        Conditions can fall under two categories: 'True' Conditions, and 'Derived' Conditions
            - True Conditions: those imposed by spells, items, etc.
            - Derived Conditions: those imposed by situation, environment, etc.

            e.g.
            - "poisoned" condition given by poisoned blade (True Condition) fixed by antidote
            - "threatened" condition given by non-prone enemy being within 5ft of affected creature
    """

    blinded             = {"label": "Blinded"}
    charmed             = {"label": "Charmed"}
    deafened            = {"label": "Deafened"}
    frightened          = {"label": "Frightened"}
    grappled            = {"label": "Grappled"}
    incapacitated       = {"label": "Incapacitated"}
    stunned             = {"label": "Stunned"}
    petrified           = {"label": "Petrified"}
    unconscious         = {"label": "Unconscious"}
    restrained          = {"label": "Restrained"}
    invisible           = {"label": "Invisible"}
    paralyzed           = {"label": "Paralyzed"}
    poisoned            = {"label": "Poisoned"}
    prone               = {"label": "Prone"}
    threatened          = {"label": "Threatened"}  # for marking a Creature as being within 5ft of another (page 3 of bg3 conditions)
    # TODO: look at how the exhaustion mechanic works, find out how to put it to code (every 24 hours that a player does not long rest there is a DC check)
    exhaustion_lvl1     = {"label": "Somewhat Exhausted"}
    exhaustion_lvl2     = {"label": "Exhausted"}
    exhaustion_lvl3     = {"label": "Very Exhausted"}
    exhaustion_lvl4     = {"label": "Very-Very Exhausted"}
    exhaustion_lvl5     = {"label": "Extremely Exhausted"}
    exhaustion_lvl6     = {"label": "Deadly Exhausted"}

    @property
    def label(self):
        return self.value["label"]


class CreatureCondition:
    def __init__(self, condition_name:str):
        self.name = ConditionType(condition_name).label
        self.type = ConditionType[condition_name]
        self.description = None
        self.condition_effects = None


class CreatureMetadata:
    def __init__(self):
        """
        Information about the creature that falls outside of mechanics
        """
        self.name = None            # what the creature wants to be called
        self.age = None
        self.gender = None          # what the creature identifies in terms of gender (no mechanics relating to it)
        self.physical_description = None     # text blurb describing the creature's physical appearance
        self.personality = None
        self.backstory = None
        self.alignment = Alignment.nn       # middle-ground between meta, and mechanical (Default: NN)


class Creature:

    def __init__(self, creature_name:str=None):
        """
        The mechanical aspect of Creatures, NPCs, and PC (meta/desc data is stored as well, but as separate class)
        :param creature_name: a dictionary that holds all the details for the Creature to be created
        """

        # identity
        self.creature_type = None
        self.race = None
        self.race_desc = None
        self.size = None

        # core stats
        self.ability_scores = {ability.name: 10 for ability in Ability}
        self.modifiers = None  # will be populated based on the ability scores
        self.skills = {skill.name: 0 for skill in Skill}
        self.passive_perception = None
        self.spellcasting_ability = None  # given either by creature stat block, or by class selection (Default: None)

        # health
        self.max_health = None
        self.current_health = None
        self.temporary_health = None
        self.death_saving_throws = False  # whether the creature gets death saving throws or not

        # combat
        self.ac = None
        self.speed = None
        self.actions = None
        self.senses = None

        # progression
        self.level = None
        self.challenge_rating = None    # for monsters/creatures specifically

        # inventory
        self.inventory = []
        self.equipped_items = []
        self.carrying_capacity = None

        # misc
        self.current_conditions = []  # which effects are currently listed for this creature
        self.languages = None
        self.metadata = CreatureMetadata()

        if creature_name is not None:  # if creature name is provided from the get-go, just build it
            self.extract_data(creature_name)

    @property
    def proficiency_bonus(self):
        if self.level is not None:
            return self.level.prof_bonus
        elif self.challenge_rating is not None:
            return int(eval(self.challenge_rating)) // 4 + 2
        else:
            return 2

    @property
    def spell_save_dc(self):
        """ONLY applies to spellcasters"""
        if self.spellcasting_ability is not None:
            return 8 + self.proficiency_bonus + self.modifiers[self.spellcasting_ability.name]
        return None

    @property
    def spell_attack_bonus(self):
        """ONLY applies to spellcasters"""
        if self.spellcasting_ability is not None:
            return self.proficiency_bonus + self.modifiers[self.spellcasting_ability.name]
        return None

    @property
    def alignment(self):
        """
        making this a property because alignment is not called frequently enough (nor is it mechanically so important
        to make it part of the Creature class proper)
        :return: the creature's alignment
        """
        return self.metadata.alignment

    @property
    def kill_xp(self) -> int:
        return _CR_XP_TABLE[self.challenge_rating]

    def apply_condition(self, condition:ConditionType):
        self.current_conditions.append(condition)

    def remove_condition(self, condition:ConditionType):
        self.current_conditions.remove(condition)

    def extract_data(self, creature_name:str, file_override:str=None):

        if file_override is not None:  # allows for specific directing towards a different file
            with open(file_override, "r") as creature_raw_file:
                creature_dict = json.load(creature_raw_file)
        else:  # otherwise, pull from the general file
            with open(_CREATURE_JSON_FILENAME, "r") as creature_raw_file:
                creature_dict = json.load(creature_raw_file)

        for entry in creature_dict:
            if entry["name"] == creature_name:
                relevant_entry = entry

    def calculate_modifiers(self):

        self.modifiers = {  "str": math.floor(float(self.ability_scores["str"])-10/2),
                            "dex": math.floor(float(self.ability_scores["dex"])-10/2),
                            "con": math.floor(float(self.ability_scores["con"])-10/2),
                            "int": math.floor(float(self.ability_scores["int"])-10/2),
                            "wis": math.floor(float(self.ability_scores["wis"])-10/2),
                            "cha": math.floor(float(self.ability_scores["cha"])-10/2)}

    def display_info(self):
        for attribute, value in self.__dict__.items():
            print(f"{attribute}: {value}")
