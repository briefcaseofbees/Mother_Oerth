"""

"""

import enum
from .dice import DiceRoll, DieType
from .combat import DamageType


class CoinValue(enum.Enum):  # all in copper coin values
    cp = {"label": "Copper Piece(s)",       "value": 1}
    sp = {"label": "Silver Pieces(s)",      "value": 10}
    ep = {"label": "Electrum Piece(s)",     "value": 50}
    gp = {"label": "Gold Piece(s)",         "value": 100}
    pp = {"label": "Platinum Piece(s)",     "value": 1000}

    @classmethod
    def parse(cls, cost_string):
        amount, denomination = cost_string.split(" ")
        return int(amount) * cls[denomination.lower()].value["value"]

    @classmethod
    def to_coins(cls, copper_total):
        result = {}
        remaining = copper_total
        for coin in sorted(cls, key=lambda x: x.value["value"], reverse=True):
            if remaining >= coin.value["value"]:
                result[coin.name] = remaining // coin.value["value"]
                remaining %= coin.value["value"]

        return result


class MagicalItemRarity(enum.Enum):
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


class ArmorType(enum.Enum):
    clothing    = {"label": "Clothing"}
    light       = {"label": "Light"}
    medium      = {"label": "Medium"}
    heavy       = {"label": "Heavy"}
    shield      = {"label": "Shield"}


class ArmorSlot(enum.Enum):  # the slots that (specifically) equipped items can occupy
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


class MasteryProperty(enum.Enum):
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


class WeaponType(enum.Enum):
    simple      = {"label": "Simple"}
    martial     = {"label": "Martial"}
    exotic      = {"label": "Exotic"}
    melee       = {"label": "Melee"}
    ranged      = {"label": "Ranged"}

    @property
    def label(self):
        return self.value["label"]


class WeaponProperties(enum.Enum):
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


class AmmoType(enum.Enum):
    arrow           = {"label": "Arrow"}
    bolt            = {"label": "Bolt"}
    bullet_sling    = {"label": "Bullet (Sling)"}
    bullet_firearm  = {"label": "Bullet (Firearm)"}
    needle          = {"label": "Needle"}

    @property
    def label(self):
        return self.value["label"]


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


class ToolProficiency(enum.Enum):
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


class GamingSetType(enum.Enum):
    dice                = {"label": "Dice"}
    dragonchess         = {"label": "Dragonchess"}
    playing_cards       = {"label": "Playing Cards"}
    threedragon_ante    = {"label": "Three-Dragon Ante"}

    @property
    def label(self):
        return self.value["label"]


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