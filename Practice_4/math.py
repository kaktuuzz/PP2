#Write a Python program to convert degree to radian.
import math
d = float(input())
r = d * math.pi / 180
print(round(r, 6))

#Write a Python program to calculate the area of a trapezoid.
h = float(input("height "))
a = float(input("base first value "))
b = float(input("base second value "))
s = (a + b) * h / 2
print(s)

#Write a Python program to calculate the area of regular polygon.
side = int(input())
len = float(input())
s = (side * len * len) / (4 * math.tan(math.pi / side))
print(round(s))

#Write a Python program to calculate the area of a parallelogram.
b = float(input())
h = float(input())
s = b * h
print(s)