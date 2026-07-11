import json

with open("MIL-A-83577B_requirements.json", "r") as f:
    data = json.load(f)

print("Number of entries:", len(data))
