import re

s = input()
p = input()

m = re.findall(re.escape(p), s)
print(len(m))