"""
    contains all constants in the game, these constants are for classification, enumeration, and game logic
    the enum classes do NOT have method-behaviour other than dict lookup, and returning labels
"""

import enum


# TODO: for all below enums-- add labels for assets that will be player-facing...
#  e.g.
#   DamageType attributes will be in some way displayed to the player-- (when making an attack, etc.)


class AbilityScoreMethod(enum.Enum):
    random      = enum.auto()
    standard    = enum.auto()
    manual      = enum.auto()


class AbilityType(enum.Enum):
    str     = {"label": "Strength"}
    dex     = {"label": "Dexterity"}
    con     = {"label": "Constitution"}
    int     = {"label": "Intelligence"}
    wis     = {"label": "Wisdom"}
    cha     = {"label": "Charisma"}

    @property
    def label(self):
        return self.value["label"]

    @property
    def associated_skills(self) -> list:
        associated_skills = []
        for skill, ability_type in _SKILL_TO_ABILITY_MAPPING.items():
            if self == ability_type:
                associated_skills.append(skill)
        return associated_skills


class ActionCostType(enum.Enum):
    action              = {"label": "Action"}
    bonus_action        = {"label": "Bonus Action"}
    reaction            = {"label": "Reaction"}
    legendary_action    = {"label": "Legendary Action"}

    @property
    def label(self):
        return self.value["label"]


class ActionType(enum.Enum):
    # all of these cost ActionCostType.action
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


class AlignmentType(enum.Enum):
    lg = {"label": "Lawful Good"}
    ng = {"label": "Neutral Good"}
    cg = {"label": "Chaotic Good"}
    ln = {"label": "Lawful Neutral"}
    nn = {"label": "True Neutral"}
    cn = {"label": "Chaotic Neutral"}
    le = {"label": "Lawful Evil"}
    ne = {"label": "Neutral Evil"}
    ce = {"label": "Chaotic Evil"}

    @property
    def label(self):
        return self.value["label"]


class AmmoType(enum.Enum):
    arrow           = {"label": "Arrow"}
    bolt            = {"label": "Bolt"}
    bullet_sling    = {"label": "Bullet (Sling)"}
    bullet_firearm  = {"label": "Bullet (Firearm)"}
    needle          = {"label": "Needle"}

    @property
    def label(self):
        return self.value["label"]


class ArmorSlotType(enum.Enum):  # the slots that (specifically) equipped items can occupy
    headwear                = {"label": "Headwear"}
    eyes                    = {"label": "Eyes"}
    mantle                  = {"label": "Mantle"}
    musical_instrument      = {"label": "Musical Instrument"}
    amulet                  = {"label": "Amulet"}
    armor                   = {"label": "Armor"}
    clothing                = {"label": "Clothing"}
    cloak                   = {"label": "Cloak"}
    wrists                  = {"label": "Wrists"}
    handwear                = {"label": "Handwear"}
    ring                    = {"label": "Ring"}
    shield                  = {"label": "Shield"}
    main_hand               = {"label": "Main Hand"}
    off_hand                = {"label": "Off Hand"}
    light_source            = {"label": "Light Source"}
    footwear                = {"label": "Footwear"}

    @property
    def label(self):
        return self.value["label"]


class ArmorType(enum.Enum):
    clothing    = {"label": "Clothing"}
    light       = {"label": "Light"}
    medium      = {"label": "Medium"}
    heavy       = {"label": "Heavy"}
    shield      = {"label": "Shield"}


class ClassType(enum.Enum):
    artificer       = {"label": "Artificer"}
    barbarian       = {"label": "Barbarian"}
    bard            = {"label": "Bard"}
    cleric          = {"label": "Cleric"}
    druid           = {"label": "Druid"}
    fighter         = {"label": "Fighter"}
    monk            = {"label": "Monk"}
    paladin         = {"label": "Paladin"}
    ranger          = {"label": "Ranger"}
    rogue           = {"label": "Rogue"}
    sorcerer        = {"label": "Sorcerer"}
    warlock         = {"label": "Warlock"}
    wizard          = {"label": "Wizard"}

    @property
    def label(self):
        return self.value["label"]

    @property
    def hit_dice(self):
        return _CLASS_HIT_DICE_TABLE[self.name]

    @property
    def starting_array(self):
        return _CLASS_STARTING_ABILITY_ARRAY_TABLE[self.name]


class CoinType(enum.Enum):
    cp = {"label_short": "CP", "label_long": "Copper Piece(s)", "value": 1}
    sp = {"label_short": "SP", "label_long": "Silver Pieces(s)", "value": 10}
    ep = {"label_short": "EP", "label_long": "Electrum Piece(s)", "value": 50}
    gp = {"label_short": "GP", "label_long": "Gold Piece(s)", "value": 100}
    pp = {"label_short": "PP", "label_long": "Platinum Piece(s)", "value": 1000}

    def label(self, short_form: bool = False):
        if short_form:
            return self.value["label_short"]
        else:
            return self.value["label_long"]


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


