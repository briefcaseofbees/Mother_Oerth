"""

"""

_CLASSES_FILENAME = "./resources/classes.json"

import enum, json
from .ability import Ability
from .dice import DieType
from .item import WeaponType, ArmorType, ToolProficiency


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


class CreatureClass:
    def __init__(self, class_type: ClassType):
        self.type = class_type
        self.hit_dice = class_type.hit_dice
        self.desc = None
        self.hit_dice_pool_qty = None
        self.proficiency_bonus = None
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
        self.concentrating = False  # whether class is concentrating on a spell currently

    def extract_data(self):

        # open the json file and load the dictionary with all the class entries
        with open(_CLASSES_FILENAME) as classes_file:
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
        self.saving_throws = [Ability[saving_throw_attribute] for saving_throw_attribute in corresponding_class["saving_throw_profs"]]
        self.weapon_proficiencies = [WeaponType[weapon_type] for weapon_type in corresponding_class["weapon_profs"]]
        self.armor_proficiencies = [ArmorType[armor_type] for armor_type in corresponding_class["armor_profs"]]
        self.tool_proficiencies = [ToolProficiency[tool_type] for tool_type in corresponding_class["tool_profs"]]


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




