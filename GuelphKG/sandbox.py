
import json

import pandas as pd
from utils import *


attributes= ['yeas', 'nays']

data= read_json("entities/MeetingMinutes/MeetingMinutes.json")

with open('tables/aliases.json', 'r') as file:
    aliases= json.load(file)

aliases_to_id = {name: alias["id"] for alias in aliases for name in [alias["display"]] + alias["aliases"]}

def replace_names_with_ids(data_list, aliases_to_id, attribute_name):
    for meeting_data in data_list:
        if attribute_name not in meeting_data:
            continue

        attribute_value = meeting_data.get(attribute_name, {}).get('object', [])
        
        # Replace names with corresponding IDs, remove names not found
        updated_attribute = [aliases_to_id.get(name, None) for name in attribute_value if aliases_to_id.get(name)]
        
        # Remove names not found (replace None with ID)
        updated_attribute = [item_id for item_id in updated_attribute if item_id is not None]
        
        # Update the attribute list in the meeting_data
        meeting_data[attribute_name]['object'] = updated_attribute

for attribute in attributes:
    replace_names_with_ids(data, aliases_to_id, attribute)

with open("entities/MeetingMinutes/MeetingMinutes.json", 'w') as file:
    json.dump(data, file, indent=4)