class ConditionType(enum.Enum):
    # https://bg3.wiki/wiki/Conditions  <-- use to borrow some conditions that are not listed (some may fit into Trigger)
    # page 1: https://bg3.wiki/wiki/Conditions/List_(1-500)
    # page 2: https://bg3.wiki/wiki/Conditions/List_(501-1000)
    # page 3: https://bg3.wiki/wiki/Conditions/List_(1001-1500)

    """
        Conditions can fall under two categories: 'True' Conditions, and 'Derived' Conditions
            - True Conditions: those imposed by spells, items, etc.
            - Derived Conditions: those imposed by situation, environment, etc.

            e.g.
            - "poisoned" condition given by poisoned blade (True Condition) fixed by antidote
            - "threatened" condition given by non-prone enemy being within 5ft of affected creature
    """

    blinded             = {"label": "Blinded"}
    charmed             = {"label": "Charmed"}
    deafened            = {"label": "Deafened"}
    frightened          = {"label": "Frightened"}
    grappled            = {"label": "Grappled"}
    incapacitated       = {"label": "Incapacitated"}
    stunned             = {"label": "Stunned"}
    petrified           = {"label": "Petrified"}
    unconscious         = {"label": "Unconscious"}
    restrained          = {"label": "Restrained"}
    invisible           = {"label": "Invisible"}
    paralyzed           = {"label": "Paralyzed"}
    poisoned            = {"label": "Poisoned"}
    prone               = {"label": "Prone"}
    threatened          = {"label": "Threatened"}  # for marking a Creature as being within 5ft of another (page 3 of bg3 conditions)
    # TODO: look at how the exhaustion mechanic works, find out how to put it to code (every 24 hours that a player does not long rest there is a DC check)
    exhaustion_lvl1     = {"label": "Somewhat Exhausted"}
    exhaustion_lvl2     = {"label": "Exhausted"}
    exhaustion_lvl3     = {"label": "Very Exhausted"}
    exhaustion_lvl4     = {"label": "Very-Very Exhausted"}
    exhaustion_lvl5     = {"label": "Extremely Exhausted"}
    exhaustion_lvl6     = {"label": "Deadly Exhausted"}

    @property
    def label(self):
        return self.value["label"]


class CoverType(enum.Enum):
    # TODO: convert to a dictionary, so that the bonuses can be part of the cover type as well

    exposed = 0             # no bonuses
    half = 1                # +2 AC, adv DEX saving throws
    three_quarters = 2      # +5 AC, adv DEX saving throws
    total = 3               # can't be targeted directly


class CreatureAttitude(enum.Enum):
    # overall sentiment towards another creature
    hostile = 0  # disadvantage on ability check to influence creature
    indifferent = 1  # no desire to help or hinder (normal/default)
    friendly = 2  # advantage on ability check to influence creature


class CreatureSentiment(enum.Enum):
    # creature sentiment towards a specific action that it's being asked to do
    unwilling = 0  # no ability checks needed, it doesn't comply
    hesitant = 1  # ability check whose outcome is dependent on CreatureAttitude
    willing = 2  # no ability checks needed, it will fulfill your request in the way it prefers


class CreatureSize(enum.Enum):
    tiny            = {"label": "Tiny"}
    small           = {"label": "Small"}
    medium          = {"label": "Medium"}
    large           = {"label": "Large"}
    huge            = {"label": "Huge"}
    gargantuan      = {"label": "Gargantuan"}

    @property
    def label(self):
        return self.value["label"]

    @property
    def hit_dice(self):
        return _CREATURE_SIZE_HIT_DICE_TABLE[self]


class CreatureType(enum.Enum):
    beast           = {"label": "Beast"}
    humanoid        = {"label": "Humanoid"}
    monstrosity     = {"label": "Monstrosity"}
    dragon          = {"label": "Dragon"}
    fiend           = {"label": "Fiend"}
    celestial       = {"label": "Celestial"}
    undead          = {"label": "Undead"}
    elemental       = {"label": "Elemental"}
    fey             = {"label": "Fey"}
    ooze            = {"label": "Ooze"}
    construct       = {"label": "Construct"}
    plant           = {"label": "Plant"}
    giant           = {"label": "Giant"}
    aberration      = {"label": "Aberration"}

    @property
    def label(self):
        return self.value["label"]


class DamageResistType(enum.Enum):
    vulnerable      = {"label": "Vulnerable"}
    no_resistance   = {"label": "No Resistance"}
    resistance      = {"label": "Resistance"}
    immune          = {"label": "Immune"}

    @property
    def label(self):
        return self.value["label"]


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


class DayOfWeek(enum.Enum):
    starday     = {"label": "Starday"}   # saturday
    sunday      = {"label": "Sunday"}    # sunday
    moonday     = {"label": "Moonday"}   # monday
    godsday     = {"label": "Godsday"}   # tuesday
    waterday    = {"label": "Waterday"}  # wednesday
    earthday    = {"label": "Earthday"}  # thursday
    freeday     = {"label": "Freeday"}   # friday

    @property
    def label(self):
        return self.value["label"]

    @property
    def next(self):
        members = list(DayOfWeek)
        current_index = members.index(self)
        next_member = members[(current_index + 1) % len(members)]
        return next_member


class D20ModifierType(enum.Enum):
    disadvantage = -1
    normal = 0
    advantage = 1


class D20ModifierStackingRule(enum.Enum):
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


class D20TestType(enum.Enum):
    ability_check   = enum.auto()
    saving_throw    = enum.auto()
    attack_roll     = enum.auto()


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


class EncumbranceEnforcementRule(enum.Enum):
    strict = 0  # encumbrance levels are real, and dangerous
    strict_ignore = 1  # encumbrance levels are real, but only stat disadv are applied


class EncumbranceStatus(enum.Enum):
    # TODO: These should just be conditions...
    unencumbered                = {"label": "Unencumbered"}
    encumbered                  = {"label": "Encumbered"}
    heavily_encumbered          = {"label": "Heavily Encumbered"}
    very_heavily_encumbered     = {"label": "Very Heavily Encumbered"}

    @property
    def label(self):
        return self.value["label"]


