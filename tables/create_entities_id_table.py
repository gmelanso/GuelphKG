import csv
import json
import uuid
import pandas as pd

from ..utils import *

entities= [
    'entities/CityCouncil/CityCouncil.json',
    'entities/MeetingMinutes/MeetingMinutes.json'
]

minutes= open_json(entities[1])
council= open_json(entities[0])
entities= minutes + council

table= [
    {
        "id": obj['id'],
        "display_name": f"{obj['givenName'].get('value', '')} {obj['familyName'].get('value', '')}" if obj.get('givenName') and obj.get('familyName') else obj['id'],
        "type": obj['type']
    } for obj in entities
]

df= pd.DataFrame(table)
write_csv(df, 'tables/entity_to_id.csv')
