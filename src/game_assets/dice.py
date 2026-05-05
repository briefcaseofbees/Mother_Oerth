"""

"""

import math, random
from .game_constants import D20ModifierType, D20ModifierStackingRule, _STACK_MODIFIER_CAP, DifficultyClass, DieType


class Dice:
    def __init__(self, die:DieType, qty:int):
        self.die = die
        self.qty = qty

    def roll(self) -> int:
        total_roll = 0
        roll_history = []

        for die in range(self.qty):
            roll = random.randint(1, self.die.value)
            roll_history.append(roll)
            total_roll += roll

        return total_roll

    def flat_avg(self) -> int:
        return self.qty * math.ceil((1 + self.die.value) / 2)


def resolve_multiple_d20modifiers(modifiers_list:list[D20ModifierType], current_session_rules:D20ModifierStackingRule) -> tuple[D20ModifierType, int]:
    # the modifiers list should have more than one entry, shoot an error if it is ever called with empty, or single item
    assert len(modifiers_list) > 1

    if current_session_rules == D20ModifierStackingRule.allowed:
        # resolve pairwise advantage and disadvantage dies (cancellation)
        while ((D20ModifierType.advantage in modifiers_list)
               and (D20ModifierType.disadvantage in modifiers_list)):
            modifiers_list.remove(D20ModifierType.advantage)
            modifiers_list.remove(D20ModifierType.disadvantage)
            # continue until all cancellations are done

        if len(modifiers_list) > 0:
            base_modifier = modifiers_list[0]
            roll_modifier = sum([D20Mod.value for D20Mod in modifiers_list[1:]])

            roll_modifier = max(-_STACK_MODIFIER_CAP, min(_STACK_MODIFIER_CAP, roll_modifier))  # keep the modifier within bounds

            return base_modifier, roll_modifier
        else:  # list is empty, cancellation yielded empty list-- leading to normal roll with no stack modifier
            return D20ModifierType.normal, 0

    else:
        # resolves advantages and disadvantages with RAW (Rules as Written)
        if ((D20ModifierType.advantage in modifiers_list)
                and (D20ModifierType.disadvantage in modifiers_list)):
            return D20ModifierType.normal, 0
        else:
            return modifiers_list[0], 0


def d20_test(modifiers:list = None, dc:DifficultyClass = DifficultyClass.medium, roll_type:D20ModifierType = D20ModifierType.normal) -> bool:
    """
    Rolling a D20 against a check (DC) to determine if roll passes or not
    :param modifiers: positive or negative influence on outcome of roll
    :param dc: number that needs to be met, or exceeded
    :param roll_type: whether the roll is with advantage, disadvantage, or neither (normal)
    :return: bool indicating if roll passes or not
    """
    roll_history = [Dice(DieType.d20, 1).roll()]
    roll_result = roll_history[0]

    if roll_type == D20ModifierType.disadvantage or roll_type == D20ModifierType.advantage:
        roll_history.append(Dice(DieType.d20, 1).roll())

        if roll_type == D20ModifierType.disadvantage:
            roll_result = min(roll_history)
        if roll_type == D20ModifierType.advantage:
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


def roll_ability_scores() -> list[int]:
    results = []
    for stat_roll in range(6):
        rolled_stats = []


        # add grace-roll mechanic for rolling stats... (if I feel like it's necessary)

        for dice_roll in range(4):
            results.append(random.randint(1, 6))

        results.sort()
        result_sum = sum(results[1:])
        rolled_stats[stat_roll] = result_sum

    return results