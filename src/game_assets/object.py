"""

"""

import enum
from .dice import DieType, DiceRoll


class DamageThreshold(enum.Enum):
    # TODO: find more official documentation on how damage thresholds work in dnd 5e

    indestructible = -1     # can never be destroyed
    none = 0                # can be destroyed with repeated light attacks
    light = 5
    medium = 10
    heavy = 20
    impenetrable = 30


class ObjectSize(enum.Enum):
    tiny        = {"label": "tiny"}
    small       = {"label": "small"}
    medium      = {"label": "medium"}
    large       = {"label": "large"}

    @property
    def label(self):
        return self.value["label"]


class ObjectMaterial(enum.Enum):
    cloth =         {"label": "Cloth",      "ac": 11}
    paper =         {"label": "Paper",      "ac": 11}
    rope =          {"label": "Rope",       "ac": 11}
    crystal =       {"label": "Crystal",    "ac": 13}
    glass =         {"label": "Glass",      "ac": 13}
    ice =           {"label": "Ice",        "ac": 13}
    wood =          {"label": "Wood",       "ac": 15}
    bone =          {"label": "Bone",       "ac": 15}
    stone =         {"label": "Stone",      "ac": 17}
    iron =          {"label": "Iron",       "ac": 19}
    steel =         {"label": "Steel",      "ac": 19}
    mithral =       {"label": "Mithral",    "ac": 21}
    adamantine =    {"label": "Adamantine", "ac": 23}

    @property
    def label(self):
        return self.value["label"]

    @property
    def ac(self):
        return self.value["ac"]


class ObjectHP(enum.Enum):
    tiny = {    "fragile": {
                    "flat": 2,
                    "rolled": DiceRoll(DieType.d4,1)},
                "resilient": {
                    "flat": 5,
                    "rolled": DiceRoll(DieType.d4, 2)}}

    small = {   "fragile": {
                    "flat": 3,
                    "rolled": DiceRoll(DieType.d6,1)},
                "resilient": {
                    "flat": 10,
                    "rolled": DiceRoll(DieType.d6, 3)}}

    medium = {  "fragile": {
                    "flat": 4,
                    "rolled": DiceRoll(DieType.d8, 1)},
                "resilient": {
                    "flat": 18,
                    "rolled": DiceRoll(DieType.d8,4)}}

    large = {   "fragile": {
                    "flat": 5,
                    "rolled": DiceRoll(DieType.d10,1)},
                "resilient": {
                    "flat": 27,
                    "rolled": DiceRoll(DieType.d10,5)}}

    @classmethod
    def get_hp(cls, object_size:ObjectSize, object_fragility, flat:bool) -> int:
        """

        :param object_size: ObjectSize
        :param object_fragility: "fragile" or "resilient"
        :param flat: flat calculation or rolled
        :return: integer value of health of object
        """
        if flat:
            return cls[object_size.label].value[object_fragility]["flat"]
        else:
            return cls[object_size.label].value[object_fragility]["rolled"].roll()


class ObjectInstance:
    def __init__(self, object_name:str, object_size:ObjectSize, object_material:ObjectMaterial):
        # object stats
        self.hp = ObjectHP.get_hp(object_size, "resilient", False)
        self.ac = object_material.ac
        self.destructible = True  # is the object able to be destroyed? (default: yes)

        # object metadata
        self.name = object_name
        self.material = object_material.label

    def __repr__(self):
        return f"{self.name}: {self.hp}; ac: {self.ac}, material: {self.material}"
