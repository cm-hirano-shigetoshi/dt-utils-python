import datetime
from datetime import date as datemod
from datetime import datetime as dtmod
from datetime import timedelta, timezone

import pytest

"""
ts
    UNIX時刻の整数値
    例: 1483196400
    秒単位の整数値
dt
    日時の文字列
    例: "2024-04-02 00:00:00"
    タイムゾーン概念を持たない
dttz
    datetime.datetime型
    タイムゾーンありの日時
date
    日付の文字列
    例: "2024-04-02"
    タイムゾーンという概念はない
time
    時刻部分の文字列
    例: "12:34:56"
    時分秒とも0埋めの2桁
dur
    経過時刻の文字列
    例: "65:43:21"
    分秒は0埋めの2桁。時は桁数を問わないが0の時は0と表示する
"""


def ts2dt(ts, offset=0):
    dttz = ts2dttz(ts, offset=offset)
    return str(dttz)[:19]


def ts2dttz(ts, offset=0):
    utc_dt = dtmod.fromtimestamp(ts)
    return utc_dt.replace(tzinfo=timezone(timedelta(hours=offset)))


def ts2date(ts):
    return dt2date(ts2dt(ts))


def dt2ts(dt, offset=0):
    dttz = dtmod.fromisoformat(dt).replace(tzinfo=timezone(timedelta(hours=offset)))
    return dttz2ts(dttz)


def dt2dttz(dt, offset=0):
    return dtmod.fromisoformat(dt).replace(tzinfo=timezone(timedelta(hours=offset)))


def dt2date(dt):
    return dt[:10]


def dt2time(dt):
    return dt[11:]


def dttz2ts(dttz):
    return int(dttz.timestamp())


def dttz2dt(dttz, offset=None):
    if offset is None:
        return str(dttz)[:19]
    else:
        return str(dttz.astimezone(timezone(timedelta(hours=offset))))[:19]


def dttz2date(dttz, offset=None):
    return dttz2dt(dttz, offset)[:10]


def date2ts(date, offset):
    return dt2ts(date + " 00:00:00", offset)


def date2dt(date):
    return date + " 00:00:00"


def date2dttz(date, offset):
    return dt2dttz(date + " 00:00:00", offset)


def add_days(date, n):
    return str(datemod.fromisoformat(date) + timedelta(days=n))


def add_seconds(dttz, n):
    return dttz + timedelta(seconds=n)


def add_seconds_to_dur(dur, n):
    def split_dur(dur):
        return (int(dur[:-6]), int(dur[-5:-3]), int(dur[-2:]))

    def split_n(n):
        minute, second = divmod(n, 60)
        hour, minute = divmod(minute, 60)
        return (hour, minute, second)

    durs = split_dur(dur)
    ns = split_n(n)
    carry, second = divmod(durs[2] + ns[2], 60)
    carry, minute = divmod(durs[1] + ns[1] + carry, 60)
    hour = durs[0] + ns[0] + carry
    return f"{hour}:{str(minute).zfill(2)}:{str(second).zfill(2)}"


def calc_dur(start_dttz, end_dttz):
    elapsed_days = (end_dttz - start_dttz).days
    elapsed_seconds = (end_dttz - start_dttz).seconds
    elapsed_minutes, second = divmod(elapsed_seconds, 60)
    elapsed_hours, minute = divmod(elapsed_minutes, 60)
    second = str(second).zfill(2)
    minute = str(minute).zfill(2)
    hour = str(elapsed_days * 24 + elapsed_hours)
    return f"{hour}:{minute}:{second}"


def sum_dur(dur1, dur2):
    def split_dur(dur):
        return (int(dur[:-6]), int(dur[-5:-3]), int(dur[-2:]))

    durs1 = split_dur(dur1)
    durs2 = split_dur(dur2)
    carry, second = divmod(durs1[2] + durs2[2], 60)
    carry, minute = divmod(durs1[1] + durs2[1] + carry, 60)
    hour = durs1[0] + durs2[0] + carry
    return f"{hour}:{str(minute).zfill(2)}:{str(second).zfill(2)}"


def get_day_of_week(date):
    # "Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"
    return datemod.fromisoformat(date).strftime("%a")


def get_date_iter(start_date, end_date):
    def get_generator(start_date, end_date):
        d = start_date
        while d != end_date:
            yield d
            d = add_days(d, 1)
        yield d

    return get_generator(start_date, end_date)


def get_date_list(start_date, end_date):
    return list(get_date_iter(start_date, end_date))


def now(offset=0):
    return datetime.datetime.now(timezone(timedelta(hours=+offset))).replace(
        microsecond=0
    )


def now_jst():
    return now(offset=9)


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
        (0, 9, dtmod.fromisoformat("1970-01-01T09:00:00+09:00")),
    ],
)
def test_ts2dttz(ts, offset, expected):
    response = ts2dttz(ts, offset=offset)
    assert response == expected


@pytest.mark.parametrize(
    "ts,expected",
    [
        (0, "1970-01-01"),
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
        ("1970-01-01 09:00:00", 9, dtmod.fromisoformat("1970-01-01T09:00:00+09:00")),
        ("1970-01-01 09:00:00", 0, dtmod.fromisoformat("1970-01-01T09:00:00+00:00")),
    ],
)
def test_dt2dttz(dt, offset, expected):
    response = dt2dttz(dt, offset)
    assert response == expected


@pytest.mark.parametrize(
    "dt,expected",
    [
        ("1970-01-01 00:00:00", "1970-01-01"),
    ],
)
def test_dt2date(dt, expected):
    response = dt2date(dt)
    assert response == expected


