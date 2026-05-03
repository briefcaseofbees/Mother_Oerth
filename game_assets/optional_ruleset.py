import enum

_STACK_MODIFIER_CAP = 3  # maximum modifier on stacked advantage/disadvantage D20Modifiers

# TODO: look at optional rules as listed in the SRD, similar to what is mentioned below in the MaterialEnforcement enum



class NonPCDeathSavingThrows(enum.Enum):
    standard = 0  # only PCs get death saving throws
    essential = 1  # essential NPCs get death saving throws, but can succeed
    essential_fail = 2  # essential NPCs get death saving throws, but fail each time
    all = 3  # all NPCs (even enemies) get death saving throws, and can succeed


class MaterialEnforcement(enum.Enum):
    """
    all spells in the spells.json will have ALL available information as listed in SRD, but based on setting below--
    may be set to ignore certain elements of the data stored
    """

    none = 0  # BG3-esque spell material setting
    partial = 1  # only gold-cost components enforced, flavour components ignored
    strict = 2  # all components required, spell focus rule applies


class ItemWeightEnforcement(enum.Enum):
    strict = 0  # all items that have a listed weight in SRD count against carrying cap
    strict_gold_ammo = 1  # all items except ammo and gold with listed weight in SRD count against carrying cap
    equipped_ignore = 2  # only inventory items count against carrying cap (equipped items are ignored)
    ignore = 3  # all item weights are ignored


class EncumbranceEnforcement(enum.Enum):
    strict = 0  # encumbrance levels are real, and dangerous
    strict_ignore = 1  # encumbrance levels are real, but only stat disadv are applied


class MultiClassAllowance(enum.Enum):
    # Multiclassing could, or could not be allowed in a session

    allowed = 0  # allowed, but ability score req apply (DND standard)
    allowed_ignore = 1  # allowed, but ability score req is ignored (BG3)
    disallowed = 2  # completely disallowed (no multiclassing) (Table rules)


class EquipTimeEnforcement(enum.Enum):
    strict_all = 0  # regardless of whether in combat or not, don/doff, and swapping weapons takes time
    strict_combat = 1  # don/doff, and swapping weapons takes time ONLY in combat
    ignored = 2  # equipment can be swapped instantly (BG3)


class D20ModifierStacking(enum.Enum):
    """
    In the SRD, it states that D20 tests are subject to D20 modifiers (advantage/disadvantage). In the RAW (rules as
    written) it states that the stacking these advantages/disadvantages does not occur-- only cancellation and a
    resultant normal D20 test roll should an action have any combination of these D20 modifiers.

    This optional rule has two states: allowed, and disallowed, defined as follows:
        disallowed (default): Sticks to the RAW case, no stacking, and if both advantage and disadvantage are present
        for a particular action (regardless of quantity) it will be rolled as a normal D20 test.

        allowed: D20 modifiers are not stacked in the case of multiple rolls with advantage-- but rather beyond the
            first advantage or disadvantage (after cancellation) a slight modifier value is added to the result of the
            D20 test.

            e.g.
            advantage: if a player has 3 advantage D20 modifiers on the D20 test, then the D20
            test is rolled as advantage, but will have a +2 added to the result of the roll.

            disadvantage: if a player has 2 disadvantage D20 modifiers on the D20 test, then the D20
            test is rolled as disadvantage, but will have a -1 added to the result of the roll.

            This optional rule is primarily to reward players who through strategy manage to fetch multiple
            advantages for a roll but also punish players who rack up multiple disadvantages (in this way-- it is a
            double-edged sword!)

            The cap for this modifier is given by the _STACK_MODIFIER_CAP constant-- and is to prevent excessive
            stacks of these bonuses. (This may change as playtesting dictates!)
    """
    disallowed = 0
    allowed = 1

# EOF