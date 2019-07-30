from holidays import Holiday
import io

from holidays.__main__ import render_csv, render_json


def test_holidays_smoke():
    # TODO: Improve this test
    h = Holiday("FI.yml")
    assert list(h.get_holidays(2019))


def test_render_csv():
    h = Holiday("FI.yml")
    render_csv(io.StringIO(), h, 2019)


def test_render_json():
    h = Holiday("FI.yml")
    render_json(io.StringIO(), h, 2019)


def test_list():
    assert set(Holiday.get_available_country_files()) == {"FI"}
