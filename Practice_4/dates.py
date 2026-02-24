#Write a Python program to subtract five days from current date.
import datetime
a = datetime.datetime.now()
b = a - datetime.timedelta(days=5)
print(a)
print(b)

#Write a Python program to print yesterday, today, tomorrow.
import datetime
a = datetime.datetime.now().date()
b = a - datetime.timedelta(days=1)
c = a + datetime.timedelta(days=1)
print(b)
print(a)
print(c)

#Write a Python program to drop microseconds from datetime.
import datetime
a = datetime.datetime.now()
b = a.replace(microsecond=0)
print(a)
print(b)

#import datetime
a = datetime.datetime(2025, 1, 1, 12, 0, 0)
b = datetime.datetime(2025, 1, 2, 12, 0, 0)
c = b - a
print(c.total_seconds())