import enum
from .dice import DiceRoll, DieType
from .combat import DamageType


class CoinValue(enum.Enum):  # all in copper coin values
    cp = 1
    sp = 10
    ep = 50
    gp = 100
    pp = 1000

    @classmethod
    def parse(cls, cost_string):
        amount, denomination = cost_string.split(" ")
        return int(amount) * cls[denomination.lower()].value

    @classmethod
    def to_coins(cls, copper_total):
        result = {}
        remaining = copper_total
        for coin in sorted(cls, key=lambda x: x.value, reverse=True):
            if remaining >= coin.value:
                result[coin.name] = remaining // coin.value
                remaining %= coin.value

        return result


class MagicalItemRarity(enum.Enum):
    mundane = -1    # non-magical items
    common = 0      # basic magical items
    uncommon = 1    # items with moderate magical effects
    rare = 2        # powerful items with significant effects
    very_rare = 3   # exceptional items with strong magical abilities
    legendary = 4   # unique items with extraordinary powers
    artifact = 5    # singular, world altering items with immense power


class ArmorType(enum.Enum):
    clothing = -1  # non-armor type
    light = 0
    medium = 1
    heavy = 2
    shield = 3


class ArmorSlot(enum.Enum):  # the slots that (specifically) equipped items can occupy
    # generally following the BG3 conventions, but adding additional slots as per the SRD

    # TODO: will likely need to go through all items/weapons/armor/etc. and add the necessary tags

    headwear = 0
    armor = 1
    cloak = 2
    amulet = 3
    ring = 4  # two rings, as with the BG3 system
    shield = 5
    main_hand = 6  # bear in mind that some equipment has the versatile property, will need to account for that
    musical_instrument = 7
    light_source = 8
    handwear = 9
    footwear = 10
    clothing = 11
    eyes = 12
    wrists = 13
    mantle = 14
    off_hand = 15


class MasteryProperty(enum.Enum):
    cleave = 0
    graze = 1
    nick = 2
    push = 3
    sap = 4
    slow = 5
    topple = 6
    vex = 7


class WeaponType(enum.Enum):
    simple = 0
    martial = 1
    exotic = 2
    melee = 3
    ranged = 4


class WeaponProperties(enum.Enum):
    ammunition = 0
    finesse = 1
    heavy = 2
    light = 3
    loading = 4
    range = 5
    reach = 6
    thrown = 7
    two_handed = 8
    versatile = 9
    special = 10
    silvered = 11


class AmmoType(enum.Enum):
    arrow = 0
    bolt = 1
    bullet_sling = 2
    bullet_firearm = 3
    needle = 4


# TODO: need to deal with magical weapons and armour... how? unsure yet


class Weapon:
    def __init__(self, weapon_dict:dict):
        # attribute initialization
        self.name = None
        self.type = None
        self.range = []  # will have an effective range, and a maximum range
        self.ammo_type = None
        self.dmg = None  # unsure how to deal with versatile equipment
        self.dmg_type = None
        self.properties = []
        self.mastery = None
        self.weight = None
        self.cost = None

        self.extract_data(weapon_dict)  # pull data from provided dictionary (from JSON file)

    def extract_data(self, weapon_dict:dict):
        self.name = weapon_dict["name"]
        self.type = weapon_dict["type"]  # list: ["simple"/"martial", "melee"/"ranged"]

        # pull damage type, damage dice count, and damage type
        damage_dice = weapon_dict["dmg"]["die"]  # will be in form "(qty)(die_type)" (as a single sting)
        qty = int(damage_dice[0])
        die_type = DieType[damage_dice[1:]]

        # check if weapon is strictly two_handed
        is_two_handed = "two_handed" in weapon_dict["properties"]

        if is_two_handed:
            self.dmg = {
                "one_handed": None,  # will remain blank
                "two_handed": DiceRoll(die_type, qty),
            }
        else:
            self.dmg = {
                "one_handed": DiceRoll(die_type, qty),
                "two_handed": None  # populated if "versatile" tag exists
            }

        self.dmg_type = DamageType[weapon_dict["dmg"]["type"]]

        self.mastery = MasteryProperty[weapon_dict["mastery"]]
        self.weight = weapon_dict["weight"]

        self.cost = CoinValue.parse(weapon_dict["cost"])

        # strip properties from dict
        for prop in weapon_dict["properties"]:

            prop_str = prop.split(" ")  # properties with multiple parts will be space-separated
            self.properties.append(WeaponProperties[prop_str[0]])  # add the first part of the (potentially) multipart prop

            if len(prop_str) > 1:
                if prop_str[0] == "versatile":  # prop_str[1] will be in form "versatile (1d8)" - strip the parens

                    # strip brackets from second item, and pull details from resultant string
                    two_handed_dice = prop_str[1].strip("()")
                    qty_2h = int(two_handed_dice[0])
                    die_2h = DieType[two_handed_dice[1:]]

                    self.dmg["two_handed"] = DiceRoll(die=die_2h, qty=qty_2h)

                elif prop_str[0] == "thrown":
                    self.range.append(prop_str[1].strip("()").split("/"))  # pull ranges from second item in property

                elif prop_str[0] == "ammunition":  # prop_str[1] will have ranges, but prop_str[2] will have ammo type
                    self.range.append(prop_str[1].strip("()").split("/"))  # pull ranges from second item in property
                    self.ammo_type = AmmoType[prop_str[2].strip("()")]  # pull ammo type from third item in property


"""# DEBUGGING THE WEAPON CLASS
weapon_json_file = json.load(open("resources/weapons.json"))

weapon_collection = []

for item in weapon_json_file:
    weapon_collection.append(Weapon(item))

for weapon in weapon_collection:
    if weapon.dmg["two_handed"]:
        print(f"{weapon.name} did {weapon.dmg['two_handed'].roll()} damage!")"""


class Armour:
    def __init__(self, armor_dict:dict):
        self.name = None
        self.type = None
        self.ac = {"num": None, "dex_mod": False, "max_dex_mod": 0}
        self.str_req = 0
        self.stealth_disadvantage = False
        self.weight = None
        self.cost = None

        # TODO: add don/duff time (when appropriate)

        self.extract_data(armor_dict)

    def extract_data(self, armor_dict:dict):
        self.name = armor_dict["name"]
        self.type = ArmorType[armor_dict["type"]]
        self.ac["num"] = armor_dict["ac"]["num"]
        self.ac["dex_mod"] = armor_dict["ac"]["dex_mod"]
        self.ac["max_dex_mod"] = armor_dict["ac"]["max_dex"]
        self.str_req = armor_dict["str_req"]
        self.stealth_disadvantage = armor_dict["stealth_disadvantage"]
        self.weight = armor_dict["weight"]
        self.cost = CoinValue.parse(armor_dict["cost"])


"""# DEBUGGING THE ARMOUR CLASS
armor_json_file = json.load(open("armours.json"))

armour_collection = []

for item in armor_json_file:
    armour_collection.append(Armour(item))

for armour in armour_collection:
    print(armour.__dict__)
"""


class AdventuringTool:
    def __init__(self):
        self.item_id = None
        self.name = None
        self.cost = None
        self.description = None
        self.effects = None
        self.damage = None
        self.weight = None
        self.properties = None
        self.type = None
        self.rarity = None

    def extract_data(self, adventuring_tool_dict:dict):
        pass