import json
with open("sample-data.json") as f:
    d = json.load(f)

print("Interface Status")
print("=" * 80)
print(f"{'DN':50} {'Description':20} {'Speed':8} {'MTU':6}")
print("-" * 80)

for i in d["imdata"]:
    a = i["l1PhysIf"]["attributes"]
    dn = a["dn"]
    desc = a["descr"]
    sp = a["speed"]
    mtu = a["mtu"]

    print(f"{dn:50} {desc:20} {sp:8} {mtu:6}")
