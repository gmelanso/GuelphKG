import json
import uuid
import pandas as pd

entity_jsons= [
    './entities/json/MeetingMinutes.json'
]

def_relations= {
    "isPartOf": str(uuid.uuid4()),
    "hasPart": str(uuid.uuid4()),
    "attendees": str(uuid.uuid4()),
    "movedBy": str(uuid.uuid4()),
    "secondedBy": str(uuid.uuid4()),
    "vote": str(uuid.uuid4()),
    "yeas": str(uuid.uuid4()),
    "nays": str(uuid.uuid4()),
    "subjectOf": str(uuid.uuid4())
}

with open('entities/MeetingMinutes/MeetingMinutes.json', 'r') as file:
    meeting_minutes= json.load(file)


df = pd.DataFrame()
relations = []

for meeting in meeting_minutes:
    for key, value in meeting.items():
        if isinstance(value, dict) and value['type'] == "Relationship":
            relation = def_relations.get(key)
            if relation is not None:
                for tail in value.get("object", []):
                    if meeting.get("id") and relation and tail:
                        relations.append({
                            "head": meeting["id"],
                            "relation": relation,
                            "tail": tail,
                            "display_relation": key
                        })

df = pd.DataFrame(relations)

df.to_csv('entities_relations_table.csv', index=False)


