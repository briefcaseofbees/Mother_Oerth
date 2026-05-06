"""

"""

import random

from .ability import Ability
from .alignment import KarmicState
from .creature import Creature
from .dice import roll_ability_scores
from .game_constants import AbilityType, AbilityScoreMethod, ClassType, LevelAdvancement
from .game_constants import _CLASSES_JSON_FILE_PATH, _LVL_PROF_BONUS_TABLE, _LVL_XP_TABLE
from .program_mechanic import extract_data


class PlayerCharacter:
    def __init__(self, player_username:str, player_id: int):
        """
        The player-forward items that extend the Creature class
        :param player_id: a unique int id for identifying the player
        """

        # player identification information
        self.player_name = player_username
        self.player_id = player_id

        self.player_creature = Creature("resources/default_player.json")
        self.player_abilities = [Ability(ability_type=ability_type, ability_score=10, proficiency_bonus=2) for ability_type in AbilityType]
        self.player_classes = []
        self.player_hit_dice = []
        self.inspiration = False  # only players get inspiration, but they start with NO inspiration
        self.character_background = None
        self.player_xp = 0
        self.total_player_level = LevelAdvancement.level_1
        self.proficiency_bonus = _LVL_PROF_BONUS_TABLE[self.total_player_level]  # player proficiency bonus comes directly from total player level (sum of all class levels taken)

        self.player_karmic_state = KarmicState(self.player_creature.alignment)
        self.spellbook = None  # spellcaster specific, very-much a player concern (not stored in Creature class)

    def check_xp(self):
        # TriggerType.on_xp_gained: whenever xp is gained by a player, it should check if they leveled up

        for xp_threshold in _LVL_XP_TABLE:
            # below should cover multiple level ups (if that occurs)
            if xp_threshold[self.total_player_level] <= self.player_xp:
                # TriggerType.on_level_up
                self.level_up()

    def level_up(self):
        # CHOOSE WHICH CLASS YOU WANT TO LEVEL UP IN

        # IF MULTICLASSING IS ALLOWED, THERE NEEDS TO BE A CHECK FOR REQUIREMENTS FOR PARTICULAR MULTICLASS CHOICES
        classes_dict = extract_data(_CLASSES_JSON_FILE_PATH)
        class_name = input("which class to multiclass?")  # AGAIN, this will be put in a UI or player interface...

        relevant_entry = None

        for entry in classes_dict:
            if entry["name"] == class_name:
                relevant_entry = entry

        requirements_met = False

        if len(relevant_entry["multiclass_req"].keys()) == 1:
            # single stat requirement

            stat_req_type, threshold = relevant_entry["multiclass_req"].items()
            needed_ability = AbilityType[stat_req_type]

            relevant_player_ability = None

            for ability in self.player_abilities:
                if ability.type == needed_ability:
                    relevant_player_ability = ability

            if relevant_player_ability.base_score >= threshold:
                requirements_met = True
        elif len(relevant_entry["multiclass_req"].keys()) == 3:
            # two stat requirements...

            stat_req_logic = relevant_entry["multiclass_req"]["logic"]  # will either be 'AND' or 'OR'

            first_stat_req_type, first_stat_threshold = relevant_entry["multiclass_req"][0]
            second_stat_req_type, second_stat_threshold = relevant_entry["multiclass_req"][1]

            first_stat_req_met = False
            second_stat_req_met = False

            first_relevant_player_ability = None
            second_relevant_player_ability = None

            for ability in self.player_abilities:
                if ability.type == first_stat_req_type:
                    first_relevant_player_ability = ability
                elif ability.type == second_stat_req_type:
                    second_relevant_player_ability = ability

            if first_relevant_player_ability.base_score >= first_stat_threshold:
                first_stat_req_met = True

            if second_relevant_player_ability.base_score >= second_stat_threshold:
                second_stat_req_met = True

            if stat_req_logic == 'AND':
                requirements_met = first_stat_req_met and second_stat_req_met
            elif stat_req_logic == 'OR':
                requirements_met = first_stat_req_met or second_stat_req_met

            pass

        pass


 # TODO: need to delegate character creation to an event-based process... (UI-interaction, essentially)
def create_new_character(player_username:str = "Tav", player_id_number:int = -1, stat_assign_type: AbilityScoreMethod = AbilityScoreMethod.standard) -> PlayerCharacter:
    # outline the process of making a character in DND (by the player)

    new_character = PlayerCharacter(player_username=player_username, player_id=player_id_number)
    new_character_locked_in = False

    while not new_character_locked_in:

        # CHOOSE CLASS
        chosen_class = ClassType.barbarian  # default: Barbarian

        # DETERMINE ORIGIN

        # DETERMINE ABILITY SCORES

        character_ability_scores = [Ability(ability_type=ability_type, ability_score=8, proficiency_bonus=2) for ability_type in AbilityType]

        match stat_assign_type:

            case AbilityScoreMethod.random:
                character_ability_scores = roll_ability_scores()

                # player gets 3 attempts to roll their random scores

            case AbilityScoreMethod.standard:
                character_ability_scores = [15,14,13,12,10,8]

            case AbilityScoreMethod.manual:
                character_ability_scores = [8,8,8,8,8,8]
                point_pool = 27
                is_point_pool_zero = False  # the point pool needs to be fully used up


        # CHOOSE ALIGNMENT
        # TODO: how to best represent the process of choosing an alignment?

        # TODO: how best to describe the karmic state system to new players? (it is much different than 5e...)

        # FILL IN REMAINING DETAILS
        # TODO: metadata, and other details?

    return new_character