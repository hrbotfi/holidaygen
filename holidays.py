from datetime import date
from dateutil.easter import easter
from dateutil.relativedelta import relativedelta
from yaml import load, FullLoader
import os
import csv
import uuid


def get_available_languages() -> []:
    available_langs = []
    for file in os.listdir(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "countries")
    ):
        if file.endswith(".yml"):
            available_langs.append(str(file))

    return available_langs


def parse_yaml(filename: str, year: int) -> dict:
    fullpath = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "countries", filename
    )
    with open(fullpath, "r") as f:
        data = load(f, Loader=FullLoader)

    formatted_days = []
    for day in data["days"]:
        formatted_days.append(_convert_date(day, year))

    data["days"] = formatted_days
    return data


def _convert_date(day: dict, year: int) -> dict:
    if day["date"]:
        day["date"] = date(year, int(day["date"]["month"]), int(day["date"]["day"]))

    if day["special-date"]:
        if day["special-date"]["type"] == "easter":
            day["date"] = _get_easter_date(year, day["special-date"]["days-difference"])
        if day["special-date"]["type"] == "midsummer":
            day["date"] = _get_midsummer_date(year, day["special-date"]["weekday"])
        if day["special-date"]["type"] == "allsaints":
            day["date"] = _get_allsaints_date(year)

        del day["special-date"]

    return day


def _get_easter_date(year: int, shift: int):
    if shift < 0:
        return easter(year) - relativedelta(days=(shift * (-1)))

    return easter(year) + relativedelta(days=shift)


def _get_midsummer_date(year: int, weekday: str):
    return date(year, 6, 19) + relativedelta(weekday=weekday)


def _get_allsaints_date(year: int):
    return date(year, 10, 31) + relativedelta(weekday=5)


def create_temp_csv_file(
    holidaydata: dict, include_common_holidays: bool = True, tmpfolder: str = "/tmp"
) -> str:
    tempfile = "{}/{}.csv".format(tmpfolder, str(uuid.uuid4()))
    with open(tempfile, "w") as newcsv:
        writer = csv.writer(newcsv)
        writer.writerow(
            ["Name", "Native name", "Date", "Public holiday", "Common holiday"]
        )

    return tempfile