class EnvironmentEffectType(enum.Enum):
    deep_water = enum.auto()
    extreme_cold = enum.auto()
    extreme_heat = enum.auto()
    frigid_water = enum.auto()
    heavy_precipitation = enum.auto()
    high_altitude = enum.auto()
    slippery_ice = enum.auto()
    strong_wind = enum.auto()
    thin_ice = enum.auto()


class EnvironmentLightLevel(enum.Enum):
    magical_light = 0
    bright_light = 1
    dim_light = 2
    darkness = 3
    magical_darkness = 4


class EquipTimeEnforcementRule(enum.Enum):
    strict_all = 0  # regardless of whether in combat or not, don/doff, and swapping weapons takes time
    strict_combat = 1  # don/doff, and swapping weapons takes time ONLY in combat
    ignored = 2  # equipment can be swapped instantly (BG3)


class FestivalDay(enum.Enum):
    day_1 = {"label": "Low Festival (Starday)"}
    day_2 = {"label": "Low Festival (Sunday)"}
    day_3 = {"label": "Low Festival (Moonday)"}
    day_4 = {"label": "Mid-Festival (Godsday)"}
    day_5 = {"label": "High Festival (Waterday)"}
    day_6 = {"label": "High Festival (Earthday)"}
    day_7 = {"label": "High Festival (Freeday)"}


class FestivalWeek(enum.Enum):
    needfest = 0  # Midwinter     (between Sunsebb and Fireseek)
    growfest = 1  # Spring        (between Coldeven and Planting)
    richfest = 2  # Midsummer     (between Wealsun and Reaping)
    brewfest = 3  # Harvest       (between Harvester and Patchwall)

    @property
    def label(self):
        festival_labels = ["Needfest", "Growfest", "Richfest", "Brewfest"]
        return festival_labels[self.value]


class GamingSetType(enum.Enum):
    dice                = {"label": "Dice"}
    dragonchess         = {"label": "Dragonchess"}
    playing_cards       = {"label": "Playing Cards"}
    threedragon_ante    = {"label": "Three-Dragon Ante"}

    @property
    def label(self):
        return self.value["label"]


class HazardType(enum.Enum):
    burning         = {"label": "Burning"}
    falling         = {"label": "Falling"}
    suffocation     = {"label": "Suffocation"}
    dehydration     = {"label": "Dehydration"}
    malnutrition    = {"label": "Malnutrition"}

    @property
    def label(self):
        return self.value["label"]


class ItemRarityType(enum.Enum):
    mundane         = {"label": "Mundane"}
    common          = {"label": "Common"}
    uncommon        = {"label": "Uncommon"}
    rare            = {"label": "Rare"}
    very_rare       = {"label": "Very Rare"}
    legendary       = {"label": "Legendary"}
    artifact        = {"label": "Artifact"}

    @property
    def label(self):
        return self.value["label"]


class ItemType(enum.Enum):
    scroll = {"label": "Scroll"}
    potion = {"label": "Potion"}
    poison = {"label": "Poison"}


class ItemWeightEnforcementRule(enum.Enum):
    strict = 0  # all items that have a listed weight in SRD count against carrying cap
    strict_gold_ammo = 1  # all items except ammo and gold with listed weight in SRD count against carrying cap
    equipped_ignore = 2  # only inventory items count against carrying cap (equipped items are ignored)
    ignore = 3  # all item weights are ignored


class LanguageType(enum.Enum):
    common          = {"label": "Common",       "rarity": "standard"}
    draconic        = {"label": "Draconic",     "rarity": "standard"}
    dwarvish        = {"label": "Dwarvish",     "rarity": "standard"}
    elvish          = {"label": "Elvish",       "rarity": "standard"}
    giant           = {"label": "Giant",        "rarity": "standard"}
    gnomish         = {"label": "Gnomish",      "rarity": "standard"}
    goblin          = {"label": "Goblin",       "rarity": "standard"}
    halfling        = {"label": "Halfling",     "rarity": "standard"}
    orc             = {"label": "Orc",          "rarity": "standard"}
    abyssal         = {"label": "Abyssal",          "rarity": "rare"}
    celestial       = {"label": "Celestial",        "rarity": "rare"}
    deep_speech     = {"label": "Deep Speech",      "rarity": "rare"}
    druidic         = {"label": "Druidic",          "rarity": "rare"}
    infernal        = {"label": "Infernal",         "rarity": "rare"}
    primordial      = {"label": "Primordial",       "rarity": "rare"}
    sylvan          = {"label": "Sylvan",           "rarity": "rare"}
    thieves_cant    = {"label": "Thieves Cant",     "rarity": "rare"}
    undercommon     = {"label": "Undercommon",      "rarity": "rare"}

    @property
    def label(self):
        return self.value["label"]

    @property
    def rarity(self):
        return self.value["rarity"]

    @classmethod
    def by_rarity(cls, rarity):
        return [lang for lang in cls if lang.rarity == rarity]


class LevelAdvancement(enum.Enum):
    level_1     = enum.auto()
    level_2     = enum.auto()
    level_3     = enum.auto()
    level_4     = enum.auto()
    level_5     = enum.auto()
    level_6     = enum.auto()
    level_7     = enum.auto()
    level_8     = enum.auto()
    level_9     = enum.auto()
    level_10    = enum.auto()
    level_11    = enum.auto()
    level_12    = enum.auto()
    level_13    = enum.auto()
    level_14    = enum.auto()
    level_15    = enum.auto()
    level_16    = enum.auto()
    level_17    = enum.auto()
    level_18    = enum.auto()
    level_19    = enum.auto()
    level_20    = enum.auto()

    @property
    def number(self):
        return self.name.split("_")[1]

    @property
    def required_xp(self):
        return _LVL_XP_TABLE[self]

    @property
    def prof_bonus(self):
        return _LVL_PROF_BONUS_TABLE[self]


