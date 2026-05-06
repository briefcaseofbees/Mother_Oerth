"""

"""

import json
from .game_constants import AbilityType, ClassType, _CLASSES_JSON_FILE_PATH, WeaponType, ArmorType, ToolProficiencyType


class CreatureClass:
    def __init__(self, class_type: ClassType):
        self.type = class_type
        self.name = self.type.label
        self.class_level = 1
        self.hit_dice = self.type.hit_dice  # number of hit dice corresponds to levels taken in class
        self.desc = None
        self.armor_proficiencies = None
        self.weapon_proficiencies = None
        self.tool_proficiencies = None
        self.starting_tools = None
        self.saving_throws = None
        self.starting_skills = None
        self.class_features = None
        self.subclass = None

        # Spellcaster-specific
        self.spell_save_DC = None  # if applicable
        self.spells_known = []
        self.prepared_spells = []   # subset of known spells
        self.spellcasting_ability = None

    def populate_object(self):

        # open the json file and load the dictionary with all the class entries
        with open(_CLASSES_JSON_FILE_PATH) as classes_file:
            classes_dict = json.load(classes_file)

        corresponding_class = None

        # of all the class entries in the class dictionary, we need to pinpoint the correct one
        for class_entry in classes_dict:
            if class_entry["name"] == self.type.name:  # entry key "name" is encoded with the same name as ClassType
                corresponding_class = class_entry

        if corresponding_class is None:
            print(f"A corresponding class matching with {self.type.label} was not found!")
            print("Exiting...")
            return  # should throw an error

        self.desc = corresponding_class["desc"]
        self.saving_throws = [AbilityType[saving_throw_attribute] for saving_throw_attribute in corresponding_class["saving_throw_profs"]]
        self.weapon_proficiencies = [WeaponType[weapon_type] for weapon_type in corresponding_class["weapon_profs"]]
        self.armor_proficiencies = [ArmorType[armor_type] for armor_type in corresponding_class["armor_profs"]]
        self.tool_proficiencies = [ToolProficiencyType[tool_type] for tool_type in corresponding_class["tool_profs"]]