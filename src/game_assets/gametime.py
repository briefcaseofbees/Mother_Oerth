"""

"""

import enum


class TimeOfDay(enum.Enum):
    dead_of_night = {"label": "Dead of Night", "stealth_bonus": 2, "npc_activity": "asleep"}  # 12am - 3am
    twilight =      {"label": "Twilight", "stealth_bonus": 1, "npc_activity": "asleep"}  # 3am - 6am
    dawn =          {"label": "Dawn", "stealth_bonus": 1, "npc_activity": "waking"}  # 6am - 9am
    morning =       {"label": "Morning", "stealth_bonus": 0, "npc_activity": "active"}  # 9am - 12pm
    midday =        {"label": "Midday", "stealth_bonus": 0, "npc_activity": "active"}  # 12pm - 3pm
    afternoon =     {"label": "Afternoon", "stealth_bonus": 0, "npc_activity": "active"}  # 3pm - 6pm
    dusk =          {"label": "Dusk", "stealth_bonus": 1, "npc_activity": "winding_down"}  # 6pm - 9pm
    night =         {"label": "Night", "stealth_bonus": 2, "npc_activity": "minimal"}  # 9pm - 12am

    @property
    def label(self):
        return self.value["label"]


class DayOfWeek(enum.Enum):
    starday     = {"label": "Starday"}   # saturday
    sunday      = {"label": "Sunday"}    # sunday
    moonday     = {"label": "Moonday"}   # monday
    godsday     = {"label": "Godsday"}   # tuesday
    waterday    = {"label": "Waterday"}  # wednesday
    earthday    = {"label": "Earthday"}  # thursday
    freeday     = {"label": "Freeday"}   # friday

    @property
    def label(self):
        return self.value["label"]

    @property
    def next(self):
        members = list(DayOfWeek)
        current_index = members.index(self)
        next_member = members[(current_index + 1) % len(members)]
        return next_member


class Month(enum.Enum):
    fireseek    = {"label": "Fireseek"}  # january equivalent
    readying    = {"label": "Readying"}
    coldeven    = {"label": "Coldeven"}
    planting    = {"label": "Planting"}
    flocktime   = {"label": "Flocktime"}
    wealsun     = {"label": "Wealsun"}
    reaping     = {"label": "Reaping"}
    goodmonth   = {"label": "Goodmonth"}
    harvester   = {"label": "Harvester"}
    patchwall   = {"label": "Patchwall"}
    ready_reat  = {"label": "Ready'reat"}
    sunsebb     = {"label": "Sunsebb"}

    @property
    def label(self):
        return self.value["label"]

    @classmethod
    def index(cls, month_num):
        members = list(cls.__members__.values())
        return members[month_num - 1]

    def next(self):
        members = list(Month)
        current_index = members.index(self)
        next_member = members[(current_index + 1) % len(members)]
        return next_member


class FestivalDay(enum.Enum):
    day_1 = {"label": "Low Festival (Starday)"}
    day_2 = {"label": "Low Festival (Sunday)"}
    day_3 = {"label": "Low Festival (Moonday)"}
    day_4 = {"label": "Mid-Festival (Godsday)"}
    day_5 = {"label": "High Festival (Waterday)"}
    day_6 = {"label": "High Festival (Earthday)"}
    day_7 = {"label": "High Festival (Freeday)"}


class FestivalWeek(enum.Enum):
    needfest = 0  # Midwinter     (between Sunsebb and Fireseek)
    growfest = 1  # Spring        (between Coldeven and Planting)
    richfest = 2  # Midsummer     (between Wealsun and Reaping)
    brewfest = 3  # Harvest       (between Harvester and Patchwall)

    @property
    def label(self):
        festival_labels = ["Needfest", "Growfest", "Richfest", "Brewfest"]
        return festival_labels[self.value]


FESTIVAL_MONTHS = {
    Month.sunsebb: FestivalWeek.needfest,
    Month.coldeven: FestivalWeek.growfest,
    Month.wealsun: FestivalWeek.richfest,
    Month.harvester: FestivalWeek.brewfest,
}

POST_FESTIVAL_MONTHS = {
    FestivalWeek.needfest: Month.fireseek,
    FestivalWeek.growfest: Month.planting,
    FestivalWeek.richfest: Month.reaping,
    FestivalWeek.brewfest: Month.patchwall,
}


class GameTime:
    def __init__(self, year:int = 576, month:int = 1, day_num:int = 1, hour:int = 6, minute:int = 0):
        self.round      = 0
        self.minute     = minute
        self.hour       = hour  # running on the 24h clock 0 == 12am; 1 == 1am, etc.
        self.day_num    = day_num
        self.day_name   = DayOfWeek.starday
        self.month      = Month.index(month_num=month)
        self.festival   = None
        self.year       = year

    @property
    def in_festival(self):
        return self.festival is not None

    @property
    def time_of_day(self):
        periods = list(TimeOfDay)
        return periods[self.hour // 3]

    @property
    def day_of_week(self):
        periods = list(DayOfWeek)
        return periods[(self.day_num - 1) % 7]

    @property
    def formatted_time(self):
        return f"{self.hour:02d}:{self.minute:02d} ({self.time_of_day.label})"

    @property
    def formatted_date(self):
        return f"{self.year} | {self.month.label} | {self.day_num} ({self.day_of_week.label})" if self.month is not None else f"{self.year} | {self.festival.label} | {FestivalDay[f"day_{self.day_num}"].value["label"]}"

    def move_time_forward(self, time_to_increase:dict):
        # time should increase in the correct denomination (round, minute, etc.) and the correct amount

        affected_denomination = time_to_increase["denom"]  # find the string that corresponds to the denomination

        if affected_denomination == "round":
            self.round += time_to_increase["qty"]
        elif affected_denomination == "minute":
            self.minute += time_to_increase["qty"]
        elif affected_denomination == "hour":
            self.hour += time_to_increase["qty"]
        elif affected_denomination == "day":
            self.day_num += time_to_increase["qty"]
            self.day_name = self.day_name.next

        if self.round >= 10:
            self.round %= 10
            self.minute += 1

        if self.minute >= 60:
            self.minute %= 60
            self.hour += 1

        if self.hour >= 24:
            self.hour %= 24
            self.day_num += 1
            self.day_name = self.day_name.next

        if self.day_num > 7 and self.in_festival:  # move beyond festival back into months...
            if self.festival == FestivalWeek.needfest:
                self.year += 1
                self.month = Month.fireseek
            else:
                self.month = POST_FESTIVAL_MONTHS[self.festival]
            self.festival = None
            self.day_num = 1

        if self.day_num > 28:  # move beyond month (possibly into festival)
            if self.month in FESTIVAL_MONTHS:
                self.festival = FESTIVAL_MONTHS[self.month]
                self.month = None  # temporary state...
                self.day_num = 1
            else:
                self.month = self.month.next()
                self.day_num = 1
