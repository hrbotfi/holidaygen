from typing import Dict, Optional, Any, Tuple
from datetime import date

from holidays import Holiday, Day, BoundDay, get_available_country_files
from flask import Flask, abort

application = Flask(__name__)
application.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
application.config["JSON_AS_ASCII"] = False

def _check_country_existance(country: str) -> bool:
    countries = get_available_country_files()
    if country.upper() in countries:
        return True

    return False

def _get_serializable_holiday(holiday: Day) -> Dict[str, Any]:
    day = {
        "date": str(holiday.date),
        "names": holiday.names,
        "tags": list(holiday.tags),
    }
    return day

@application.route("/holidays/")
@application.route("/holidays")
def available_countries() -> Tuple[Dict[str, Any], int]:
    countries = {
        "available_countries": [],
    }
    for country in get_available_country_files().keys():
        countries["available_countries"].append(get_country_description(country))

    return countries, 200

@application.route("/holidays/<string:country>/")
@application.route("/holidays/<string:country>")
def get_country_description(country: str) -> Dict[str, Any]:
    if not _check_country_existance(country):
        abort(404)

    info = Holiday.for_country(country.upper())
    country_description = {
        "names": info.names,
        "country-code-alpha2": info.alpha2_country_code,
        "country-code-alpha3": info.alpha3_country_code,
    }

    return country_description


@application.route("/holidays/<string:country>/<int:year>")
def get_holidays_in_year(country: str, year: int) -> Tuple[Dict[str, Any], int]:
    if not _check_country_existance(country):
        abort(404)

    holidays = Holiday.for_country(country.upper()).get_holidays(year)
    result = {
        "holidays": [],
    }

    for holiday in holidays:
        result["holidays"].append(_get_serializable_holiday(holiday))

    return result, 200

@application.route("/holidays/<string:country>/<int:year>/<int:month>")
def get_holidays_in_month(country: str, year: int, month: int) -> Tuple[Dict[str, Any], int]:
    if not _check_country_existance(country):
        abort(404)

    holidays = Holiday.for_country(country.upper()).get_holidays(year)
    result = {
        "holidays": [],
    }

    for holiday in holidays:
        if holiday.date.month == month:
            result["holidays"].append(_get_serializable_holiday(holiday))
    
    return result, 200

@application.route("/holidays/<string:country>/<int:year>/<int:month>/<int:day>")
def check_date_for_holidays(country: str, year: int, month: int, day: int) -> Tuple[Dict[str, Any], int]:
    if not _check_country_existance(country):
        abort(404)
    holidays = Holiday.for_country(country.upper()).get_holidays(year)
    result = {
        "holidays": [],
    }
    wanted_date = date(year, month, day)

    for holiday in holidays:
        if holiday.date == wanted_date:
            result["holidays"].append(_get_serializable_holiday(holiday))
    
    return result, 200