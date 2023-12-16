import argparse
import json
import re
import uuid

from definitions import ByLaw

def bylaws_from_minutes():

    with open('./entities/json/MeetingMinutes.json', 'r') as file:
        entities= json.load(file)
    
    minutes= [e for e in entities if e['type'] == "MeetingMinutes"]
    agendai= [e for e in entities if e['type'] == "AgendaItem"]
    motions= [e for e in entities if e['type'] == "Motion"]

    pattern= r'(\(\d{4}\)-\d{1,5})'

    bylaws = [
        ByLaw(
            bylawId=match_item,
            isPartOf=[motion['id']],
            dateCreated=motion['dateCreated']['value'],
            recordedAt=[minute['id'] for minute in minutes if motion['dateCreated']['value'] == minute['dateCreated']['value']]
        )
        for motion in motions

        if (matches := re.findall(pattern, motion['abstract']['value']))

        for match_item in matches
    ]

    return bylaws


if __name__=="__main__":
    
    with open('entities/json/ByLaws.json', 'r') as file:
        bylaws= json.load(file)
    
    new_bylaws= bylaws_from_minutes()

    bylaws.append(new_bylaws)

    with open('entities/json/ByLaws.json', 'w') as file:
        json.dump(bylaws, file, indent=4)
