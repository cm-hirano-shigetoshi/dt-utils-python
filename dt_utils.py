from datetime import date, datetime, timedelta, timezone

import pytest

"""
ts
    UNIX時刻の整数値
    1483196400
    秒単位の整数値
dt
    日時の文字列
    "2024-04-02 00:00:00"
dttz
    datetime.datetime型
    タイムゾーンありの日時
date
    datetime.date型
    タイムゾーンという概念はない
"""


def ts2dt(ts, offset=0):
    dttz = ts2dttz(ts, offset=offset)
    return str(dttz)[:19]


def ts2dttz(ts, offset=0):
    utc_dt = datetime.fromtimestamp(ts)
    return utc_dt.replace(tzinfo=timezone(timedelta(hours=offset)))


def ts2date(ts):
    return dt2date(ts2dt(ts))


def dt2ts(dt, offset=0):
    dttz = datetime.fromisoformat(dt).replace(tzinfo=timezone(timedelta(hours=offset)))
    return dttz2ts(dttz)


def dt2dttz(dt, offset):
    return datetime.fromisoformat(dt).replace(tzinfo=timezone(timedelta(hours=offset)))


def dt2date(dt):
    return date.fromisoformat(dt[:10])


def dttz2ts(dttz):
    return int(dttz.timestamp())


def dttz2dt(dttz, offset=None):
    if offset is None:
        return str(dttz)[:19]
    else:
        return str(dttz.astimezone(timezone(timedelta(hours=offset))))[:19]


def dttz2date(dttz, offset=None):
    return date.fromisoformat(dttz2dt(dttz, offset)[:10])


def date2ts(date, offset):
    return dt2ts(str(date) + " 00:00:00", offset)


def date2dt(date):
    return str(date) + " 00:00:00"


def date2dttz(date, offset):
    return dt2dttz(str(date) + " 00:00:00", offset)


def add_days(date, n):
    return date + timedelta(days=n)


def get_day_of_week(date):
    # "Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"
    return date.strftime("%a")


def now(offset=0):
    return datetime.now(timezone(timedelta(hours=+offset))).replace(microsecond=0)


"""
test
"""


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
    "ts,offset,expected",
    [
        (0, 9, datetime.fromisoformat("1970-01-01T09:00:00+09:00")),
    ],
)
def test_ts2dttz(ts, offset, expected):
    response = ts2dttz(ts, offset=offset)
    assert response == expected


@pytest.mark.parametrize(
    "ts,expected",
    [
        (0, date.fromisoformat("1970-01-01")),
    ],
)
def test_ts2date(ts, expected):
    response = ts2date(ts)
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
    [
        ("1970-01-01 00:00:00", date.fromisoformat("1970-01-01")),
    ],
)
def test_dt2date(dt, expected):
    response = dt2date(dt)
    assert response == expected


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
    "dttz,offset,expected",
    [
        (
            datetime.fromisoformat("1970-01-01T00:00:00+00:00"),
            None,
            date.fromisoformat("1970-01-01"),
        ),
        (
            datetime.fromisoformat("1970-01-01T00:00:00+00:00"),
            0,
            date.fromisoformat("1970-01-01"),
        ),
        (
            datetime.fromisoformat("1970-01-01T15:00:00+00:00"),
            9,
            date.fromisoformat("1970-01-02"),
        ),
    ],
)
def test_dttz2date(dttz, offset, expected):
    response = dttz2date(dttz, offset)
    assert response == expected


@pytest.mark.parametrize(
    "date,offset,expected",
    [
        (date.fromisoformat("1970-01-02"), 0, 86400),
        (date.fromisoformat("1970-01-02"), 9, 54000),
    ],
)
def test_date2ts(date, offset, expected):
    response = date2ts(date, offset)
    assert response == expected


@pytest.mark.parametrize(
    "date,expected",
    [
        (date.fromisoformat("1970-01-01"), "1970-01-01 00:00:00"),
    ],
)
def test_date2dt(date, expected):
    response = date2dt(date)
    assert response == expected


@pytest.mark.parametrize(
    "date,offset,expected",
    [
        (
            date.fromisoformat("1970-01-01"),
            0,
            datetime.fromisoformat("1970-01-01 00:00:00+00:00"),
        ),
        (
            date.fromisoformat("1970-01-01"),
            9,
            datetime.fromisoformat("1970-01-01 00:00:00+09:00"),
        ),
    ],
)
def test_date2dttz(date, offset, expected):
    response = date2dttz(date, offset)
    assert response == expected


@pytest.mark.parametrize(
    "date,n,expected",
    [
        (date.fromisoformat("2024-05-01"), 1, date.fromisoformat("2024-05-02")),
        (date.fromisoformat("2024-05-01"), 0, date.fromisoformat("2024-05-01")),
        (date.fromisoformat("2024-05-01"), -1, date.fromisoformat("2024-04-30")),
    ],
)
def test_add_days(date, n, expected):
    response = add_days(date, n)
    assert response == expected


@pytest.mark.parametrize(
    "date,expected",
    [(date.fromisoformat("2024-05-14"), "Tue")],
)
def test_get_day_of_week(date, expected):
    response = get_day_of_week(date)
    assert response == expected


"""
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
"""
