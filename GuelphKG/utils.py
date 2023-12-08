import re
import string

import json
import pandas as pd
import requests

from bs4 import BeautifulSoup
from itertools import chain

def create_directory(d_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        return
    else:
        return


def convert_to_iso_format(
    input_date, 
    input_format="%m/%d/%Y %I:%M:%S %p"
    ):

    parsed_date = datetime.strptime(input_date, input_format)

    return parsed_date.strftime("%Y-%m-%dT%H:%M%z") 
    
def read_json(f_path):
    with open(f_path, 'r') as file:
        return json.load(file)

def save_json(objs, f_path, indent=4):
    with open(f_path, 'w') as file:
        return json.dump(objs, file, indent=indent)

def replace_aliases(s, replace_ids=False):

    def alias_table():
        with open('tables/aliases.json', '') as file:
            return json.load(file)
    
    def aliases():
        aliases= alias_table()
        return list(chain.from_iterable(map(lambda obj: obj.get("aliases", []) + obj.get("display", []), aliases)))
    
    def replace_id(name):
        df= pd.read_csv('tables/entity_to_id.csv')
        return df[df['display_name'] == name]['id'].pop(0)
    
    if replace_ids:
        aliases= aliases()

        if s in aliases:
            return replace_id(s)
        
        else:
            aliases= aliases()
            return [alias for alias in aliases if re.search(re.escape(alias), s)]


def replace_names_with_ids(data_list, aliases_to_id, attribute_name):
    for meeting_data in data_list:
        if attribute_name not in meeting_data:
            continue

        attribute_value = meeting_data.get(attribute_name, {}).get('object', [])
        
        updated_attribute = [aliases_to_id.get(name, None) for name in attribute_value if aliases_to_id.get(name)]
        
        updated_attribute = [item_id for item_id in updated_attribute if item_id is not None]
        
        meeting_data[attribute_name]['object'] = updated_attribute
    
    return


def write_csv(df, o_path):
    return df.to_csv(o_path, sep=',')