class MagicalSchoolType(enum.Enum):
    abjuration = 0      # focus: protection/shielding
    conjuration = 1     # focus: summoning/creating magical objects/creatures
    divination = 2      # focus: allows caster to perceive beyond their normal senses
    enchantment = 3     # focus: enchants mind or body of others
    evocation = 4       # focus: manipulates elemental energies
    illusion = 5        # focus: creates illusions to deceive others
    necromancy = 6      # focus: manipulates dead creatures
    transmutation = 7   # focus: manipulates matter and life


class MaterialEnforcementRule(enum.Enum):
    """
    all spells in the spells.json will have ALL available information as listed in SRD, but based on setting below--
    may be set to ignore certain elements of the data stored
    """

    none = 0  # BG3-esque spell material setting
    partial = 1  # only gold-cost components enforced, flavour components ignored
    strict = 2  # all components required, spell focus rule applies


class Month(enum.Enum):
    fireseek    = {"label": "Fireseek"}  # january equivalent
    readying    = {"label": "Readying"}
    coldeven    = {"label": "Coldeven"}
    planting    = {"label": "Planting"}
    flocktime   = {"label": "Flocktime"}
    wealsun     = {"label": "Wealsun"}
    reaping     = {"label": "Reaping"}
    goodmonth   = {"label": "Goodmonth"}
    harvester   = {"label": "Harvester"}
    patchwall   = {"label": "Patchwall"}
    ready_reat  = {"label": "Ready'reat"}
    sunsebb     = {"label": "Sunsebb"}

    @property
    def label(self):
        return self.value["label"]

    @classmethod
    def index(cls, month_num):
        members = list(cls.__members__.values())
        return members[month_num - 1]

    def next(self):
        members = list(Month)
        current_index = members.index(self)
        next_member = members[(current_index + 1) % len(members)]
        return next_member


class MultiClassAllowanceRule(enum.Enum):
    # Multiclassing could, or could not be allowed in a session

    allowed = 0  # allowed, but ability score req apply (DND standard)
    allowed_ignore = 1  # allowed, but ability score req is ignored (BG3)
    disallowed = 2  # completely disallowed (no multiclassing) (Table rules)


class MusicalInstrumentType(enum.Enum):
    bagpipes        = {"label": "Bagpipes"}
    drum            = {"label": "Drum"}
    dulcimer        = {"label": "Dulcimer"}
    flute           = {"label": "Flute"}
    horn            = {"label": "Horn"}
    lute            = {"label": "Lute"}
    lyre            = {"label": "Lyre"}
    pan_flute       = {"label": "Pan Flute"}
    shawm           = {"label": "Shawm"}
    viol            = {"label": "Viol"}

    @property
    def label(self):
        return self.value["label"]


class NonPCDeathSavingThrowsRule(enum.Enum):
    standard = 0  # only PCs get death saving throws
    essential = 1  # essential NPCs get death saving throws, but can succeed
    essential_fail = 2  # essential NPCs get death saving throws, but fail each time
    all = 3  # all NPCs (even enemies) get death saving throws, and can succeed


class ObjectDamageThresholdType(enum.Enum):
    # TODO: find more official documentation on how damage thresholds work in dnd 5e

    indestructible = -1     # can never be destroyed
    none = 0                # can be destroyed with repeated light attacks
    light = 5
    medium = 10
    heavy = 20
    impenetrable = 30


class ObjectMaterialType(enum.Enum):
    cloth =         {"label": "Cloth"}
    paper =         {"label": "Paper"}
    rope =          {"label": "Rope"}
    crystal =       {"label": "Crystal"}
    glass =         {"label": "Glass"}
    ice =           {"label": "Ice"}
    wood =          {"label": "Wood"}
    bone =          {"label": "Bone"}
    stone =         {"label": "Stone"}
    iron =          {"label": "Iron"}
    steel =         {"label": "Steel"}
    mithral =       {"label": "Mithral"}
    adamantine =    {"label": "Adamantine"}

    @property
    def label(self):
        return self.value["label"]

    @property
    def ac(self):
        return _OBJECT_MATERIAL_AC_TABLE[self.name]


class ObjectSizeType(enum.Enum):
    tiny        = {"label": "tiny"}
    small       = {"label": "small"}
    medium      = {"label": "medium"}
    large       = {"label": "large"}

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


class SenseType(enum.Enum):
    normal = -1  # no special senses
    blind_sight = 0
    dark_vision = 1
    tremor_sense = 2
    true_sight = 3


class SkillProficiencyType(enum.Enum):
    normal          = {"label": "Normal"}
    proficient      = {"label": "Proficient"}
    expert          = {"label": "Expert"}


class SkillType(enum.Enum):  # should have a JSON file with the associated skill and description for each skill
    athletics           = {"label": "Athletics"}
    acrobatics          = {"label": "Acrobatics"}
    sleight_of_hand     = {"label": "Sleight of Hand"}
    stealth             = {"label": "Stealth"}
    arcana              = {"label": "Arcana"}
    history             = {"label": "History"}
    investigation       = {"label": "Investigation"}
    nature              = {"label": "Nature"}
    religion            = {"label": "Religion"}
    animal_handling     = {"label": "Animal Handling"}
    insight             = {"label": "Insight"}
    medicine            = {"label": "Medicine"}
    perception          = {"label": "Perception"}
    survival            = {"label": "Survival"}
    deception           = {"label": "Deception"}
    intimidation        = {"label": "Intimidation"}
    performance         = {"label": "Performance"}
    persuasion          = {"label": "Persuasion"}

    @property
    def label(self):
        return self.value["label"]

    @property
    def associated_ability(self):
        return _SKILL_TO_ABILITY_MAPPING[self]


