from datetime import datetime, timedelta, timezone

import pytest

"""
ts
    UNIX時刻
    1483196400
    秒単位の整数値
dt
    日時の文字列
    "2024-04-02 00:00:00"
dttz
    タイムゾーンありの日時
    datetime.datetime(1970, 1, 1, 9, 0, tzinfo=datetime.timezone(datetime.timedelta(seconds=32400)))
"""


def dttz2ts(dttz):
    return int(dttz.timestamp())


def dt2ts(dt, offset=0):
    dttz = datetime.fromisoformat(dt).replace(tzinfo=timezone(timedelta(hours=offset)))
    return dttz2ts(dttz)


def ts2dttz(ts, offset=0):
    utc_dt = datetime.fromtimestamp(ts)
    return utc_dt.replace(tzinfo=timezone(timedelta(hours=offset)))


def ts2dt(ts, offset=0):
    dttz = ts2dttz(ts, offset=offset)
    return str(dttz)[:19]


def dttz2dt(dttz, offset=None):
    if offset is None:
        return str(dttz)[:19]
    else:
        return str(dttz.astimezone(timezone(timedelta(hours=offset))))[:19]


def dt2dttz(dt, offset):
    return datetime.fromisoformat(dt).replace(tzinfo=timezone(timedelta(hours=offset)))


def now(offset=0):
    return datetime.now(timezone(timedelta(hours=+offset))).replace(microsecond=0)


def get_day_of_week(dt):
    # "Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"
    return dt2dttz(dt, 0).strftime("%a")


@pytest.mark.parametrize(
    "dttz,expected",
    [
        (datetime.fromisoformat("1970-01-01T09:00:00+09:00"), 0),
    ],
)
def test_dttz2ts(dttz, expected):
    response = dttz2ts(dttz)
    assert response == expected


@pytest.mark.parametrize(
    "dt,offset,expected",
    [
        ("1970-01-01 09:00:00", 9, 0),
    ],
)
def test_dt2ts(dt, offset, expected):
    response = dt2ts(dt, offset=offset)
    assert response == expected


@pytest.mark.parametrize(
    "ts,offset,expected",
    [
        (0, 9, datetime.fromisoformat("1970-01-01T09:00:00+09:00")),
    ],
)
def test_ts2dttz(ts, offset, expected):
    response = ts2dttz(ts, offset=offset)
    assert response == expected


@pytest.mark.parametrize(
    "ts,offset,expected",
    [
        (0, 9, "1970-01-01 09:00:00"),
    ],
)
def test_ts2dt(ts, offset, expected):
    response = ts2dt(ts, offset=offset)
    assert response == expected


@pytest.mark.parametrize(
    "dttz,offset,expected",
    [
        (datetime.fromisoformat("1970-01-01T09:00:00+09:00"), 9, "1970-01-01 09:00:00"),
        (datetime.fromisoformat("1970-01-01T09:00:00+09:00"), 0, "1970-01-01 00:00:00"),
        (
            datetime.fromisoformat("1970-01-01T09:00:00+09:00"),
            None,
            "1970-01-01 09:00:00",
        ),
        (
            datetime.fromisoformat("1970-01-01T09:00:00+00:00"),
            None,
            "1970-01-01 09:00:00",
        ),
    ],
)
def test_dttz2dt(dttz, offset, expected):
    response = dttz2dt(dttz, offset)
    assert response == expected


@pytest.mark.parametrize(
    "dt,offset,expected",
    [
        ("1970-01-01 09:00:00", 9, datetime.fromisoformat("1970-01-01T09:00:00+09:00")),
        ("1970-01-01 09:00:00", 0, datetime.fromisoformat("1970-01-01T09:00:00+00:00")),
    ],
)
def test_dt2dttz(dt, offset, expected):
    response = dt2dttz(dt, offset)
    assert response == expected


@pytest.mark.parametrize(
    "dt,expected",
    [("2024-05-14", "Tue")],
)
def test_get_day_of_week(dt, expected):
    response = get_day_of_week(dt)
    assert response == expected


@pytest.mark.parametrize(
    "offset,expected",
    [
        (0, datetime.fromisoformat("2024-05-12 16:48:20+00:00")),
        (9, datetime.fromisoformat("2024-05-13 01:48:20+09:00")),
    ],
)
def test_now(offset, expected):
    response = now(offset)
    assert response == expected
