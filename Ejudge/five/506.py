import re
n = input()
p = r'\S+@\S+\.\S+'
s = re.search(p, n)
if s:
    print(s.group())
else:
    print("No email")