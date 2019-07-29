from datetime import date
from dateutil.easter import easter
from dateutil.relativedelta import relativedelta
from yaml import load, safe_load
from typing import Dict, List
from pathlib import Path
import os


class Holiday:
    def __init__(self, filename: str) -> None:
        fullpath = Path("countries", filename)
        with open(fullpath, "r") as f:
            data = safe_load(f)

        self.days = data["days"]
        self.names = data["names"]
        self.alpha2 = data["countrycode-alpha2"]
        self.alpha3 = data["countrycode-alpha3"]
        self.numeric = data["countrycode-numeric"]

    def get_country_code(self) -> str:
        return self.alpha2 # According to ISO 3166-2

    def get_holidays(self, year: int) -> List[Dict]:
        holidays = []
        for day in self.days:
            convertable_day = {}
            convertable_day.update(day)
            holidays.append(_convert_date(convertable_day, year))

        return holidays

    def get_base_info(self) -> Dict[str, str]:
        return {
            "countrycode-alpha2": self.alpha2,
            "countrycode-alpha3": self.alpha3,
            "countrycode-numeric": self.numeric
        }

    def get_names(self) -> Dict[str, str]:
        names = {}
        for name in self.names:
            names[name] = self.names[name]
        return names

    @staticmethod
    def get_available_country_files() -> Dict[str, str]:
        available_country_files = {}
        for file in os.listdir(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "countries")
        ):
            if file.endswith(".yml"):
                available_country_files[str(file).split(".")[0]] = os.path.join(os.path.dirname(os.path.abspath(__file__)), "countries", file)

        return available_country_files


def _convert_date(day: dict, year: int) -> dict:
    if "date" in day:
        day["date"] = date(year, int(day["date"]["month"]), int(day["date"]["day"]))

    if "special-date" in day:
        if day["special-date"]["type"] == "easter":
            day["date"] = _get_easter_date(year, day["special-date"]["days-difference"])
        if day["special-date"]["type"] == "midsummer":
            day["date"] = _get_midsummer_date(year, day["special-date"]["weekday"])
        if day["special-date"]["type"] == "allsaints":
            day["date"] = _get_allsaints_date(year)

        del day["special-date"]

    day["date"] = str(day["date"]) # For serializability
    return day


def _get_easter_date(year: int, shift: int):
    if shift < 0:
        return easter(year) - relativedelta(days=(shift * (-1)))

    return easter(year) + relativedelta(days=shift)


def _get_midsummer_date(year: int, weekday: str):
    return date(year, 6, 19) + relativedelta(weekday=weekday)


def _get_allsaints_date(year: int):
    return date(year, 10, 31) + relativedelta(weekday=5)

