"""

"""

import json
from .dice import Dice
from .economy import CoinPurse
from .game_constants import AmmoType, ArmorType, DamageType, DieType, _ITEMS_JSON_FILE_PATH, WeaponMasteryType, WeaponPropertyType
from .program_mechanic import extract_data

class Weapon:
    def __init__(self, weapon_name:str):
        # attribute initialization
        self.name = None
        self.type = None
        self.range = []  # will have an effective range, and a maximum range
        self.ammo_type = None
        self.dmg = Dice
        self.dmg_type = None
        self.properties = []
        self.mastery = None
        self.weight = None
        self.cost = None

        self.populate_object(weapon_name)  # pull data from provided dictionary (from JSON file)

    def populate_object(self, weapon_name:str):

        weapon_dict = extract_data(_ITEMS_JSON_FILE_PATH)

        relevant_entry = None

        for entry in weapon_dict:
            if entry["name"] == weapon_name:
                relevant_entry = entry

        if relevant_entry is None:
            print(f"Weapon {weapon_name} not found in JSON file")
        else:
            print(f"Weapon {weapon_name} found in JSON file")

            self.name = relevant_entry["name"]
            self.type = relevant_entry["type"]  # list: ["simple"/"martial", "melee"/"ranged"]

            # pull damage type, damage dice count, and damage type
            damage_dice = relevant_entry["dmg"]["die"]  # will be in form "(qty)(die_type)" (as a single sting)
            qty = int(damage_dice[0])
            die_type = DieType[damage_dice[1:]]

            # check if weapon is strictly two_handed
            is_two_handed = "two_handed" in relevant_entry["properties"]

            if is_two_handed:
                self.dmg = {
                    "one_handed": None,  # will remain blank
                    "two_handed": Dice(die_type, qty),
                }
            else:
                self.dmg = {
                    "one_handed": Dice(die_type, qty),
                    "two_handed": None  # populated if "versatile" tag exists
                }

            self.dmg_type = DamageType[relevant_entry["dmg"]["type"]]

            self.mastery = WeaponMasteryType[relevant_entry["mastery"]]
            self.weight = relevant_entry["weight"]

            self.cost = CoinPurse.parse(relevant_entry["cost"])

            # strip properties from dict
            for prop in relevant_entry["properties"]:

                prop_str = prop.split(" ")  # properties with multiple parts will be space-separated
                self.properties.append(WeaponPropertyType[prop_str[0]])  # add the first part of the (potentially) multipart prop

                if len(prop_str) > 1:
                    if prop_str[0] == "versatile":  # prop_str[1] will be in form "versatile (1d8)" - strip the parens

                        # strip brackets from second item, and pull details from resultant string
                        two_handed_dice = prop_str[1].strip("()")
                        qty_2h = int(two_handed_dice[0])
                        die_2h = DieType[two_handed_dice[1:]]

                        self.dmg["two_handed"] = Dice(die=die_2h, qty=qty_2h)

                    elif prop_str[0] == "thrown":
                        self.range.append(prop_str[1].strip("()").split("/"))  # pull ranges from second item in property

                    elif prop_str[0] == "ammunition":  # prop_str[1] will have ranges, but prop_str[2] will have ammo type
                        self.range.append(prop_str[1].strip("()").split("/"))  # pull ranges from second item in property
                        self.ammo_type = AmmoType[prop_str[2].strip("()")]  # pull ammo type from third item in property


class Armor:
    def __init__(self, armor_name:str):
        self.name = None
        self.type = None
        self.ac = {"num": None, "dex_mod": False, "max_dex_mod": 0}
        self.str_req = 0
        self.stealth_disadvantage = False
        self.weight = None
        self.cost = CoinPurse()

        self.populate_object(armor_name)

    def populate_object(self, armor_name:str):

        armor_dict = extract_data(_ITEMS_JSON_FILE_PATH)

        relevant_entry = None

        for entry in armor_dict:
            if entry["name"] == armor_name:
                relevant_entry = entry

        if relevant_entry is None:
            print(f"Armor {armor_name} not found in JSON file")
        else:
            print(f"Armor {armor_name} found in JSON file")

            self.name = relevant_entry["name"]
            self.type = ArmorType[relevant_entry["type"]]
            self.ac["num"] = relevant_entry["ac"]["num"]
            self.ac["dex_mod"] = relevant_entry["ac"]["dex_mod"]
            self.ac["max_dex_mod"] = relevant_entry["ac"]["max_dex"]
            self.str_req = relevant_entry["str_req"]
            self.stealth_disadvantage = relevant_entry["stealth_disadvantage"]
            self.weight = relevant_entry["weight"]
            self.cost.parse(cost_string=relevant_entry["cost"])


class AdventuringTool:
    def __init__(self, adventuring_tool_name:str):
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

        self.populate_object(adventuring_tool_name)

    def populate_object(self, adventuring_tool_name:str):
        adventuring_tool_dict = extract_data(_ITEMS_JSON_FILE_PATH)

        relevant_entry = None
        for entry in adventuring_tool_dict:
            if entry["name"] == adventuring_tool_name:
                relevant_entry = entry

        if relevant_entry is None:
            print(f"Adventuring tool {adventuring_tool_name} not found in JSON file")
        else:
            print(f"Adventuring tool {adventuring_tool_name} found in JSON file")