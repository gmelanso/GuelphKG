import json
from entities.utils import *
from entities.definitions import PERSON

minutes= read_json('./entities/json/MeetingMinutes.json')

def aliases_to_ids(l_string):

    if l_string is None:
        return []

    def alias_table():
        with open('tables/json/aliases.json', 'r') as file:
            return json.load(file)

    ids = []
    aliases= alias_table()

    for s in l_string:
        for alias in aliases:
            if s in alias['aliases'] or s == (alias['display']):
                ids.append(alias['id'])

    return ids

for minute in minutes:
    for key, value in minute.items():
        if key in PERSON['relationships']:
            minute[key]['object']= aliases_to_ids(minute[key]['object'])

save_json(minutes, 'test.json')

