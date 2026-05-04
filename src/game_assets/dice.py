"""

"""

import enum, math, random
from .optional_ruleset import D20ModifierStacking, _STACK_MODIFIER_CAP

_DC_VALUE_TABLE = {
    "very_easy": 5,
    "easy": 10,
    "medium": 15,
    "hard": 20,
    "very_hard": 25,
    "nearly_impossible": 30
}


class D20TestType(enum.Enum):
    ability_check   = enum.auto()
    saving_throw    = enum.auto()
    attack_roll     = enum.auto()


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


def resolve_multiple_d20modifiers(modifiers_list:list[D20Modifier], current_session_rules:D20ModifierStacking) -> tuple[D20Modifier, int]:
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
            return D20Modifier.normal, 0
        else:
            return modifiers_list[0], 0


def d20_test(modifiers:list = None,
             dc:DifficultyClass = DifficultyClass.medium,
             roll_type:D20Modifier = D20Modifier.normal) -> bool:
    """
    Rolling a D20 against a check (DC) to determine if roll passes or not
    :param modifiers: positive or negative influence on outcome of roll
    :param dc: number that needs to be met, or exceeded
    :param roll_type: whether the roll is with advantage, disadvantage, or neither (normal)
    :return: bool indicating if roll passes or not
    """
    roll_history = [DieType.d20.roll()]
    roll_result = roll_history[0]

    if roll_type == D20Modifier.disadvantage or roll_type == D20Modifier.advantage:
        roll_history.append(DieType.d20.roll())

        if roll_type == D20Modifier.disadvantage:
            roll_result = min(roll_history)
        if roll_type == D20Modifier.advantage:
            roll_result = max(roll_history)

    premod_roll = roll_result

    if premod_roll == 20:
        # modifiers don't matter: auto-succeed
        # Trigger.on_critical_success
        return True
    elif premod_roll == 1:
        # modifiers don't matter: auto-fail
        # Trigger.on_critical_failure
        return False

    if modifiers:
        for modifier in modifiers:
            roll_result += int(modifier)

    return roll_result >= dc.value