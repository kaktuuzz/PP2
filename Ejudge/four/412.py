import json

def find_differences(obj1, obj2, path=""):
    diffs = []

    keys = set(obj1.keys()).union(obj2.keys())

    for key in keys:
        new_path = f"{path}.{key}" if path else key

        v1 = obj1.get(key, "<missing>")
        v2 = obj2.get(key, "<missing>")

        if isinstance(v1, dict) and isinstance(v2, dict):
            diffs.extend(find_differences(v1, v2, new_path))
        elif v1 != v2:
            s1 = json.dumps(v1, separators=(',', ':')) if v1 != "<missing>" else "<missing>"
            s2 = json.dumps(v2, separators=(',', ':')) if v2 != "<missing>" else "<missing>"
            diffs.append(f"{new_path} : {s1} -> {s2}")

    return diffs


obj1 = json.loads(input())
obj2 = json.loads(input())

diffs = find_differences(obj1, obj2)

if diffs:
    for line in sorted(diffs):
        print(line)
else:
    print("No differences")
