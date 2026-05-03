"""

"""

import enum


class Action(enum.Enum):
    attack          = {"label": "Attack"}      # attack with a weapon, or unarmed strike
    dash            = {"label": "Dash"}        # doubles movement speed
    disengage       = {"label": "Disengage"}   # prevents opportunity attacks
    dodge           = {"label": "Dodge"}       # makes attacks again you have disadvantage, makes dexterity saving throws have advantage
    help            = {"label": "Help"}        # help another creature's ability check or attack roll, or administer first aid
    hide            = {"label": "Hide"}        # make a stealth check
    influence       = {"label": "Influence"}   # make a deception, intimidation, performance, persuasion or animal handling check to alter a creature's attitude
    magic           = {"label": "Magic"}       # cast a spell, use a magic item, or use a magical feature
    ready           = {"label": "Ready"}       # prepare to take an action in response to a trigger you define
    search          = {"label": "Search"}      # make an insight, medicine, perception, or survival check
    study           = {"label": "Study"}      # make an arcana, history, investigation, nature, or religion check
    utilize         = {"label": "Utilize"}    # use a non-magical object

    @property
    def label(self):
        return self.value["label"]


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


class EncumbranceStatus(enum.Enum):
    unencumbrance               = enum.auto()
    encumbered                  = enum.auto()
    heavily_encumbered          = enum.auto()
    very_heavily_encumbered     = enum.auto()


class DamageResistLevel(enum.Enum):
    vulnerable      = enum.auto()
    no_resistance   = enum.auto()
    resistance      = enum.auto()
    immune          = enum.auto()


class ActionEconomy(enum.Enum):
    action              = enum.auto()
    bonus_action        = enum.auto()
    reaction            = enum.auto()
    legendary_action    = enum.auto()
