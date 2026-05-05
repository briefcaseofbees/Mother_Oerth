"""

"""

import random

from .alignment import KarmicState
from .creature import Creature
from .dice import roll_ability_scores
from .game_constants import AbilityScoreMethod, ClassType


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
        self.player_classes = []
        self.inspiration = False  # only players get inspiration, but they start with NO inspiration
        self.character_background = None
        self.player_xp = 0

        self.player_karmic_state = KarmicState(self.player_creature.alignment)
        self.spellbook = None  # spellcaster specific, very-much a player concern (not stored in Creature class)


    def create_character(self, stat_assign_type: AbilityScoreMethod):
        # outline the process of making a character in DND (by the player)

        # CHOOSE CLASS
        # TODO: figure out how class selection works
        # a. there will be a standard ability score array per class
        chosen_class = ClassType.barbarian  # default: Barbarian

        # TODO: need to delegate the below to an event-based process... (UI-interaction, essentially)

        class_confirmed = False  # has the player locked in?
        while not class_confirmed:

            # TODO: should display an overview of the class to the player with encyclopedia entries for skills, etc.
            break

        # TODO: worth exploring the Paladin Oath mechanic, and expressing that to the player in serious terms
        #   it, like KarmicState is a mechanic that is taken seriously in this version

        # b. each class will have progression, starting equipment, skills, saving throws, etc. need to display that

        # DETERMINE ORIGIN
        # TODO: figure out how origin determination works


        # DETERMINE ABILITY SCORES
        match stat_assign_type:

            case AbilityScoreMethod.random:  # random rolls with 4d6, drop lowest die value
                rolled_stats = roll_ability_scores()


            case AbilityScoreMethod.standard:  # standard array values
                rolled_stats = [15,14,13,12,10,8]

                # need way to allow users to assign values to stats with UI

            case AbilityScoreMethod.manual:
                rolled_stats = [8,8,8,8,8,8]
                point_pool = 27

                # need UI with: <= STAT <number> =>
                # need logic so that player can add/subtract pts and depending on the qty of points in a stat--
                # it needs to cost different amounts

                # what is the equation for point adding?
                # every point above 13 costs double

                while point_pool > 0:  # condition should be tied to user accepting the results, AND point_pool > 0

                    # replace all below with a proper UI
                    stat_to_alter = int(input("which stat to change?"))
                    point_direction = input("what direction?")

                    # stats should not be able to go above 18... or maybe I allow it?
                    # stats should definitely NOT be able to go above 20 though

                    match stat_to_alter:
                        case "STR":
                            if rolled_stats[0] >= 18:
                                pass

                            if rolled_stats[0] >= 14:
                                if point_direction == "UP":
                                    point_pool -= 2
                                else:
                                    point_pool += 2
                                break
                            else:
                                if point_direction == "UP":
                                    point_pool -= 1
                                else:
                                    point_pool += 1
                        case "DEX":
                            pass
                        case "CON":
                            pass
                        case "INT":
                            pass
                        case "WIS":
                            pass
                        case "CHA":
                            pass

        # CHOOSE ALIGNMENT
        # TODO: how to best represent the process of choosing an alignment?
        chosen_alignment = self.player_creature.alignment  # default starting alignment

        # TODO: how best to describe the karmic state system to new players? (it is much different than 5e...)

        self.player_karmic_state = KarmicState(chosen_alignment)  # setup KarmicState with the chosen alignment

        # FILL IN REMAINING DETAILS
        # TODO: metadata, and other details?