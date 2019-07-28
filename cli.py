#!/usr/bin/python3

import argparse
from holidays import get_available_languages, parse_yaml


def create_json_file(lang_data: dict) -> None:
    json_file_name = "foo"  # TODO actually create the file
    print("Created JSON file {}".format(json_file_name))


def create_csv_file(lang_data: dict) -> None:
    csv_file_name = "foo"  # TODO actually create the file
    print("Created CSV file {}".format(csv_file_name))


def print_languages(language_files) -> None:
    for lang in language_files:
        print(lang.split(".")[0])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-j", "--json", action="store_true", help="Create JSON files")
    parser.add_argument("-c", "--csv", action="store_true", help="Create CSV files")
    parser.add_argument(
        "-l",
        "--language",
        help="Specify language (eg. FI, SE). Default: all languages are created",
    )
    parser.add_argument(
        "-y",
        "--year",
        required=True,
        help="The year you want the date files for (eg. 2020, 2500)",
    )
    args = parser.parse_args()

    year = int(args.year)
    if not year:
        print("No valid year specified.")
        exit(1)

    language_files = get_available_languages()
    if not args.json and not args.csv:
        print(
            "No creatable files specified (see --help), these languages are available:"
        )
        print_languages(language_files)
        exit(0)

    if args.language:
        lang_filename = "{}.yml".format(args.language)
        print("Creating specified file(s) for language {}.".format(args.language))
        if lang_filename not in language_files:
            print(
                "Specified language {} does not exist in available language files. These are available:"
            )
            print_languages(language_files)
            exit(1)

        lang_data = parse_yaml(lang_filename, args.year)
        if args.json:
            create_json_file(lang_data)
        if args.csv:
            create_csv_file(lang_data)
    else:
        print("Creating specified file(s) for all available languages.")
        for lang_file in language_files:
            lang_data = parse_yaml(lang_filename, args.year)
            if args.json:
                create_json_file(lang_data)
            if args.csv:
                create_csv_file(lang_data)


if __name__ == "__main__":
    main()