@pytest.mark.parametrize(
    "dt,expected",
    [("1970-01-01 00:00:00", "00:00:00")],
)
def test_dt2time(dt, expected):
    response = dt2time(dt)
    assert response == expected


@pytest.mark.parametrize(
    "dttz,expected",
    [
        (dtmod.fromisoformat("1970-01-01T09:00:00+09:00"), 0),
    ],
)
def test_dttz2ts(dttz, expected):
    response = dttz2ts(dttz)
    assert response == expected


@pytest.mark.parametrize(
    "dttz,offset,expected",
    [
        (dtmod.fromisoformat("1970-01-01T09:00:00+09:00"), 9, "1970-01-01 09:00:00"),
        (dtmod.fromisoformat("1970-01-01T09:00:00+09:00"), 0, "1970-01-01 00:00:00"),
        (
            dtmod.fromisoformat("1970-01-01T09:00:00+09:00"),
            None,
            "1970-01-01 09:00:00",
        ),
        (
            dtmod.fromisoformat("1970-01-01T09:00:00+00:00"),
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
            dtmod.fromisoformat("1970-01-01T00:00:00+00:00"),
            None,
            "1970-01-01",
        ),
        (
            dtmod.fromisoformat("1970-01-01T00:00:00+00:00"),
            0,
            "1970-01-01",
        ),
        (
            dtmod.fromisoformat("1970-01-01T15:00:00+00:00"),
            9,
            "1970-01-02",
        ),
    ],
)
def test_dttz2date(dttz, offset, expected):
    response = dttz2date(dttz, offset)
    assert response == expected


@pytest.mark.parametrize(
    "date,offset,expected",
    [
        ("1970-01-02", 0, 86400),
        ("1970-01-02", 9, 54000),
    ],
)
def test_date2ts(date, offset, expected):
    response = date2ts(date, offset)
    assert response == expected


@pytest.mark.parametrize(
    "date,expected",
    [
        ("1970-01-01", "1970-01-01 00:00:00"),
    ],
)
def test_date2dt(date, expected):
    response = date2dt(date)
    assert response == expected


@pytest.mark.parametrize(
    "date,offset,expected",
    [
        (
            "1970-01-01",
            0,
            dtmod.fromisoformat("1970-01-01 00:00:00+00:00"),
        ),
        (
            "1970-01-01",
            9,
            dtmod.fromisoformat("1970-01-01 00:00:00+09:00"),
        ),
    ],
)
def test_date2dttz(date, offset, expected):
    response = date2dttz(date, offset)
    assert response == expected


@pytest.mark.parametrize(
    "date,n,expected",
    [
        ("2024-05-01", 1, "2024-05-02"),
        ("2024-05-01", 0, "2024-05-01"),
        ("2024-05-01", -1, "2024-04-30"),
    ],
)
def test_add_days(date, n, expected):
    response = add_days(date, n)
    assert response == expected


@pytest.mark.parametrize(
    "dttz,n,expected",
    [
        (
            dtmod.fromisoformat("2024-05-01 00:00:00"),
            1,
            dtmod.fromisoformat("2024-05-01 00:00:01"),
        ),
        (
            dtmod.fromisoformat("2024-05-01 00:00:00"),
            3601,
            dtmod.fromisoformat("2024-05-01 01:00:01"),
        ),
    ],
)
def test_add_seconds(dttz, n, expected):
    response = add_seconds(dttz, n)
    assert response == expected


@pytest.mark.parametrize(
    "dur,n,expected",
    [
        (
            "9:00:00",
            3601,
            "10:00:01",
        ),
        (
            "10:00:00",
            -3600,
            "9:00:00",
        ),
    ],
)
def test_add_seconds_to_dur(dur, n, expected):
    response = add_seconds_to_dur(dur, n)
    assert response == expected


@pytest.mark.parametrize(
    "start_dttz,end_dttz,expected",
    [
        (
            dtmod.fromisoformat("1970-01-01T00:00:00+00:00"),
            dtmod.fromisoformat("1970-01-01T02:34:56+00:00"),
            "2:34:56",
        ),
        (
            dtmod.fromisoformat("1970-01-01T00:00:00+00:00"),
            dtmod.fromisoformat("1970-01-02T12:34:56+00:00"),
            "36:34:56",
        ),
        (
            dtmod.fromisoformat("1970-01-01T00:00:00+00:00"),
            dtmod.fromisoformat("1970-01-02T12:34:56+09:00"),
            "27:34:56",
        ),
    ],
)
def test_calc_dur(start_dttz, end_dttz, expected):
    response = calc_dur(start_dttz, end_dttz)
    assert response == expected


@pytest.mark.parametrize(
    "dur1,dur2,expected",
    [
        ("5:55:55", "4:44:44", "10:40:39"),
    ],
)
def test_sum_dur(dur1, dur2, expected):
    response = sum_dur(dur1, dur2)
    assert response == expected


@pytest.mark.parametrize(
    "date,expected",
    [("2024-05-14", "Tue")],
)
def test_get_day_of_week(date, expected):
    response = get_day_of_week(date)
    assert response == expected


@pytest.mark.parametrize(
    "start_date,end_date,expected",
    [
        (
            "2024-06-29",
            "2024-07-02",
            ["2024-06-29", "2024-06-30", "2024-07-01", "2024-07-02"],
        )
    ],
)
def test_get_date_list(start_date, end_date, expected):
    response = get_date_list(start_date, end_date)
    assert response == expected


"""
@pytest.mark.parametrize(
    "offset,expected",
    [
        (0, dtmod.fromisoformat("2024-05-12 16:48:20+00:00")),
        (9, dtmod.fromisoformat("2024-05-13 01:48:20+09:00")),
    ],
)
def test_now(offset, expected):
    response = now(offset)
    assert response == expected
"""
