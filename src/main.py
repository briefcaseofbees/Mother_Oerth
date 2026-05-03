import random, enum
import asyncio
import json
from game_assets import *


class EventBus:  # TODO: figure out how this works, and what it'll be used for
    def __init__(self):
        self._listeners = {}

    def subscribe(self, event_type, callback):
        self._listeners.setdefault(event_type, []).append(callback)

    async def emit(self, event_type, data = None):
        callbacks = self._listeners.get(event_type, [])
        await asyncio.gather(*[callback(data) for callback in callbacks])


"""GAME MECHANICS AND TOOLS"""


def is_encounter_balanced(allies:list[Creature], opponents:list[Creature]) -> bool:
    # in DND-- encounters are typically balanced via comparison of opponent challenge rating, and party level
    return sum([]) >= sum([])


class Trigger(enum.Enum):
    """list of game logic triggers"""

    # COMBAT TRIGGERS
    on_attack_rolled = enum.auto()
    on_hit = enum.auto()
    on_miss = enum.auto()
    on_damage_dealt = enum.auto()
    on_damage_taken = enum.auto()
    on_critical_hit = enum.auto()
    on_kill = enum.auto()
    on_death_save = enum.auto()
    on_stabilize = enum.auto()
    on_spell_cast = enum.auto()
    on_spell_hit = enum.auto()
    on_concentration_broken = enum.auto()

    # TURN STRUCTURE
    on_turn_start = enum.auto()
    on_turn_end = enum.auto()
    on_round_start = enum.auto()
    on_round_end = enum.auto()
    on_initiative_rolled = enum.auto()

    # CHARACTER STATE
    on_heal = enum.auto()
    on_condition_applied = enum.auto()
    on_condition_removed = enum.auto()
    on_level_up = enum.auto()
    on_ability_score_change = enum.auto()
    on_temp_hp_gained = enum.auto()
    on_exhaustion_gained = enum.auto()
    on_exhaustion_removed = enum.auto()

    # EQUIPMENT
    on_equip = enum.auto()
    on_unequip = enum.auto()
    on_attune = enum.auto()
    on_attunement_broken = enum.auto()
    on_item_used = enum.auto()
    on_item_consumed = enum.auto()
    on_ammo_expended = enum.auto()

    # REST
    on_long_rest = enum.auto()
    on_short_rest = enum.auto()
    on_hit_dice_spent = enum.auto()

    # MOVEMENT
    on_move = enum.auto()
    on_enter_tile = enum.auto()
    on_leave_tile = enum.auto()
    on_stand = enum.auto()
    on_go_prone = enum.auto()

    # ENCOUNTER
    on_encounter_start = enum.auto()
    on_encounter_end = enum.auto()
    on_creature_joins = enum.auto()
    on_creature_flees = enum.auto()

    # EXPLORATION/NARRATIVE
    on_room_enter = enum.auto()
    on_room_exit = enum.auto()
    on_item_found = enum.auto()
    on_trap_triggered = enum.auto()
    on_door_opened = enum.auto()
    on_npc_interaction = enum.auto()
    on_quest_updated = enum.auto()
    on_quest_completed = enum.auto()
    on_quest_failed = enum.auto()
    on_morally_significant_action = enum.auto()

    # TIME-BASED
    on_festival_start = enum.auto()
    on_festival_end = enum.auto()
    on_holy_day = enum.auto()
    on_season_change = enum.auto()

    # SESSION
    on_session_start = enum.auto()
    on_session_end = enum.auto()
    on_player_connect = enum.auto()
    on_player_disconnect = enum.auto()


class Action(enum.Enum):
    attack = 0
    dash = 1
    disengage = 2
    dodge = 3
    help = 4
    hide = 5
    influence = 6
    magic = 7
    ready = 8
    search = 9
    study = 10
    utilize = 11


class ToolProficiency(enum.Enum):
    alchemist_supplies = 0
    brewer_supplies = 1
    calligrapher_supplies = 2
    carpenter_tools = 3
    cartographer_tools = 4
    cobbler_tools = 5
    cook_utensils = 6
    glassblower_tools = 7
    jeweler_tools = 8
    leatherworker_tools = 9
    mason_tools = 10
    painter_supplies = 11
    potter_tools = 12
    smith_tools = 13
    tinker_tools = 14
    weaver_tools = 15
    woodcarver_tools = 16
    disguise_kit = 17
    forgery_kit = 18
    gaming_set = 19
    herbalism_kit = 20
    musical_instrument = 21
    navigator_tools = 22
    poisoner_kit = 23
    thief_tools = 24


