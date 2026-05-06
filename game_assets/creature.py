"""
houses code pertaining to the mechanical aspects of creatures-- includes creature-size, creature-conditions,
creature-classes, creature-metadata, etc.
"""

import json
from .game_constants import AbilityType, AlignmentType, ConditionType, SkillType
from .game_constants import _CR_XP_TABLE, _CREATURES_JSON_FILE_PATH
from .program_mechanic import extract_data


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
        self.alignment = AlignmentType.nn       # middle-ground between meta, and mechanical (Default: NN)


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
        self.ability_scores = {ability.name: 10 for ability in AbilityType}
        self.modifiers = None  # will be populated based on the ability scores
        self.skills = {skill.name: 0 for skill in SkillType}
        self.passive_perception = None
        self.spellcasting_ability = None  # given either by creature stat block, or by class selection (Default: None)

        # health
        self.max_health = None
        self.current_health = None
        self.hit_dice = []  # total hit dice quantities will be dependent on which class(es) the creature has taken levels in
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
            self.populate_object(creature_name)

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

    def populate_object(self, creature_name:str):

        creature_dict = extract_data(_CREATURES_JSON_FILE_PATH)

        relevant_entry = None

        for entry in creature_dict:
            if entry['name'] == creature_name:
                relevant_entry = entry

        if relevant_entry is None:
            print(f"Creature {creature_name} not found in JSON file")
        else:
            print(f"Creature {creature_name} found in JSON file")


    def display_info(self):
        for attribute, value in self.__dict__.items():
            print(f"{attribute}: {value}")
