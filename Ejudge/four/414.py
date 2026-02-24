from datetime import datetime, timedelta, timezone

def parse_datetime(s):

    date_str, tz_str = s.split()
    

    dt = datetime.strptime(date_str, "%Y-%m-%d")
    

    sign = 1 if tz_str[3] == '+' else -1
    hours = int(tz_str[4:6])
    minutes = int(tz_str[7:9])
    offset = timedelta(hours=hours, minutes=minutes) * sign
    

    dt = dt.replace(tzinfo=timezone(offset))
    return dt


dt1 = parse_datetime(input())
dt2 = parse_datetime(input())

utc1 = dt1.astimezone(timezone.utc)
utc2 = dt2.astimezone(timezone.utc)

delta_seconds = abs((utc2 - utc1).total_seconds())

days = int(delta_seconds // 86400)
print(days)