class GamingSetType(enum.Enum):
    dice = 0
    dragonchess = 1
    playing_cards = 2
    threedragon_ante = 3


class MusicalInstrumentType(enum.Enum):
    bagpipes = 0
    drum = 1
    dulcimer = 2
    flute = 3
    horn = 4
    lute = 5
    lyre = 6
    pan_flute = 7
    shawm = 8
    viol = 9


class DamageThreshold(enum.Enum):
    # TODO: find more official documentation on how damage thresholds work in dnd 5e

    indestructible = -1     # can never be destroyed
    none = 0                # can be destroyed with repeated light attacks
    light = 5
    medium = 10
    heavy = 20
    impenetrable = 30


class ObjectSize(enum.Enum):
    tiny = {"label": "tiny"}
    small = {"label": "small"}
    medium = {"label": "medium"}
    large = {"label": "large"}

    @property
    def label(self):
        return self.value["label"]


class ObjectMaterial(enum.Enum):
    cloth =         {"label": "Cloth",      "ac": 11}
    paper =         {"label": "Paper",      "ac": 11}
    rope =          {"label": "Rope",       "ac": 11}
    crystal =       {"label": "Crystal",    "ac": 13}
    glass =         {"label": "Glass",      "ac": 13}
    ice =           {"label": "Ice",        "ac": 13}
    wood =          {"label": "Wood",       "ac": 15}
    bone =          {"label": "Bone",       "ac": 15}
    stone =         {"label": "Stone",      "ac": 17}
    iron =          {"label": "Iron",       "ac": 19}
    steel =         {"label": "Steel",      "ac": 19}
    mithral =       {"label": "Mithral",    "ac": 21}
    adamantine =    {"label": "Adamantine", "ac": 23}

    @property
    def label(self):
        return self.value["label"]

    @property
    def ac(self):
        return self.value["ac"]


class ObjectHP(enum.Enum):
    tiny = {    "fragile": {
                    "flat": 2,
                    "rolled": DiceRoll(DieType.d4,1)},
                "resilient": {
                    "flat": 5,
                    "rolled": DiceRoll(DieType.d4, 2)}}

    small = {   "fragile": {
                    "flat": 3,
                    "rolled": DiceRoll(DieType.d6,1)},
                "resilient": {
                    "flat": 10,
                    "rolled": DiceRoll(DieType.d6, 3)}}

    medium = {  "fragile": {
                    "flat": 4,
                    "rolled": DiceRoll(DieType.d8, 1)},
                "resilient": {
                    "flat": 18,
                    "rolled": DiceRoll(DieType.d8,4)}}

    large = {   "fragile": {
                    "flat": 5,
                    "rolled": DiceRoll(DieType.d10,1)},
                "resilient": {
                    "flat": 27,
                    "rolled": DiceRoll(DieType.d10,5)}}

    @classmethod
    def get_hp(cls, object_size:ObjectSize, object_fragility, flat:bool) -> int:
        """

        :param object_size: ObjectSize
        :param object_fragility: "fragile" or "resilient"
        :param flat: flat calculation or rolled
        :return: integer value of health of object
        """
        if flat:
            return cls[object_size.label].value[object_fragility]["flat"]
        else:
            return cls[object_size.label].value[object_fragility]["rolled"].roll()


class ObjectInstance:
    def __init__(self, object_name:str, object_size:ObjectSize, object_material:ObjectMaterial):
        # object stats
        self.hp = ObjectHP.get_hp(object_size, "resilient", False)
        self.ac = object_material.ac
        self.destructible = True  # is the object able to be destroyed? (default: yes)

        # object metadata
        self.name = object_name
        self.material = object_material.label

    def __repr__(self):
        return f"{self.name}: {self.hp}; ac: {self.ac}, material: {self.material}"


class SpecialSense(enum.Enum):
    normal = -1  # no special senses
    blind_sight = 0
    dark_vision = 1
    tremor_sense = 2
    true_sight = 3


