"""

"""
from .program_mechanic import extract_data
from .game_constants import _SPELLS_JSON_FILE_PATH


class Spell:
    def __init__(self, spell_name:str):
        self.spell_id = None
        self.name = None
        self.spell_level = None
        self.casting_time = None
        self.duration = None
        self.range = None
        self.components = None          # material/verbal components
        self.description = None         # string describing spell
        self.effects = None             # specific effects tied to spell target
        self.damage = None
        self.magic_school = None
        self.spell_list = None          # which classes can use it
        self.higher_level_cast = None   # what happens when cast at higher level

        self.populate_object(spell_name)

    def populate_object(self, spell_name:str):

        spell_dict = extract_data(_SPELLS_JSON_FILE_PATH)

        relevant_entry = None

        for entry in spell_dict:
            if entry['name'] == spell_name:
                relevant_entry = entry

        if relevant_entry is None:
            print(f"Spell {spell_name} not found in JSON file")
        else:
            print(f"Spell {spell_name} found in JSON file")


class SpellBook:
    def __init__(self):
        """
        Wizard-specific item, has a few functionalities that are worth dividing into its own class
        """
        self.contained_spells = []

    def copy_scroll(self, scroll_item):
        # check if scroll item contains a spell of level 1 or above (qualifying)
        # check if wizard level is equal to, or greater than what is on scroll item
        # check how long it will take for the spell to be copied over (2h/lvl of scroll item)
        # check how much it will cost for the spell to be copied over (50GP/lvl of scroll item)
        pass

    def copy_book(self, book_item):
        # check if book item is an empty book (unassigned to something else)
        # check if spell being copied over exists in the first book
        # check how long it will take for the spell to be copied over (1h/lvl of known-spell)
        # check how much it will cost for the spell to be copied over (10GP/lvl of known-spell)
        pass


class SpellList:
    def __init__(self):
        self.spellbook = None       # specific to Wizards
        self.prepared_spells = []   #
