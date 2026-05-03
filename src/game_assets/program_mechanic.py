"""

"""

import enum, asyncio


class Trigger(enum.Enum):
    """list of game logic triggers"""

    # COMBAT TRIGGERS
    on_attack_rolled = enum.auto()
    on_hit = enum.auto()
    on_miss = enum.auto()
    on_damage_dealt = enum.auto()
    on_damage_taken = enum.auto()
    on_critical_hit = enum.auto()
    on_kill = enum.auto()
    on_death_save = enum.auto()
    on_stabilize = enum.auto()
    on_spell_cast = enum.auto()
    on_spell_hit = enum.auto()
    on_concentration_broken = enum.auto()

    # TURN STRUCTURE
    on_turn_start = enum.auto()
    on_turn_end = enum.auto()
    on_round_start = enum.auto()
    on_round_end = enum.auto()
    on_initiative_rolled = enum.auto()

    # CHARACTER STATE
    on_heal = enum.auto()
    on_condition_applied = enum.auto()
    on_condition_removed = enum.auto()
    on_level_up = enum.auto()
    on_ability_score_change = enum.auto()
    on_temp_hp_gained = enum.auto()
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
    on_room_enter = enum.auto()
    on_room_exit = enum.auto()
    on_item_found = enum.auto()
    on_trap_triggered = enum.auto()
    on_door_opened = enum.auto()
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


class EventBus:  # TODO: figure out how this works, and what it'll be used for
    def __init__(self):
        self._listeners = {}

    def subscribe(self, event_type, callback):
        self._listeners.setdefault(event_type, []).append(callback)

    async def emit(self, event_type, data = None):
        callbacks = self._listeners.get(event_type, [])
        await asyncio.gather(*[callback(data) for callback in callbacks])
