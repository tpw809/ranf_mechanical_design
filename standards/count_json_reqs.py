import json

with open("dfmr_requirements.json", "r") as f:
    data = json.load(f)
    
# check if unique_ids are unique:
# or create new unique_id
# unique_id = id + random 10 digits

# increment version:
new_version_value = 0.2


print("Number of entries:", len(data))
