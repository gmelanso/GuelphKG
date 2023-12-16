import re
import string

import json
import pandas as pd
import requests

from bs4 import BeautifulSoup
from datetime import datetime
from itertools import chain

def newRelation(obj):
    return {
        "type": "Relationship",
        "object": obj if obj else []
    }


def newProperty(obj):
    return {
        "type": "Property",
        "value": obj if obj else []
    }


def create_directory(d_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        return
    else:
        return


def convert_to_iso_format(input_date, input_format="%m/%d/%Y %I:%M:%S %p"):

    parsed_date = datetime.strptime(input_date, input_format)

    return parsed_date.strftime("%Y-%m-%dT%H:%M%z") 


def read_json(f_path):
    with open(f_path, 'r') as file:
        return json.load(file)


def save_json(objs, f_path, indent=4):
    with open(f_path, 'w') as file:
        return json.dump(objs, file, indent=indent)


def replace_aliases(data_list):

    def alias_table():
        with open('tables/json/aliases.json', 'r') as file:
            return json.load(file)
    
    def search(a, name):
        for _ in a:
            for key, value in _.items():
                if name in value:
                    return _['id']
        return None

    aliases= alias_table()

    if data_list:
        return [search(aliases, data) for data in data_list]
    
    else:
        return []


def write_csv(df, o_path):
    return df.to_csv(o_path, sep=',')

