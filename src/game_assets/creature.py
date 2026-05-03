"""

"""

import enum, math
import json

from .ability import Ability, Skill
from .alignment import Alignment
from .dice import DieType
from .progression import LevelAdvancement, _CR_XP_TABLE


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
    tiny = 0
    small = 1
    medium = 2
    large = 3
    huge = 4
    gargantuan = 5

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


class CreatureConditions(enum.Enum):
    blinded = 0
    charmed = 1
    deafened = 2
    frightened = 3
    grappled = 4
    incapacitated = 5
    stunned = 6
    petrified = 7
    unconscious = 8
    restrained = 9
    invisible = 10
    paralyzed = 11
    poisoned = 12
    prone = 13
    exhaustion_lvl1 = 14
    exhaustion_lvl2 = 15
    exhaustion_lvl3 = 16
    exhaustion_lvl4 = 17
    exhaustion_lvl5 = 18
    exhaustion_lvl6 = 19


class CreatureClass:
    def __init__(self):
        self.name = None
        self.hit_dice = None
        self.hit_dice_pool_qty = None
        self.proficiency_bonus = None
        self.armor_proficiencies = None
        self.weapon_proficiencies = None
        self.starting_tools = None
        self.saving_throws = None
        self.starting_skills = None
        self.class_features = {
            "1st Level": ["where features would go-- since there's no repetition, it doesn't make sense to have ids"]
        }
        self.subclass = None

        # Spellcaster-specific
        self.spell_save_DC = None  # if applicable
        self.spells_known = []
        self.prepared_spells = []   # subset of known spells
        self.spellcasting_ability = None
        self.concentrating = False  # whether class is concentrating on a spell currently


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

    def __init__(self, creature_dict:str):
        """
        The mechanical aspect of Creatures, NPCs, and PC (meta/desc data is stored as well, but as separate class)
        :param creature_dict: a dictionary that holds all the details for the Creature to be created
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
        self.languages = None
        self.metadata = CreatureMetadata()

        self.extract_data(creature_dict)  # pull

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

    def extract_data(self, creature_dict:str):
        print("Extracting creature data")
        with open(creature_dict, "r") as base_file:
            base_data = json.load(base_file)

        """PULL METADATA IF IT EXISTS"""

        if 'name' in base_data.keys():
            self.metadata.name = base_data["name"]

        if 'age' in base_data.keys():
            self.metadata.age = base_data["age"]

        if 'gender' in base_data.keys():
            self.metadata.gender = base_data["gender"]

        if 'physical_desc' in base_data.keys():
            self.metadata.physical_description = base_data["physical_desc"]

        if 'personality' in base_data.keys():
            self.metadata.personality = base_data["personality"]

        if 'backstory' in base_data.keys():
            self.metadata.backstory = base_data["backstory"]

        if 'alignment' in base_data.keys():
            self.metadata.alignment = Alignment[base_data["alignment"]]

        if 'race' in base_data.keys():
            # if race exists we need to pull the appropriate data
            self.race = base_data["race"]

            with open("resources/races.json", "r") as race_file:
                race_data = json.load(race_file)

            for race_dict in race_data:
                if race_dict["name"] == self.race:
                    self.creature_type = race_dict["type"]
                    self.size = race_dict["size"]
                    self.speed = race_dict["speed"]
                    self.race_desc = race_dict["desc"]




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