class TravelPace(enum.Enum):
    # TODO: make into a dictionary so that the extra information can be stored in the enum

    # pace = pace_id    # distance travelled = {/minute, /hour, /day}
    slow = -1           # 200ft, 2miles, 18miles (adv on WIS (perception/survival))
    normal = 0          # 300ft, 3miles, 24miles (dis-adv on DEX (stealth))
    fast = 1            # 400ft, 4miles, 30miles (dis-adv on WIS & DEX (perception/survival/stealth))


class Hazard(enum.Enum):
    burning = 0
    falling = 1
    suffocation = 2
    dehydration = 3
    malnutrition = 4


class Reputation(enum.Enum):
    # ... continues into negative territory
    wary = -1       # known slightly for bad
    unknown = 0     # stranger
    favorable = 1
    # ... continues into positive territory


class Language(enum.Enum):
    common = {"label": "Common", "rarity": "standard"}
    draconic = {"label": "Draconic", "rarity": "standard"}
    dwarvish = {"label": "Dwarvish", "rarity": "standard"}
    elvish = {"label": "Elvish", "rarity": "standard"}
    giant = {"label": "Giant", "rarity": "standard"}
    gnomish = {"label": "Gnomish", "rarity": "standard"}
    goblin = {"label": "Goblin", "rarity": "standard"}
    halfling = {"label": "Halfling", "rarity": "standard"}
    orc = {"label": "Orc", "rarity": "standard"}
    abyssal = {"label": "Abyssal", "rarity": "rare"}
    celestial = {"label": "Celestial", "rarity": "rare"}
    deep_speech = {"label": "Deep Speech", "rarity": "rare"}
    druidic = {"label": "Druidic", "rarity": "rare"}
    infernal = {"label": "Infernal", "rarity": "rare"}
    primordial = {"label": "Primordial", "rarity": "rare"}
    sylvan = {"label": "Sylvan", "rarity": "rare"}
    thieves_cant = {"label": "Thieves Cant", "rarity": "rare"}
    undercommon = {"label": "Undercommon", "rarity": "rare"}

    # TODO: use the below (as well as any other tricks) to make the enums more efficient

    @property
    def label(self):
        return self.value["label"]

    @property
    def rarity(self):
        return self.value["rarity"]

    @classmethod
    def by_rarity(cls, rarity):
        return [lang for lang in cls if lang.rarity == rarity]

""" something to consider emulating with other classes
for language in Languages.by_rarity("standard"):
    print(language.label)
"""


class EncumbranceStatus(enum.Enum):
    unencumbrance = -1
    encumbered = 0
    heavily_encumbered = 1
    very_heavily_encumbered = 2


class DamageResistLevel(enum.Enum):
    vulnerable = -1
    no_resistance = 0
    resistance = 1
    immune = 2


class ActionEconomy(enum.Enum):
    action = 0
    bonus_action = 1
    reaction = 2
    legendary_action = 3


class PlayerCharacter:
    def __init__(self, player_username:str, player_id: int):
        """
        The player-forward items that extend the Creature class
        :param player_id: a unique int id for identifying the player
        """

        # player identification information
        self.player_name = player_username
        self.player_id = player_id

        self.player_creature = Creature({})  # TODO: create a default creature dict for character creation
        self.player_class = None
        self.inspiration = False  # only players get inspiration, but they start with NO inspiration
        self.character_background = None
        self.player_xp = 0

        self.player_karmic_state = KarmicState(self.player_creature.alignment)
        self.spellbook = None  # spellcaster specific, very-much a player concern (not stored in Creature class)


    def create_character(self, stat_assign_type: AbilityDeterminationType):
        # outline the process of making a character in DND (by the player)

        # CHOOSE CLASS
        # TODO: figure out how class selection works
        # a. there will be a standard ability score array per class
        chosen_class = CreatureClass.barbarian  # default: Barbarian

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

            case AbilityDeterminationType.random:  # random rolls with 4d6, drop lowest die value
                rolled_stats = []
                for stat_roll in range(6):
                    results = []

                    # add grace-roll mechanic for rolling stats... (if I feel like it's necessary)

                    for dice_roll in range(4):
                        results.append(random.randint(1, 6))

                    results.sort()
                    result_sum = sum(results[1:])
                    rolled_stats[stat_roll] = result_sum

            case AbilityDeterminationType.standard:  # standard array values
                rolled_stats = [15,14,13,12,10,8]

                # need way to allow users to assign values to stats with UI

            case AbilityDeterminationType.manual:
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