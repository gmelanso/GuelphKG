import pandas as pd
import json

files= [
    'entities/CityCouncil/CityCouncil.json',
    'entities/MeetingMinutes/MeetingMinutes.json'
]

with open(files[1], "r") as file:
    json_object= json.load(file)

entities = []
for obj in json_object:
    new_obj = {}
    for k, v in obj.items():
        if isinstance(v, dict):
            if v.get("type") == "Property":
                new_obj.update({k: v.get('value')})
            elif v.get("type") == "Relationship":
                continue
        else:
            new_obj.update({k: v})
    entities.append(new_obj)

df = pd.DataFrame(entities)
df.to_csv('./tables/meeting_entities_property_table.csv', index=False)