"""

"""

import enum
from typing import Union
from .creature import Creature
from .object import ObjectInstance
from .dice import DieType, d20_test, D20Modifier, resolve_multiple_d20modifiers
from .item import Weapon, WeaponType, WeaponProperties
from .optional_ruleset import D20ModifierStacking

# TODO: How does combat typically work?
# TODO: How should turn order in general work? (in/out of encounters)

class DamageType(enum.Enum):
    piercing = 0
    bludgeoning = 1
    slashing = 2
    fire = 3
    cold = 4
    lightning = 5
    thunder = 6
    acid = 7
    poison = 8
    psychic = 9
    radiant = 10
    necrotic = 11
    force = 12


class Combatant:
    def __init__(self, creature_obj:Creature):
        self.creature = creature_obj  # each combatant is a creature, but
        self.has_action = True
        self.has_bonus_action = True
        self.has_reaction = True
        self.has_movement = True
        self.movement_speed = 0  #

    def roll_initiative(self):
        init_roll = DieType.d20.roll()  # roll basic d20 for base initiative number

        # TODO: figure out how to define check for initiative modifiers ("alert" feat, gear, etc.)
        init_modifiers = [1,-2,3]  # placeholder for code that will actually pull all the
        init_modifiers.sort(reverse=True)  # sort modifiers by value (highest at end of list)
        highest_mod = init_modifiers[0]  # in the case of ties, we use the "highest mod" rule

        for score in init_modifiers:
            init_roll += score

        return init_roll, highest_mod

    def reset_action_economy(self):
        # resets the Combatant for the start of their turn

        # check for anything that might prevent actions, bonus actions, reactions, movement, etc. from resetting
        # i.e. conditions, statuses, etc.

        pass


    def move(self):
        pass

    def attack(self, weapon:Weapon, attacker: Creature, target: Creature | ObjectInstance, target_distance: int):
        """
        docstring
        """


        # note: target can be either a Creature, or an ObjectInstance

        """1. VERIFY TARGET IS VALID"""
        if not (isinstance(target, Creature) or isinstance(target, ObjectInstance)):
            # invalid target: ~(F + F) -> T
            # need to exit function without doing anything...
            # also need to give meaningful feedback to player as to WHY the attack doesn't go through
            # should only give feedback to the specific player!!! (should figure out tunneled player communication)
            pass
        else:
            # valid target: ~(T + F) (or ~(F + T)) -> F

            """2. GATHER NECESSARY INFORMATION"""
            """
                in order to complete the attack action, the following information is required:
                    a. whether the attack is even in range (melee range, or ranged range)
                    b. AC of the target
                    c. whether the attack is being made with advantage or disadvantage
            """



            """2a. FIND WEAPON RANGE"""

            weapon_attack_reach = []

            # check if weapon is melee or ranged
            if WeaponType["melee"] in weapon.type:  # weapon.type is a list that will have properties in it
                weapon_attack_reach.append(5)
                # base case: attack must be made within 5ft
                if WeaponProperties["reach"] in weapon.properties:
                    # reach increases effective range by 5ft
                    weapon_attack_reach[0] += 5
                    pass

                if WeaponProperties["thrown"] in weapon.properties:
                    weapon_attack_reach.append(weapon.range)
                    pass
                pass
            elif WeaponType["ranged"] in weapon.type:
                weapon_attack_reach.append(weapon.range)
                pass
            else:
                # this shouldn't be accessible, throw error!
                pass

            if len(weapon_attack_reach) == 1:
                # will either be a melee or ranged weapon
                if isinstance(weapon_attack_reach[0], list):
                    # if the first index is a list, then it's a ranged weapon

                    if target_distance < weapon_attack_reach[0][0]:
                        # it's in the weapon's effective reach
                        pass
                    elif weapon_attack_reach[0][0] < target_distance < weapon_attack_reach[0][1]:
                        # it's not in the weapon's effective reach, but below the maximum
                        pass
                    else:
                        # the target is out of range
                        pass
                    pass
                else:
                    # otherwise it's a melee weapon without the thrown property
                    if target_distance <= weapon_attack_reach[0]:
                        # target is within the weapon's reach
                        pass
                    else:
                        # target is out of range
                        pass
                    pass
                pass
            else:
                # will be a melee weapon with the thrown property

                if target_distance <= weapon_attack_reach[0]:
                    # target is within the weapon's melee reach
                    pass
                else:
                    # target is out of range... check if thrown range works?
                    if target_distance <= weapon_attack_reach[1][0]:
                        # target is within effective range
                        pass
                    elif target_distance <= weapon_attack_reach[1][1]:
                        # target is within maximum range
                        pass
                    else:
                        # target is beyond maximum thrown weapon reach
                        pass
                pass

            """2b. DETERMINE TARGET AC"""

            target_ac = target.ac  # easy enough, but there may be more to it than that... (conditional AC?)


            """2c. DETERMINE ADVANTAGE/DISADVANTAGE AND ROLL-BONUSES"""
            """
                a few things impose disadvantage and advantage:
                    - creature status conditions
                    - cover
                    - etc.
            """
            d20_modifiers = []  # will be populated with d20 modifiers (advantage, disadvantage)
            roll_modifiers = []
            d20_modifier = D20Modifier.normal

            # go through every possible thing to determine what needs to be appended to the d20_modifiers

            if len(d20_modifiers) > 1:
                d20_modifier, multi_d20_modifier = resolve_multiple_d20modifiers(d20_modifiers,
                                                              current_session_rules=D20ModifierStacking.disallowed)
                if multi_d20_modifier != 0:
                    roll_modifiers.append(multi_d20_modifier)
            elif len(d20_modifiers) == 1:
                # d20_modifiers list with a single item
                d20_modifier = d20_modifiers[0]  # modifier is just the first item in the list
                pass
            else:
                # empty d20_modifiers list, do nothing
                pass

            # also need to determine if there's any other roll bonuses that need to be applied...
            # e.g. weapon enchantments, etc.

            """ 3. MAKE ATTACK ROLL"""

            attack_successful = d20_test(modifiers=roll_modifiers, dc=target_ac, roll_type=d20_modifier)  # True/False
            # Trigger.on_attack_rolled

            # check for Trigger.on_critical_success (will change damage dealt!)

            if attack_successful:
                # roll for damage
                damage_dealt = weapon.dmg.roll  # weapon.dmg is of type DiceRoll which has
                # Trigger.on_melee_hit | Trigger.on_ranged_hit event
                target.current_health -= damage_dealt  # take away the health that was just dealt
                # Trigger.on_damage_dealt event | Trigger.on_damage_taken
                pass
            else:
                # Trigger.on_melee_miss | Trigger.on_ranged_miss
                pass

            pass

        # conclude attack action!

        pass


