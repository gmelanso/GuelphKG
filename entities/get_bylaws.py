import argparse
import json
import re
import uuid

from definitions import ByLaw

with open('./entities/json/MeetingMinutes.json', 'r') as file:
    minutes= json.load(file)

def bylaws_from_minutes():

    def openJSON(j_path, t):
        with open(j_path, t) as file:
            return json.load(file)
    
    entities= openJSON('./entities/json/MeetingMinutes.json', 'r')
    
    minutes= [e for e in entities if e['type'] == "MeetingMinutes"]
    agendai= [e for e in entities if e['type'] == "AgendaItem"]
    motions= [e for e in entities if e['type'] == "Motion"]

    pattern= r'(\(\d{4}\)-\d{1,5})'


    bylaws = [
        ByLaw(
            bylawId=match_item,
            recordedAt=[motion['id']]
        )
        for motion in motions

        if (matches := re.findall(pattern, motion['abstract']['value']))

        for match_item in matches
    ]

    return bylaws



if __name__=="__main__":
    x= bylaws_from_minutes()
    print(x)
"""    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('integers', metavar='N', type=int, nargs='+',help='an integer for the accumulator')
    parser.add_argument('--sum', dest='accumulate', action='store_const',const=sum, default=max,help='sum the integers (default: find the max)')

    args = parser.parse_args()"""
