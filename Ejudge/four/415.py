from datetime import datetime, timedelta, timezone
import sys

def parse(line):
    date_part, tz_part = line.strip().split()
    sign = 1 if tz_part[3] == '+' else -1
    hours, minutes = map(int, tz_part[4:].split(':'))
    offset = timedelta(hours=hours, minutes=minutes) * sign
    tz = timezone(offset)
    return datetime.strptime(date_part, "%Y-%m-%d").replace(tzinfo=tz)

birth = parse(sys.stdin.readline())
current = parse(sys.stdin.readline())

def next_birthday(birth, current):
    year = current.year
    month = birth.month
    day = birth.day

    def make_date(y):
        if month == 2 and day == 29:
            try:
                return datetime(y, 2, 29, tzinfo=birth.tzinfo)
            except ValueError:
                return datetime(y, 2, 28, tzinfo=birth.tzinfo)
        return datetime(y, month, day, tzinfo=birth.tzinfo)

    candidate = make_date(year).astimezone(timezone.utc)
    current_utc = current.astimezone(timezone.utc)

    if candidate < current_utc:
        candidate = make_date(year + 1).astimezone(timezone.utc)

    return candidate

nb = next_birthday(birth, current)
current_utc = current.astimezone(timezone.utc)

delta_seconds = int((nb - current_utc).total_seconds())

print((delta_seconds + 86399) // 86400)
