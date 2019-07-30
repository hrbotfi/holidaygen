import datetime
import os
from collections import namedtuple
from typing import Dict, Iterable, Optional, Set

from dateutil.easter import easter
from dateutil.relativedelta import relativedelta
from yaml import safe_load

COUNTRIES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "countries")


def get_available_country_files() -> Dict[str, str]:
    """
    Retrieve a mapping of ISO3166-2 country code to YAML path
    for all country files available.
    """
    available_country_files = {}

    for file in os.listdir(COUNTRIES_DIR):
        if file.endswith(".yml"):
            available_country_files[str(file).split(".")[0]] = os.path.join(
                COUNTRIES_DIR, file
            )

    return available_country_files


class Holiday:
    def __init__(self, data: dict) -> None:
        self.data = data.copy()

    @classmethod
    def from_file(cls, filename: str) -> "Holiday":
        with open(filename, "r") as f:
            data = safe_load(f)
        return cls(data=data)

    @classmethod
    def for_country(cls, country: str) -> "Holiday":
        filename = os.path.join(COUNTRIES_DIR, "{}.yml".format(country))
        return cls.from_file(filename)

    def get_holidays(self, year: int) -> Iterable["BoundDay"]:
        for day in self.data["days"]:
            yield Day(day).bind(year)

    @property
    def names(self) -> Dict[str, str]:
        return self.data["names"].copy()

    @property
    def alpha2_country_code(self) -> str:
        return self.data["countrycode-alpha2"]

    @property
    def alpha3_country_code(self) -> str:
        return self.data["countrycode-alpha3"]

    @property
    def numeric_country_code(self) -> str:
        return self.data["countrycode-numeric"]


SPECIAL_DAYS = {
    "easter": lambda year: easter(year),
    "midsummer": lambda year: datetime.date(year, 6, 19),
    "allsaints": lambda year: datetime.date(year, 10, 31),
}


class Day:
    """
    A specification for a special day.
    """

    def __init__(self, data):
        self.data = data

    def get_name(self, locale="en") -> Optional[str]:
        return self.names.get(locale)

    @property
    def names(self) -> Dict[str, str]:
        return self.data.get("names", {})

    @property
    def tags(self) -> Set[str]:
        return set(self.data.get("tags", ()))

    def bind(self, year: int) -> "BoundDay":
        day = self.data
        if "date" in day:
            date = datetime.date(
                year, int(day["date"]["month"]), int(day["date"]["day"])
            )
        elif "special-date" in day:
            special_date = day["special-date"]
            date = SPECIAL_DAYS[special_date["type"]](year)
            days_diff = special_date.get("days-difference")
            if days_diff:
                # TODO: does this work OOTB for negative diffs?
                date += relativedelta(days=days_diff)
            weekday = special_date.get("weekday")
            if weekday:
                date += relativedelta(weekday=weekday)
        else:
            raise ValueError("Could not infer date from {}".format(self.data))

        return BoundDay(date, self)


class BoundDay(namedtuple("_BoundDay", ("date", "day"))):
    """
    A Day bound to a given year.
    """

    def __getattr__(self, item):
        # Delegate everything else to the Day
        return getattr(self.day, item)
