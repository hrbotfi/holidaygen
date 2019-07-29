#!/usr/bin/python3

from holidays import Holiday

from typing import Dict
from pathlib import Path
import argparse
import csv
import json

json_folder = "json"
csv_folder = "csv"


def create_json_file(h: Holiday, year: int) -> None:
    json_file = Path(json_folder, "{}-{}.json".format(h.get_country_code(), year))

    data = h.get_base_info()
    data["names"] = h.get_names()
    data["holidays"] = h.get_holidays(year)
    with open(json_file, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print("Created JSON file {}".format(json_file))


def create_csv_file(h: Holiday, year: int) -> None:
    csv_file = Path(csv_folder, "{}-{}.csv".format(h.get_country_code(), year))

    title_row = []
    names = h.get_names()
    for name in names:
        title_row.append("name_{}".format(name))
    title_row.append("date")
    title_row.append("public_holiday")
    title_row.append("common_holiday")
    with open(csv_file, "w") as f:
        writer = csv.writer(f)
        writer.writerow(title_row)
        for holiday in h.get_holidays(year):
            result_row = []
            for name in names:
                if name in holiday["names"]:
                    result_row.append(holiday["names"][name])
                else:
                    result_row.append("")
            result_row.append(holiday["date"])
            result_row.append("yes" if "public" in holiday["tags"] else "no")
            result_row.append("yes" if "common" in holiday["tags"] else "no")

            writer.writerow(result_row)

    print("Created CSV file {}".format(csv_file))

def print_countries(country_files) -> None:
    for country in country_files:
        print(country.split(".")[0])

def main():
    parser = argparse.ArgumentParser()
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

    country_files = Holiday.get_available_country_files()
    if not args.json and not args.csv:
        print(
            "No creatable country files specified (see --help), these are available:"
        )
        print_countries(country_files)
        exit(0)

    if args.country:
        country_filename = "{}.yml".format(args.country)
        print("Creating specified file(s) for country {}.".format(args.country))
        if country_filename not in country_files:
            print(
                "Specified country {} does not exist in available country files. These are available:"
            )
            print_countries(country_files)
            exit(1)

        h = Holiday(country_filename)
        if args.json:
            create_json_file(h, year)
        if args.csv:
            create_csv_file(h, year)
    else:
        print("Creating specified file(s) for all available countries.")
        for country_filename in country_files:
            h = Holiday(country_files[country_filename])
            if args.json:
                create_json_file(h, year)
            if args.csv:
                create_csv_file(h, year)


if __name__ == "__main__":
    main()
