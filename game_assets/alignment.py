"""

"""

from .game_constants import AlignmentType, _STARTING_ALIGNMENT_COORDINATES_TABLE


class KarmicState:
    def __init__(self, starting_alignment:AlignmentType):
        """
        KarmicState is a unique game construct that is not present in the SRD, it seeks to solve the issues surrounding
        alignment in D&D. Firstly, it turns the normally rigid and discrete alignment system into a spectrum/range that
        has coordinates in the canon alignment system. Second, it implements "inertia" which is a concept by which actions
        that alter a character's alignment (e.g. a neutral character doing a morally "good" act) can be magnified or
        made smaller by nature of previous karmic actions.

        For example, a purely "Good" character that has a long history of good actions will not instantly swap to a
        "neutral" or "evil" alignment by one bad deed alone, but rather the distance by which the bad action will shift
        the normally good character towards neutrality/evil will be weighed against the inertia that has been gained
        through the history of the character's good actions.

        This has two benefits:
        1. Character arcs of a long-standing evil character becoming good, or vice versa will be made longer/meaningful.
        2. No longer will alignment swapping be instantaneous and undeserved, a "Good" character will not be punished
        for a lapse in judgement when they've had history of do-good behaviour.

        :param starting_alignment: AlignmentType
        """
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

        return AlignmentType.nn  # returns true neutral as a default, but this should probably be fixed to throw an error

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