class CombatQueue(list):
    # there should be the possibility of multiple combat queues?

    # if there are multiple separate Combat Queues-- then Combat Queues will take turns between them using the init-based
    # method (compare next-combatant init values between queues, whoever rolled highest goes first)
    # if two combat queues need to be stitched together, create new queue using existing init rolls, collapsing into
    # a single queue, continue combat as per usual

    # combat queues should act ON TOP of the world layer-- essentially if there's combat, the world cannot go on its own...
    # applying mutex-locking-- everything in the world goes by the pace of the combat

    # CombatQueues ONLY apply if there's a PC involved in the fight
    # if a PC escapes combat, the CombatQueue is lifted, and combat resolves normally
    # might need to come up with a non-CombatQueue resolution of combat-- some ideas:
    #   - CR-based resolution; - narrative-based resolution; - random-chance-based? (dice rolls)
    # could possibly implement some combination of the above, and a few other things...?

    def __init__(self):
        super().__init__()
        self.current_combatant = None  # the current creature acting in the turn order


    def add_combatant(self, combatant:Combatant):
        pass

    def delete_combatant(self, combatant:Combatant):
        pass

    def next_combatant(self):
        # should wait for a creature to end their turn (event-based signal (if player), boolean-based signal (if NPC))
        pass


# need to come up with a decision tree to map how an NPC combatant would behave

class CombatBehaviour(enum.Enum):
    # poles of combat behaviour

    # aggression
    aggressive = 0
    cowardice = 1

    # competency
    strategic = 2  # are they professionally trained? or just experienced?
    unhinged = 3  # do they have a history of barbarism, or are they beastial?

    # comfortable range
    close_quarters = 4
    ranged = 5

    organized = 6
    detached = 7

    risky = 8
    cautious = 9

    # facets of combat behaviour...?
    # some of these have priorities and layers (with specific creatures having access to some, or all of the layers)
    # morale (winning/losing)
    # CR of enemies versus party
    # recent occurrences (deaths/kills/etc.)
    # intelligence of enemies

    # dynamic emergence of behavioural tree based on the above factors

def is_encounter_balanced(allies:list[Creature], opponents:list[Creature]) -> bool:
    # in DND-- encounters are typically balanced via comparison of opponent challenge rating, and party level
    return sum([]) >= sum([])
