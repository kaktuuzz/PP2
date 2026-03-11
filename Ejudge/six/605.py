s = input()

if any(c.lower() in "aeiou" for c in s):
    print("Yes")
else:
    print("No")