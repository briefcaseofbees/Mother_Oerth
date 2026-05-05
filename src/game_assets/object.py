"""

"""

from .game_constants import ObjectMaterialType, ObjectSizeType


class ObjectInstance:
    def __init__(self, object_name:str, object_size:ObjectSizeType, object_material:ObjectMaterialType):
        # object stats
        self.hp = None
        self.ac = object_material.ac
        self.destructible = True  # is the object able to be destroyed? (default: yes)

        # object metadata
        self.name = object_name
        self.material = object_material.label

    def __repr__(self):
        return f"{self.name}: {self.hp}; ac: {self.ac}, material: {self.material}"
