import enum, math, random
from optional_ruleset import D20ModifierStacking, _STACK_MODIFIER_CAP

_DC_VALUE_TABLE = {
    "very_easy": 5,
    "easy": 10,
    "medium": 15,
    "hard": 20,
    "very_hard": 25,
    "nearly_impossible": 30
}


class D20Test(enum.Enum):
    ability_check = 0
    saving_throw = 1
    attack_roll = 2


class DifficultyClass(enum.Enum):
    very_easy =         {"label": "Very Easy"}
    easy =              {"label": "Easy"}
    medium =            {"label": "Medium"}
    hard =              {"label": "Hard"}
    very_hard =         {"label": "Very Hard"}
    nearly_impossible = {"label": "Nearly Impossible"}

    @property
    def label(self):
        return self.value["label"]

    @property
    def value(self):
        return _DC_VALUE_TABLE[self.name]


class D20Modifier(enum.Enum):
    disadvantage = -1
    normal = 0
    advantage = 1


def resolve_multiple_d20modifiers(modifiers_list:list[D20Modifier], current_session_rules:D20ModifierStacking):
    # the modifiers list should have more than one entry, shoot an error if it is ever called with empty, or single item
    assert len(modifiers_list) > 1

    if current_session_rules == D20ModifierStacking.allowed:
        # resolve pairwise advantage and disadvantage dies (cancellation)
        while ((D20Modifier.advantage in modifiers_list)
               and (D20Modifier.disadvantage in modifiers_list)):
            modifiers_list.remove(D20Modifier.advantage)
            modifiers_list.remove(D20Modifier.disadvantage)
            # continue until all cancellations are done

        if len(modifiers_list) > 0:
            base_modifier = modifiers_list[0]
            roll_modifier = sum([D20Mod.value for D20Mod in modifiers_list[1:]])

            roll_modifier = max(-_STACK_MODIFIER_CAP, min(_STACK_MODIFIER_CAP, roll_modifier))  # keep the modifier within bounds

            return base_modifier, roll_modifier
        else:  # list is empty, cancellation yielded empty list-- leading to normal roll with no stack modifier
            return D20Modifier.normal, 0

    else:
        # resolves advantages and disadvantages with RAW (Rules as Written)
        if ((D20Modifier.advantage in modifiers_list)
                and (D20Modifier.disadvantage in modifiers_list)):
            return D20Modifier.normal
        else:
            return modifiers_list[0]


class DieType(enum.Enum):  # represents the upper bound of the dice type in human-readable format
    d1 = 1  # weird edge case when considering the "Blowgun" weapon
    d2 = 2
    d4 = 4
    d6 = 6
    d8 = 8
    d10 = 10
    d12 = 12
    d20 = 20
    d100 = 100

    def flat_avg(self):
        return math.ceil((1 + self.value) / 2)

    def roll(self, quantity:int=1) -> int:
        total_roll = 0
        roll_history = []

        for die in range(quantity):
            roll = random.randint(1, self.value)
            roll_history.append(roll)
            total_roll += roll

        return total_roll


class DiceRoll:
    def __init__(self, die:DieType, qty:int):
        self.die = die
        self.qty = qty

    def roll(self) -> int:
        return self.die.roll(self.qty)

    def flat_avg(self) -> int:
        return self.qty * self.die.flat_avg()