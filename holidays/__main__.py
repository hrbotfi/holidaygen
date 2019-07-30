#!/usr/bin/python3
import argparse
import csv
import datetime
import json
from pathlib import Path
from typing import TextIO

from holidays import Holiday, get_available_country_files

json_folder = "json"
csv_folder = "csv"


def render_csv(f: TextIO, h: Holiday, year: int) -> None:
    title_row = []
    languages = sorted(set(h.names))
    for language in languages:
        title_row.append("name_{}".format(language))
    title_row.append("date")
    title_row.append("public_holiday")
    title_row.append("common_holiday")
    writer = csv.writer(f)
    writer.writerow(title_row)
    for holiday in h.get_holidays(year):
        result_row = []
        for language in languages:
            result_row.append(holiday.names.get(language, ""))
        result_row.append(holiday.date)
        result_row.append("yes" if "public" in holiday.tags else "no")
        result_row.append("yes" if "common" in holiday.tags else "no")

        writer.writerow(result_row)


def format_json_object(o):
    if isinstance(o, datetime.date):
        return o.isoformat()
    raise ValueError("Object {!r} is not serializable".format(o))


def render_json(f: TextIO, h: Holiday, year: int) -> None:
    data = {
        "countrycode-alpha2": h.alpha2_country_code,
        "countrycode-alpha3": h.alpha3_country_code,
        "countrycode-numeric": h.numeric_country_code,
        "names": h.names,
        "holidays": [
            {"names": bd.names, "tags": sorted(bd.tags), "date": bd.date}
            for bd in h.get_holidays(year)
        ],
    }
    json.dump(data, f, ensure_ascii=False, indent=4, default=format_json_object)


def create_json_file(h: Holiday, year: int) -> None:
    json_file = Path(json_folder, "{}-{}.json".format(h.alpha2_country_code, year))

    with open(json_file, "w") as f:
        render_json(f, h, year)

    print("Created JSON file {}".format(json_file))


def create_csv_file(h: Holiday, year: int) -> None:
    csv_file = Path(csv_folder, "{}-{}.csv".format(h.alpha2_country_code, year))

    with open(csv_file, "w") as f:
        render_csv(f, h, year)

    print("Created CSV file {}".format(csv_file))


def print_countries(country_files) -> None:
    for country in country_files:
        print(country)


def main():
    parser = argparse.ArgumentParser(prog="holidays")
    parser.add_argument("--json", action="store_true", help="Create JSON files")
    parser.add_argument("--csv", action="store_true", help="Create CSV files")
    parser.add_argument(
        "-c",
        "--country",
        help="Specify country (eg. FI, SE). Default: all countries are created",
    )
    parser.add_argument(
        "-y",
        "--year",
        required=True,
        help="The year you want the date files for (eg. 2020, 2025)",
    )
    args = parser.parse_args()

    year = int(args.year)
    if not year:
        print("No valid year specified.")
        exit(1)

    country_map = get_available_country_files()
    if not args.json and not args.csv:
        print("No creatable country files specified (see --help), these are available:")
        print_countries(country_map)
        exit(0)

    if args.country:
        countries = [args.country]
    else:
        countries = sorted(country_map)

    for country in countries:
        print("Creating specified file(s) for country {}.".format(country))
        if country not in country_map:
            print(
                "Specified country {} does not exist in available country files. "
                "These are available:".format(args.country)
            )
            print_countries(country_map)
            exit(1)

        h = Holiday.for_country(country)
        if args.json:
            create_json_file(h, year)
        if args.csv:
            create_csv_file(h, year)


if __name__ == "__main__":
    main()