class SpellAOEType(enum.Enum):
    target = -1  # single target (no AOE), can refer to spells that affect multiple targets
    # TODO: need to determine the exact dimensions of a cone, cube, and any other multi-square AOEs
    cone = 0
    cube = 1
    cylinder = 2
    emanation = 3
    line = 4
    sphere = 5


class SpellDurationType(enum.Enum):
    instant = 0
    concentration = 1
    time_span = 2


class SpellFocusType(enum.Enum):
    arcane_focus = 0  # applies to sorcerers, warlocks, wizards
    druidic_focus = 1  # applies to druids
    holy_symbol = 2  # applies to clerics, paladins
    musical_instrument = 3  # applies to bards


class SpellLevelType(enum.Enum):
    cantrip = 0
    first_level = 1
    second_level = 2
    third_level = 3
    fourth_level = 4
    fifth_level = 5
    sixth_level = 6
    seventh_level = 7
    eighth_level = 8
    nineth_level = 9


class SpellRangeType(enum.Enum):
    self = 0
    touch = 1
    distance = 2


class TagType(enum.Enum):
    """
    INCOMPLETE: TagType covers the closed set of categories that the Tag class (in tag.py) can fall under...
    """
    identity = enum.auto()              # covers race, class, organization
    weapon_proficiency = enum.auto()
    armor_proficiency = enum.auto()


class TimeOfDay(enum.Enum):
    dead_of_night = {"label": "Dead of Night", "stealth_bonus": 2, "npc_activity": "asleep"}  # 12am - 3am
    twilight =      {"label": "Twilight", "stealth_bonus": 1, "npc_activity": "asleep"}  # 3am - 6am
    dawn =          {"label": "Dawn", "stealth_bonus": 1, "npc_activity": "waking"}  # 6am - 9am
    morning =       {"label": "Morning", "stealth_bonus": 0, "npc_activity": "active"}  # 9am - 12pm
    midday =        {"label": "Midday", "stealth_bonus": 0, "npc_activity": "active"}  # 12pm - 3pm
    afternoon =     {"label": "Afternoon", "stealth_bonus": 0, "npc_activity": "active"}  # 3pm - 6pm
    dusk =          {"label": "Dusk", "stealth_bonus": 1, "npc_activity": "winding_down"}  # 6pm - 9pm
    night =         {"label": "Night", "stealth_bonus": 2, "npc_activity": "minimal"}  # 9pm - 12am

    @property
    def label(self):
        return self.value["label"]


class ToolProficiencyType(enum.Enum):
    alchemist_supplies          = {"label": "Alchemist Supplies"}
    brewer_supplies             = {"label": "Brewer Supplies"}
    calligrapher_supplies       = {"label": "Calligrapher Supplies"}
    carpenter_tools             = {"label": "Carpenter Tools"}
    cartographer_tools          = {"label": "Cartographer Tools"}
    cobbler_tools               = {"label": "Cobbler Tools"}
    cook_utensils               = {"label": "Cook Utensils"}
    glassblower_tools           = {"label": "Glassblower Tools"}
    jeweler_tools               = {"label": "Jeweler Tools"}
    leatherworker_tools         = {"label": "Leatherworker Tools"}
    mason_tools                 = {"label": "Mason Tools"}
    painter_supplies            = {"label": "Painter Supplies"}
    potter_tools                = {"label": "Potter Tools"}
    smith_tools                 = {"label": "Smith Tools"}
    tinker_tools                = {"label": "Tinker Tools"}
    weaver_tools                = {"label": "Weaver Tools"}
    woodcarver_tools            = {"label": "Woodcarver Tools"}
    disguise_kit                = {"label": "Disguise Kit"}
    forgery_kit                 = {"label": "Forgery Kit"}
    gaming_set                  = {"label": "Gaming Set"}
    herbalism_kit               = {"label": "Herbalism Kit"}
    musical_instrument          = {"label": "Musical Instrument"}
    navigator_tools             = {"label": "Navigator Tools"}
    poisoner_kit                = {"label": "Poisoner Kit"}
    thief_tools                 = {"label": "Thief Tools"}

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


class TriggerType(enum.Enum):
    """list of game logic triggers"""

    # COMBAT TRIGGERS
    on_attack_rolled = enum.auto()
    on_melee_hit = enum.auto()
    on_melee_miss = enum.auto()
    on_ranged_hit = enum.auto()
    on_ranged_miss = enum.auto()
    on_damage_dealt = enum.auto()
    on_damage_taken = enum.auto()
    on_critical_hit = enum.auto()
    on_kill = enum.auto()
    on_death_save = enum.auto()
    on_stabilize = enum.auto()
    on_spell_cast = enum.auto()
    on_spell_hit = enum.auto()
    on_concentration_broken = enum.auto()

    # DICE TRIGGERS
    on_critical_success = enum.auto()  # nat 20
    on_critical_failure = enum.auto()  # nat 1

    # TURN STRUCTURE
    on_turn_start = enum.auto()
    on_turn_end = enum.auto()
    on_round_start = enum.auto()
    on_round_end = enum.auto()
    on_initiative_rolled = enum.auto()

    # CHARACTER STATE
    on_hp_gained = enum.auto()
    on_temp_hp_gained = enum.auto()
    on_condition_applied = enum.auto()
    on_condition_removed = enum.auto()
    on_xp_gained = enum.auto()
    on_level_up = enum.auto()
    on_ability_score_change = enum.auto()
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
    on_player_seen = enum.auto()
    on_player_talk = enum.auto()
    on_room_enter = enum.auto()
    on_room_exit = enum.auto()
    on_item_found = enum.auto()
    on_trap_triggered = enum.auto()
    on_trap_disarmed = enum.auto()
    on_door_opened = enum.auto()
    on_door_closed = enum.auto()
    on_door_unlocked = enum.auto()
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


