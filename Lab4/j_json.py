import json

with open("sample-data.json") as file:
    data = json.load(file)

print("Interface Status")
print("=" * 80)
print(f"{'DN':<55} {'Description':<20} {'Speed':<10} {'MTU':<5}")
print("-" * 80)

for item in data["imdata"]:
    attributes = item["l1PhysIf"]["attributes"]
    dn = attributes["dn"]
    description = attributes["descr"]   
    speed = attributes["speed"]
    mtu = attributes["mtu"]

    print(f"{dn:<55} {description:<20} {speed:<10} {mtu:<5}")
