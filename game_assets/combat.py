import enum
from creature import Creature
from dice import DieType

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