class VendorMagicalItemOfferings(enum.Enum):
    poor = enum.auto()
    humble = enum.auto()
    moderate = enum.auto()
    higher = enum.auto()
    highest = enum.auto()


class VendorType(enum.Enum):
    general_store = enum.auto()
    weapon_store = enum.auto()
    armor_store = enum.auto()
    potion_store = enum.auto()
    poison_store = enum.auto()
    scroll_vendor = enum.auto()
    food_store = enum.auto()
    clothing_store = enum.auto()
    musical_instrument_store = enum.auto()
    jewelry_store = enum.auto()
    curios_store = enum.auto()
    junk_store = enum.auto()
    game_store = enum.auto()


class WealthLevel(enum.Enum):
    poor = enum.auto()
    lower_class = enum.auto()
    middle_class = enum.auto()
    upper_class = enum.auto()
    rich = enum.auto()


class WeaponMasteryType(enum.Enum):
    cleave      = {"label": "Cleave"}
    graze       = {"label": "Graze"}
    nick        = {"label": "Nick"}
    push        = {"label": "Push"}
    sap         = {"label": "Sap"}
    slow        = {"label": "Slow"}
    topple      = {"label": "Topple"}
    vex         = {"label": "Vex"}

    @property
    def label(self):
        return self.value["label"]


class WeaponPropertyType(enum.Enum):
    ammunition      = {"label": "Ammunition"}
    finesse         = {"label": "Finesse"}
    heavy           = {"label": "Heavy"}
    light           = {"label": "Light"}
    loading         = {"label": "Loading"}
    range           = {"label": "Range"}
    reach           = {"label": "Reach"}
    thrown          = {"label": "Thrown"}
    two_handed      = {"label": "Two-handed"}
    versatile       = {"label": "Versatile"}
    special         = {"label": "Special"}
    silvered        = {"label": "Silvered"}

    @property
    def label(self):
        return self.value["label"]


class WeaponType(enum.Enum):
    simple      = {"label": "Simple"}
    martial     = {"label": "Martial"}
    exotic      = {"label": "Exotic"}
    melee       = {"label": "Melee"}
    ranged      = {"label": "Ranged"}

    @property
    def label(self):
        return self.value["label"]


"""FILE PATH CONSTANTS"""
_DATA_DIRECTORY = "../data/"

_ADVENTURING_GEAR_JSON_FILE_PATH    = f"{_DATA_DIRECTORY}adventuring_gear.json"
_ARMORS_JSON_FILE_PATH              = f"{_DATA_DIRECTORY}armors.json"
_CLASSES_JSON_FILE_PATH             = f"{_DATA_DIRECTORY}classes.json"
_CREATURES_JSON_FILE_PATH           = f"{_DATA_DIRECTORY}creatures.json"
_SPELLS_JSON_FILE_PATH              = f"{_DATA_DIRECTORY}spells.json"
_WEAPONS_JSON_FILE_PATH             = f"{_DATA_DIRECTORY}weapons.json"


"""LOOKUP TABLE CONSTANTS"""
_CLASS_HIT_DICE_TABLE = {
    ClassType.artificer:    DieType.d8,
    ClassType.barbarian:    DieType.d12,
    ClassType.bard:         DieType.d8,
    ClassType.cleric:       DieType.d8,
    ClassType.druid:        DieType.d8,
    ClassType.fighter:      DieType.d10,
    ClassType.monk:         DieType.d8,
    ClassType.paladin:      DieType.d10,
    ClassType.ranger:       DieType.d10,
    ClassType.rogue:        DieType.d8,
    ClassType.sorcerer:     DieType.d6,
    ClassType.warlock:      DieType.d8,
    ClassType.wizard:       DieType.d6
}

_CLASS_STARTING_ABILITY_ARRAY_TABLE = {
    ClassType.artificer:    [10, 14, 14, 16, 10, 10],
    ClassType.barbarian:    [15, 13, 14, 10, 12, 8],
    ClassType.bard:         [8, 14, 12, 13, 10, 15],
    ClassType.cleric:       [14, 8, 13, 10, 15, 12],
    ClassType.druid:        [8, 12, 14, 13, 15, 10],
    ClassType.fighter:      [15, 14, 13, 8, 10, 12],
    ClassType.monk:         [12, 15, 13, 10, 14, 8],
    ClassType.paladin:      [15, 10, 13, 8, 12, 14],
    ClassType.ranger:       [12, 15, 13, 8, 14, 10],
    ClassType.rogue:        [12, 15, 13, 14, 10, 8],
    ClassType.sorcerer:     [10, 13, 14, 8, 12, 15],
    ClassType.warlock:      [8, 14, 13, 12, 10, 15],
    ClassType.wizard:       [8, 12, 13, 15, 14, 10]
}

