"""

"""

from .game_constants import AlignmentType, _STARTING_ALIGNMENT_COORDINATES_TABLE


class KarmicState:
    def __init__(self, starting_alignment:AlignmentType):
        self.good_evil = 0.0  # range: [-1, 1] (evil, good)
        self.law_chaos = 0.0  # range: [-1, 1] (chaotic, lawful)
        self.good_evil_inertia = 0.0  # 0.0 to 1.0 - resistance to change in good/evil
        self.law_chaos_inertia = 0.0  # 0.0 to 1.0 - resistance to change in law/chaos

        self._initialize_alignment(starting_alignment)

    @property
    def alignment(self) -> AlignmentType:
        # x (CHAOTIC/LAWFUL)
        if -1 <= self.law_chaos < -0.33:
            x = "Chaotic"
        elif -0.33 <= self.law_chaos < 0.33:
            x = "Neutral"
        else:
            x = "Lawful"

        # y (EVIL/GOOD)

        if -1 <= self.good_evil < -0.33:
            y = "Evil"
        elif -0.33 <= self.good_evil < 0.33:
            y = "Neutral"
        else:
            y = "Good"

        if x == y:
            x = "True"  # catching true neutral edge case

        alignment_label = f"{x} {y}"
        alignment_members = list(AlignmentType)

        for member in alignment_members:
            if member.label == alignment_label:
                return member
        return None

    @property
    def karmic_coords(self):
        return self.law_chaos, self.good_evil

    def _initialize_alignment(self, alignment:AlignmentType):
        self.law_chaos, self.good_evil = _STARTING_ALIGNMENT_COORDINATES_TABLE[alignment]

    def apply_karmic_delta(self, good_evil_delta: float, law_chaos_delta: float):
        if good_evil_delta * self.good_evil < 0:  # opposite good/evil action to current good/evil leanings (resist)
            good_evil_delta *= (1 - self.good_evil_inertia)
        if law_chaos_delta * self.law_chaos < 0:  # opposite law/chaos action to current law/chaos leanings (resist)
            law_chaos_delta *= (1 - self.law_chaos_inertia)

        # apply changes to good/evil and law/chaos values
        self.good_evil = max(-1.0, min(1.0, self.good_evil + good_evil_delta))
        self.law_chaos = max(-1.0, min(1.0, self.law_chaos + law_chaos_delta))

        # build inertia for good/evil and law/chaos if leaning in any direction is strong enough
        if abs(self.good_evil) > 0.7:
            self.good_evil_inertia = min(1.0, self.good_evil_inertia + 0.01)
        if abs(self.law_chaos) > 0.7:
            self.law_chaos_inertia = min(1.0, self.law_chaos_inertia + 0.01)

        # decay inertia for good/evil and law/chaos if lean is not extreme
        if abs(self.good_evil) < 0.7:
            self.good_evil_inertia = min(0.0, self.good_evil_inertia - 0.005)
        if abs(self.law_chaos) < 0.7:
            self.law_chaos_inertia = min(0.0, self.law_chaos_inertia - 0.005)