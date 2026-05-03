import enum


class LevelAdvancement(enum.Enum):
    level_1     = enum.auto()
    level_2     = enum.auto()
    level_3     = enum.auto()
    level_4     = enum.auto()
    level_5     = enum.auto()
    level_6     = enum.auto()
    level_7     = enum.auto()
    level_8     = enum.auto()
    level_9     = enum.auto()
    level_10    = enum.auto()
    level_11    = enum.auto()
    level_12    = enum.auto()
    level_13    = enum.auto()
    level_14    = enum.auto()
    level_15    = enum.auto()
    level_16    = enum.auto()
    level_17    = enum.auto()
    level_18    = enum.auto()
    level_19    = enum.auto()
    level_20    = enum.auto()

    @property
    def number(self):
        return self.name.split("_")[1]

    @property
    def required_xp(self):
        return _LVL_XP_TABLE[self]

    @property
    def prof_bonus(self):
        return _LVL_PROF_BONUS_TABLE[self]

_LVL_XP_TABLE = {
    # lookup table for xp thresholds for levels
    LevelAdvancement.level_1:   0,
    LevelAdvancement.level_2:   300,
    LevelAdvancement.level_3:   900,
    LevelAdvancement.level_4:   2700,
    LevelAdvancement.level_5:   6500,
    LevelAdvancement.level_6:   14000,
    LevelAdvancement.level_7:   23000,
    LevelAdvancement.level_8:   34000,
    LevelAdvancement.level_9:   48000,
    LevelAdvancement.level_10:  64000,
    LevelAdvancement.level_11:  85000,
    LevelAdvancement.level_12:  100000,
    LevelAdvancement.level_13:  120000,
    LevelAdvancement.level_14:  140000,
    LevelAdvancement.level_15:  165000,
    LevelAdvancement.level_16:  195000,
    LevelAdvancement.level_17:  225000,
    LevelAdvancement.level_18:  265000,
    LevelAdvancement.level_19:  305000,
    LevelAdvancement.level_20:  355000
}

_LVL_PROF_BONUS_TABLE = {
    # lookup table for proficiency bonus for levels
    LevelAdvancement.level_1:   2,
    LevelAdvancement.level_2:   2,
    LevelAdvancement.level_3:   2,
    LevelAdvancement.level_4:   2,
    LevelAdvancement.level_5:   3,
    LevelAdvancement.level_6:   3,
    LevelAdvancement.level_7:   3,
    LevelAdvancement.level_8:   3,
    LevelAdvancement.level_9:   4,
    LevelAdvancement.level_10:  4,
    LevelAdvancement.level_11:  4,
    LevelAdvancement.level_12:  4,
    LevelAdvancement.level_13:  5,
    LevelAdvancement.level_14:  5,
    LevelAdvancement.level_15:  5,
    LevelAdvancement.level_16:  5,
    LevelAdvancement.level_17:  6,
    LevelAdvancement.level_18:  6,
    LevelAdvancement.level_19:  6,
    LevelAdvancement.level_20:  6
}

_CR_XP_TABLE = {
    # lookup table for xp-gain by creature challenge rating
    "0": None,
    "1/8": 25,
    "1/4": 50,
    "1/2": 100,
    "1": 200,
    "2": 450,
    "3": 700,
    "4": 1100,
    "5": 1800,
    "6": 2300,
    "7": 2900,
    "8": 3900,
    "9": 5000,
    "10": 5900,
    "11": 7200,
    "12": 8400,
    "13": 10000,
    "14": 11500,
    "15": 13000,
    "16": 15000,
    "17": 18000,
    "18": 20000,
    "19": 22000,
    "20": 25000,
    "21": 33000,
    "22": 41000,
    "23": 50000,
    "24": 62000,
    "25": 75000,
    "26": 90000,
    "27": 105000,
    "28": 120000,
    "29": 135000,
    "30": 155000,
}

_CR_PROF_BONUS_TABLE = {
    "0":    2,
    "1/8":  2,
    "1/4":  2,
    "1/2":  2,
    "1":    2,
    "2":    2,
    "3":    2,
    "4":    2,
    "5":    3,
    "6":    3,
    "7":    3,
    "8":    3,
    "9":    4,
    "10":   4,
    "11":   4,
    "12":   4,
    "13":   5,
    "14":   5,
    "15":   5,
    "16":   5,
    "17":   6,
    "18":   6,
    "19":   6,
    "20":   6,
    "21":   7,
    "22":   7,
    "23":   7,
    "24":   7,
    "25":   8,
    "26":   8,
    "27":   8,
    "28":   8,
    "29":   9,
    "30":   9
}