_CR_PROF_BONUS_TABLE = {
    "0":    2,
    "1/8":  2,
    "1/4":  2,
    "1/2":  2,
    "1":    2,
    "2":    2,
    "3":    2,
    "4":    2,
    "5":    3,
    "6":    3,
    "7":    3,
    "8":    3,
    "9":    4,
    "10":   4,
    "11":   4,
    "12":   4,
    "13":   5,
    "14":   5,
    "15":   5,
    "16":   5,
    "17":   6,
    "18":   6,
    "19":   6,
    "20":   6,
    "21":   7,
    "22":   7,
    "23":   7,
    "24":   7,
    "25":   8,
    "26":   8,
    "27":   8,
    "28":   8,
    "29":   9,
    "30":   9
}

_CR_XP_TABLE = {
    # lookup table for xp-gain by creature challenge rating
    "0": None,
    "1/8": 25,
    "1/4": 50,
    "1/2": 100,
    "1": 200,
    "2": 450,
    "3": 700,
    "4": 1100,
    "5": 1800,
    "6": 2300,
    "7": 2900,
    "8": 3900,
    "9": 5000,
    "10": 5900,
    "11": 7200,
    "12": 8400,
    "13": 10000,
    "14": 11500,
    "15": 13000,
    "16": 15000,
    "17": 18000,
    "18": 20000,
    "19": 22000,
    "20": 25000,
    "21": 33000,
    "22": 41000,
    "23": 50000,
    "24": 62000,
    "25": 75000,
    "26": 90000,
    "27": 105000,
    "28": 120000,
    "29": 135000,
    "30": 155000,
}

_CREATURE_SIZE_CARRY_WEIGHT_TABLE = {
    # creature size to carry weight (equation: str * values-below)
    CreatureSize.tiny:          7.5,
    CreatureSize.small:         15,
    CreatureSize.medium:        15,
    CreatureSize.large:         30,
    CreatureSize.huge:          60,
    CreatureSize.gargantuan:    120
}

_CREATURE_SIZE_DRAG_LIFT_PUSH_TABLE = {
    # creature size to capacity to drag, lift, and push (equation: str * values-below) (values are 2x their carry weight)
    CreatureSize.tiny:          _CREATURE_SIZE_CARRY_WEIGHT_TABLE[CreatureSize.tiny] * 2,
    CreatureSize.small:         _CREATURE_SIZE_CARRY_WEIGHT_TABLE[CreatureSize.small] * 2,
    CreatureSize.medium:        _CREATURE_SIZE_CARRY_WEIGHT_TABLE[CreatureSize.medium] * 2,
    CreatureSize.large:         _CREATURE_SIZE_CARRY_WEIGHT_TABLE[CreatureSize.large] * 2,
    CreatureSize.huge:          _CREATURE_SIZE_CARRY_WEIGHT_TABLE[CreatureSize.huge] * 2,
    CreatureSize.gargantuan:    _CREATURE_SIZE_CARRY_WEIGHT_TABLE[CreatureSize.gargantuan] * 2,
}

_CREATURE_SIZE_HEIGHT_TABLE = {
    # creature size to height range (ft)
    CreatureSize.tiny:          [0, 2.5],       # unbound lower value
    CreatureSize.small:         [2.5, 4.5],
    CreatureSize.medium:        [4.5, 7.5],
    CreatureSize.large:         [7.5, 12],
    CreatureSize.huge:          [12, 20],
    CreatureSize.gargantuan:    [20, None]      # unbound upper value
}

_CREATURE_SIZE_HIT_DICE_TABLE = {
    CreatureSize.tiny:          DieType.d4,
    CreatureSize.small:         DieType.d6,
    CreatureSize.medium:        DieType.d8,
    CreatureSize.large:         DieType.d10,
    CreatureSize.huge:          DieType.d12,
    CreatureSize.gargantuan:    DieType.d20
}

_CREATURE_SIZE_WEIGHT_TABLE = {
    # creature size to weight range (lbs)
    CreatureSize.tiny:          [0, 30],        # unbound lower value
    CreatureSize.small:         [30, 60],
    CreatureSize.medium:        [60, 250],
    CreatureSize.large:         [250, 1000],
    CreatureSize.huge:          [1000, 4000],
    CreatureSize.gargantuan:    [4000, None]    # unbound upper value
}

_DC_VALUE_TABLE = {
    "very_easy": 5,
    "easy": 10,
    "medium": 15,
    "hard": 20,
    "very_hard": 25,
    "nearly_impossible": 30
}

_FESTIVAL_MONTH_TABLE = {
    Month.sunsebb: FestivalWeek.needfest,
    Month.coldeven: FestivalWeek.growfest,
    Month.wealsun: FestivalWeek.richfest,
    Month.harvester: FestivalWeek.brewfest,
}

_LVL_PROF_BONUS_TABLE = {
    # lookup table for proficiency bonus for levels
    LevelAdvancement.level_1:   2,
    LevelAdvancement.level_2:   2,
    LevelAdvancement.level_3:   2,
    LevelAdvancement.level_4:   2,
    LevelAdvancement.level_5:   3,
    LevelAdvancement.level_6:   3,
    LevelAdvancement.level_7:   3,
    LevelAdvancement.level_8:   3,
    LevelAdvancement.level_9:   4,
    LevelAdvancement.level_10:  4,
    LevelAdvancement.level_11:  4,
    LevelAdvancement.level_12:  4,
    LevelAdvancement.level_13:  5,
    LevelAdvancement.level_14:  5,
    LevelAdvancement.level_15:  5,
    LevelAdvancement.level_16:  5,
    LevelAdvancement.level_17:  6,
    LevelAdvancement.level_18:  6,
    LevelAdvancement.level_19:  6,
    LevelAdvancement.level_20:  6
}

