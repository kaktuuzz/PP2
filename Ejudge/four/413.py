import json
import re

def resolve_query(obj, query):
    parts = re.findall(r'\w+|\[\d+\]', query)
    current = obj
    for part in parts:
        if part.startswith('['):
            index = int(part[1:-1])
            current = current[index]
        else:
            current = current[part]
    return current


data = json.loads(input())

q = int(input())

for d in range(q):
    query = input()
    value = resolve_query(data, query)
    print(json.dumps(value, separators=(',', ':')))
