import pytest

from holidays import Holiday, get_available_country_files
import io

from holidays.__main__ import render_csv, render_json


@pytest.fixture
def fi_holiday():
    return Holiday.for_country("FI")


def test_holidays_smoke(fi_holiday):
    # TODO: Improve this test
    assert list(fi_holiday.get_holidays(2019))


def test_render_csv(fi_holiday):
    render_csv(io.StringIO(), fi_holiday, 2019)


def test_render_json(fi_holiday):
    render_json(io.StringIO(), fi_holiday, 2019)


def test_list():
    assert set(get_available_country_files()) == {"FI"}
