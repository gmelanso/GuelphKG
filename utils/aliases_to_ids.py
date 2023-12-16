import argparse
import json

from GuelphKG.entities.definitions import PERSON

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

if __name__=="__main__":

    parser = argparse.ArgumentParser(
        prog='aliases_to_ids',
        description='Converts a list of strings to a list of IDs.'
    )

    parser.add_argument(
        'f_name',
        help= "Location of the entities file."
    )

    args = parser.parse_args()

    with open(args.f_name, 'r') as file:
        minutes= json.load(file)

    for minute in minutes:
        for key, value in minute.items():
            if key in PERSON['relationships']:
                minute[key]['object']= aliases_to_ids(minute[key]['object'])

    with open(args.f_name, 'w') as file:
        minutes= json.dump(minutes, file, indent=4)

