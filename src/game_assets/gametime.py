"""

"""

from .game_constants import DayOfWeek, Month, TimeOfDay, FestivalDay, FestivalWeek, _FESTIVAL_MONTH_TABLE, _POST_FESTIVAL_MONTH_TABLE


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
                self.month = _POST_FESTIVAL_MONTH_TABLE[self.festival]
            self.festival = None
            self.day_num = 1

        if self.day_num > 28:  # move beyond month (possibly into festival)
            if self.month in _FESTIVAL_MONTH_TABLE:
                self.festival = _FESTIVAL_MONTH_TABLE[self.month]
                self.month = None  # temporary state...
                self.day_num = 1
            else:
                self.month = self.month.next()
                self.day_num = 1