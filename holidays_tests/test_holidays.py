from holidays import Holiday


def test_holidays_smoke():
    # TODO: Improve this test
    h = Holiday("FI.yml")
    assert list(h.get_holidays(2019))
