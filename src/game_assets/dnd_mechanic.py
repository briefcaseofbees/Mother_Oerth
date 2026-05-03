"""

"""

import enum


class Action(enum.Enum):
    # all of these cost ActionEconomy.action
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
    slow    = {
                "label": "Slow",
                "per_min": 200,
                "per_hour": 10560,
                "per_day": 95040,
                "effect": "advantage(perception, survival)"
                }

    normal  = {
                "label": "Normal",
                "per_min": 300,
                "per_hour": 15840,
                "per_day": 126720,
                "effect": "disadvantage(stealth)"
                }

    fast    = {
                "label": "Fast",
                "per_min": 400,
                "per_hour": 21120,
                "per_day": 158400,
                "effect": "disadvantage(perception, survival, stealth)"
                }

    @property
    def label(self):
        return self.value["label"]

    @property
    def per_min(self):
        return self.value["per_min"]

    @property
    def per_hour(self):
        return self.value["per_hour"]

    @property
    def per_day(self):
        return self.value["per_day"]

    @property
    def effect(self):
        return self.value["effect"]


class Hazard(enum.Enum):
    burning         = {"label": "Burning"}
    falling         = {"label": "Falling"}
    suffocation     = {"label": "Suffocation"}
    dehydration     = {"label": "Dehydration"}
    malnutrition    = {"label": "Malnutrition"}

    @property
    def label(self):
        return self.value["label"]


class Reputation(enum.Enum):
    # reputation score ranges per faction
    feared          = {"label": "Feared",       "score_range": [-100, -90]}
    blacklisted     = {"label": "Blacklisted",  "score_range": [-90, -70]}
    reviled         = {"label": "Reviled",      "score_range": [-70, -40]}
    untrusted       = {"label": "Untrusted",    "score_range": [-40, -10]}
    neutral         = {"label": "Neutral",      "score_range": [-10, 10]}
    trusted         = {"label": "Trusted",      "score_range": [10, 40]}
    respected       = {"label": "Respected",    "score_range": [40, 70]}
    honored         = {"label": "Honored",      "score_range": [70, 90]}
    exalted         = {"label": "Exalted",      "score_range": [90, 100]}


class EncumbranceStatus(enum.Enum):
    unencumbered                = {"label": "Unencumbered"}
    encumbered                  = {"label": "Encumbered"}
    heavily_encumbered          = {"label": "Heavily Encumbered"}
    very_heavily_encumbered     = {"label": "Very Heavily Encumbered"}

    @property
    def label(self):
        return self.value["label"]


class DamageResistLevel(enum.Enum):
    vulnerable      = {"label": "Vulnerable"}
    no_resistance   = {"label": "No Resistance"}
    resistance      = {"label": "Resistance"}
    immune          = {"label": "Immune"}

    @property
    def label(self):
        return self.value["label"]


class ActionEconomy(enum.Enum):
    action              = {"label": "Action"}
    bonus_action        = {"label": "Bonus Action"}
    reaction            = {"label": "Reaction"}
    legendary_action    = {"label": "Legendary Action"}

    @property
    def label(self):
        return self.value["label"]
