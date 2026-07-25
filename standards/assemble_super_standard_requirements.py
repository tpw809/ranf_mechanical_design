"""Combined requirement json to make a super-standard json"""
import json

list_to_assemble = [
    "MA2-00-057_DFMR/dfmr_requirements.json",
    "MIL-A-83577/MIL-A-83577B_requirements.json",
    "NASA-STD-5017B/nasa_5017b_requirements.json",
]

super_data = []

for json_reqs_file in list_to_assemble:
    print(json_reqs_file)
    with open(json_reqs_file, "r") as f:
        data = json.load(f)
        print(len(data))
        super_data += data

print(len(super_data))

# save as new json:
with open("super_standard_requirements.json", "w") as f:
    json.dump(super_data, f, indent=4)