_LVL_XP_TABLE = {
    # lookup table for xp thresholds for levels
    LevelAdvancement.level_1:   0,
    LevelAdvancement.level_2:   300,
    LevelAdvancement.level_3:   900,
    LevelAdvancement.level_4:   2700,
    LevelAdvancement.level_5:   6500,
    LevelAdvancement.level_6:   14000,
    LevelAdvancement.level_7:   23000,
    LevelAdvancement.level_8:   34000,
    LevelAdvancement.level_9:   48000,
    LevelAdvancement.level_10:  64000,
    LevelAdvancement.level_11:  85000,
    LevelAdvancement.level_12:  100000,
    LevelAdvancement.level_13:  120000,
    LevelAdvancement.level_14:  140000,
    LevelAdvancement.level_15:  165000,
    LevelAdvancement.level_16:  195000,
    LevelAdvancement.level_17:  225000,
    LevelAdvancement.level_18:  265000,
    LevelAdvancement.level_19:  305000,
    LevelAdvancement.level_20:  355000
}

_MAGICAL_OFFERINGS_QTY_TABLE = {
    VendorMagicalItemOfferings.poor: [1, 2],
    VendorMagicalItemOfferings.humble: [2, 4],
    VendorMagicalItemOfferings.moderate: [4, 7],
    VendorMagicalItemOfferings.higher: [7, 10],
    VendorMagicalItemOfferings.highest: [10, 15]
}

_OBJECT_MATERIAL_AC_TABLE = {
    ObjectMaterialType.cloth: 11,
    ObjectMaterialType.paper: 11,
    ObjectMaterialType.rope: 11,
    ObjectMaterialType.crystal: 13,
    ObjectMaterialType.glass: 13,
    ObjectMaterialType.ice: 13,
    ObjectMaterialType.wood: 15,
    ObjectMaterialType.bone: 15,
    ObjectMaterialType.stone: 17,
    ObjectMaterialType.iron: 19,
    ObjectMaterialType.steel: 19,
    ObjectMaterialType.mithral: 21,
    ObjectMaterialType.adamantine: 23,
}

_OBJECT_SIZE_HP_TABLE = {
    ObjectSizeType.tiny: {"fragile": {
                    "flat": 2,
                    "rolled": "1d4"},
                "resilient": {
                    "flat": 5,
                    "rolled": "2d4"}},
    ObjectSizeType.small: {"fragile": {
                    "flat": 3,
                    "rolled": "1d6"},
                "resilient": {
                    "flat": 10,
                    "rolled": "3d6"}},
    ObjectSizeType.medium: {"fragile": {
                    "flat": 4,
                    "rolled": "1d8"},
                "resilient": {
                    "flat": 18,
                    "rolled": "4d8"}},
    ObjectSizeType.large: {"fragile": {
                    "flat": 5,
                    "rolled": "1d10"},
                "resilient": {
                    "flat": 27,
                    "rolled": "5d10"}}
}

_POST_FESTIVAL_MONTH_TABLE = {
    FestivalWeek.needfest: Month.fireseek,
    FestivalWeek.growfest: Month.planting,
    FestivalWeek.richfest: Month.reaping,
    FestivalWeek.brewfest: Month.patchwall,
}

_SKILL_TO_ABILITY_MAPPING = {
    SkillType["athletics"]:         AbilityType.str,
    SkillType["acrobatics"]:        AbilityType.dex,
    SkillType["sleight_of_hand"]:   AbilityType.dex,
    SkillType["stealth"]:           AbilityType.dex,
    SkillType["arcana"]:            AbilityType.int,
    SkillType["history"]:           AbilityType.int,
    SkillType["investigation"]:     AbilityType.int,
    SkillType["nature"]:            AbilityType.int,
    SkillType["religion"]:          AbilityType.int,
    SkillType["animal_handling"]:   AbilityType.wis,
    SkillType["insight"]:           AbilityType.wis,
    SkillType["medicine"]:          AbilityType.wis,
    SkillType["perception"]:        AbilityType.wis,
    SkillType["survival"]:          AbilityType.wis,
    SkillType["deception"]:         AbilityType.cha,
    SkillType["intimidation"]:      AbilityType.cha,
    SkillType["performance"]:       AbilityType.cha,
    SkillType["persuasion"]:        AbilityType.cha
}

_STARTING_ALIGNMENT_COORDINATES_TABLE = {
    AlignmentType.lg: (0.66, 0.66),
    AlignmentType.ng: (0.0, 0.66),
    AlignmentType.cg: (-0.66, 0.66),
    AlignmentType.ln: (0.66, 0.0),
    AlignmentType.nn: (0.0, 0.0),
    AlignmentType.cn: (-0.66, 0.0),
    AlignmentType.le: (0.66, -0.66),
    AlignmentType.ne: (0.0, -0.66),
    AlignmentType.ce: (-0.66, -0.66),
}

_WEALTH_TABLE = {
    WealthLevel.poor: "",
    WealthLevel.lower_class: "",
    WealthLevel.middle_class: "",
    WealthLevel.upper_class: "",
    WealthLevel.rich: ""
}

"""OPTIONAL RULES CONSTANTS"""
_STACK_MODIFIER_CAP = 3  # maximum modifier on stacked advantage/disadvantage D20Modifiers
